import fused_app
import pydeck as pdk
import streamlit as st

st.header("Buffer analysis")

st.write("""
This app illustrates the buffer analysis between two GeoPandas GeoDataFrames: road segment represented with `LineStrings` and a table of vehicle GPS locations represented with `Points`. To determine which vehicles are using specific roads, we create a buffer around the road segments using the GeoDataFrame's `buffer` method and check which GPS points fall in this area using the `within` method.

Users can interact with the two sliders on the sidebar to adjust:
- The number of vehicle points to show on the map
- The size of the buffer, causing the blue area to expand or contract accordingly
""")

# Slider widgets
n_points = st.sidebar.slider("Number of points:", 0, 1000, 100)
buffer = st.sidebar.slider("Buffer:", 0.0, 0.01, 0.0025, step=0.001)

# Run UDF
@st.cache_data
def load_data(n_points=15, buffer=0.0025):
    gdf_points = fused_app.run(
        "46bd457dddfbc47dbddaa703a2603d95ef06ed5d4d9c43bf8225758a3192955d",
        n_points=n_points,
        buffer=buffer,
        return_object="points",
    )
    gdf_linestring = fused_app.run(
        "46bd457dddfbc47dbddaa703a2603d95ef06ed5d4d9c43bf8225758a3192955d",
        n_points=n_points,
        buffer=buffer,
        return_object="linestring",
    )
    buffered_polygon = fused_app.run(
        "46bd457dddfbc47dbddaa703a2603d95ef06ed5d4d9c43bf8225758a3192955d",
        n_points=n_points,
        buffer=buffer,
        return_object="other",
    )
    return gdf_points, gdf_linestring, buffered_polygon


gdf_points, gdf_linestring, buffered_polygon = load_data(
    n_points=n_points, buffer=buffer
)

gdf_points['lat'], gdf_points['lng'] = gdf_points.geometry.centroid.y, gdf_points.geometry.centroid.x


col1, col2 = st.columns(2)

with col1:
    st.write("### 🚗 Vehicle GPS points") # TODO: car and timestamp
    edited_gdf_points = st.data_editor(gdf_points[['lat', 'lng']].head(10).T)
    # TODO: geometry

with col2:
    st.write("### 🛣️ Roads")
    gdf_linestring['geometry_str'] = [str(each) for each in gdf_linestring.geometry]
    st.data_editor(gdf_linestring[['name', 'geometry_str']])


# Create map
st.pydeck_chart(
    pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v9",
        initial_view_state=pdk.ViewState(
            latitude=37.78323,
            longitude=-122.43259,
            zoom=12,
            pitch=0,
        ),
        layers=[
            pdk.Layer(
                "GeoJsonLayer",
                data=gdf_points,
                filled=True,
                stroked=True,
                get_line_color="[100*color, color, 10]",
                get_line_width=100,
            ),
            pdk.Layer(
                "GeoJsonLayer",
                data=gdf_linestring,
                filled=True,
                stroked=True,
                get_line_color="[100*color, color, 10]",
                get_line_width=100,
            ),
            pdk.Layer(
                "GeoJsonLayer",
                data=buffered_polygon,
                filled=False,
                stroked=True,
                get_line_color="[0,0,225]",
                get_line_width=50,
            ),
        ],
    )
)
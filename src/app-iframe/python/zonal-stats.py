import streamlit as st

st.header("Zonal Stats")

st.write(
    """Zonal statistics between a raster and a table of polygons: the raster array is represented by a grayscale image of the DSM and the building footprint are represented with purple `Polygon` objects.

The checkboxes on the sidebar to toggle:
- The raster image
- The building footprint outlines
- The building footprints colored by the mean pixel value of the raster

Buildings are colored based on the mean pixel value of the raster within the polygon.

"""
)

# Imports
import micropip

await micropip.install("pydeck")
import pydeck as pdk

# Create map
lat, lng = 40.76965, -73.990094

layers = {
    "raster": pdk.Layer(
        "BitmapLayer",
        image="https://staging.fused.io/server/v1/realtime-shared/bb187c65d00ffd0d0dfca0e01008699cc80d99ab8a4b9411f451540df379368f/run/tiles/14/4824/6156?dtype_out_raster=png&return_object=arr",
        bounds=[-74.00390625, 40.76390128094588, -73.98193359375, 40.780541431860314],
        opacity=2,
    ),
    "vector": pdk.Layer(
        "GeoJsonLayer",
        data="https://staging.fused.io/server/v1/realtime-shared/bb187c65d00ffd0d0dfca0e01008699cc80d99ab8a4b9411f451540df379368f/run/tiles/16/19298/24626?dtype_out_raster=png&dtype_out_vector=geojson",
        pickable=True,
        filled=False,
        stroked=True,
        get_line_color="[100, 0, 252]",
        get_line_width=4,
    ),
    "vector_sz": pdk.Layer(
        "GeoJsonLayer",
        data="https://staging.fused.io/server/v1/realtime-shared/bb187c65d00ffd0d0dfca0e01008699cc80d99ab8a4b9411f451540df379368f/run/tiles/16/19298/24626?dtype_out_raster=png&dtype_out_vector=geojson",
        pickable=True,
        filled=True,
        stroked=False,
        get_fill_color="[properties.count*.3, properties.count*0.10, properties.count*2]",
        get_line_width=0,
    ),
}

# Filter based on checkboxes
show_raster = st.sidebar.checkbox("Show raster", value=True)
if not show_raster:
    layers.pop("raster")
show_vector = st.sidebar.checkbox("Show vector", value=True)
if not show_vector:
    layers.pop("vector")
show_vector_zs = st.sidebar.checkbox("Show vector with zonal stats", value=True)
if not show_vector_zs:
    layers.pop("vector_sz")

st.pydeck_chart(
    pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v9",
        initial_view_state=pdk.ViewState(
            latitude=lat,
            longitude=lng,
            zoom=15,
            pitch=0,
        ),
        layers=list(layers.values()),
    )
)

import pydeck as pdk
import streamlit as st

st.header('Zonal Stats')

st.write("""
In this tutorial we'll focus on zonal statistics between a raster and polygons in a table. We'll explore how to perform zonal statistics to approximate the height of buildings using a digital surface model (DSM) raster dataset and a table of building footprint polygons. The raster is the ALOS Global DSM "ALOS World 3D - 30m (AW3D30)" captured by the PRISM optical sensor on the ALOS satellite, with a 30-meter horizontal resolution. The buildings dataset is the "Building Footprints" dataset from Microsoft, which contains the `Polygon` of buildings in the United States.


This example interactively illustrates zonal statistics between a raster and a table of polygons: the raster array is represented by a grayscale image of the DSM and the building footprint are represented with purple `Polygon` objects. 


Users can interact with the checkboxes on the sidebar to toggle show/hide:
- The raster image
- The building footprint outlines
- The building footprints colored by the mean pixel value of the raster

You'll notice that the building footprints are colored based on the mean pixel value of the raster within the polygon. The color scale ranges from dark (low values) to bright (high values). This visualization helps identify buildings with higher or lower height based on the average pixel values. 

""")

# Create map
lat, lng = 40.76965, -73.990094

layers = {
    "raster": pdk.Layer(
        "BitmapLayer",
        # data="https://staging.fused.io/server/v1/realtime-shared/bb187c65d00ffd0d0dfca0e01008699cc80d99ab8a4b9411f451540df379368f/run/tiles/{z}/{x}/{y}?dtype_out_raster=png&dtype_out_vector=geojson",
        image="https://staging.fused.io/server/v1/realtime-shared/bb187c65d00ffd0d0dfca0e01008699cc80d99ab8a4b9411f451540df379368f/run/tiles/14/4824/6156?dtype_out_raster=png&return_object=arr",
        bounds=[-74.00390625, 40.76390128094588, -73.98193359375, 40.780541431860314],
        opacity=2,
        # tooltip={"text": "Agg value: {cnt}"} # TODO: UDF should return properties
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
    # TODO
    # 'raster2': pdk.Layer(
    #     "RasterTileLayer",
    #     data="https://staging.fused.io/server/v1/realtime-shared/bb187c65d00ffd0d0dfca0e01008699cc80d99ab8a4b9411f451540df379368f/run/tiles/{z}/{x}/{y}?dtype_out_raster=png",
    #     opacity=200,
    # ),
    "vector_sz": pdk.Layer(
        "GeoJsonLayer",
        # data="https://staging.fused.io/server/v1/realtime-shared/bb187c65d00ffd0d0dfca0e01008699cc80d99ab8a4b9411f451540df379368f/run/tiles/{z}/{x}/{y}?dtype_out_raster=png&dtype_out_vector=geojson",
        data="https://staging.fused.io/server/v1/realtime-shared/bb187c65d00ffd0d0dfca0e01008699cc80d99ab8a4b9411f451540df379368f/run/tiles/16/19298/24626?dtype_out_raster=png&dtype_out_vector=geojson",
        pickable=True,
        filled=True,
        stroked=False,
        get_fill_color="[properties.count*.3, properties.count*0.10, properties.count*2]",
        get_line_width=0,
        tooltip={
            "text": "Agg value: {properties.count}"
        },  # TODO: UDF should return properties
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
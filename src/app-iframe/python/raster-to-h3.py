import streamlit as st

st.title("Raster to H3")

ASSETS = {
    "JRC_GFC2020_V1_S40_E50.tif": {
        "url": "s3://fused-asset/gfc2020/JRC_GFC2020_V1_N60_E20.tif",
        "latlng": [55, 25],
    },
    "JRC_GFC2020_V1_S40_E60.tif": {
        "url": "s3://fused-asset/gfc2020/JRC_GFC2020_V1_S40_E60.tif",
        "latlng": [-45, 65],
    },
    "JRC_GFC2020_V1_N40_E130.tif": {
        "url": "s3://fused-asset/gfc2020/JRC_GFC2020_V1_N40_E130.tif",
        "latlng": [35, 135],
    },
    "JRC_GFC2020_V1_S20_E130.tif": {
        "url": "s3://fused-asset/gfc2020/JRC_GFC2020_V1_S20_E130.tif",
        "latlng": [-25, 135],
    },
    "JRC_GFC2020_V1_N20_E70.tif": {
        "url": "s3://fused-asset/gfc2020/JRC_GFC2020_V1_N20_E70.tif",
        "latlng": [15, 75],
    },
    "JRC_GFC2020_V1_N10_E40.tif": {
        "url": "s3://fused-asset/gfc2020/JRC_GFC2020_V1_N10_E40.tif",
        "latlng": [5, 45],
    },
    "JRC_GFC2020_V1_N50_E0.tif": {
        "url": "s3://fused-asset/gfc2020/JRC_GFC2020_V1_N50_E0.tif",
        "latlng": [45, 5],
    },
    "JRC_GFC2020_V1_N30_W110.tif": {
        "url": "s3://fused-asset/gfc2020/JRC_GFC2020_V1_N30_W110.tif",
        "latlng": [25, -105],
    },
}


asset = st.selectbox("Select Tiff asset", ASSETS.keys())
asset_custom = st.text_input(
    "Or pass your own TIFF _(clear this box to return focus to dropdown)_", None
)
st.write("Your TIFF path is", asset_custom)
h3_size = st.selectbox("Select H3 size", range(4, 8))

st.write("You selected:", ASSETS[asset]["url"])

set_asset = asset_custom or ASSETS[asset]["url"]


# Imports
import micropip

await micropip.install("requests")
await micropip.install("geopandas")
await micropip.install("pydeck")
import fused_app
import pydeck as pdk


@st.cache_data
def load_data(asset, h3_size=5):
    df = fused_app.run(
        "d3802030c15910e19d180c88d5b4cd50281e110a42846eba2d5b73cfb6e93bdb",
        tiff_path=asset,
        h3_size=h3_size,
    )
    return df


df = load_data(set_asset, h3_size=h3_size)
lat, lng = ASSETS[asset]["latlng"]


# Define a layer to display on a map
layer = pdk.Layer(
    "H3HexagonLayer",
    df,
    pickable=True,
    stroked=True,
    filled=True,
    extruded=False,
    get_hexagon="hex",
    get_fill_color="[255 - metric*10, 255, metric*10]",  # metric
    get_line_color=[240, 25, 0],
    line_width_min_pixels=2,
)


# Render
st.pydeck_chart(
    pdk.Deck(
        map_style="mapbox://styles/mapbox/satellite-v9",
        initial_view_state=pdk.ViewState(
            latitude=lat, longitude=lng, zoom=4, bearing=0, pitch=0
        ),
        layers=[layer],
        tooltip={"text": "Agg value: {agg_data}"},
    )
)

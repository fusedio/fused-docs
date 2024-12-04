import micropip
import streamlit as st

await micropip.install(["streamlit-folium"])
import folium
from streamlit_folium import st_folium

st.title("🌎 Exploring VIDA's NEX-GDDP-based climate model")


# Select from list of dataset layers
layers = [
    "cooling_degree_days",
    "dry_spells",
    "extreme_heat_percentile",
    "extreme_pr_percentile",
    "frost_free_season",
    "heating_degree_days",
    "pr",
    "tas",
    "tasmax",
    "tasmin",
]
layer = st.selectbox("Select layer to show", layers)

# Create map
m = folium.Map(
    location=[54.5260, 12.2551], min_zoom=2, zoom_start=3, tiles="Cartodb Positron"
)

# Structure URL to call public UDF
url_raster = (
    "https://www.fused.io/server/v1/realtime-shared/UDF_NEX_GDDP_Cmip6_VIDA/run/tiles/{z}/{x}/{y}?dtype_out_raster=png"
    + f"&layer={layer}"
)

# Create raster tile layer
folium.TileLayer(tiles=url_raster, attr="Fused").add_to(m)

# Render map
st_folium(m, width=300, height=500, use_container_width=True)

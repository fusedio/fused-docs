import folium
import fused_app
import geopandas as gpd
import streamlit as st
from streamlit_folium import st_folium

year = option = st.selectbox(
    "Which year?",
    (2014, 2015, 2016, 2018, 2019, 2020),
)

# st.write("You selected:", option)
# year = st.slider("year", 2014, 2020, 2016)
month = st.slider("month", 1, 12, 6)

period = "a"
# Create map
m = folium.Map(
    location=[39, -98], zoom_start=4, max_zoom=18, min_zoom=2, tiles="Cartodb Positron"
)

# ArcGIS RGB
url_raster = (
    "https://www.fused.io/server/v1/realtime-shared/fsh_7ZrKGaoXb0pLNoDlLVC4mf/run/tiles/{z}/{x}/{y}?dtype_out_raster=png"
    + f"&year={year}"
    + f"&month={str(month).zfill(2)}"
    + f"&period={period}"
)
# st.write(url_raster)

# Create raster tile layer
folium.TileLayer(tiles=url_raster, attr="Fused").add_to(m)  # Base image

# Render map
st_folium(m, width=300, height=500, use_container_width=True)

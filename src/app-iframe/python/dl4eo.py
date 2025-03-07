import micropip

await micropip.install(["folium", "streamlit-folium"])
import folium
import streamlit as st
from streamlit_folium import st_folium

st.title("✈️ AI for object detection on 50cm imagery")

# Create map
m = folium.Map(location=[32.1680, -110.8607], zoom_start=17, tiles="Cartodb Positron")

url_raster = "https://www.fused.io/server/v1/realtime-shared/fsh_4q8U06MA0i7zxHKwr38lvG/run/tiles/{z}/{x}/{y}?dtype_out_raster=png"
url_vector = "https://www.fused.io/server/v1/realtime-shared/fsh_1lgqIqpGaSw9PCXU43mlNh/run/tiles/{z}/{x}/{y}?&dtype_out_vector=mvt"

# Create raster tile layer
folium.TileLayer(tiles=url_raster, attr="Fused").add_to(m)
# Render bounding boxes
folium.plugins.VectorGridProtobuf(url_vector, "inference").add_to(m)

# Render map
st_folium(m, width=300, height=500, use_container_width=True)

st.write(
    """The source GeoTIFF is an Airbus Pleiades image at 50cm over the "The Historic Aviation Bone Yard", in Tucson."""
)

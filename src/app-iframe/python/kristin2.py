import branca
import folium
import fused
import geopandas as gpd
import streamlit as st
from streamlit_folium import st_folium

# Set the title and description of the app
st.title("🌽 Zonal Stats")

# Create map
m = folium.Map(
    location=[39, -98],
    zoom_start=4,
    max_zoom=18,
    min_zoom=2,
    tiles="Cartodb Darkmatter",
)

geo_json_data = fused.run("UDF_Crop_Mask_Zonal_Statistics")


colormap1 = branca.colormap.linear.OrRd_09.colors  # .scale(0, 1)#.reverse()
# colormap1.reverse()
colormap = branca.colormap.LinearColormap(colors=colormap1).scale(0, 1)


# Define a function to style the GeoJson features
def style_function(feature):
    sim_value = feature["properties"].get("corn_sif_mean", -1)
    try:
        color = colormap(sim_value)
        return {"fillColor": color, "color": color, "fillOpacity": 0.7}
    except:
        return {"fillColor": "grey", "color": "grey", "fillOpacity": 0.2}


# Define the tooltip to show the sim value
tooltip = folium.GeoJsonTooltip(
    fields=["corn_sif_mean"],  # Field in the GeoDataFrame to display
    aliases=["SIF:"],  # Alias for the field in the tooltip
    localize=True,
)

folium.GeoJson(geo_json_data, style_function=style_function, tooltip=tooltip).add_to(m)

# Render map
st_folium(m, width=300, height=500, use_container_width=True)

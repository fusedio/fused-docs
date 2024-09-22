import folium
import fused_app
import geopandas as gpd
import streamlit as st
from streamlit_folium import st_folium

# Set the title and description of the app
st.title("Orbiting Carbon Observatory-2 (OCO-2) SIF Observations")
st.write(
    """
This dataset offers global mean daily solar-induced chlorophyll fluorescence (SIF) estimates at 0.05-degree (5 km) spatial and 16-day temporal resolution from September 2014 to July 2020.
Derived from Orbiting Carbon Observatory-2 (OCO-2) SIF data, it uses an artificial neural network (ANN) trained on OCO-2 observations and Moderate Resolution Imaging Spectroradiometer (MODIS) surface reflectance.
The ANN model fills data gaps based on MODIS reflectance and landcover, stratified by biomes and 16-day intervals.
This dataset supports dynamic drought monitoring, agricultural planning, and future SIF satellite missions.
"""
)

# Select year within the date range 2014-09-01 to 2020-07-31
year = st.selectbox(
    "Which year?",
    (2014, 2015, 2016, 2017, 2018, 2019, 2020),
    index=4,  # Sets default year to 2018
)

# Mapping for slider: custom labels adjusted to show 'Month a' and 'Month b'
period_mapping = {
    "2014": [
        "September a",
        "September b",
        "October a",
        "October b",
        "November a",
        "November b",
        "December a",
        "December b",
    ],
    "2015": [
        "January a",
        "January b",
        "February a",
        "February b",
        "March a",
        "March b",
        "April a",
        "April b",
        "May a",
        "May b",
        "June a",
        "June b",
        "July a",
        "July b",
        "August a",
        "August b",
        "September a",
        "September b",
        "October a",
        "October b",
        "November a",
        "November b",
        "December a",
        "December b",
    ],
    "2016": [
        "January a",
        "January b",
        "February a",
        "February b",
        "March a",
        "March b",
        "April a",
        "April b",
        "May a",
        "May b",
        "June a",
        "June b",
        "July a",
        "July b",
        "August a",
        "August b",
        "September a",
        "September b",
        "October a",
        "October b",
        "November a",
        "November b",
        "December a",
        "December b",
    ],
    "2017": [
        "January a",
        "January b",
        "February a",
        "February b",
        "March a",
        "March b",
        "April a",
        "April b",
        "May a",
        "May b",
        "June a",
        "June b",
        "July a",
        "July b",
        "September b",
        "October a",
        "October b",
        "November a",
        "November b",
        "December a",
        "December b",
    ],  # Removed 201708a, 201708b, 201709a
    "2018": [
        "January a",
        "January b",
        "February a",
        "February b",
        "March a",
        "March b",
        "April a",
        "April b",
        "May a",
        "May b",
        "June a",
        "June b",
        "July a",
        "July b",
        "August a",
        "August b",
        "September a",
        "September b",
        "October a",
        "October b",
        "November a",
        "November b",
        "December a",
        "December b",
    ],
    "2019": [
        "January a",
        "January b",
        "February a",
        "February b",
        "March a",
        "March b",
        "April a",
        "April b",
        "May a",
        "May b",
        "June a",
        "June b",
        "July a",
        "July b",
        "August a",
        "August b",
        "September a",
        "September b",
        "October a",
        "October b",
        "November a",
        "November b",
        "December a",
        "December b",
    ],
    "2020": [
        "January a",
        "January b",
        "February a",
        "February b",
        "March a",
        "March b",
        "April a",
        "April b",
        "May a",
        "May b",
        "June a",
        "June b",
        "July a",
        "July b",
    ],
}

# Display the available periods based on selected year
available_periods = period_mapping[str(year)]

# Use select_slider to display custom labels on the slider
selected_label = st.select_slider(
    "Select period:",
    options=available_periods,
    value=available_periods[
        12
    ],  # Default to the first available period of the selected year
)

# Map the selected label to the corresponding period value
period = available_periods.index(selected_label) + 1

# Extract month and sub-period from the selected period
month = (period + 1) // 2  # Approximate month number
sub_period = "a" if period % 2 == 1 else "b"

# Create map
m = folium.Map(
    location=[39, -98], zoom_start=4, max_zoom=18, min_zoom=2, tiles="Cartodb Positron"
)

# ArcGIS RGB
url_raster = f"https://www.fused.io/server/v1/realtime-shared/fsh_7ZrKGaoXb0pLNoDlLVC4mf/run/tiles/{{z}}/{{x}}/{{y}}?dtype_out_raster=png&year={year}&month={str(month).zfill(2)}&period={sub_period}"

# Create raster tile layer
folium.TileLayer(tiles=url_raster, attr="Fused").add_to(m)  # Base image

# Render map
st_folium(m, width=300, height=500, use_container_width=True)

# Add footer with missing data information
st.markdown(
    "<sub>Four time periods (April b 2015, August a 2017, August b 2017, September a 2017) are missing data due to OCO-2 instrument failure, so no SIF data were collected during these times.</sub>",
    unsafe_allow_html=True,
)

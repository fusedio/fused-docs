# Streamlit

Streamlit is an open source Python app builder to turn data scripts into shareable web apps.

![streamlit](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/gifs/streamlit_leaflet.gif)

## Basic walkthrough

### Step 1: Install streamlit

Prepare an environment and install streamlit.

```bash
pip install streamlit
```

### Step 2: Create a UDF

Create a UDF.

As an example, this minimalist UDF returns a dataframe with polygons for each administrative zone in Washington DC.

```python showLineNumbers
@fused.udf
def my_udf(url='https://www2.census.gov/geo/tiger/TIGER_RD18/STATE/11_DISTRICT_OF_COLUMBIA/11/tl_rd22_11_bg.zip'):
    import geopandas as gpd
    return gpd.read_file(url)
```

### Step 3: Create your streamlit app

Create a new Python script for your Streamlit app - in this case in a file called `app.py`. This script will be the entry point of your application.

This script creates a minimalist Streamlit app that runs the UDF then displays its output dataframe.

```python showLineNumbers
import fused
import streamlit as st


st.title("🌎 Dataframe generator")

@fused.udf
def my_udf(url='https://www2.census.gov/geo/tiger/TIGER_RD18/STATE/11_DISTRICT_OF_COLUMBIA/11/tl_rd22_11_bg.zip'):
    import geopandas as gpd
    return gpd.read_file(url)

df = fused.run(udf=my_udf)
st.dataframe(df)
```

### Step 4. Run your streamlit app

Start the app using Streamlit's CLI command.

```bash
streamlit run app.py
```

## Intermediate examples


### Vector

Copy and save the [Isochrone UDF](https://github.com/fusedio/udfs/tree/main/public/Get_Isochrone) on your Workbench. Create a Streamlit app with this code and paste your UDF's token below.

```python showLineNumbers
import folium
import fused
import streamlit as st
import streamlit.components.v1 as components
from streamlit_folium import st_folium

# Parameters
st.markdown("# Isochrone calculator")
costing = st.selectbox(
    "Select transportation mode",
    ["auto", "pedestrian", "bicycle", "truck", "bus", "motor_scooter"],
)
lat = 39.949610
lng = -75.150282

# Run UDF
TOKEN = "53bcd145dc75d8056045470f6c23861c8bd37fe7d0ee42eae716e755cebe2765"
gdf = fused.run(TOKEN, costing=costing, lat=float(lat), lng=float(lng))
gdf.set_crs(epsg=4326, inplace=True)

# Generate map
m = folium.Map([lat, lng], zoom_start=10, tiles="OpenStreetMap.Mapnik")

# Generate point and vector layers
folium.GeoJson(gdf).add_to(m)
folium.Marker(location=[lat, lng], icon=folium.Icon(icon="cloud")).add_to(m)

# Render map
folium_data = st_folium(m)
```


### Raster Tiles

Copy and save the [CDLs Tile UDF](https://github.com/fusedio/udfs/tree/main/public/CDLs_Tile_Example) on your Workbench. Create a Streamlit app with this code and paste your UDF's token below.



```python showLineNumbers
import folium
import streamlit as st
from streamlit_folium import st_folium

# Create map
m = folium.Map(location=[37.43997405227058, -120.9375], zoom_start=11, tiles="Stadia.AlidadeSmoothDark")

# Widgets
st.markdown("# 🚀 Streamlit + Folium + Fused 🚀")
st.markdown("""This UDF shows how to open Cropland Data Layer (CDL) tiff files. The CDL is a categorical land cover dataset that provides information about the types of crops and land cover on agricultural lands in the United States. The CDL is produced by the United States Department of Agriculture (USDA) National Agricultural Statistics Service (NASS) on an annual basis.""")
crop_type = st.selectbox("🌽 Select crop", ["corn", "soy", "wheat", "all", "almond", "grass"])

# Structure URL
TOKEN = "8110ef6e0c66f07f0c73f39843db27ece3960f98f268f38ef2f79f3623faae01"
url = f"https://www.fused.io/server/v1/realtime-shared/{TOKEN}/run/tiles/{{z}}/{{x}}/{{y}}?dtype_out_raster=png"
if crop_type != "all": url += f"&crop_type={crop_type}"

# Create raster tile layer
folium.TileLayer(
    tiles=url,
    attr="Fused",
    name="fused",
    max_zoom=19,
    subdomains=["a", "b", "c"],
).add_to(m)

# Render map
st_folium(m, width=300, height=500, use_container_width=True)
```

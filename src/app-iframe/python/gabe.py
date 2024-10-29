import time
from calendar import month_abbr
from datetime import datetime
from io import BytesIO

import folium
import fused
import geopandas as gpd
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import mercantile
import micropip
import numpy as np
import pandas as pd
import requests
import streamlit as st
from folium.plugins import Draw, SideBySideLayers
from matplotlib.ticker import MaxNLocator
from PIL import Image, ImageColor
from shapely.geometry import box, shape
from streamlit_folium import st_folium

await micropip.install("geopandas")
await micropip.install("fused")

# =====================================
# Helper Functions
# =====================================


# Helper function to create colorbar images for each colormap, including reversed versions
def generate_colormap_images():
    colormap_options = [
        "terrain",
        "viridis",
        "plasma",
        "magma",
        "cividis",
        "twilight",
        "twilight_shifted",
        "turbo",
        "hsv",
        "gist_earth",
        "cubehelix",
    ]
    colormap_images = {}

    for cmap_name in colormap_options:
        for reverse in [False, True]:
            cmap_full_name = cmap_name + ("_r" if reverse else "")
            cmap = cm.get_cmap(cmap_full_name)
            gradient = np.linspace(0, 1, 256)
            gradient = np.vstack((gradient, gradient))

            fig, ax = plt.subplots(figsize=(3, 0.15))
            ax.imshow(gradient, aspect="auto", cmap=cmap)
            ax.axis("off")

            buf = BytesIO()
            fig.savefig(buf, format="png", bbox_inches="tight", pad_inches=0)
            plt.close(fig)
            buf.seek(0)

            colormap_images[cmap_full_name] = Image.open(buf)
    return colormap_images


colormap_images = generate_colormap_images()


# Ensure all session state variables, including default cmap and reverse settings, are initialized
def initialize_session_state():
    if "dem_scale_left" not in st.session_state:
        st.session_state.dem_scale_left = 1000.0
    if "dem_scale_right" not in st.session_state:
        st.session_state.dem_scale_right = 1000.0
    if "grad_scale_left" not in st.session_state:
        st.session_state.grad_scale_left = 0.4
    if "grad_scale_right" not in st.session_state:
        st.session_state.grad_scale_right = 0.4
    if "output_type_left" not in st.session_state:
        st.session_state.output_type_left = "elevation"
    if "output_type_right" not in st.session_state:
        st.session_state.output_type_right = "elevation"
    if "colormap_left" not in st.session_state:
        st.session_state.colormap_left = "terrain"  # Set default cmap
    if "colormap_right" not in st.session_state:
        st.session_state.colormap_right = "terrain"  # Set default cmap
    if "reverse_colormap_left" not in st.session_state:
        st.session_state.reverse_colormap_left = False
    if "reverse_colormap_right" not in st.session_state:
        st.session_state.reverse_colormap_right = False
    if "left_layer_select" not in st.session_state:
        st.session_state.left_layer_select = "Sentinel-2 (S2)"
    if "right_layer_select" not in st.session_state:
        st.session_state.right_layer_select = "Sentinel-1 (S1)"


initialize_session_state()

# Colormap dropdowns for DEM layers
colormap_options = [
    "terrain",
    "viridis",
    "plasma",
    "magma",
    "cividis",
    "twilight",
    "twilight_shifted",
    "turbo",
    "hsv",
    "gist_earth",
    "cubehelix",
]


def get_tiles_from_polygons(polygons, zoom=14):
    all_tiles = []
    for geom in polygons:
        tiles = list(mercantile.tiles(*geom.bounds, zooms=[zoom]))
        polygons_list = []
        filtered_tiles = []

        for tile in tiles:
            west, south, east, north = mercantile.bounds(tile)
            tile_geom = box(west, south, east, north)
            if tile_geom.intersects(geom):
                polygons_list.append(tile_geom)
                filtered_tiles.append(tile)

        data = {
            "x": [tile.x for tile in filtered_tiles],
            "y": [tile.y for tile in filtered_tiles],
            "z": [tile.z for tile in filtered_tiles],
            "geometry": polygons_list,
        }

        gdf = gpd.GeoDataFrame(data, crs="EPSG:4326")
        all_tiles.append(gdf)

    if all_tiles:
        return pd.concat(all_tiles, ignore_index=True)
    else:
        return gpd.GeoDataFrame(columns=["x", "y", "z", "geometry"], crs="EPSG:4326")


def shorten_place_name(full_name):
    if "," in full_name:
        short_name = full_name.split(",")[0]
    else:
        short_name = full_name
    return short_name.replace(" ", "_")


# Define color mapping for CDL and ML layers
land_cover_mapping = {
    0: {"color": "white", "label": "background"},
    1: {"color": "blue", "label": "water"},
    2: {"color": "grey", "label": "developed"},
    3: {"color": "yellow", "label": "corn"},
    4: {"color": "green", "label": "soybeans"},
    5: {"color": "brown", "label": "wheat"},
    6: {"color": "pink", "label": "other agriculture"},
    7: {"color": "olive", "label": "forest/wetlands"},
    8: {"color": "limegreen", "label": "open lands"},
    9: {"color": "orange", "label": "barren"},
}


def generate_histogram(st_map, layer_url_template, layer_name):
    if st_map and "center" in st_map and "zoom" in st_map:
        center_lat = st_map["center"]["lat"]
        center_lng = st_map["center"]["lng"]
        current_zoom = st_map["zoom"]
        tile = mercantile.tile(center_lng, center_lat, current_zoom)
        x, y, z = tile.x, tile.y, tile.z
        tile_url = layer_url_template.format(z=z, x=x, y=y)
        response = requests.get(tile_url)

        if response.status_code == 200:
            img = Image.open(BytesIO(response.content)).convert("RGB")
            img_array = np.array(img)
            all_pixels = img_array.reshape(-1, 3)

            if layer_name in ["Cropland Data (CDL)", "Mask2Former (ML)"]:
                pixel_colors = ["#%02x%02x%02x" % tuple(pixel) for pixel in all_pixels]
                class_counts = {}

                for idx, class_info in land_cover_mapping.items():
                    class_color = class_info["color"]
                    class_color_rgb = ImageColor.getrgb(class_color)
                    class_color_hex = "#%02x%02x%02x" % class_color_rgb
                    count = pixel_colors.count(class_color_hex)
                    class_counts[idx] = count

                total_pixels = sum(class_counts.values())
                class_percentages = {
                    idx: (count / total_pixels) * 100 if total_pixels > 0 else 0
                    for idx, count in class_counts.items()
                }

                fig, ax = plt.subplots(figsize=(6, 4))
                indices = list(class_percentages.keys())
                percentages = [class_percentages[idx] for idx in indices]
                colors = [land_cover_mapping[idx]["color"] for idx in indices]
                labels = [land_cover_mapping[idx]["label"] for idx in indices]

                ax.bar(labels, percentages, color=colors)
                ax.set_ylabel("Percentage of Pixels", color="white")
                ax.set_title(f"Land Cover Distribution ({layer_name})", color="white")
                ax.tick_params(axis="x", rotation=45, colors="white")
                ax.tick_params(axis="y", colors="white")
                ax.set_facecolor("black")
                fig.patch.set_facecolor("black")
                plt.tight_layout()
                return fig
            else:
                fig, axs = plt.subplots(3, 1, figsize=(4, 3), sharex=True)
                colors = ["red", "green", "blue"]
                for i in range(3):
                    axs[i].hist(
                        all_pixels[:, i],
                        bins=40,
                        color=colors[i],
                        alpha=0.7,
                        density=True,
                    )
                    axs[i].set_ylabel("Frequency", color="white")
                    axs[i].set_title(
                        f"{colors[i].capitalize()}", color="white", fontsize=10
                    )
                    axs[i].xaxis.set_major_locator(MaxNLocator(integer=True))
                    axs[i].set_xlim(0, 255)
                    axs[i].set_facecolor("black")
                    axs[i].tick_params(axis="x", colors="white")
                    axs[i].tick_params(axis="y", colors="white")
                    for spine in axs[i].spines.values():
                        spine.set_edgecolor("white")
                axs[-1].set_xlabel("Pixel Intensity", color="white")
                fig.patch.set_facecolor("black")
                plt.tight_layout()
                return fig
        else:
            st.write(f"No pixel data available for {layer_name}.")
            return None
    else:
        st.write("Map bounds not available.")
        return None


def create_layers(layer_name, base_url, params_left, params_right):
    url_left = base_url.format(**params_left)
    url_right = base_url.format(**params_right)
    layer_left = folium.TileLayer(
        tiles=url_left,
        attr=f"{layer_name} Left",
        name=f"{layer_name} Left",
        overlay=True,
        control=False,
    )
    layer_right = folium.TileLayer(
        tiles=url_right,
        attr=f"{layer_name} Right",
        name=f"{layer_name} Right",
        overlay=True,
        control=False,
    )
    return layer_left, layer_right, url_left, url_right


# =====================================
# Streamlit App Configuration
# =====================================

st.set_page_config(
    page_title="Cube Factory", layout="wide", initial_sidebar_state="expanded"
)

# =====================================
# Initialize Session State
# =====================================

if "drawn_polygons" not in st.session_state:
    st.session_state.drawn_polygons = []

if "all_tiles" not in st.session_state:
    st.session_state.all_tiles = gpd.GeoDataFrame(
        columns=["x", "y", "z", "geometry"], crs="EPSG:4326"
    )

if "map_center" not in st.session_state:
    st.session_state.map_center = [37.773972, -122.431297]

if "map_zoom" not in st.session_state:
    st.session_state.map_zoom = 12

if "searched_location" not in st.session_state:
    st.session_state.searched_location = None

if "place_name" not in st.session_state:
    st.session_state.place_name = ""

if "selected_place" not in st.session_state:
    st.session_state.selected_place = None

if "last_selected_place" not in st.session_state:
    st.session_state.last_selected_place = None

if "time_slice_count" not in st.session_state:
    st.session_state.time_slice_count = 2

if "brightness_left" not in st.session_state:
    st.session_state.brightness_left = 1.2

if "gamma_left" not in st.session_state:
    st.session_state.gamma_left = 0.55

if "brightness_right" not in st.session_state:
    st.session_state.brightness_right = 1.2

if "gamma_right" not in st.session_state:
    st.session_state.gamma_right = 0.55

if "threshold" not in st.session_state:
    st.session_state.threshold = 0.35

if "report_year" not in st.session_state:
    st.session_state.report_year = 2022

if "report_month_number" not in st.session_state:
    st.session_state.report_month_number = "06"

if "left_histogram" not in st.session_state:
    st.session_state.left_histogram = None

if "right_histogram" not in st.session_state:
    st.session_state.right_histogram = None

if "zoom_level" not in st.session_state:
    st.session_state.zoom_level = 14

# Initialize other session state variables
initialize_session_state()

# =====================================
# Geocoder Functionality
# =====================================


def geocode_location(place_name):
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={place_name}"
    response = requests.get(url)
    if response.status_code == 200 and response.json():
        return response.json()
    else:
        st.error("Location not found. Please try another place.")
        return None


# Add a search bar for the geocoder
st.sidebar.subheader("Location Search")
st.session_state.place_name = st.sidebar.text_input(
    "Enter a place to search", value=st.session_state.place_name
)

if st.session_state.place_name:
    with st.spinner("Searching for places..."):
        results = geocode_location(st.session_state.place_name)
    if results:
        options = {
            f"{res['display_name']}": (float(res["lat"]), float(res["lon"]))
            for res in results
        }
        if (
            "last_search" not in st.session_state
            or st.session_state.last_search != st.session_state.place_name
        ):
            st.session_state.selected_place = list(options.keys())[0]
        st.session_state.selected_place = st.sidebar.selectbox(
            "Select the correct location:",
            list(options.keys()),
            index=list(options.keys()).index(st.session_state.selected_place),
        )
        st.session_state.last_search = st.session_state.place_name

        if st.session_state.last_selected_place != st.session_state.selected_place:
            coordinates = options[st.session_state.selected_place]
            st.session_state.map_center = [coordinates[0], coordinates[1]]
            st.session_state.map_zoom = 12
            st.session_state.searched_location = {
                "coordinates": coordinates,
                "full_name": st.session_state.selected_place,
            }
            st.session_state.last_selected_place = st.session_state.selected_place
else:
    st.session_state.selected_place = None

# =====================================
# Survey Period Selection
# =====================================

st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.subheader("Select Survey Period")
years = [2021, 2022, 2023, 2024]
month_abbr_list = list(month_abbr)[1:]

col1, col2 = st.sidebar.columns([2, 3])

with col1:
    st.session_state.report_year = st.selectbox("Year", years, index=1)

with col2:
    report_month_str = st.radio("Month", month_abbr_list, index=5, horizontal=True)
    report_month = month_abbr_list.index(report_month_str) + 1
    st.session_state.report_month_number = f"{report_month:02d}"

st.title("Cube Factory")

# Buttons row at the top
col_left_button, col_right_button, col_zoom = st.columns([1, 1, 1])

with col_left_button:
    if st.button("Reset Drawings", key="reset_button"):
        with st.spinner("Resetting the map..."):
            time.sleep(1)
            st.session_state.drawn_polygons = []
            st.session_state.all_tiles = gpd.GeoDataFrame(
                columns=["x", "y", "z", "geometry"], crs="EPSG:4326"
            )
            st.experimental_rerun()

with col_right_button:
    st.session_state.zoom_level = st.selectbox(
        "Tile Zoom Level",
        [13, 14, 15],
        index=1,
        help="Select the zoom level for tile generation. Higher zoom means smaller tiles but more detail.",
    )

# Remove the "Refresh Map" button
st.markdown(
    """
    <style>
    div.stButton > button:first-child {
            color: cyan;
        border: 2px solid cyan;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Define available bands
bands_dict = {
    "S2 Band 1 - Coastal aerosol (443 nm)": "B01",
    "S2 Band 2 - Blue (490 nm)": "B02",
    "S2 Band 3 - Green (560 nm)": "B03",
    "S2 Band 4 - Red (665 nm)": "B04",
    "S2 Band 5 - Vegetation Red Edge 1 (705 nm)": "B05",
    "S2 Band 6 - Vegetation Red Edge 2 (740 nm)": "B06",
    "S2 Band 7 - Vegetation Red Edge 3 (783 nm)": "B07",
    "S2 Band 8 - NIR (842 nm)": "B08",
    "S2 Band 8A - Narrow NIR (865 nm)": "B8A",
    "S2 Band 9 - Water vapor (945 nm)": "B09",
    "S2 Band 10 - SWIR - Cirrus (1375 nm)": "B10",
    "S2 Band 11 - SWIR 1 (1610 nm)": "B11",
    "S2 Band 12 - SWIR 2 (2190 nm)": "B12",
    "Burn ND Index: Bands [8,12]": "burn",
    "Glacier ND Index: Bands [3,4]": "glacier",
    "Moisture ND Index: Bands [8,11]": "moisture",
    "Snow ND Index: Bands [3,11]": "snow",
    "Vegetation ND Index: Bands [8,4]": "veg",
    "Water ND Index: Bands [3,8]": "water",
    "Scene Classification Layer": "SCL",
    "DEM (Digital Elevation Model)": "DEM",
    "CDL (Cropland Data)": "CDL",
    "ML (Mask2Former)": "ML",
    "LULC (International Land Use Land Cover)": "LULC",
    "None": "None",
}

st.sidebar.markdown(
    "<h2 style='text-align:center;'>Select Cube Layers</h2>", unsafe_allow_html=True
)

# Red Channel
st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown(
    "<span class='selectbox-label' style='color:red;'>Red Channel</span>",
    unsafe_allow_html=True,
)
red_band_options = [f"🔴 {option}" for option in bands_dict.keys()]
red_band = st.sidebar.selectbox("", red_band_options, index=3, key="red_band")
red_band = red_band.replace("🔴 ", "")

# Green Channel
st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown(
    "<span class='selectbox-label' style='color:green;'>Green Channel</span>",
    unsafe_allow_html=True,
)
green_band_options = [f"🟢 {option}" for option in bands_dict.keys()]
green_band = st.sidebar.selectbox("", green_band_options, index=2, key="green_band")
green_band = green_band.replace("🟢 ", "")

# Blue Channel
st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown(
    "<span class='selectbox-label' style='color:blue;'>Blue Channel</span>",
    unsafe_allow_html=True,
)
blue_band_options = [f"🔵 {option}" for option in bands_dict.keys()]
blue_band = st.sidebar.selectbox("", blue_band_options, index=1, key="blue_band")
blue_band = blue_band.replace("🔵 ", "")

# Alpha Channel
st.sidebar.markdown("<hr>", unsafe_allow_html=True)
st.sidebar.markdown(
    "<span class='selectbox-label' style='color:white;'>Alpha Channel</span>",
    unsafe_allow_html=True,
)
alpha_band_options = bands_dict.keys()
alpha_band = st.sidebar.selectbox(
    "", alpha_band_options, index=len(bands_dict) - 1, key="alpha_band"
)

pR, pG, pB = bands_dict[red_band], bands_dict[green_band], bands_dict[blue_band]
alpha_var = bands_dict.get(alpha_band, False)

# Base URL definitions including DEM parameters
base_url_dem = (
    "https://www.fused.io/server/v1/realtime-shared/fsh_LNOYawr1nTZ2J9ipmQX8H/run/tiles/{z}/{x}/{y}"
    "?dtype_out_raster=png"
    "&scale={scale}"
    "&grad_scale={grad_scale}"
    "&output_type={output_type}"
    "&cmap={cmap}"  # Include cmap in the URL
)

# Common parameters with the latest inputs
common_params_left = {
    "z": "{z}",
    "x": "{x}",
    "y": "{y}",
    "time_slice_count": st.session_state.time_slice_count,
    "month": st.session_state.report_month_number,
    "year": st.session_state.report_year,
    "threshold": st.session_state.threshold,
    "gamma": st.session_state.gamma_left,
    "brightness": st.session_state.brightness_left,
    "pR": pR,
    "pG": pG,
    "pB": pB,
}

common_params_right = {
    "z": "{z}",
    "x": "{x}",
    "y": "{y}",
    "time_slice_count": st.session_state.time_slice_count,
    "month": st.session_state.report_month_number,
    "year": st.session_state.report_year,
    "threshold": st.session_state.threshold,
    "gamma": st.session_state.gamma_right,
    "brightness": st.session_state.brightness_right,
    "pR": pR,
    "pG": pG,
    "pB": pB,
}


# Map Creation and Layer Addition
def create_map(common_params_left, common_params_right):
    url_raster = "https://www.fused.io/server/v1/realtime-shared/fsh_3QYQiMYzgyV18rUBdrOEpO/run/tiles/{z}/{x}/{y}?dtype_out_raster=png"
    m = folium.Map(
        location=st.session_state.map_center,
        zoom_start=st.session_state.map_zoom,
        max_zoom=16,
        min_zoom=10,
    )

    folium.TileLayer(
        tiles=url_raster,
        name="Raster Layer",
        attr="© Raster Data",
        overlay=False,
        control=False,
        show=True,
    ).add_to(m)

    # Commenting out the marker addition to prevent snapping back
    # if st.session_state.searched_location:
    #     coordinates = st.session_state.searched_location["coordinates"]
    #     full_name = st.session_state.searched_location["full_name"]
    #     folium.Marker(location=coordinates, popup=folium.Popup(full_name, max_width=300), tooltip="Click for more info").add_to(m)

    base_url_s2 = (
        "https://www.fused.io/server/v1/realtime-shared/fsh_1vSzLmBR893VbEB431S8Q7/run/tiles/{z}/{x}/{y}"
        "?dtype_out_raster=png"
        "&time_slice_count={time_slice_count}"
        "&month={month}"
        "&year={year}"
        "&threshold={threshold}"
        "&gamma={gamma}"
        "&brightness={brightness}"
        "&pR={pR}"
        "&pG={pG}"
        "&pB={pB}"
    )

    base_url_s1 = (
        "https://www.fused.io/server/v1/realtime-shared/fsh_5XNFWLhOQl2uu9NZQVyBRq/run/tiles/{z}/{x}/{y}"
        "?dtype_out_raster=png"
        "&month={month}"
        "&year={year}"
        "&threshold={threshold}"
        "&gamma={gamma}"
        "&brightness={brightness}"
    )

    base_url_cdl = "https://www.fused.io/server/v1/realtime-shared/fsh_5yk3sgkauZEb6LFZIW6RqU/run/tiles/{z}/{x}/{y}?dtype_out_raster=png&year={year}"
    base_url_ml = "https://www.fused.io/server/v1/realtime-shared/fsh_6odGdx7ImVuDN8GNhSspHY/run/tiles/{z}/{x}/{y}?dtype_out_raster=png&year={year}"
    base_url_lulc = "https://www.fused.io/server/v1/realtime-shared/fsh_79UwhJ3nA78ncxFTZtCNei/run/tiles/{z}/{x}/{y}?dtype_out_raster=png"

    # Recompute params_dem_left and params_dem_right using the latest values
    colormap_name_left = st.session_state.colormap_left
    if st.session_state.reverse_colormap_left:
        colormap_name_left += "_r"

    params_dem_left = {
        "z": "{z}",
        "x": "{x}",
        "y": "{y}",
        "scale": st.session_state.dem_scale_left,
        "grad_scale": st.session_state.grad_scale_left,
        "output_type": st.session_state.output_type_left,
        "cmap": colormap_name_left,
    }

    colormap_name_right = st.session_state.colormap_right
    if st.session_state.reverse_colormap_right:
        colormap_name_right += "_r"

    params_dem_right = {
        "z": "{z}",
        "x": "{x}",
        "y": "{y}",
        "scale": st.session_state.dem_scale_right,
        "grad_scale": st.session_state.grad_scale_right,
        "output_type": st.session_state.output_type_right,
        "cmap": colormap_name_right,
    }

    # Create layers
    s2_layer_left, s2_layer_right, url_s2_left, url_s2_right = create_layers(
        "Sentinel-2 (S2)", base_url_s2, common_params_left, common_params_right
    )
    s1_layer_left, s1_layer_right, url_s1_left, url_s1_right = create_layers(
        "Sentinel-1 (S1)", base_url_s1, common_params_left, common_params_right
    )

    params_no_bg_left = {
        "z": "{z}",
        "x": "{x}",
        "y": "{y}",
        "year": st.session_state.report_year,
    }
    params_no_bg_right = {
        "z": "{z}",
        "x": "{x}",
        "y": "{y}",
        "year": st.session_state.report_year,
    }

    cdl_layer_left, cdl_layer_right, url_cdl_left, url_cdl_right = create_layers(
        "Cropland Data (CDL)", base_url_cdl, params_no_bg_left, params_no_bg_right
    )
    ml_layer_left, ml_layer_right, url_ml_left, url_ml_right = create_layers(
        "Mask2Former (ML)", base_url_ml, params_no_bg_left, params_no_bg_right
    )
    dem_layer_left, dem_layer_right, url_dem_left, url_dem_right = create_layers(
        "Digital Elevation Model (DEM)", base_url_dem, params_dem_left, params_dem_right
    )
    lulc_layer_left, lulc_layer_right, url_lulc_left, url_lulc_right = create_layers(
        "Land Use Land Cover (LULC)",
        base_url_lulc,
        params_no_bg_left,
        params_no_bg_right,
    )

    layers_dict = {
        "Sentinel-2 (S2)": {
            "layer_left": s2_layer_left,
            "layer_right": s2_layer_right,
            "url_template_left": url_s2_left,
            "url_template_right": url_s2_right,
        },
        "Sentinel-1 (S1)": {
            "layer_left": s1_layer_left,
            "layer_right": s1_layer_right,
            "url_template_left": url_s1_left,
            "url_template_right": url_s1_right,
        },
        "Cropland Data (CDL)": {
            "layer_left": cdl_layer_left,
            "layer_right": cdl_layer_right,
            "url_template_left": url_cdl_left,
            "url_template_right": url_cdl_right,
        },
        "Mask2Former (ML)": {
            "layer_left": ml_layer_left,
            "layer_right": ml_layer_right,
            "url_template_left": url_ml_left,
            "url_template_right": url_ml_right,
        },
        "Digital Elevation Model (DEM)": {
            "layer_left": dem_layer_left,
            "layer_right": dem_layer_right,
            "url_template_left": url_dem_left,
            "url_template_right": url_dem_right,
        },
        "Land Use Land Cover (LULC)": {
            "layer_left": lulc_layer_left,
            "layer_right": lulc_layer_right,
            "url_template_left": url_lulc_left,
            "url_template_right": url_lulc_right,
        },
    }

    if not st.session_state.all_tiles.empty:
        folium.GeoJson(
            st.session_state.all_tiles,
            name="Overlapping Tiles",
            style_function=lambda feature: {
                "color": "cyan",
                "fillColor": "cyan",
                "opacity": 0.5,
                "weight": 2,
            },
        ).add_to(m)

    if st.session_state.drawn_polygons:
        drawn_polygons_gdf = gpd.GeoDataFrame(
            geometry=st.session_state.drawn_polygons, crs="EPSG:4326"
        )
        folium.GeoJson(
            drawn_polygons_gdf,
            name="Drawn Polygons",
            style_function=lambda feature: {
                "color": "yellow",
                "fillColor": "yellow",
                "opacity": 0.5,
                "weight": 2,
            },
        ).add_to(m)

    draw = Draw(
        export=False,
        position="topleft",
        draw_options={
            "polyline": False,
            "polygon": True,
            "circle": False,
            "rectangle": True,
            "marker": False,
            "circlemarker": False,
        },
        edit_options={"edit": False, "remove": False},
    )
    draw.add_to(m)
    return m, layers_dict


# Update the common parameters
common_params_left["gamma"], common_params_left["brightness"] = (
    st.session_state.gamma_left,
    st.session_state.brightness_left,
)
common_params_right["gamma"], common_params_right["brightness"] = (
    st.session_state.gamma_right,
    st.session_state.brightness_right,
)

# Re-create the map with updated parameters
m, layers_dict = create_map(common_params_left, common_params_right)

# Map headers and controls
col_left_map, col_right_map = st.columns(2)

with col_left_map:
    # Use st.session_state.left_layer_select directly
    left_layer_display_name = st.selectbox(
        "Select Input (Left)",
        list(layers_dict.keys()),
        index=list(layers_dict.keys()).index(st.session_state.left_layer_select),
        key="left_layer_select",
    )

    # DEM controls if DEM is selected
    if st.session_state.left_layer_select == "Digital Elevation Model (DEM)":
        selected_colormap_left = st.selectbox(
            "Colormap (Left)",
            options=colormap_options,
            format_func=lambda name: f"{name.capitalize()}",
            index=colormap_options.index(st.session_state.colormap_left),
            key="left_colormap_select",
        )
        if selected_colormap_left != st.session_state.colormap_left:
            st.session_state.colormap_left = selected_colormap_left
            st.experimental_rerun()

        # Reverse colormap checkbox
        st.checkbox(
            "Reverse Colormap (Left)",
            value=st.session_state.reverse_colormap_left,
            key="reverse_colormap_left",
        )

        # Update colormap name based on reverse_colormap_left
        colormap_name_left = st.session_state.colormap_left
        if st.session_state.reverse_colormap_left:
            colormap_name_left += "_r"

        # Display colormap image
        st.image(
            colormap_images[colormap_name_left],
            caption=f"{colormap_name_left.capitalize()} Colormap",
            use_column_width=True,
        )

        # Gradient and elevation scales
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.grad_scale_left = st.slider(
                "Gradient Scale (Left)",
                0.1,
                2.0,
                value=st.session_state.grad_scale_left,
                step=0.1,
            )
        with col2:
            st.session_state.dem_scale_left = st.slider(
                "Elevation Scale (Left)",
                50.0,
                5000.0,
                value=st.session_state.dem_scale_left,
                step=50.0,
            )

        # Output type
        selected_output_type = st.selectbox(
            "Output Type (Left)",
            ["elevation", "grad_angle", "grad_mag", "grad_x", "grad_y"],
            index=["elevation", "grad_angle", "grad_mag", "grad_x", "grad_y"].index(
                st.session_state.output_type_left
            ),
            key="left_output_type",
        )
        if selected_output_type != st.session_state.output_type_left:
            st.session_state.output_type_left = selected_output_type
            st.experimental_rerun()

    # S2 controls if S2 is selected
    elif st.session_state.left_layer_select == "Sentinel-2 (S2)":
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.time_slice_count = st.slider(
                "Time Slice Agg (Left)",
                min_value=1,
                max_value=5,
                value=st.session_state.time_slice_count,
                step=1,
            )
        with col2:
            st.session_state.threshold = st.slider(
                "Radiance Threshold (Left)",
                min_value=0.3,
                max_value=1.3,
                value=st.session_state.threshold,
                step=0.05,
            )

    # Brightness/Gamma controls for Sentinel layers
    if st.session_state.left_layer_select in ["Sentinel-2 (S2)", "Sentinel-1 (S1)"]:
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.brightness_left = st.slider(
                "Brightness (Left)",
                min_value=0.0,
                max_value=2.0,
                value=st.session_state.brightness_left,
                step=0.1,
            )
        with col2:
            st.session_state.gamma_left = st.slider(
                "Gamma (Left)",
                min_value=0.0,
                max_value=2.0,
                value=st.session_state.gamma_left,
                step=0.05,
            )

with col_right_map:
    # Use st.session_state.right_layer_select directly
    right_layer_display_name = st.selectbox(
        "Select Target (Right)",
        list(layers_dict.keys()),
        index=list(layers_dict.keys()).index(st.session_state.right_layer_select),
        key="right_layer_select",
    )

    if st.session_state.right_layer_select == "Digital Elevation Model (DEM)":
        selected_colormap_right = st.selectbox(
            "Colormap (Right)",
            options=colormap_options,
            format_func=lambda name: f"{name.capitalize()}",
            index=colormap_options.index(st.session_state.colormap_right),
            key="right_colormap_select",
        )
        if selected_colormap_right != st.session_state.colormap_right:
            st.session_state.colormap_right = selected_colormap_right
            st.experimental_rerun()

        st.checkbox(
            "Reverse Colormap (Right)",
            value=st.session_state.reverse_colormap_right,
            key="reverse_colormap_right",
        )

        colormap_name_right = st.session_state.colormap_right
        if st.session_state.reverse_colormap_right:
            colormap_name_right += "_r"

        st.image(
            colormap_images[colormap_name_right],
            caption=f"{colormap_name_right.capitalize()} Colormap",
            use_column_width=True,
        )

        col1, col2 = st.columns(2)
        with col1:
            st.session_state.grad_scale_right = st.slider(
                "Gradient Scale (Right)",
                0.1,
                2.0,
                value=st.session_state.grad_scale_right,
                step=0.1,
            )
        with col2:
            st.session_state.dem_scale_right = st.slider(
                "Elevation Scale (Right)",
                50.0,
                5000.0,
                value=st.session_state.dem_scale_right,
                step=50.0,
            )

        selected_output_type = st.selectbox(
            "Output Type (Right)",
            ["elevation", "grad_angle", "grad_mag", "grad_x", "grad_y"],
            index=["elevation", "grad_angle", "grad_mag", "grad_x", "grad_y"].index(
                st.session_state.output_type_right
            ),
            key="right_output_type",
        )
        if selected_output_type != st.session_state.output_type_right:
            st.session_state.output_type_right = selected_output_type
            st.experimental_rerun()

    elif st.session_state.right_layer_select == "Sentinel-2 (S2)":
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.time_slice_count = st.slider(
                "Time Slice Agg (Right)",
                min_value=1,
                max_value=5,
                value=st.session_state.time_slice_count,
                step=1,
            )
        with col2:
            st.session_state.threshold = st.slider(
                "Radiance Threshold (Right)",
                min_value=0.3,
                max_value=1.3,
                value=st.session_state.threshold,
                step=0.05,
            )

    if st.session_state.right_layer_select in ["Sentinel-2 (S2)", "Sentinel-1 (S1)"]:
        col1, col2 = st.columns(2)
        with col1:
            st.session_state.brightness_right = st.slider(
                "Brightness (Right)",
                min_value=0.0,
                max_value=2.0,
                value=st.session_state.brightness_right,
                step=0.1,
            )
        with col2:
            st.session_state.gamma_right = st.slider(
                "Gamma (Right)",
                min_value=0.0,
                max_value=2.0,
                value=st.session_state.gamma_right,
                step=0.05,
            )

# Update the common parameters again if any changes were made
common_params_left["gamma"], common_params_left["brightness"] = (
    st.session_state.gamma_left,
    st.session_state.brightness_left,
)
common_params_right["gamma"], common_params_right["brightness"] = (
    st.session_state.gamma_right,
    st.session_state.brightness_right,
)

# Re-create the map with updated parameters
m, layers_dict = create_map(common_params_left, common_params_right)

left_layer_display_name = st.session_state.left_layer_select
right_layer_display_name = st.session_state.right_layer_select
left_layer = layers_dict[left_layer_display_name]["layer_left"]
right_layer = layers_dict[right_layer_display_name]["layer_right"]
left_layer_url_template = layers_dict[left_layer_display_name]["url_template_left"]
right_layer_url_template = layers_dict[right_layer_display_name]["url_template_right"]

left_layer.add_to(m)
right_layer.add_to(m)
sbs = SideBySideLayers(left_layer, right_layer)
sbs.add_to(m)

col_map, col_analytics = st.columns([3, 1])

with col_map:
    st.markdown(f"[L] {left_layer_display_name} <> [R] {right_layer_display_name}")
    st_map = st_folium(m, height=700, key="map", use_container_width=True)

    # Capture the current map center and zoom level
    if st_map and "center" in st_map and "zoom" in st_map:
        st.session_state.map_center = [st_map["center"]["lat"], st_map["center"]["lng"]]
        st.session_state.map_zoom = st_map["zoom"]
        # Overwrite the last searched location with the current map center
        st.session_state.searched_location = {
            "coordinates": st.session_state.map_center,
            "full_name": "Current Location",
        }
        st.session_state.last_selected_place = "Current Location"

    # Move the "Tilefy!" button below the map
    tilefy_button = st.button("Tilefy!", key="tilefy_button")
    st.markdown(
        """
        <style>
        div.stButton > button:first-child {
            width: 100%;
            color: cyan;
            border: 2px solid cyan;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.write(f"**Total Tiles Selected:** {len(st.session_state.all_tiles)}")

    st.header("Export Tiles")
    base_filename = st.text_input(
        "Enter a base filename for the export:", value="tiles"
    )

    if st.button("Export Tiles"):
        if not st.session_state.all_tiles.empty:
            with st.spinner("Exporting tiles..."):
                (
                    st.session_state.all_tiles["R"],
                    st.session_state.all_tiles["G"],
                    st.session_state.all_tiles["B"],
                    st.session_state.all_tiles["A"],
                    st.session_state.all_tiles["Target"],
                ) = (pR, pG, pB, alpha_var, right_layer_display_name)
                timestamp, short_place_name = datetime.now().strftime(
                    "%Y%m%d_%H%M%S"
                ), (
                    shorten_place_name(st.session_state.selected_place)
                    if st.session_state.selected_place
                    else "unknown_location"
                )
                filename = f"{base_filename}_{timestamp}_{short_place_name}.pq"
                st.session_state.all_tiles.to_parquet("tiles.pq")
                fused.api.upload("tiles.pq", f"fd://gabe/gdf_folder/{filename}")
                st.success(f"Tiles exported successfully as {filename}")
        else:
            st.info(
                "No tiles to export. Please draw polygons on the map and press 'Tilefy!' to process them."
            )

with col_analytics:
    st.markdown("<h4>Spot Analytics (L)</h4>", unsafe_allow_html=True)
    if st.button("Update L"):
        with st.spinner("Generating histogram..."):
            st.session_state.left_histogram = generate_histogram(
                st_map, left_layer_url_template, left_layer_display_name
            )
    if st.session_state.left_histogram:
        st.pyplot(st.session_state.left_histogram)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h4>Spot Analytics (R)</h4>", unsafe_allow_html=True)
    if st.button("Update R"):
        with st.spinner("Generating histogram..."):
            st.session_state.right_histogram = generate_histogram(
                st_map, right_layer_url_template, right_layer_display_name
            )
    if st.session_state.right_histogram:
        st.pyplot(st.session_state.right_histogram)

# Capture drawn features and update the map center and zoom
if st_map and "all_drawings" in st_map and st_map["all_drawings"]:
    drawn_features = st_map["all_drawings"]
    if isinstance(drawn_features, list):
        new_drawn = False
        for feature in drawn_features:
            geom = shape(feature["geometry"])
            wkt = geom.wkt
            if wkt not in [poly.wkt for poly in st.session_state.drawn_polygons]:
                st.session_state.drawn_polygons.append(geom)
                new_drawn = True
        if new_drawn:
            st.experimental_rerun()

if "tilefy_button" in locals() and tilefy_button:
    if st.session_state.drawn_polygons:
        with st.spinner("Processing tiles..."):
            # Update map center and zoom based on current map view
            if st_map and "center" in st_map and "zoom" in st_map:
                st.session_state.map_center = [
                    st_map["center"]["lat"],
                    st_map["center"]["lng"],
                ]
                st.session_state.map_zoom = st_map["zoom"]
            new_tiles = get_tiles_from_polygons(
                st.session_state.drawn_polygons, zoom=st.session_state.zoom_level
            )
            st.session_state.all_tiles = new_tiles.drop_duplicates(
                subset=["x", "y", "z"]
            )
            st.success(
                f"Tiles have been processed at zoom level {st.session_state.zoom_level}! You can now export them."
            )
        st.experimental_rerun()
    else:
        st.info(
            "No polygons drawn. Please draw polygons on the map before pressing 'Tilefy!'."
        )

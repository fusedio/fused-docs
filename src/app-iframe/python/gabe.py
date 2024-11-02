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
import numpy as np
import pandas as pd
import requests
import streamlit as st
from folium.plugins import Draw, SideBySideLayers
from matplotlib.ticker import MaxNLocator
from PIL import Image, ImageColor
from shapely.geometry import box, shape
from streamlit_folium import st_folium

# =====================================
# Helper Functions
# =====================================

LULC_IO_COLORS = {
    1: {"color": (65, 155, 223), "label": "Water"},
    2: {"color": (57, 125, 73), "label": "Trees"},
    4: {"color": (57, 125, 73), "label": "Flooded Veg"},
    5: {"color": (228, 150, 53), "label": "Crops"},
    7: {"color": (196, 40, 27), "label": "Built"},
    8: {"color": (165, 155, 143), "label": "Bare"},
    9: {"color": (168, 235, 255), "label": "Snow"},
    10: {"color": (97, 97, 97), "label": "Clouds"},
    11: {"color": (227, 226, 195), "label": "Rangeland"},
}


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
    if "initial_map_loaded" not in st.session_state:
        st.session_state.initial_map_loaded = False  # Flag to track the very first load
    if "user_moved_map" not in st.session_state:
        st.session_state.user_moved_map = (
            False  # Track if the user has moved the map manually
        )
    if "initial_map_loaded" not in st.session_state:
        st.session_state.initial_map_loaded = False  # Flag for the initial map load
    if "reverse_colormap_left" not in st.session_state:
        st.session_state.reverse_colormap_left = False
    if "reverse_colormap_right" not in st.session_state:
        st.session_state.reverse_colormap_right = False
    if "colormap_left" not in st.session_state:
        st.session_state.colormap_left = "terrain"
    if "colormap_right" not in st.session_state:
        st.session_state.colormap_right = "terrain"
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


def get_tiles_from_polygons(polygons, zoom=None):
    # Force the function to use the zoom level defined in session state
    zoom = st.session_state.zoom_level

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
    6: {"color": "pink", "label": "agri (other)"},
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

            if layer_name == "Digital Elevation Model (DEM)":
                # Get pixel intensities before they are mapped to colors
                grayscale_intensity = np.mean(img_array, axis=2).flatten()

                # Get the colormap for coloring bars
                cmap_name = (
                    st.session_state.colormap_left
                    if layer_name == st.session_state.left_layer_select
                    else st.session_state.colormap_right
                )
                cmap = cm.get_cmap(cmap_name)

                # Create histogram
                fig, ax = plt.subplots(figsize=(6, 4))
                n, bins, patches = ax.hist(
                    grayscale_intensity,
                    bins=40,
                    color="gray",
                    alpha=0.7,
                    edgecolor="black",
                )

                # Apply colormap to histogram bars
                bin_centers = 0.5 * (bins[:-1] + bins[1:])
                colormap_colors = cmap(
                    (bin_centers - bin_centers.min())
                    / (bin_centers.max() - bin_centers.min())
                )

                for patch, color in zip(patches, colormap_colors):
                    patch.set_facecolor(color)

                ax.set_xlabel("Pixel Intensity", color="white")
                ax.set_ylabel("Frequency", color="white")
                ax.set_title(f"DEM Pixel Intensity Distribution", color="white")
                ax.tick_params(colors="white")
                ax.set_facecolor("black")
                fig.patch.set_facecolor("black")
                plt.tight_layout()
                return fig
            elif layer_name in [
                "Cropland Data (CDL)",
                "Mask2Former (ML)",
                "Land Use Land Cover (LULC)",
            ]:
                # Histogram generation for CDL, ML, and LULC layers (as implemented before)
                if layer_name == "Land Use Land Cover (LULC)":
                    color_dict = LULC_IO_COLORS
                else:
                    color_dict = {
                        k: {"color": ImageColor.getrgb(v["color"]), "label": v["label"]}
                        for k, v in land_cover_mapping.items()
                    }

                class_counts = {}
                for idx, info in color_dict.items():
                    color_rgb = info["color"]
                    label = info["label"]
                    count = (np.all(all_pixels == color_rgb, axis=1)).sum()
                    class_counts[label] = count

                total_pixels = sum(class_counts.values())
                class_percentages = {
                    label: (count / total_pixels) * 100 if total_pixels > 0 else 0
                    for label, count in class_counts.items()
                }

                fig, ax = plt.subplots(figsize=(6, 4))
                labels = list(class_percentages.keys())
                percentages = list(class_percentages.values())
                colors = [
                    "#%02x%02x%02x" % color_dict[idx]["color"]
                    for idx in color_dict
                    if color_dict[idx]["label"] in labels
                ]

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
                # RGB histograms for other layers
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


def generate_model_evaluation(st_map, cdl_layer_url_template, ml_layer_url_template):
    from io import BytesIO

    import matplotlib.pyplot as plt
    import numpy as np
    import requests
    from PIL import Image, ImageColor

    if st_map and "center" in st_map and "zoom" in st_map:
        center_lat = st_map["center"]["lat"]
        center_lng = st_map["center"]["lng"]
        current_zoom = st_map["zoom"]
        tile = mercantile.tile(center_lng, center_lat, current_zoom)
        x, y, z = tile.x, tile.y, tile.z

        # Get CDL and ML tile images
        cdl_tile_url = cdl_layer_url_template.format(z=z, x=x, y=y)
        ml_tile_url = ml_layer_url_template.format(z=z, x=x, y=y)

        cdl_response = requests.get(cdl_tile_url)
        ml_response = requests.get(ml_tile_url)

        if cdl_response.status_code == 200 and ml_response.status_code == 200:
            cdl_img = Image.open(BytesIO(cdl_response.content)).convert("RGB")
            ml_img = Image.open(BytesIO(ml_response.content)).convert("RGB")

            # Resize the ML image to match the CDL image dimensions using nearest-neighbor interpolation
            ml_img_resized = ml_img.resize(cdl_img.size, Image.NEAREST)

            # Convert images to numpy arrays
            cdl_pixels = np.array(cdl_img).reshape(-1, 3)
            ml_pixels = np.array(ml_img_resized).reshape(-1, 3)

            # Define color classes and calculate IoU
            # Assuming land_cover_mapping is defined elsewhere
            color_dict = {
                k: {"color": ImageColor.getrgb(v["color"]), "label": v["label"]}
                for k, v in land_cover_mapping.items()
            }

            fig, axes = plt.subplots(3, 3, figsize=(18, 18))
            for idx, (class_id, info) in enumerate(color_dict.items()):
                if class_id == 0:
                    continue  # Skip background class

                color_rgb = info["color"]
                label = info["label"]

                # Calculate pixel counts for CDL, ML, and intersection
                cdl_mask = np.all(cdl_pixels == color_rgb, axis=1)
                ml_mask = np.all(ml_pixels == color_rgb, axis=1)

                cdl_count = np.sum(cdl_mask)
                ml_count = np.sum(ml_mask)
                intersection_count = np.sum(cdl_mask & ml_mask)

                # Set positions for the squares
                row, col = divmod(idx - 1, 3)
                ax = axes[row, col]

                # Ensure the axes facecolor is black
                ax.set_facecolor("black")

                # Calculate IoU
                union_count = cdl_count + ml_count - intersection_count
                iou = 100 * intersection_count / union_count if union_count > 0 else 0

                # Class label centered at the bottom
                ax.text(
                    0.5,
                    -0.05,
                    label,
                    ha="center",
                    va="top",
                    fontsize=30,
                    color="white",
                    transform=ax.transAxes,
                )

                # Plot IoU value in the center of the tile with larger font size
                ax.text(
                    0.5,
                    0.5,
                    f"IoU: {iou:.2f}%",
                    ha="center",
                    va="center",
                    fontsize=40,
                    color="white",
                    weight="bold",
                    transform=ax.transAxes,
                )

                # If either CDL or ML has zero pixels, no squares are drawn
                if cdl_count == 0 or ml_count == 0:
                    ax.axis("off")
                    continue

                # Calculate square sizes using absolute scale (10 times the number of pixels)
                scale_factor = 10
                side_length_cdl = np.sqrt(cdl_count * scale_factor)
                side_length_ml = np.sqrt(ml_count * scale_factor)

                # Calculate overlap area proportionally to the IoU
                overlap_area = intersection_count * scale_factor
                side_length_overlap = np.sqrt(overlap_area)

                # Positions for CDL and ML squares
                cdl_square = plt.Rectangle(
                    (0, 0),
                    side_length_cdl,
                    side_length_cdl,
                    edgecolor=np.array(color_rgb) / 255,
                    facecolor=np.array(color_rgb) / 255,
                    alpha=0.5,
                    linewidth=1,
                )
                ax.add_patch(cdl_square)

                ml_square_pos_x = side_length_cdl - side_length_overlap
                ml_square_pos_y = side_length_cdl - side_length_overlap

                ml_square = plt.Rectangle(
                    (ml_square_pos_x, ml_square_pos_y),
                    side_length_ml,
                    side_length_ml,
                    edgecolor=np.array(color_rgb) / 255,
                    facecolor=np.array(color_rgb) / 255,
                    alpha=0.5,
                    linewidth=1,
                )
                ax.add_patch(ml_square)

                # Add CDL label at bottom-left of the CDL square
                ax.text(0, 0, "CDL", ha="left", va="bottom", fontsize=20, color="white")

                # Add ML label at top-right of the ML square
                ax.text(
                    ml_square_pos_x + side_length_ml,
                    ml_square_pos_y + side_length_ml,
                    "ML",
                    ha="right",
                    va="top",
                    fontsize=20,
                    color="white",
                )

                # Adjust axis limits
                max_x = max(side_length_cdl, ml_square_pos_x + side_length_ml)
                max_y = max(side_length_cdl, ml_square_pos_y + side_length_ml)
                ax.set_xlim(-0.5, max_x + 1)
                ax.set_ylim(-0.5, max_y + 1)
                ax.set_aspect("equal")
                ax.axis("off")

            fig.suptitle(
                "Model Evaluation - Intersection over Union (IoU)",
                color="white",
                fontsize=26,
            )
            fig.patch.set_facecolor("black")
            plt.tight_layout()
            return fig
        else:
            print("No pixel data available for evaluation.")
            return None
    else:
        print("Map bounds not available.")
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
    page_title="GeoSynth", layout="wide", initial_sidebar_state="expanded"
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

if "model_evaluation" not in st.session_state:
    st.session_state.model_evaluation = None

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

st.title("GeoSynth (a Fused app)")

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
            # No need for st.experimental_rerun(), Streamlit will rerun automatically

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
    # Initialize map with center if it's the very first load
    if not st.session_state.initial_map_loaded:
        m = folium.Map(
            location=st.session_state.map_center,
            zoom_start=st.session_state.map_zoom,
            max_zoom=16,
            min_zoom=10,
        )
        st.session_state.initial_map_loaded = True
    else:
        # Use the current map center and zoom state for subsequent interactions
        m = folium.Map(
            location=st.session_state.map_center,
            zoom_start=st.session_state.map_zoom,
            max_zoom=16,
            min_zoom=10,
        )

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
        # Colormap Selection (Left)
        st.selectbox(
            "Colormap (Left)",
            options=colormap_options,
            index=colormap_options.index(st.session_state.colormap_left),
            key="colormap_left",  # Streamlit manages this session state key
        )

        # Reverse Colormap Checkbox (Left)
        st.checkbox(
            "Reverse Colormap (Left)",
            value=st.session_state.reverse_colormap_left,
            key="reverse_colormap_left",  # Streamlit manages this session state key
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
            st.slider(
                "Gradient Scale (Left)",
                0.1,
                2.0,
                value=st.session_state.grad_scale_left,
                step=0.1,
                key="grad_scale_left",  # Streamlit manages this session state key
            )
        with col2:
            st.slider(
                "Elevation Scale (Left)",
                50.0,
                5000.0,
                value=st.session_state.dem_scale_left,
                step=50.0,
                key="dem_scale_left",  # Streamlit manages this session state key
            )

        # Output type selection (Left)
        st.selectbox(
            "Output Type (Left)",
            ["elevation", "grad_angle", "grad_mag", "grad_x", "grad_y"],
            index=["elevation", "grad_angle", "grad_mag", "grad_x", "grad_y"].index(
                st.session_state.output_type_left
            ),
            key="output_type_left",  # Streamlit manages this session state key
        )

    # S2 controls if S2 is selected
    elif st.session_state.left_layer_select == "Sentinel-2 (S2)":
        col1, col2 = st.columns(2)
        with col1:
            st.slider(
                "Time Slice Agg (Left)",
                min_value=1,
                max_value=5,
                value=st.session_state.time_slice_count,
                step=1,
                key="time_slice_count",  # Streamlit manages this session state key
            )
        with col2:
            st.slider(
                "Radiance Threshold (Left)",
                min_value=0.3,
                max_value=1.3,
                value=st.session_state.threshold,
                step=0.05,
                key="threshold",  # Streamlit manages this session state key
            )

    # Brightness/Gamma controls for Sentinel layers
    if st.session_state.left_layer_select in ["Sentinel-2 (S2)", "Sentinel-1 (S1)"]:
        col1, col2 = st.columns(2)
        with col1:
            st.slider(
                "Brightness (Left)",
                min_value=0.0,
                max_value=2.0,
                value=st.session_state.brightness_left,
                step=0.1,
                key="brightness_left",  # Streamlit manages this session state key
            )
        with col2:
            st.slider(
                "Gamma (Left)",
                min_value=0.0,
                max_value=2.0,
                value=st.session_state.gamma_left,
                step=0.05,
                key="gamma_left",  # Streamlit manages this session state key
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
        # Colormap Selection (Right)
        st.selectbox(
            "Colormap (Right)",
            options=colormap_options,
            index=colormap_options.index(st.session_state.colormap_right),
            key="colormap_right",  # Streamlit manages this session state key
        )

        # Reverse Colormap Checkbox (Right)
        st.checkbox(
            "Reverse Colormap (Right)",
            value=st.session_state.reverse_colormap_right,
            key="reverse_colormap_right",  # Streamlit manages this session state key
        )

        # Update colormap name based on reverse_colormap_right
        colormap_name_right = st.session_state.colormap_right
        if st.session_state.reverse_colormap_right:
            colormap_name_right += "_r"

        # Display colormap image
        st.image(
            colormap_images[colormap_name_right],
            caption=f"{colormap_name_right.capitalize()} Colormap",
            use_column_width=True,
        )

        col1, col2 = st.columns(2)
        with col1:
            st.slider(
                "Gradient Scale (Right)",
                0.1,
                2.0,
                value=st.session_state.grad_scale_right,
                step=0.1,
                key="grad_scale_right",  # Streamlit manages this session state key
            )
        with col2:
            st.slider(
                "Elevation Scale (Right)",
                50.0,
                5000.0,
                value=st.session_state.dem_scale_right,
                step=50.0,
                key="dem_scale_right",  # Streamlit manages this session state key
            )

        # Output type selection (Right)
        st.selectbox(
            "Output Type (Right)",
            ["elevation", "grad_angle", "grad_mag", "grad_x", "grad_y"],
            index=["elevation", "grad_angle", "grad_mag", "grad_x", "grad_y"].index(
                st.session_state.output_type_right
            ),
            key="output_type_right",  # Streamlit manages this session state key
        )

    elif st.session_state.right_layer_select == "Sentinel-2 (S2)":
        col1, col2 = st.columns(2)
        with col1:
            st.slider(
                "Time Slice Agg (Right)",
                min_value=1,
                max_value=5,
                value=st.session_state.time_slice_count,
                step=1,
                key="time_slice_count",  # Streamlit manages this session state key
            )
        with col2:
            st.slider(
                "Radiance Threshold (Right)",
                min_value=0.3,
                max_value=1.3,
                value=st.session_state.threshold,
                step=0.05,
                key="threshold",  # Streamlit manages this session state key
            )

    if st.session_state.right_layer_select in ["Sentinel-2 (S2)", "Sentinel-1 (S1)"]:
        col1, col2 = st.columns(2)
        with col1:
            st.slider(
                "Brightness (Right)",
                min_value=0.0,
                max_value=2.0,
                value=st.session_state.brightness_right,
                step=0.1,
                key="brightness_right",  # Streamlit manages this session state key
            )
        with col2:
            st.slider(
                "Gamma (Right)",
                min_value=0.0,
                max_value=2.0,
                value=st.session_state.gamma_right,
                step=0.05,
                key="gamma_right",  # Streamlit manages this session state key
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

col_map, col_analytics = st.columns([4, 1])

with col_map:
    st_map = st_folium(m, height=700, key="map", use_container_width=True)

    # Capture the map's center and zoom, but only if the user hasn't moved it yet
    if st_map and "center" in st_map and "zoom" in st_map:
        if not st.session_state.user_moved_map:
            st.session_state.map_center = [
                st_map["center"]["lat"],
                st_map["center"]["lng"],
            ]
            st.session_state.map_zoom = st_map["zoom"]
            st.session_state.user_moved_map = (
                True  # Prevent further resets on pan or zoom
            )

        # Ensure searched locations reset the map to new coordinates
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
                st.session_state.all_tiles["R"] = pR
                st.session_state.all_tiles["G"] = pG
                st.session_state.all_tiles["B"] = pB
                st.session_state.all_tiles["A"] = alpha_var
                st.session_state.all_tiles["Target"] = right_layer_display_name
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                short_place_name = (
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

    # Add Model Evaluation Panel
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h4>Model Evaluation</h4>", unsafe_allow_html=True)
    if st.button("Evaluate Model"):
        with st.spinner("Generating model evaluation..."):
            st.session_state.model_evaluation = generate_model_evaluation(
                st_map, left_layer_url_template, right_layer_url_template
            )
    if "model_evaluation" in st.session_state and st.session_state.model_evaluation:
        st.pyplot(st.session_state.model_evaluation)

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
        # Instead of rerunning, rely on Streamlit's natural rerun on state change
        if new_drawn:
            # Optionally, display a message or update specific components if needed
            st.experimental_set_query_params()  # This can help trigger a rerun if necessary

if tilefy_button:
    if st.session_state.drawn_polygons:
        with st.spinner("Processing tiles..."):
            # Explicitly use st.session_state.zoom_level
            new_tiles = get_tiles_from_polygons(
                st.session_state.drawn_polygons, zoom=st.session_state.zoom_level
            )
            st.session_state.all_tiles = new_tiles.drop_duplicates(
                subset=["x", "y", "z"]
            )
            st.success(
                f"Tiles have been processed at zoom level {st.session_state.zoom_level}! You can now export them."
            )
    else:
        st.info(
            "No polygons drawn. Please draw polygons on the map before pressing 'Tilefy!'."
        )

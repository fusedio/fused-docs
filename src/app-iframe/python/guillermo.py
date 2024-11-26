import micropip

await micropip.install(["streamlit-folium", "fused", "plotly"])
import json

import folium
import fused
import plotly.graph_objects as go
import streamlit as st
from shapely.geometry import box
from streamlit_folium import st_folium

# Set page config for wider layout and dark theme
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# Custom CSS to deal with plotly plot
st.markdown(
    """
  <style>
  .main > div { padding: 2rem; }
  .stPlotlyChart {
      padding: 1rem;
      background: rgba(0,0,0,0);
      border-radius: 0.5rem;
  }
  .st-emotion-cache-1y4p8pa {
      padding: 1rem;
      background-color: #0E1117;
  }
  .st-emotion-cache-16idsys p { color: #FAFAFA; }
  .leaflet-grab { cursor: default !important; }
  .leaflet-grabbing { cursor: default !important; }
  .leaflet-interactive { cursor: default !important; }
  .leaflet-container, .leaflet-grab, .leaflet-grabbing, .leaflet-interactive, .leaflet-pane * {
      cursor: default !important;
  }
  </style>
  """,
    unsafe_allow_html=True,
)

# Initialize session state to deal with user switching from site and years.
if "current_site" not in st.session_state:
    st.session_state.current_site = None
if "current_year" not in st.session_state:
    st.session_state.current_year = None
if "last_clicked" not in st.session_state:
    st.session_state.last_clicked = None
if "current_data" not in st.session_state:
    st.session_state.current_data = None

# Get sites and years data
sites_years = fused.run(
    "fsh_5K7SGo1rXr1TKZVtdvtvBb", None
)  # Call UDF to populate Site and Year lists dropdown menus
sites = sorted(sites_years[sites_years["metadata_type"] == "sites"]["value"].tolist())

# Get initial site (ABBY) data for initial location since the sites are listed in alphabetical order
initial_site_data = fused.run(
    "fsh_2jwrJEz0G7mPu0emafaQ6t", lat=0, lng=0, site="ABBY", year=2021
)

# Zoom-in to the initial location
initial_geojson = initial_site_data["site_geo"].iloc[0]
if isinstance(initial_geojson, str):
    initial_geojson = json.loads(initial_geojson)

bounds = folium.GeoJson(initial_geojson).get_bounds()
initial_location = [
    (bounds[0][0] + bounds[1][0]) / 2,
    (bounds[0][1] + bounds[1][1]) / 2,
]

st.title("🌍 NEON Hyperspectral Signature Explorer")
st.markdown("<br>", unsafe_allow_html=True)

spacer1, col1, spacer2, col2, spacer3, col3, spacer4 = st.columns(
    [0.1, 1.2, 0.2, 4, 0.2, 2.2, 0.1]
)

# Site and Year Selection
with col1:
    st.markdown("### Site Selection")
    selected_site = st.selectbox(
        "Select NEON Site", sites, label_visibility="collapsed"
    )

    if selected_site != st.session_state.current_site:
        st.session_state.current_site = selected_site
        # Get years for selected site
        site_metadata = fused.run("fsh_5K7SGo1rXr1TKZVtdvtvBb", site=selected_site)
        available_years = sorted(
            [
                int(year)
                for year in site_metadata[site_metadata["metadata_type"] == "years"][
                    "value"
                ].tolist()
            ]
        )
        st.session_state.available_years = available_years

        # Get site data and update map
        site_data = fused.run(
            "fsh_2jwrJEz0G7mPu0emafaQ6t",
            lat=initial_location[0],
            lng=initial_location[1],
            site=selected_site,
            year=available_years[0],
        )
        st.session_state.site_geojson = site_data["site_geo"].iloc[0]
        if isinstance(st.session_state.site_geojson, str):
            st.session_state.site_geojson = json.loads(st.session_state.site_geojson)
        st.session_state.last_clicked = None
        st.session_state.current_data = None
        st.rerun()

    st.markdown("### Year Selection")
    if "available_years" in st.session_state:
        selected_year = st.selectbox(
            "Select Year",
            st.session_state.available_years,
            label_visibility="collapsed",
        )
        if selected_year != st.session_state.current_year:
            st.session_state.current_year = selected_year
            st.rerun()

# Map Creation
m = folium.Map(
    location=initial_location,
    zoom_start=12,
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attr="Esri",
)

# Add site boundary if available
if hasattr(st.session_state, "site_geojson"):
    site_layer = folium.GeoJson(
        st.session_state.site_geojson,
        style_function=lambda x: {
            "fillColor": "#00B3FF",
            "color": "#00B3FF",
            "weight": 2,
            "fillOpacity": 0.2,
        },
    ).add_to(m)
    m.fit_bounds(folium.GeoJson(st.session_state.site_geojson).get_bounds())

# Add marker if there's a last clicked location
if "last_clicked" in st.session_state and st.session_state.last_clicked:
    lat = st.session_state.last_clicked["lat"]
    lng = st.session_state.last_clicked["lng"]
    folium.Marker(
        [lat, lng],
        popup=f"Lat: {lat:.4f}, Lng: {lng:.4f}",
        tooltip="Sampling location",
        icon=folium.Icon(color="red", icon="crosshairs", prefix="fa"),
    ).add_to(m)

# Display map
with col2:
    st.markdown("### Interactive Map")
    st.markdown(
        """
       <div style="
           background-color: rgba(0,179,255,0.1);
           border-left: 4px solid #00B3FF;
           padding: 0.5rem 1rem;
           margin-bottom: 1rem;
           border-radius: 0.2rem;
       ">
           🎯 Click within the highlighted area to view the spectral signature at your selected point
       </div>
   """,
        unsafe_allow_html=True,
    )
    map_data = st_folium(m, width=None, height=500)

# Handle click events
if map_data and map_data.get("last_clicked"):
    new_click = map_data["last_clicked"]

    # Only update if it's a new click or first click
    if (
        "last_clicked" not in st.session_state
        or new_click != st.session_state.last_clicked
    ):
        st.session_state.last_clicked = new_click
        lat = new_click["lat"]
        lng = new_click["lng"]

        if st.session_state.current_site and st.session_state.current_year:
            # Get hyperspectral data
            att = fused.run(
                "fsh_2jwrJEz0G7mPu0emafaQ6t",
                lat=lat,
                lng=lng,
                site=st.session_state.current_site,
                year=st.session_state.current_year,
            )

            # Store the data in session state for reuse
            st.session_state.current_data = att
            st.rerun()

# Display plot only if we get data
if (
    hasattr(st.session_state, "current_data")
    and st.session_state.current_data is not None
):
    att = st.session_state.current_data
    with col3:
        st.markdown("### Hyperspectral Signature")
        if st.session_state.last_clicked:
            st.markdown(
                f"<p style='color: #666666;'>Location: {st.session_state.last_clicked['lat']:.4f}, {st.session_state.last_clicked['lng']:.4f}</p>",
                unsafe_allow_html=True,
            )

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=att["wavelength"],
                y=att["reflectance"],
                mode="lines",
                name="Reflectance",
                line=dict(color="#00B3FF", width=2),
                fill="tozeroy",
                fillcolor="rgba(0,179,255,0.1)",
            )
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=400,
            margin=dict(l=20, r=20, t=30, b=20),
            xaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor="#333333",
                title="Band",
                title_font=dict(size=14, color="white"),
                tickfont=dict(color="white"),
            ),
            yaxis=dict(
                showgrid=True,
                gridwidth=1,
                gridcolor="#333333",
                title="Reflectance",
                title_font=dict(size=14, color="white"),
                tickfont=dict(color="white"),
            ),
            font=dict(size=12, color="white"),
            showlegend=False,
            hovermode="x unified",
        )

        fig.update_traces(
            hovertemplate="<b>Band</b>: %{x}<br><b>Reflectance</b>: %{y:.2f}<extra></extra>"
        )

        st.plotly_chart(fig, use_container_width=True)

        # Statistics
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Summary Statistics")
        stats_col1, stats_col2 = st.columns(2)

        def custom_metric(label, value):
            st.markdown(
                f"""
               <div style="
                   background-color: #1E1E1E;
                   padding: 1rem;
                   border-radius: 0.5rem;
                   margin: 0.5rem 0;
               ">
                   <p style="color: #666666; margin: 0; font-size: 0.8rem;">{label}</p>
                   <p style="color: #00B3FF; margin: 0; font-size: 1.5rem; font-weight: bold;">{value:.2f}</p>
               </div>
               """,
                unsafe_allow_html=True,
            )

        with stats_col1:
            custom_metric("Mean Reflectance", att["reflectance"].mean())
            custom_metric("Max Reflectance", att["reflectance"].max())
        with stats_col2:
            custom_metric("Min Reflectance", att["reflectance"].min())

st.markdown("<br><br>", unsafe_allow_html=True)

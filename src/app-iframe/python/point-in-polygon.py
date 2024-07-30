import fused_app
import pydeck as pdk
import streamlit as st

st.header("Point in Polygon: Overture + NSI")

st.write("""
Point-in-polygon analysis using Overture building polygons and NSI point data is a powerful technique for geospatial risk assessment and urban planning. By combining the detailed building footprints from Overture Maps with the comprehensive hazard and value information from the National Structure Inventory, we can create rich, informative risk maps and indices.
""")
lng, lat =  -73.9874, 40.7431



# Create map

view_tile = st.sidebar.checkbox("View data for tiled map?")
st.sidebar.divider()

if view_tile:
    tile_url = "{z}/{x}/{y}"
else:
    x,y,z = 9649, 12316,15
    tile_url = f"{z}/{x}/{y}"

target_metric = st.sidebar.selectbox(
    "Select metric:",
    ['med_yr_blt', 'val_struct', 'val_cont', 'val_vehic'],
)

st.write("You selected:", target_metric)

url_nsi = f'https://www.fused.io/server/v1/realtime-shared/c8679490a7c130178e2781a45f4090208c9bcd8d8d7572532c4c39c4d0914467/run/tiles/{tile_url}?dtype_out_vector=geojson&return_object=gdf_nsi&target_metric={target_metric}'
url_overture = f'https://www.fused.io/server/v1/realtime-shared/c8679490a7c130178e2781a45f4090208c9bcd8d8d7572532c4c39c4d0914467/run/tiles/{tile_url}?dtype_out_vector=geojson&return_object=gdf_overture&target_metric={target_metric}'
url_out = f'https://www.fused.io/server/v1/realtime-shared/c8679490a7c130178e2781a45f4090208c9bcd8d8d7572532c4c39c4d0914467/run/tiles/{tile_url}?dtype_out_vector=geojson&return_object=end_result&target_metric={target_metric}'





layers=[]

if st.sidebar.checkbox("Show end result"):
    layers.append(pdk.Layer(
        "TileLayer",
        data=url_out,
        get_line_color=[255, 255, 2, 1000],
        stroked=True,
        get_line_width=10,
        pickable=True,
        extruded=True,
        get_elevation='properties.stats / 20',
        get_fill_color="[properties.stats/100000, properties.stats/100000, properties.stats]",
    ))
if st.sidebar.checkbox("Show building"):
    layers.append(pdk.Layer(
        "TileLayer",
        data=url_overture,
        get_line_color=[255, 25, 2, 100],
        stroked=True,
        get_line_width=2,
        pickable=True,

        filled=False,
    ))
if st.sidebar.checkbox("Show NSI"):
    layers.append(pdk.Layer(
        "TileLayer",
        data=url_nsi,
        get_line_color=[255, 255, 2, 1000],
        stroked=True,
        get_line_width=4,
        pickable=True,
        extruded=True,
        # get_elevation='properties.val_struct / 200000',
        # get_fill_color="[properties.val_struct/100000, properties.val_struct/100000, properties.val_struct]",
    ))




st.pydeck_chart(
    pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v9",
        initial_view_state=pdk.ViewState(
            latitude=lat,
            longitude=lng,
            zoom=14,
            pitch=25,
        ),
        tooltip = {
             "html": "<b>Structure Value:</b> ${val_struct}",
                   "style": {
                        "backgroundColor": "steelblue",
                        "color": "white"
                   }
        },
        layers=layers
    )
)

# st_damcat
# med_yr_blt
# geometry
# val_vehic
# occtype
# val_struct
# stats 


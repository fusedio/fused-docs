import pydeck as pdk
import streamlit as st

st.title("Zonal Stats by global municipalities")

url = "https://www.fused.io/server/v1/realtime-shared/488204c72ca1052c99d249556401c89cb35b066716e1fc0084d3d28f064ea435/run/tiles/{z}/{x}/{y}?dtype_out_vector=geojson"

import streamlit as st

option = st.selectbox("Aggregation", ("Average", "Max", "Min"))

st.write("You selected:", option)

lat, lng = 28.3949, 84.1240

st.pydeck_chart(
    pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v9",
        initial_view_state=pdk.ViewState(
            latitude=lat, longitude=lng, zoom=5, pitch=0, bearing=-6
        ),
        tooltip={
            "html": "<b>Value:</b> {stats_mean}",
            "style": {"backgroundColor": "steelblue", "color": "white"},
        },
        layers=[
            pdk.Layer(
                "TileLayer",
                data=url,
                get_line_color=[255, 25, 2, 1000],
                get_elevation="properties.stats_mean",
                stroked=True,
                get_line_width=2,
                pickable=True,
                extruded=True,
                filled=True,
                get_fill_color="[properties.stats_mean*25, properties.stats_mean*256, properties.stats_mean*25]",
            )
        ],
    )
)

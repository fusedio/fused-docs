import pydeck as pdk
import streamlit as st

st.title("🏢 NSI + Overture")
url = "https://www.fused.io/server/v1/realtime-shared/fsh_3q5XyVfgw4z7X4XzdugudF/run/tiles/{z}/{x}/{y}?dtype_out_vector=geojson"
st.pydeck_chart(
    pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v9",
        initial_view_state=pdk.ViewState(
            latitude=46.6077, longitude=-112.0223, zoom=14, pitch=25
        ),
        layers=[
            pdk.Layer(
                "TileLayer",
                data=url,
                get_line_color=[255, 25, 2, 100],
                stroked=True,
                get_line_width=2,
                pickable=True,
                filled=True,
                extruded=True,
                elevation_scale=0.1,
                elevation="properties.height",
                get_fill_color=["properties.height *20", "255/properties.height", 140],
            )
        ],
        tooltip={
            "html": "<b>Height:</b> {height} <br/> ",
            "style": {"backgroundColor": "steelblue", "color": "white"},
        },
    )
)

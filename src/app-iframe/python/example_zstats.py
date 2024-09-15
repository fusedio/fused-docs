import pydeck as pdk
import streamlit as st

url_overture = "https://www.fused.io/server/v1/realtime-shared/fsh_6eYdGuG95JPEmUPaHu2CQX/run/tiles/{z}/{x}/{y}?dtype_out_vector=geojson"
st.pydeck_chart(
    pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v9",
        initial_view_state=pdk.ViewState(latitude=42.2027, longitude=-121.6551, zoom=6),
        layers=[
            pdk.Layer(
                "TileLayer",
                data=url_overture,
                get_line_color=[255, 25, 2, 100],
                stroked=True,
                get_line_width=2,
                pickable=True,
                filled=True,
                get_fill_color=["properties.stats / 10", 10, 140],
            )
        ],
        tooltip={
            "html": "<b>Average elevation:</b> {stats} <br/> meters. ",
            "style": {"backgroundColor": "steelblue", "color": "white"},
        },
    ),
)

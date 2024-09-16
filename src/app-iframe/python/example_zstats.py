import pydeck as pdk
import streamlit as st

st.title("🌽 CDL Zonal Stats")
year = st.selectbox("Year", [2020, 2021, 2022])

url = (
    "https://www.fused.io/server/v1/realtime-shared/fsh_46eSFZaR3q3SnoVB28pN0g/run/tiles/{z}/{x}/{y}?dtype_out_vector=geojson"
    + f"&year={year}"
)
st.pydeck_chart(
    pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v9",
        initial_view_state=pdk.ViewState(latitude=40.3612, longitude=-111.5386, zoom=6),
        layers=[
            pdk.Layer(
                "TileLayer",
                data=url,
                get_line_color=[255, 255, 255, 100],
                stroked=True,
                line_width_min_pixels=1,
                pickable=True,
                filled=True,
                get_fill_color=[
                    "properties.stats * 200",
                    "properties.stats * 100",
                    10,
                    100,
                ],
            )
        ],
        tooltip={
            "html": "<b>Stats:</b> {stats} <br/> ",
            "style": {"backgroundColor": "steelblue", "color": "white"},
        },
    )
)

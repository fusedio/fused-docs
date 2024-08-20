import pydeck as pdk
import streamlit as st

st.title("Real Estate Site Selector")

METRICS = {
    "Sructure value": "val_struct",
    "Content value": "val_cont",
    "Vehicle value": "val_vehic",
}

metric = st.selectbox("Aggregate by:", METRICS.keys())
url_nsi = (
    "https://www.fused.io/server/v1/realtime-shared/fsh_38dVZMy7vNoXVu5iiYir3h/run/tiles/{z}/{x}/{y}?dtype_out_vector=geojson"
    + f"&target_metric={METRICS[metric]}"
)
lat, lng = 40.7812, -73.9747

st.pydeck_chart(
    pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v9",
        initial_view_state=pdk.ViewState(
            latitude=lat, longitude=lng, zoom=15, pitch=50, bearing=-6
        ),
        tooltip={
            "html": "<b>Value:</b> ${" + METRICS[metric] + "}",
            "style": {"backgroundColor": "steelblue", "color": "white"},
        },
        layers=[
            pdk.Layer(
                "TileLayer",
                data=url_nsi,
                get_line_color=[255, 25, 2, 100],
                get_elevation="properties.stats / 20",
                stroked=True,
                get_line_width=2,
                pickable=True,
                extruded=True,
                filled=True,
                get_fill_color="[properties.stats*2, properties.stats*3, properties.stats*3]",
            )
        ],
    )
)

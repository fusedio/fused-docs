import fused
import pydeck as pdk
import streamlit as st

st.title("U.S. Census Viewer")

token = st.text_input("Input your UDF Token", "fsh_28jQAxvQuK5n8msWf2ZNlt")
df = fused.run(token)
st.write(df.head())

st.pydeck_chart(
    pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v9",
        initial_view_state=pdk.ViewState(
            latitude=35.1743, longitude=-120.3190, zoom=6, pitch=0
        ),
        layers=[
            pdk.Layer(
                "GeoJsonLayer",
                data=df,
                opacity=0.2,
                get_fill_color="[10,10, AWATER/10000]",
                stroked=True,
                get_line_width=2,
                pickable=True,
                filled=True,
            )
        ],
    )
)

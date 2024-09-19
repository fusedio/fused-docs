import pydeck as pdk
import streamlit as st

st.title("🏢 NSI + Overture")
st.write(
    """
The UDF then performs spatial join between Overture Buildings and NSI using GeoPandas with `gdf_overture.sjoin(gdf)`. This operation returns a unified table with Overture building footprints with GERS IDs enriched with NSI attributes.

Coverage expands in (top right) Astoria when you add heights from the NSI dataset to Overture buildings.
"""
)
url = "https://www.fused.io/server/v1/realtime-shared/fsh_3q5XyVfgw4z7X4XzdugudF/run/tiles/{z}/{x}/{y}?dtype_out_vector=geojson"
st.pydeck_chart(
    pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v9",
        initial_view_state=pdk.ViewState(
            latitude=46.1869, longitude=-123.8476, zoom=13, pitch=40
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
                get_fill_color=["properties.height *10", "properties.height*30", 200],
            )
        ],
        tooltip={
            "html": "<b>Height:</b> {height} <br/> ",
            "style": {"backgroundColor": "steelblue", "color": "white"},
        },
    )
)

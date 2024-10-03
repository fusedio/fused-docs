import fused
import pydeck as pdk
import streamlit as st

st.title("U.S. Census Viewer")

token = st.text_input("Input your UDF Token", "fsh_28jQAxvQuK5n8msWf2ZNlt")
df = fused.run(token)
st.dataframe(df.head())

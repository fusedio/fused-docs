# This is a sample app that shows a chart
import numpy as np
import pandas as pd
import streamlit as st


@st.cache_data
def load_data(n):
    df = pd.DataFrame(
        {
            "col1": list(range(20)) * 3 * n,
            "col2": np.random.randn(60 * n),
            "col3": ["A"] * 20 * n + ["B"] * 20 * n + ["C"] * 20 * n,
        }
    )
    return df


number = int(st.number_input("Insert a number", min_value=1, step=1))
st.write("The current number is ", number)
chart_data = load_data(number)

st.bar_chart(chart_data, x="col1", y="col2", color="col3")

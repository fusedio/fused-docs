import numpy as np
import pandas as pd
import streamlit as st

points = st.slider("Number of points", 1, 100, 25)
chart_data = pd.DataFrame(np.random.randn(points, 3), columns=["a", "b", "c"])

st.line_chart(chart_data)

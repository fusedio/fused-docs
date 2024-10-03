import asyncio
import json
import random

import altair as alt
import folium
import fused
import pandas as pd
import streamlit as st
from folium.plugins import Draw
from requests.exceptions import HTTPError
from streamlit_folium import st_folium

# del st.session_state['last_clicked']
# del st.session_state['markers']

st.markdown("# DayMet Time Series Demo")
st.write("""Click anywhere in North America to add a location.""")


cities = [
    ("San Francisco", 37.7749, -122.4194),
    ("Los Angeles", 34.0522, -118.2437),
    ("New York City", 40.7128, -74.006),
]

colors = [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#7f7f7f",
    "#bcbd22",
    "#17becf",
    "#aec7e8",
    "#ffbb78",
    "#98df8a",
    "#ff9896",
    "#c5b0d5",
    "#c49c94",
    "#f7b6d2",
    "#c7c7c7",
    "#dbdb8d",
    "#9edae5",
]


def app_not_initialized():
    return "last_clicked" not in st.session_state


# Initialize session state
def initialize_state():
    st.session_state.last_clicked = None
    st.session_state.markers = cities


if app_not_initialized():
    initialize_state()


# Map
m = folium.Map(location=[40, -95], zoom_start=4)
fg = folium.FeatureGroup(name="State bounds")

for marker, color in zip(st.session_state.markers, colors):
    city, lat, lng = marker
    fg.add_child(
        folium.CircleMarker(
            location=[lat, lng],
            radius=6,
            popup=city,
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.5,
        )
    )

map_data = st_folium(
    m,
    feature_group_to_add=fg,
    width=700,
    height=500,
    key="map",
)


# Map interaction
if (
    map_data["last_clicked"]
    and map_data["last_clicked"] != st.session_state.last_clicked
):
    st.session_state.last_clicked = map_data["last_clicked"]
    lat, lon = (
        st.session_state.last_clicked["lat"],
        st.session_state.last_clicked["lng"],
    )
    l = len(st.session_state.markers) - len(cities)
    name = f"Location {l + 1}"

    st.session_state.markers.append([name, lat, lon])

    st.experimental_rerun()


token = "fsh_176uPeXyRSh0DQTckPcnYA"

year_start_end = st.sidebar.slider(
    "Select the year range", min_value=1980, max_value=2023, value=(2015, 2023), step=1
)


# Fetch data
loc_col = " "
old_col_names = [
    "location",
    "lat",
    "lng",
    "year",
    "yday",
    "tmax",
    "tmin",
    "prcp",
    "dayl",
    "srad",
    "swe",
    "vp",
]
new_col_names = [
    loc_col,
    "lat",
    "lng",
    "year",
    "yday",
    "Maximum temperature (°C)",
    "Minimum temperature (°C)",
    "Precipitation (mm/day)",
    "Daylength (seconds)",
    "Shortwave radiation (W/m²/day)",
    "Snow Water Equivalent (mm)",
    "Vapor pressure (Pa)",
]
options = new_col_names[5:]
option = st.selectbox("Select a parameter to visualize", options)

st.write(option)


@st.cache_resource
def func(token, json_str_list, start_year, end_year):
    results = []
    for json_str in json_str_list:
        out = asyncio.Task(
            fused.run(
                token,
                json_str=json_str,
                start_year=start_year,
                end_year=end_year,
                sync=False,
            )
        )
        results.append(out)
    return results


m = st.session_state.markers
dc = [{name: {"lat": lat, "lng": lng}} for name, lat, lng in m]
json_str_list = [json.dumps(d) for d in dc]

results = func(
    token, json_str_list, start_year=year_start_end[0], end_year=year_start_end[1]
)

l = []
for v in results:
    try:
        result = await v
        l.append(await v)
    except HTTPError:
        continue


# Process

df = pd.concat(l)
df = df[old_col_names]
df.columns = new_col_names

df["date"] = pd.to_datetime(
    df["year"].astype(str) + df["yday"].astype(str), format="%Y%j"
)
df.set_index("date")
chart_title = st.empty()
chart_plot = st.empty()
moving_window = st.slider(
    "Moving Average Window Size", min_value=1, max_value=730, value=365, step=5
)
df["value"] = a = df.groupby(loc_col)[option].transform(
    lambda x: x.rolling(window=moving_window).mean()
)


# Visualise
categories = df[loc_col].unique().tolist()

chart = (
    alt.Chart(df)
    .mark_line()
    .encode(
        x=alt.X("date:T", title=None),
        color=alt.Color(
            f"{loc_col}:N",
            scale=alt.Scale(domain=categories, range=colors),
            legend=alt.Legend(orient="bottom", offset=0, columns=5, symbolSize=100),
        ),
        y=alt.Y("value", title=option),
        tooltip=["date:T", f"{loc_col}:N", alt.Tooltip(option, format=".2f")],
    )
    .properties(
        width=700,
        height=400,
    )
    .interactive()
)

chart_plot.altair_chart(chart, use_container_width=True)

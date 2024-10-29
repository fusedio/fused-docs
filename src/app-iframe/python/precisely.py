#'https://altair-viz.github.io/gallery/index.html#maps'

# to do:
# get rid of lower cumulative plot
# figure out why the sim_norm on cumulative plot doesn't go up to 1.0


import streamlit as st

st.title("NYC Chronotypes")
st.divider()
import micropip

await micropip.install("vega_datasets")
import pandas as pd

df = pd.read_csv(
    "https://www.fused.io/server/v1/realtime-shared/fsh_4J5HBuUmbREtPSQQssYniq/run/file?dtype_out_raster=png&dtype_out_vector=csv&lat=40.7128&lng=-74.0061&threshold=0"
)
df2 = pd.read_csv(
    "https://www.fused.io/server/v1/realtime-shared/fsh_4J5HBuUmbREtPSQQssYniq/run/file?dtype_out_raster=png&dtype_out_vector=csv&lat=40.7229&lng=-73.9883&threshold=0"
)
# print(df.columns)


s = df.sort_values(
    ["sim_norm"], ascending=True
)  # .reset_index()#[24800:25000]#.head(100).reset_index()
# s=s[s['jsd']>0]
# print(s.columns)
# print(df.shape)
# print(df2.shape) # fewer hexes overall... not sure how...
# print(s.shape)

s["dummy"] = 1
s["cumulative_count"] = s.groupby(["dummy"]).cumcount(ascending=True)
s["location"] = "city hall"

s2 = df2.sort_values(
    ["sim_norm"], ascending=True
)  # .reset_index()#[24800:25000]#.head(100).reset_index()
s2["dummy"] = 1
s2["cumulative_count"] = s2.groupby(["dummy"]).cumcount(ascending=True)
s2["location"] = "LES"

lines = pd.concat([s2, s]).reset_index()

st.markdown("### Cumulative counts")
import altair as alt
from vega_datasets import data

source = lines  # data.sp500.url

brush = alt.selection_interval(encodings=["x"])

base = (
    alt.Chart(source, width=600, height=200)
    .mark_line()
    .encode(
        x="sim_norm:Q",
        y="cumulative_count:Q",
    )
)

upper = base.encode(
    alt.X("sim_norm:Q").scale(domain=brush),
    alt.Y("cumulative_count:Q").scale(domain=brush),
    alt.Color("location:N").scale(scheme="category20b"),
)

lower = base.properties(height=60).add_params(brush)

upper & lower
st.divider()


############
############

st.markdown("### Most and least similar hexes")
import altair as alt
import numpy as np
import pandas as pd

sim_a = df2
sim_b = df
h = pd.read_csv(
    "https://www.fused.io/server/v1/realtime-shared/fsh_1Ebn6rTi7jArwbeTuKQ688/run/file?dtype_out_raster=png&dtype_out_vector=csv&h3_res=10"
)


# print(h)

dec_ct = int(h.hex.nunique() / 10)

# print(dec_ct)

top_dec2 = sim_a.sort_values(["sim_norm"], ascending=False).head(dec_ct).hex
top_dp2 = h.merge(top_dec2, on="hex")
dist2L = top_dp2.groupby("daypart").metric.mean().reset_index()
bot_dec22 = sim_a.sort_values(["sim_norm"], ascending=True).head(dec_ct).hex
bot_dp2 = h.merge(bot_dec22, on="hex")
#
# print(top_dp2)
##print(h[h['hex']=='8a2a100e0787fff'])
# 8a2a100c4cf7fff

dist22 = bot_dp2.groupby("daypart").metric.mean().reset_index()
dist22["decile"] = "bottom"
dist2L["decile"] = "top"
c = pd.concat([dist22, dist2L])
src2 = c  # .pivot(index=['lev', 'daypart'], columns=[], values=['metric'])
# print()

top_dec = sim_b.sort_values(["sim_norm"], ascending=False).head(dec_ct).hex
top_dp = h.merge(top_dec, on="hex")
dist = top_dp.groupby("daypart").metric.mean().reset_index()
bot_dec = sim_b.sort_values(["sim_norm"], ascending=True).head(dec_ct).hex
bot_dp = h.merge(bot_dec, on="hex")
dist2 = bot_dp.groupby("daypart").metric.mean().reset_index()
dist2["decile"] = "bottom"
dist["decile"] = "top"
les = pd.concat([dist, dist2])
# print(top_dp)

selector = alt.selection_point(fields=["decile"], on="pointerover")

color_scale = alt.Scale(domain=["top", "bottom"], range=["#1FC3AA", "#8624F5"])

base = alt.Chart(src2).properties(width=500, height=250).add_params(selector)
color = alt.condition(selector, "decile:N", alt.value("lightgray"), scale=color_scale)
points = base.mark_point(filled=True, size=200).encode(
    alt.X("mean(daypart):Q").scale(domain=[0, 23]),
    alt.Y("mean(metric):Q").scale(domain=[0, 3000]),
    color=color,
)

hists = (
    base.mark_bar(opacity=0.5, thickness=100)
    .encode(
        alt.X("daypart")
        .bin(step=1)  # step keeps bin size the same
        .scale(domain=[0, 23]),
        alt.Y("metric").stack(None).scale(domain=[0, 3000]),
        alt.Color("decile:N").scale(color_scale),
        # color=color,
    )
    .encode(order=alt.condition(selector, alt.value(1), alt.value(0)))
)

base_L = alt.Chart(les).properties(width=500, height=250).add_params(selector)
color = alt.condition(selector, "decile:N", alt.value("lightgray"), scale=color_scale)
points = base.mark_point(filled=True, size=200).encode(
    alt.X("mean(daypart):Q").scale(domain=[0, 23]),
    alt.Y("mean(metric):Q").scale(domain=[0, 8500]),
    color=color,
)

hists_L = (
    base_L.mark_bar(opacity=0.5, thickness=100)
    .encode(
        alt.X("daypart")
        .bin(step=1)  # step keeps bin size the same
        .scale(domain=[0, 23]),
        alt.Y("metric").stack(None).scale(domain=[0, 8500]),
        alt.Color("decile:N").scale(color_scale),
        # color=color,
    )
    .encode(order=alt.condition(selector, alt.value(1), alt.value(0)))
)
# ).transform_filter(
#     selector
# )

# points | hists
hists
hists_L
st.divider()

##could add something about discriminability

import asyncio
import datetime
import io
from datetime import timedelta

import fused_app
import streamlit as st


# Run udf async
@st.cache_resource
def func(the_array):
    framesdict = {}
    for each in the_array:
        out = asyncio.Task(fused_app.run("fsh_6eYdGuG95JPEmUPaHu2CQX", sync=False))
        framesdict[each] = out
    return framesdict


func_output = func(range(2))
a = []
for k, v in func_output.items():
    out4 = await v
    for i in range(len(out4)):
        a.append(out4.iloc[i])

print(a)

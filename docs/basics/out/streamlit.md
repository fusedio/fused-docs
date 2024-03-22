---
search:
  boost: 10
---
# Streamlit integration

Streamlit is an open source Python app builder to turn data scripts into shareable web apps.



## Step 1: Install streamlit

Prepare an environment and install streamlit.

```bash
pip install streamlit
```

## Step 2: Create a UDF in Fused Hosted API

Create and save a UDF in workbench, then copy its Python snippet.

As an example, this minimalist UDF returns a dataframe with polygons for each administrative zone in Washington DC.

```python
@fused.udf
def udf(url='https://www2.census.gov/geo/tiger/TIGER_RD18/STATE/11_DISTRICT_OF_COLUMBIA/11/tl_rd22_11_bg.zip'):
    import geopandas as gpd
    return gpd.read_file(url)
```

## Step 3: Create your streamlit app

Create a new Python script for your Streamlit app - in this case in a file called `app.py`. This script will be the entry point of your application.

This script creates a minimalist Streamlit app that calls the UDF then displays its output dataframe.

```python
import fused
import streamlit as st


st.title("🌎 Dataframe generator")

df = fused.core.run_file("username@fused.io", "DuckDB_NYC_Example")
st.dataframe(df)
```

## Step 4. Run your streamlit app

Start the app using Streamlit's CLI command.

```bash
streamlit run app.py
```

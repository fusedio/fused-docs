# Leaflet

Fused can be used to display responsive Tile maps in Jupyter Notebooks with the `ipyleaflet` library.

![alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/gifs/leaflet.gif)


Follow these steps to embed a map into a Notion page.

## Step 1. Install `ipyleaflet`

Create an environment and install `ipyleaflet`.

```bash
pip install ipyleaflet
```

## Step 2. Create Tile UDF

The next step is to create a UDF in Workbench, and use generate a signed URL for its endpoint.

```python
from fused.api import FusedAPI
api = FusedAPI()

# Create a new UDF access token using its unique token string.
token_object = api.create_udf_access_token(udf_email="user@fused.io", udf_name="CDLs_Tile_Example")

# Generate a URL
url = token_object.get_tile_url()
url
```

## Step 3. Insert the embed

Create and render an ipyleaflet [TileLayer](https://ipyleaflet.readthedocs.io/en/latest/layers/tile_layer.html). You can parametrize the UDF URL to include placeholders for the tile coordinates (`{z}`, `{x}`, `{y}`), and a query parameter for the crop type. Adjust the tile_size and zoom_offset as needed for your data.


```python
import ipyleaflet

crop_type='almond'
m = ipyleaflet.Map(center=(37.316, -120.69), zoom=10, basemap=ipyleaflet.basemaps.CartoDB.PositronOnlyLabels)
l = ipyleaflet.TileLayer(
    url=f'https://app-staging.fused.io/server/v1/realtime-shared/fce1c75c21a228b7eb067aa387f573196034d9707d78c85c32c363fc88ef4d4e/run/tiles/{{z}}/{{x}}/{{y}}?crop_type={crop_type}',
    tile_size=512,
    zoom_offset=-1,
    cross_origin=True,
    show_loading=True,
)
m.add_layer(l)
m
```

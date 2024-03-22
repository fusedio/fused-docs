---
search:
  boost: 10
---

# Lonboard integration

[Lonboard](https://developmentseed.org/lonboard/latest/) is a Python library to create fast and interactive geospatial visualizations in Jupyter Notebooks.

This snippet shows how to create a Lonboard BitmapTileLayer that renders a UDF as a Tile. This ([example UDF](https://github.com/fusedio/udfs/tree/main/public/CDLs_Tile_Example)) renders Cropland Data Layer (CDL) tiff files, which is a categorical land cover dataset of crops and land cover on agricultural lands in the United States.

```python
import lonboard

crop_type = "almond"
url = f"https://app-staging.fused.io/server/v1/realtime-shared/fce1c75c21a228b7eb067aa387f573196034d9707d78c85c32c363fc88ef4d4e/run/tiles/{{z}}/{{x}}/{{y}}?crop_type={crop_type}"
layer = lonboard.BitmapTileLayer(
    data=url, tile_size=256, max_requests=-1, min_zoom=0, max_zoom=19
)
map = lonboard.Map(
    layers=[layer],
    _initial_view_state={"longitude": -121.4, "latitude": 37.7, "zoom": 10},
    basemap_style=lonboard.basemap.CartoBasemap.Voyager,
    show_tooltip=True,
)
map
```

![alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/lonboard_cdl.png)

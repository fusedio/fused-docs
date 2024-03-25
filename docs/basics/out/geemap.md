# Geemap

[Geemap](https://geemap.org/) is a Python package to visually analyze geospatial data with Google Earth Engine (GEE).

This snippet shows how to render a `GeoDataFrame` returned by a UDF in geemap. Specifically, the [UDF](https://github.com/fusedio/udfs/tree/main/public/Overture_Maps_Example) loads Buildings from the [Overture](https://beta.source.coop/repositories/fused/overture/description/) dataset, converts them to a GEE [FeatureCollection](https://developers.google.com/earth-engine/apidocs/ee-featurecollection), and renders them on the map as vectors.

![geemap](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/geemap.png)

```python
import geemap
import geopandas as gpd
import ee
import fused

ee.Initialize()

# Load UDF
udf = fused.load("https://github.com/fusedio/udfs/tree/0905bef/public/Overture_Maps_Example")

# Create a map centered at the given location
Map = geemap.Map(center=(37.8, -122.4), zoom=14)

# Run UDF
gdf_buildings = fused.run(udf=udf, x=10484, y=25324, z=16, type="tile")

# Render buildings on map
fc = geemap.geopandas_to_ee(gdf_buildings)
Map.addLayer(fc, {'color': 'red'}, "Default Overture Buildings")
Map
```

To run the same UDF for a custom polygon, draw a polygon on the map, then run this snippet.

```python
# Query for a (single) polygon drawn on the map
roi = ee.FeatureCollection(Map.draw_features)
gdf_bbox = geemap.ee_to_gdf(roi)

# Run UDF
gdf_buildings = udf(bbox=gdf_bbox).run_local()

# Render buildings on map
fc = geemap.geopandas_to_ee(gdf_buildings)
Map.addLayer(fc, {}, "Custom Overture Buildings")
```

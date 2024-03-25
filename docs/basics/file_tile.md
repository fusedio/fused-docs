---
title: UDFs
tags: [Tile, File]
sidebar_position: 6
---

# UDF execution modes

Fused can efficiently transform and load any size geospatial dataset into dynamic and performant maps into data analysis tools.

The growing popularity of analysis-ready cloud optimized data formats has revolutionized data processing by eliminating the need for specialized hardware to handle large datasets. Fused leverages industry standard cloud optimized formats to efficiently pull specific portions of a dataset corresponding to specified spatial areas.

These datasets organize vectors and raster pixels in a manner that allows Fused to request specific portions of the file. Fused UDFs are spatially aware thanks to the bbox parameter, which specifies the portion of the dataset to query.

By designing your UDFs to operating on specified areas, Fused optimizes resource allocation across multiple workers to enhance processing efficiency.

💡 For further reading on data formats, refer to resources on:

- [Cloud Optimized GeoTiff](https://www.cogeo.org/)
- [Raster](https://rasterio.readthedocs.io/en/stable/api/rasterio.windows.html)
- [Geoparquet](https://geoparquet.org/)
- [GeoArrow](https://geoarrow.org/format.html)

## File & Tile

Fused is designed to process complex datasets of any size and serve them as custom vector and raster tilesets. Instead of querying a slow backend database, a map that uses Fused’s dynamic Tile layers is smooth and loads instantly. This is especially powerful to do custom transformations on datasets with millions of records.

A UDF is essentially a serverless python function that returns a result. Spatial filtering supercharges UDFs with the capability to process only specific spatial areas within a dataset of any size.

A UDF becomes spatially aware when it leverages the `bbox` parameter to filter the datasets it operates on. This enables a UDF to run the `File` way, as a one-off task, or to become a dynamic `Tile`. 

- The `File` way, a UDF as a one-off task and returns results based on specified input parameters. It executes once for the specified inputs.
- The `Tile` way, similar to `File`, but Fused dynamically passes the `bbox` parameter.

When web mapping tools call a UDF as a `Tile`, they make multiple calls in parallel for different areas then stitch the results together to create a map. This creates a responsive visualization experience. The best part is that Fused handles data partitions, caching, and parallelization behind the scenes so users can focus on analyzing data.

Read-on to understand the nuances between the two way UDFs can run.

### When would I want to run a UDF in Tile mode?

Running a UDF in Tile mode enables compatibility with industry standard tools that render [tiled web maps](https://en.wikipedia.org/wiki/Tiled_web_map), which consist of dozens of seamlessly joined individually-requested tiles of either image or vector format. Instead of fetching an entire dataset, Tile-based mapping tools only load and render what's visible in the current viewport.

To use data in these tools, data must be sliced into "tiles" - each with a pre-defined bounding box and zoom level. But loading data from large files can be slow slow and generating precomputed tiles can be tedious. Instead, Fused UDFs can dynamically generate Tiles that load into map apps from a unique URL that Fused hosts for you. Use this to create responsive frontend applications.

In addition to integrating with other tools (such as geemap, leaflet, mapbox), running UDFs in Tile mode gives them other advantages like parallel execution and spatial caching.

You can read more about the XYZ indexing system in the [Deck.gl](http://Deck.gl) [documentation](https://deck.gl/docs/api-reference/geo-layers/tile-layer#indexing-system). In fact, Fused Workbench runs UDFs on a serverless backend and renders output in Deck.gl.

### How can I run a UDF as a Tile?

By default, a UDF runs as `File` - it executes once and returns a single output that corresponds to the input parameters. The same UDF can be triggered to run like a Tile when its called using a `bbox` spatial argument. This makes it possible to plug in its HTTP endpoint into a frontend Tile mapping application - think Leaflet, Mapbox, Foursquare Studio, Lonboard, and others.

## Writing UDFs

When writing UDFs, it’s important to understand how to strategically use the `bbox` spatial filter to select which parts of a dataset to load. This section shows approaches for different dataset types.

### The `bbox` object

`bbox` is a UDF’s spatial filter.

Tile mapping tools call Fused endpoints and dynamically pass an XYZ index for each Tile to render. When a UDF endpoint is called this way - in Tile mode - Fused passes the UDF a `bbox` object as the first parameter, which is a polygon with coordinates for the particular Tile.

This snippet shows an instance of a box object, which is a [shapely.Polygon](https://shapely.readthedocs.io/en/stable/reference/shapely.Polygon.html) type with the Tile bounding box’s 4 vertices.

```python
import shapely
bbox = shapely.Polygon([[-121.640625, 37.43997405227058], [-121.640625, 37.718590325588146], [-121.9921875, 37.718590325588146], [-121.9921875, 37.43997405227058], [-121.640625, 37.43997405227058]])
>> POLYGON ((-121.640625 37.43997405227058, -121.640625 37.718590325588146, -121.9921875 37.718590325588146, -121.9921875 37.43997405227058, -121.640625 37.43997405227058))
```

When writing a UDF, Fused recommends setting the `bbox` as the first parameter, and typing it as a `fused.types.Bbox` with a default value of None. This will enable the UDF to run in both as `File` (when `bbox` isn’t necessarily passed) and as a `Tile`. For example:

```python
@fused.udf
def udf(bbox: fused.types.Bbox=None):
    ...
    return ...
```

#### Filter raster files

Fused exposes utility functions to spatially filter raster files.

- `utils.read_tiff`

The function`utils.mosaic_tiff` generates a mosaic image from a list of TIFF files.  `bbox` defines the area of interest within the list of TIFF files set by `tiff_list`.

```python
utils = fused.load("https://github.com/fusedio/udfs/tree/f928ee1/public/common/").utils
data = utils.mosaic_tiff(
            bbox=bbox,
            tiff_list=tiff_list,
            output_shape=(256, 256),
        )
```

As an example, the [LULC_Tile UDF](https://github.com/fusedio/udfs/blob/b89a3aab05cb75dab25abb73e4c17490844ab764/public/LULC_Tile_Example/LULC_Tile_Example.py#L21-L27) uses `mosaic_tiff` to create a mosaic from a set of Land Cover tiffs.


:::tip
When returning a raster object that doesn’t have spatial metadata, like a numpy array, a UDF must also return the bbox object to tell Fused where in the globe to place the output raster. For example: 

```python
@fused.udf
def udf(bbox: fused.types.Bbox=None):
    ...
    return np.array([[…], […]]), bbox
```
:::

#### Filter STAC datasets

STAC ([SpatioTemporal Asset Catalog](https://github.com/radiantearth/stac-spec)) datasets can be queried by passing the bounding box’s bounds (`bbox.bounds`) to the pystac client of the Python [pystac-client](https://pypi.org/project/pystac-client/) library.

```jsx
import pystac_client
from pystac.extensions.eo import EOExtension as eo

catalog = pystac_client.Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=planetary_computer.sign_inplace,
)
items = catalog.search(
    collections=[collection],
    bbox=bbox.total_bounds,
).item_collection()
```

---
id: core-concepts
title: Core Concepts
tags: [Core Concepts]
sidebar_position: 2
---


# Core concepts

Client systems call Fused API endpoints to trigger and load data from serverless Python operations.

These operations can interact with data across any systems that can be interfaced with Python. For example, load a table from Salesforce, perform a transformation, then write it into another data store or even directly to a consuming application like Google Sheets. 

What differentiates Fused from traditional ETL and orchestrators is that a Fused "job" is triggered by a simple parametrized HTTP call. This means they run and load data at any point of the stack. Any mechanism that makes HTTP requests can run UDFs and load their response data - this includes the terminal, ETL jobs, webhooks, Tile maps, frontend applications, and even browser requests.

Furthermore, Fused doesn't try to boil the ocean: it loads only the fraction of data needed for an operation and strategically caches for efficiency. Like DuckDB - but with the entire flexibility of native Python at its disposal.

The following sections outline the core concepts you should grow to understand as you acquaint yourself with Fused. They begin with an overview of the User Defined Function's anatomy, navigate through helper functions and runtime state management, and conclude with an explanation of how external systems integrate with UDFs via the Fused Hosted API.

## The UDF

User Defined Functions (UDFs) are Python operations that integrate across the stack via HTTP endpoints. When called, a UDF endpoint runs a serverless Python function over any size dataset and returns the function output. UDFs are building blocks that can be assembled into complex workflows in which UDFs call eachother or run in parallel.

A UDF is a python function with the following components:

- [a) `@fused.udf` decorator](/basics/core-concepts/#a-fusedudf-decorator)
- [b) Function declaration](/basics/core-concepts/#b-function-declaration)
- [c) Typed parameters](/basics/core-concepts/#c-typed-parameters)
- [d) Return object](/basics/core-concepts/#d-return-object)

The structure of the API call determines a UDFs execution mode.

### Execution modes (File & Tile)

Fused automatically creates an endpoint for all saved Fused UDF. When a client application calls a UDF endpoint, Fused runs a lightweight serverless Python operation and returns the function output. Its engine leverages industry standard cloud optimized dataset formats to efficiently pull specific fragments of datasets - based on specified geographic or logical partitions.

Fused can processes datasets of any size and serve them as dynamic vector and raster tilesets. Instead of loading an entire dataset, which is an expensive operation, Fused tile layers load instantly because they operate on a fraction of the dataset - in parallel. Tile-level spatial filtering supercharges UDFs to process only specific spatial areas within a geopartitioned dataset. 


This enables a UDF endpoint to act as a remote `File`, as a one-off task, or to become a dynamic `Tile` endpoint that interoperates with map tiling system.

#### File & Tile

Depending on how a client application calls an endpoint, the same endpoint can run a UDF as a one-off `File` or as a dynamic `Tile`. 

- When an endpoint is called as a `File`, the UDF runs only once and returns a single batch of output data.  This behaves like the access pattern for a remote file URL.
- When and endpoint is called as a `Tile`, the endpoint becomes interoperable with map tiling clients. The endpoint is called and returns data in parallel for each tile - specified by templated `X`, `Y`, and `Z` indices.

Read-on to understand the nuances between the two way UDF endpoints can be called.

#### Call a UDF endpoint as a File

By default, a UDF runs as `File` - it executes once and returns a single output that corresponds to the input parameters. The UDF endpoint behaves like a remote file in that calling it returns a single batch of data - but the endpoint also accepts parameters that dynamically influence the UDF's execution. 

This enables client applications to make an HTTP request and load the UDF's output data into the tool that makes the call.

Note that files are downloaded entirely. Even if the data is requested as a Parquet.

#### Call a UDF endpoint as a Tile

The same UDF's API endpoint can be called to run like a Tile. This makes it possible for Fused to work like a Tile server that loads vector or raster data into industry standard tools that render [tiled web maps](https://en.wikipedia.org/wiki/Tiled_web_map) - think Leaflet, Mapbox, Foursquare Studio, Lonboard, and beyond. Tiling clients can make dozens of simultaneous calls to the Fused API endpoint - one for each tile - and seamlessly stitch the outputs to render a map. Instead of operating on an entire dataset, Fused only acts on the data that corresponds to the area visible in the current viewport.

:::tip
You can read more about the XYZ indexing system in the [Deck.gl](http://Deck.gl) [documentation](https://deck.gl/docs/api-reference/geo-layers/tile-layer#indexing-system). In fact, Fused Workbench runs UDFs on a serverless backend and renders output in Deck.gl.
:::

### a) `@fused.udf` decorator

To create a UDF, decorate a Python function with `@fused.udf`. This decorator automatically the function into a serverless endpoint that can be invoked via HTTP requests and gives it the ability to fractionally load data. 

This simplified example illustrates the concept. It's that simple.

```python
@fused.udf
def my_udf():
    ...
    return gdf
```

### b) Function declaration

The next step is to structure the function's business logic to interact with upstream data sources and return an object which will be the UDF's output.

To illustrate, this UDF is a function called `udf` that returns a dataframe. Notice how its import statements are placed within the function declaration. The `bbox` argument gives the data spatial awareness, which you can read more about [here](/basics/core-concepts/#file--tile).

```python
@fused.udf
def udf(bbox, table_path="s3://fused-asset/infra/building_msft_us"):
    from utils import table_to_tile
    df=table_to_tile(bbox, table=table_path)
    return df
```

:::tip
To visualize the output of a UDF on Workbench, the function should return a Raster or Vector object. Workbench will render the UDF's returned data as a map layer. Read more about return types [here](/basics/core-concepts/#udf-execution-modes-file-tile).
:::

#### Syntax to keep in mind

The Fused compute engine recognizes the UDF as self-contained function. This means that developers should:
- Decorate the UDF function with `@fused.udf`.
- Declare imports within the function.
- Encapsulate helper functions as importable `util modules` of the UDF.
- Optionally, enable autodetection with [explicit typing](/workbench/udf-editor/#auto-tile-and-file).

That’s all the new syntax you need to remember to get started!

### c) Typed parameters

When a UDF's signature have explicit types, Fused converts passed parameters to the specified types.

:::tip
UDF endpoints can be called via HTTP requests, so input parameters must be serializable. 

As such, it's important to explicitly define the types of input parameters. That way, Fused knows to convert serialized parameters to the correct type.  That way, for example, if a parameter is declared as an `int`, a stringified `"42"` will convert to an integer `42`.
:::




#### The `bbox` object

A UDF becomes spatially aware when it leverages the `bbox` parameter to spatially filter the datasets it operates on. A UDF can load from a cloud optimized dataset only the parts of the file that are actually required by the query. 

:::tip
The growing popularity of cloud optimized data formats revolutionized data processing by eliminating the need for specialized hardware to handle large datasets. These datasets organize vector tables and raster arrays in such a way that Fused reads only specified portions of the file. 

By strategically designing your UDFs be spatially aware (with the `bbox` parameter), Fused distributes execution across multiple workers that scale and wind down as needed. 

💡 For further reading on data formats, refer to resources on:

- [Cloud Optimized GeoTiff](https://www.cogeo.org/)
- [Raster](https://rasterio.readthedocs.io/en/stable/api/rasterio.windows.html)
- [Geoparquet](https://geoparquet.org/)
- [GeoArrow](https://geoarrow.org/format.html)

:::

When writing UDFs, it’s important to strategically use the `bbox` spatial filter to select which parts of a dataset to load. This section shows approaches for different dataset types.

Tile mapping tools call Fused endpoints and dynamically pass an XYZ index for each Tile to render. When a UDF endpoint is called this way - in Tile mode - Fused passes the UDF a `bbox` object as the first parameter. This object is a data structure with information that corresponds to the Tile's bounds and XYZ coordinates. The object is named `bbox` by convention, but it's possible to use a different name as long as its in the first parameter.

For convenience, users can decide the structure of the `bbox` object by setting explicit typing. The 3 available structures are:
- `fused.types.Bbox` is a `shapely.geometry.polygon.Polygon` corresponding to the Tile's bounds.
- `fused.types.TileXYZ` is a `mercantile.Tile` object with values for the the `x`, `y`, and `z` Tile indices.
- `fused.types.TileGDF` is a `geopandas.geodataframe.GeoDataFrame` with `x`, `y`, `z`, and `geometry` columns.

:::tip
Because a UDF can be called as either File or Tile, Workbench must explicitly know how to render their output. When a UDF is configured as "Auto", Workbench automatically handles the output as Tile if it statically checks that the types `fused.types.TileXYZ`, `fused.types.TileGDF`, or `fused.types.Bbox` are used in the UDF. Otherwise, it assumes File.

Note that the "Auto" setting is specific and applicable only to the Workbench UI. UDFs called via fused-py or HTTP requests run as Tile only if a parameter specifies the Tile geometry. If the UDF is called as a File, Fused passes a `None` value to the first parameter.
:::

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

##### Filter raster files with the `bbox` object

The Fused function `utils.mosaic_tiff` and `pystac-client`'s `catalog.search` illustrate how to use `bbox` to spatially filter a dataset.

For example, function`utils.mosaic_tiff` generates a mosaic image from a list of TIFF files.  `bbox` defines the area of interest within the list of TIFF files set by `tiff_list`.

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

##### Filter STAC datasets with the `bbox` object

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

### d) Return object

Spatial data provides type information to render it on a map. The Fused Workbench displays data on the map as either vector or raster types. Vectors are polygons typically in the form of a GeoDataFrame, and rasters are pixel arrays typically in the form of numpy arrays, or xarray Datasets or DataArrays.

> 💡 Fused expect all returned GeoDataFrame data in `EPSG:4326` - `WGS84` coordinates, using Latitude-Longitude units in decimal degrees.

When writing a UDF, the data type and CRS of its returned object determines how it’ll appear on the map.

#### Vector

Vectors represent real-world features with points, lines, and polygons. Fused accepts the following Vector return types:

- `gpd.GeoDataFrame`
- `pd.DataFrame`
- `gpd.GeoSeries`
- `pd.Series`
- `shapely geometry`

If the CRS of the returned object is not in`EPSG:4326` CRS, Fused will make a best effort to convert it - so it’s preferable if the UDF uses that CRS.

#### Raster

Raster data is comprised of pixels with values, typically arranged in a grid. Rasters can have one or multiple layers.

Fused accepts the following Raster return types

- `numpy.ndarray`
- `xarray.DataArray`
- `datashader.transfer_functions.Image`
- `io.BytesIO` (including png images)

The returned raster object must have a geospatial component. This tells Fused where on the map to render it as an image. For example, this UDF returns an `xarray` `DataArray`, which inherently contains coordinates that tell Fused where on the map to place it. Verify this by printing the object and its type.

```python
import fused
@fused.udf
def udf(lat=-10, lng=30, dataset='general', version='1.5.4'):
    import rioxarray

    lat2= int(lat//10)*10
    lng2 = int(lng//10)*10
    cog_url = f"s3://dataforgood-fb-data/hrsl-cogs/hrsl_{dataset}/v1.5/cog_globallat_{lat2}_lon_{lng2}_{dataset}-v{version}.tif"

    rds = rioxarray.open_rasterio(
        cog_url,
        masked=True,
        overview_level=4
    )

    # Show the output type
    print(type(rds))

    # Inspect the output object
    print(rds)

    return rds
```

The print statements above should display the following in the stdout box, which shows how the layer value and coordinates of the `DataArray` object.

```text
<class 'xarray.core.dataarray.DataArray'>
<xarray.DataArray (band: 1, y: 1126, x: 1126)>
[1267876 values with dtype=float64]
Coordinates:
  * band         (band) int64 1
  * x            (x) float64 30.0 30.01 30.02 30.03 ... 39.97 39.98 39.99 40.0
  * y            (y) float64 -0.0001389 -0.009028 -0.01792 ... -9.991 -10.0
    spatial_ref  int64 0
Attributes:
    AREA_OR_POINT:  Area
    scale_factor:   1.0
    add_offset:     0.0
```

> 💡 There's 2 ways to control the transparency of raster images.
>
  1. In RGB images, the color black (0,0,0) is automatically set to full transparency.
  2. If a 4 channel array is passed, i.e. RGBA, the value of the 4th channel is the transparency.

##### Bounds

At this point you might be wondering: what happens when the raster object does not have an inherent spatial attribute?

Objects like numpy *arrays* don’t inherently have a geo attribute. In these cases, the UDF must also return the object's *bounds* to tell Fused where it goes on the map.

The syntax is to return the array and an object containing its bounds, separated by a comma. For simplicity, Fused provides the `array_to_xarray` util function that converts arrays to xarrays with a geo component. This function takes the array as its first argument, and a geo reference (bounds or the `bbox` object) as its second.

```python
@fused.udf
def udf(lat=-10, lng=30, dataset='general', version='1.5.4'):
    import rioxarray

    lat2= int(lat//10)*10
    lng2 = int(lng//10)*10
    cog_url = f"s3://dataforgood-fb-data/hrsl-cogs/hrsl_{dataset}/v1.5/cog_globallat_{lat2}_lon_{lng2}_{dataset}-v{version}.tif"

    rds = rioxarray.open_rasterio(
        cog_url,
        masked=True,
        overview_level=4
    )

    ...

    # Array values
    output_object = rds.values.squeeze().astype(float)
    object_bounds = rds.rio.bounds()

    # Show outpu object and its bounds
    print(output_object)
    print(object_bounds)

    # Return array and bounds
    return output_object, object_bounds
```


<!--
TODO: reinstate once array_to_xarray relocation consistent
    # Option B: convert to xarray and return
    from fused.utils import array_to_xarray

    output_object_xarray = array_to_xarray(
      rds.values.squeeze().astype(float),
      rds.rio.bounds()
    ) -->

> 💡 If you forget to pass the bounds, Fused will default its bounds to `(-180, -90, 180, 90)` and the output image will expand to the size of the globe.



## Saving UDFs

UDFs are saved as a directory of associated files that furnish functionality to run anywhere. This makes them shareable.

For example, the following snippet saves a UDF in a local directory, `Sample_UDF`.

```python
import fused

@fused.udf
def my_udf():
    return "Hello from Fused!"

# Save locally
my_udf.to_directory('Sample_UDF')
```

The directory contains the UDF's documentation, code, metadata, and utility function code.

```
└── Sample_UDF
    ├── README.MD
    ├── Sample_UDF.py
    ├── meta.json
    └── utils.py
```

Files relevant to each UDF are:

- `README.md` Provides details of the UDF's purpose and how it works.
- `Sample_UDF.py` This eponymous Python file contains the UDF's business logic as a Python function decorated with `@fused.udf`.
- `meta.json` This file contains metadata needed to render the UDF in the Fused explorer and for the UDF to run correctly.
- `utils.py` This Python file contains helper functions the UDF (optionally) imports and references.



## Utility modules

Utility modules enhance the functionality and maintainability of UDFs.

As UDFs grow in complexity, it's useful to modularize the code to make it reusable and composable. It's also a good practice to keep only the essential "business logic" in the decorated UDF function - this makes it easy to know what a UDF does at a glance.

With this in mind, a Fused UDF can optionally reference a module to import Python objects from it, with an import statement as if importing from a Python package. These modules are reusable Python functions that promote code reuse and speed up development time. UDFs can import from a variety of sources: from the local environment, from GitHub, and from other UDFs. This section shows how to import modules into UDFs form each of these sources.

### From local

Local modules are Python files in the same environment as the UDF.


In the Workbench, the "module" code editor tab is the place for helper functions and other associated Python objects for the UDF to import. Keep in mind that the module's name is configurable in order to avoid naming collisions. In this example, UDF imports the function `arr_to_plasma` from its module, which is named `utils`. The function contains support logic the UDF uses it to transform an array.

```python
@fused.udf
def udf(bbox):
    from utils import arr_to_plasma
    ...
    return arr_to_plasma(arr.values, min_max=(0, .8))
```

![Alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/image-33.png)

When importing a module from a Python environment other than Workbench, the module must be specified as the locally-scoped file name in the `headers` argument of the `@fused.udf` decorator. This lets Fused know how to complete the reference.

```python
@fused.udf(
    headers=['utils.py']
)
def udf(bbox):
    from utils import arr_to_plasma
    ...
    return arr_to_plasma(arr.values, min_max=(0, .8))
```


### From GitHub

Fused can also import Python modules from a public GitHub URL. The URL must be of a directory that contains modules exported with Fused - that way they include the metadata needed to import them. This example shows how to import the `utils` module and call its `table_to_tile` function.

```python
utils = fused.core.import_from_github('https://github.com/fusedio/udfs/tree/main/public/common/').utils
utils.table_to_tile(...)
```

## Cache

Fused runs UDFs from top to bottom each time. This execution model makes development easy, but can be encumbered if long-running helper functions are called again and again.

Sometimes a UDF might take a while to download or process data. When this happens, developers can take advantage of Fused's built-in caching. Caching stores the results of slow function calls so they only need to run once.

All a developer must do is place slow code inside a helper function, decorate the function with `@fused.cache`, and assign the returned data object to a variable. The object will persist across runs. This empowers users to quickly iterate on downstream code without having to wait for the slow code to run each time.

Fused caches the function's output using a unique hash identifier generated based on the function's code, the value of its parameters, and the `_cache_id` argument.

#### Minimal example

To illustrate, this function accepts an argument and a keywork argument. When the function is called to set `output_1` and `output_2`, Fused caches the output of each call as separate objects. That way, the UDF only runs the function once for each set of passed arguments.

```python
@fused.cache
def sample_function(name, company="Fused"):
    # Function logic
    return f"{name}, at {company}, cached this function's output."

@fused.udf
def udf(bbox):
    ...
    output_1 = sample_function("Sina")
    output_2 = sample_function("Plinio", company="Fused.io")
    ...

```

#### Intermediate example

At this point, ony might ask: if UDFs run for each tile in the viewport, how does Fused distinguish the cache for each tile?

UDFs give spatial awareness to the cache decorator by setting `_cache_id` as string identifier unique to the tile's `bbox`. This can for example be a string such as `str(bbox.to_json())`, or something more complex that could include a date to distinguish cached outputs by.

Note that a custom caching directory can be set with the optional `path` parameter.

```python
@fused.cache(path='optional_cache_dir')
def sample_function(name, company="Fused"):
    # Function logic
    return f"{name}, at {company}, cached this function's output."

@fused.udf
def udf(bbox):
    ...
    output = sample_function("Plinio", company="Fused.io", _cache_id=str(bbox.to_json())")
    ...
```

## Download

Fused Workbench runs UDFs from top to bottom each time code changes. This means objects in the UDF are recreated each time, which can slow down a UDF that downloads files from a remote server.

> 💡 Downloaded files are written to a mounted volume shared across all UDFs in an organization. This means that a file downloaded by one UDF can be read by other UDFs.

Fused addresses the latency of downloading files with the `download` utility function. It stores files in the mounted filesystem so they only download the first time.

> 💡 Because a Tile UDF runs multiple chunks in parallel, the `download` function sets a signal lock during the first download attempt, to ensure the download happens only once.

### Example: download `.zip` file

To download a file to disk, call `fused.core.download`. The function downloads the file only on the first execution, and returns the file path for downstream functions to reference.

This example downloads a `.zip` file then returs it as a GeoDataFrame. Note how GeoPandas reads the local file path returned by `download`.

```python
@fused.udf
def udf(url='https://www2.census.gov/geo/tiger/TIGER_RD18/STATE/11_DISTRICT_OF_COLUMBIA/11/tl_rd22_11_bg.zip'):
    import fused
    import geopandas as gpd

    # Download zip file
    out_path = fused.core.download(url=url, file_path='out.zip')

    # Show path to file
    print(out_path)

    return gpd.read_file(out_path)
```


## File systems

The Fused runtime has two file systems to persist and share artifacts across UDF runs: an S3 bucket and a disk file system. These are used to store downloaded or generated objects, environment variables, and auxiliary files.

:::warning
Access to the file systems is tightly scoped at the organization level, so files stored in either system can only be accessed by accounts in the same organization. 

Given the flexibility of Fused to run any Python code on files in the file system, users should take precautions standard to working with sensitive files.
:::

### `fd://` S3 bucket

The `fd://` bucket file system serves as a namespace for an S3 bucket provisioned by Fused Cloud for your organization. It provides a unified interface for accessing files and directories stored within the bucket, abstracting away the complexities of direct interaction with S3. Fused helper functions access it like an object on S3.

For example, to fetch a file:
```python
fused.get("fd://bucket-name/file.parquet")
```

Or, for example, to ingest a table:
```python
job = fused.ingest(
    input="https://www2.census.gov/geo/tiger/TIGER_RD18/STATE/06_CALIFORNIA/06/tl_rd22_06_bg.zip",
    output="fd://census/ca_bg_2022/",
).execute()
```

### `/mnt/cache` disk

The `/mnt/cache` disk file system is the UDF runtime's local directory that persists across UDF runs. Use it store downloaded files, the output of cached functions, access keys, and to set environment variables with `.env` files.

To list files in the directory, run this in a UDF.

```python
import os

for each in os.listdir('/mnt/cache/'):
    print(each)
```

## Environment variables

Save constants and secrets to an `.env` file to make them available to your UDFs via environment variables.

First, run a UDF that sets variables in an `.env` file.

:::note
To be accessible to all UDF run events, the file must be placed on the runtime's mount path `/mnt/cache/`.
:::

```py
@fused.udf
def udf():
    env_vars = """
    MY_ENV_VAR=123
    DB_USER=username
    DB_PASS=******
    """

    # Path to .env file in disk file system
    env_file_path = '/mnt/cache/.env'

    # Write the environment variables to the .env file
    with open(env_file_path, 'w') as file:
        file.write(env_vars)
```

Then, in a different UDF, load the variables into the environment.

```py
@fused.udf
def udf():
    from dotenv import load_dotenv

    # Load environment variable
    env_file_path = '/mnt/cache/.env'
    load_dotenv(env_file_path, override=True)
    print(f"Updated MY_ENV_VAR: {os.getenv('MY_ENV_VAR')}")
```

## Hosted API 

Fused automatically creates HTTP endpoints for every UDF saved in the Fused cloud.

Using the Fused Hosted API supercharges your stack with the ability to trigger and load the output of any scale workflows. API calls automatically provision serverless compute resources to run workflows in parallel using advanced caching and geo partitioning - without your team needing to spend time on setup.

Endpoints created with Fused Hosted API seamlessly integrate with tools such as:

- Tile-based maps: Simply pass the endpoint into tile-based maps such as open source JavaScript tools (e.g. leaflet, Deck.gl, and Kepler.gl), proprietary web-based apps (such as Felt and Foursquare Studio), or desktop based tools such as ArcGIS, ESRI, and QGIS.
- Apps that make HTTP requests: Load data into low-code app builders such as Streamlit & Retool.
- Apps that render embeddable maps: Embed responsive maps to significantly enhance the utility and interactivity of documentation sites and apps, such as Notion.


The following sections describes how to create a UDF endpoint either in Workbench or with the Fused Python SDK, and how to authenticate requests to call the endpoint. They also describe how to make authenticated calls to these endpoints. Browse the ["Get data out"](/basics/out/) section for examples of how to use them to load data into specific tools.

:::note
    Endpoints can be called with "private" or "shared" authentication tokens. Shared tokens are easy to create and revoke. Use shared tokens to call UDFs from 3rd party applications or to share them with others.
:::

### Generate endpoints with Workbench

Once a UDF is saved in Workbench, the "Settings" tab of the editor shows code snippets that can be used to call the UDF from different environments. 

#### Shareable public endpoints

The "Share" subsection contains snippets with shared tokens and signed URLs. 
- `HTTP` is the URL to call the UDF endpoint.
- `cURL` is the command to call the UDF endpoint from the terminal.
- `Python` is the code to call the UDF endpoint from a Python environment using the token.
- `Token` is the shared token, which you'll notice appears in the above snippets. 

![alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/share.png)



#### Private endpoints

The "Snippets" subsection below it contains snippets that can only be called with the authoring account's authentication.
- `cURL` is the command to call the UDF endpoint from the terminal, which requires the authoring account's private token.
- `Python` is the code to call the UDF endpoint from a Python environment using the token.
- `Load this UDF` is loads the UDF into a Python environment where it can be modified, chained with other UDFs, or called. 

![alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/snippets.png)



### Generate endpoints with `fused-py`


#### Get an account's private token

Python environments where the authentication flow completed successfully store a credentials key in the default location ` ~/.fused/credentials`. Calls to UDFs from those environments will use that key, unless a token for a different account is explicitly set in the call. Making calls to endpoints from a non-authenticated environment will need the authenticated account's access token, which can be retrieved with the following commands.

```python
from fused._auth import CREDENTIALS

CREDENTIALS.credentials.access_token
```


:::danger

Note that the "private" token can access all UDFs and should be kept private. The recommended approach is instead to use "shared" tokens with tightly scoped permissions, as detailed below.

Remember that tokens are tied to the account that created them and requests to their corresponding endpoints will accrue charges on that account.
:::


This is how to call UDF endpoints via HTTP requests with the token.

```bash
curl -XGET https://app.fused.io/server/v1/realtime-shared/$SHARED_TOKEN/run/file
```

#### Create and manage shared tokens (recommended)

Shared tokens are tightly scoped to a single UDF, and can easily be revoked. Creating a shared token for a UDF returns a token object that, among other attributes, contains the token as a string and sample endpoint URLs.

This is how to to call UDF endpoints in Python with signed token URLs.
```python
from fused.api import FusedAPI
api = FusedAPI()

token_object = api.create_udf_access_token(udf_email="user@fused.io", udf_name="caltrain_live_location")
output = fused.core.run_shared_file(token=token_object.token, my_param="...")
```

#### Manage shared tokens

Fetch a specific UDF token object using its unique token string:
```python
token_object = api.get_udf_access_token(token=token.token)
```

Fetch all UDF tokens:
```python
token_objects = api.get_udf_access_tokens()
```

Update a specific UDF token using its unique token string:
```python
token_object = api.update_udf_access_token(token=token.token, enabled=True)
```

Delete a specific UDF token using its unique token string:
```python
api.delete_udf_access_token(token=token.token, enabled=True)
```


Similarly, signed URLs endpoints can be created that can be called from another application via HTTP requests.

#### Single File HTTP endpoints

Single file HTTP endpoints are suitable for handling individual requests, ideal for scenarios where a single resource is required, such as loading data into [Google Sheets](/hosted-api/integrations/google_sheets/).


```python
from fused.api import FusedAPI
api = FusedAPI()

# URL for single call
api.create_udf_access_token(udf_email="user@fused.io", udf_name="caltrain_live_location").get_file_url()
```

#### Tile HTTP endpoints

Tile HTTP endpoints are designed for serving map applications that consume Tiles, such as [Lonboard](/hosted-api/integrations/lonboard/) or [geemap](/hosted-api/integrations/geemap/).

```python
from fused.api import FusedAPI
api = FusedAPI()

# URL for XYZ tiles
api.create_udf_access_token(udf_email="user@fused.io", udf_name="caltrain_live_location").get_tile_url()
```

### Call UDFs

UDFs can be triggered via the Python SDK or HTTP requests, and they can return data in different formats depending on how they're called. The following sections describe how to call UDFs and how to configure calls to return data in different formats.

#### Call UDFs with Python


The Fused Python SDK exposes methods to call UDFs. In Python environments authenticated to Fused, the UDF be called or imported in these 3 ways:


##### Call UDF and return its output

```python
fused.run("user@fused.io", "Overture_Maps", x=2808, y=6542, z=14, my_udf_parameter=5)
```

##### Call UDF asynchronously and return its output

:::note
    [nest_asyncio](https://pypi.org/project/nest-asyncio/) might be required to run UDFs async from Jupyter Notebooks.
    ```python
    !pip install nest-asyncio -q
    import nest_asyncio
    nest_asyncio.apply()
    ```
:::

```python
import asyncio
import fused

# Run the UDF in an async function
async def main():
    return await fused.run("user@fused.io", "Overture_Maps", x=2808, y=6542, z=14, sync=False)

# Run the coroutine and capture the result
gdf = asyncio.run(main())

# Use the returned value outside the event loop
gdf.head()

```

##### Import as a UDF object

```python
my_udf = fused.core.load_udf_from_fused("user@fused.io", "caltrain_live_location")
```

:::note
Did you know UDFs can also call other UDFs? It's an easy way to chain UDFs together or even run them in parallel.
:::

#### Call UDFs with HTTP requests

Beyond Python, other frameworks can call the UDF endpoint via HTTP requests and receive output data in the response. This makes it easy to load data from UDFs into Tile-based mapping tools such as [DeckGL](https://deck.gl/docs/api-reference/geo-layers/tile-layer), [Mapbox](https://docs.mapbox.com/mapbox-gl-js/example/vector-source/), and [Felt](https://felt.com/), or no-code data analytics environments like [Google Sheets](https://support.google.com/docs/answer/3093335?hl=en) and [Retool](https://docs.retool.com/apps/web/guides/components/custom). Read the ["Get data out"](/basics/out/) section of the documentation for example integrations with your favorite tools. 


##### Shared token

To run a UDF via HTTP request, generate a [signed UDF endpoint](/basics/core-concepts/#generate-endpoints-with-workbench) then modify the provided URL. 

Structure the URL with the `file` path parameter to run as a single batch operation.

```
https://www.fused.io/server/v1/realtime-shared/******/run/file?dtype_out_raster=png
```

To integrate with a tiling service, structure the URL with the `tiles` path paramater, followed by templated `/{z}/{x}/{y}` path parameters. See [Lonboard](/basics/out/lonboard/) for an example.

```
https://www.fused.io/server/v1/realtime-shared/******/run/tiles/{z}/{x}/{y}?dtype_out_raster=png
```

##### Private token

Calling UDFs with [Bearer authentication](https://swagger.io/docs/specification/authentication/bearer-authentication/) requires an account's [private token](/basics/core-concepts/#get-an-accounts-private-token). The URL structure to run UDFs with the private token varies slightly, as the URL specifies the UDF's name and the owner's user account. 

```bash
curl -XGET "https://app.fused.io/server/v1/realtime/fused/api/v1/run/udf/saved/user@fused.io/caltrain_live_location?dtype_out_raster=png" -H "Authorization: Bearer $ACCESS_TOKEN"
```

#### Response formats

The response data format is configured with the `dtype_out_vector` and `dtype_out_raster` parameter. Because the UDF's returned object determines whether response is a vector or raster, both parameters can be specified simultaneously, which the sample snippets show in query parameters like: `?dtype_out_raster=png&dtype_out_vector=csv`.

Vector:
- parquet 
- geojson
- json 
- feather 
- csv 
- mvt 
- html 
- excel 
- xml

Raster:
- png 
- gif 
- jpg 
- jpeg
- webp 
- tif 
- tiff



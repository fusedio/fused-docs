---
id: core-concepts
title: Core Concepts
tags: [Core Concepts]
sidebar_position: 2
---


# Core concepts

## `@fused.udf`


User Defined Functions (UDFs) are building blocks of geospatial operations that integrate across the stack. They run Python functions over any size dataset and return the output.

To write a UDF, decorate a Python function with `@fused.udf` - this tells Fused to give the function special treatment. Encapsulate the business logic within the function and return the data object to visualize.

To illustrate, this UDF is a function called `udf` that returns a dataframe. Notice how its import statements are placed within the function declaration. The `bbox` argument gives the data spatial awareness, which you can read more about in the [Tile vs. File](/core_concepts/#tile-vs-file-udfs) section below.


```python

@fused.udf
def udf(bbox, table_path="s3://fused-asset/infra/building_msft_us"):
    from utils import table_to_tile
    df=table_to_tile(bbox, table=table_path)
    return df
```

:::tip
To visualize the output of a UDF on Workbench, the function should return a Raster or Vector object. Workbench will render the UDF's returned data as a map layer. Read more about return types [here](/docs/basics/core-concepts#return-types).
:::
#### Syntax to keep in mind

The Fused compute engine recognizes the UDF as self-contained function. This means that developers should:

a) Decorate the UDF function with `@fused.udf`.

b) Declare imports within the function.

c) Encapsulate helper functions as importable `util modules` of the UDF.

That’s all the new syntax you need to remember to get started!

#### Saving UDFs

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

## Return types

Spatial data provides type information to render it on a map. The Fused Workbench displays data on the map as either vector or raster types. Vectors are polygons typically in the form of a GeoDataFrame, and rasters are pixel arrays typically in the form of numpy arrays, or xarray Datasets or DataArrays.

> 💡 Fused expect all return data in `EPSG:4326` - `WGS84` coordinates, using Latitude-Longitude units in decimal degrees.

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

#### Bounds

But, what if the raster object does not have an inherent spatial attribute?

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

## Environment variables

Add constants and secrets to an `.env` file to make them available to your UDFs via environment variables.

First, run a UDF that sets variables in an `.env` file.

:::note
To be accessible to all UDF run events, the file must be placed on the runtime's mount path `/mnt/cache/`.
:::
```py
env_vars = """
MY_ENV_VAR=123
DB_USER=username
DB_PASS=******
"""

# Path to your .env file
env_file_path = '/mnt/cache/.env'

# Writing the environment variables to the .env file
with open(env_file_path, 'w') as file:
    file.write(env_vars)
```

Then, in a different UDF, load the variables into the environment.

```py
from dotenv import load_dotenv

# Load environment variable
env_file_path = '/mnt/cache/.env'
load_dotenv(env_file_path, override=True)
print(f"Updated MY_ENV_VAR: {os.getenv('MY_ENV_VAR')}")
```

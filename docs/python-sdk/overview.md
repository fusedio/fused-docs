---
id: overview
title: Overview
tags: [Overview, Python SDK]
sidebar_position: 0
---


# Python SDK Overview

The Fused Python SDK (`fused-py`) supercharges your team's workflows and maps in Jupyter notebooks, low-code web apps, the Fused Workbench webapp, ETL, or any tool in your stack that runs Python.

With the SDK, development code runs on production cloud resources. This shields your team from the need to translate code or transfer data between frameworks. Fused automatically provisions and manages cloud resources - so developers can focus on writing code.


## Install

`fused-py` is a breeze to get started with.

1. Set up a Python environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Run:

```bash
pip install fused
```

:::note
Fused support Python versions `>=3.8` to `<3.12`.
:::
3. Authenticate:

```py
from fused import NotebookCredentials
credentials = NotebookCredentials()
```
Run this snippet from a Notebook Cell and follow the authentication flow, which will store a credentials file in `~/.fused/credentials`.

## Get started

This snippet shows how to import then run a UDF from the [UDF catalog GitHub repo](https://github.com/fusedio/udfs/tree/main).

```python
import fused

udf = fused.load("https://github.com/fusedio/udfs/tree/main/public/DuckDB_NYC_Example")
gdf = udf.run_local()
gdf
```

Similarly, as a bash oneliner.

```python
python -c "import fused; gdf = fused.load('https://github.com/fusedio/udfs/tree/main/public/DuckDB_NYC_Example').run_local(); print(gdf);"
```

<!-- The following ["API Reference"](/python-sdk/api/top-level-functions/) sections show how to write, manage, and run UDFs, as well as the different utility functions designed to make your life easiy. -->

The main thing to remember at this point is that UDFs are simply Python functions decorated with `@fused.udf`.


## Load a UDF

Loading UDFs is a fundamental aspect of collaborative and streamlined workflows. It fosters discoverability within teams and the [UDF community](https://github.com/fusedio/udfs/tree/main), promotes reuse of existing code, and simplifies your code.

UDFs can be loaded from various sources, including GitHub repositories, local files, and the Fused cloud.

Loading a UDF from a GitHub URL:
```py
udf = fused.load("https://github.com/fusedio/udfs/tree/main/public/REM_with_HyRiver/")
```

Loading a UDF from a local file:
```py
udf = fused.load("/localpath/REM_with_HyRiver/")
```

Loading a UDF using a Fused platform-specific identifier:
```py
udf = fused.load("username@fused.io/REM_with_HyRiver")
```

:::note
Loading UDFs from GitHub repositories or local files do not require authentication to the Fused platform.
:::

## Run a UDF

Once a UDF is loaded, running it executes the function code and retrieves the function output. Fused provides flexibility in how the execution and output retrieval.

Fused offers the option to partition datasets and perform computation based on map tiles. UDFs by default run as a single operation, called `File` mode, and can run as spatially partitioned, called `Tile`.

- `File`. By default, UDFs run as a single operation and return all data in one call. This option is suitable for localized and smaller outputs where fetching the entire dataset at once is feasible.
- `Tile`. In this mode, UDFs process data for specific geographic areas defined by predefined bounding boxes. These bounding boxes can be specified in various ways. This option is suitable for datasets that cover geographic extents and allow for spatial queries. Compute tasks are distributed among worker, with each worker processing only the fraction of data corresponding to a specific [tile](https://deck.gl/docs/api-reference/geo-layers/tile-layer). This enables parallel processing and efficient computation.

Deciding which to use is based on the underlying dataset and on how the outputs will be represented. This is specified by the parameters passed to the `fused.run` convenience function.

### Run as File

To run as File, a UDF definition is run without specifying geometry parameters.

```python
import fused

udf = fused.load("https://github.com/fusedio/udfs/tree/main/public/DuckDB_NYC_Example")
gdf = fused.run(udf=udf)
gdf
```

### Run as Tile

To run as a Tile, a UDF definition needs to have its initial parameter specified as `bbox`, serving as a reserved keyword parameter. When this bounding box parameter is specified, UDFs slice data based on the bounds of individual tiles.

When a UDF is called with parameters that specify a tile, Fused will convert them to the corresponding `bbox`. Below are the different ways to specify tiles.


#### a) With `lat`, `lng`, `z` parameters

See the [documentation](https://mercantile.readthedocs.io/en/stable/api/mercantile.html) for the `mercantile` Python library, for reference.

```python
import fused

udf = fused.load("https://github.com/fusedio/udfs/tree/main/public/DEM_10m_Tile_Example")
fused.run(udf=udf, lat=37.1, lng=-122.0, z=13)
```

#### b) With `x`, `y` , `z` parameters

```python
import fused

# Load and run UDF
udf = fused.load("https://github.com/fusedio/udfs/tree/main/public/DEM_10m_Tile_Example")
fused.run(udf=udf, x=2411, y=3079, z=13)
```


#### c) Shapely box (coming soon)

Specify the bounding box with a `shapely.geometry.box` type.

```python
import fused
from shapely.geometry import box

# Load and run UDF
udf = fused.load("https://github.com/fusedio/udfs/tree/main/public/LULC_Tile_Example")
fused.run(udf=udf, bbox=box(-77.34375, 38.41055, -77.167968, 38.54816))

```

#### d) Shapely polygon (coming soon)

Specify the bounding box with a `shapely.geometry.Polygon` type.

```python
import fused
from shapely.geometry import Polygon

# Define bbox polygon
polygon = Polygon([[-77.16796, 38.54816], [-77.16796, 38.41055], [-77.34375, 38.41055], [-77.34375, 38.54816], [-77.16796, 38.54816]])

# Load and run UDF
udf = fused.load("https://github.com/fusedio/udfs/tree/main/public/LULC_Tile_Example")
fused.run(udf=udf, bbox=polygon)
```

#### e) GeoDataFrame

Specify the bounding box with a `geopandas.geodataframe.GeoDataFrame` type.

```python
import fused
import geopandas as gpd

# Define GeoDataFrame
gdf = gpd.read_file('{"geometry": {"type": "Polygon", "coordinates": [[[-77.16796875, 38.54816542304658], [-77.16796875, 38.410558250946075], [-77.34375, 38.410558250946075], [-77.34375, 38.54816542304658], [-77.16796875, 38.54816542304658]]]}}]')

# Load and run UDF
udf = fused.load("https://github.com/fusedio/udfs/tree/main/public/LULC_Tile_Example")
fused.run(udf=udf, bbox=gdf)
```




<!-- :::note
The `fused.run` convenience function wraps [run_tile](/python-sdk/api/core/#fused.core.run_tile) and [run_file](/python-sdk/api/core/#fused.core.run_file) functions, which can optionally be used.
::: -->





## Save a UDF

UDFs can be saved to the local file system, to the Fused cloud, and to GitHub.
- UDFs saved to the Fused cloud can be used as [HTTP endpoints](hosted-api/overview/).
- UDFs saved to the local file system or GitHub can be loaded with `fused.load` as described above.

First, create a UDF object.
```python
import fused

@fused.udf
def my_udf():
    return "Hello from Fused!"
```

Save locally as a directory:
```python
my_udf.to_directory("my_udf")
```

Save locally as a .zip file:
```python
my_udf.to_file("my_udf.zip")
```

Save to a GitHub gist:
```python
my_udf.to_gist()
```

Save remotely to Fused (under the same name as the function object):
```python
my_udf.to_fused()
```

UDFs saved to file systems are structured as a directory, which makes them easy to share and transport. Each UDF, like `Sample_UDF`, is contained within its own subdirectory within the `public` directory - along with its documentation, code, metadata, and utility function code. This means they can be thought of as a standalone Python package.

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

## Typing

Fused UDFs support [Python function annotations](https://peps.python.org/pep-0484/). Annotated parameters convert to the specified type before the UDF is called.

This is important to ensure that parameters serialized on HTTP calls resolve to the intended type. For example, the UDF below takes an integer and a dictionary, and is annotated as follows.

```python
from typing import Dict
import fused

@fused.udf
def udf(my_param: int, my_dict: Dict):
    print(my_param, type(my_param)) # int
    print(my_dict, type(my_dict)) # Dict
```

This feature is under active development. Presently supported types are `int`, `float`, `bool`, `list`, `dict`, `List`, `Dict`, `Iterable`, `uuid.UUID`, `Optional[]`, and `gpd.GeoDataFrame` from a geojson. `Union` is not supported. Parameters that are not annotated are handled as string.

<!-- Fused also exposes special types to specify whether the output in Workbench should be handled as [`Tile` or `File`](core_concepts/#tile-vs-file-udfs). These are `fused.types.TileXYZ` and `fused.types.TileGDF` respectively. The `bbox` parameter is typed as `fused.types.Bbox`. -->

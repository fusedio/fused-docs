---
id: top-level-overview
title: Overview
tags: [Overview, Getting started]
sidebar_position: 0
---


# Overview

[Fused](https://www.fused.io/) is the glue layer that interfaces data platforms and data tools via a managed serverless API.



## Ecosystem

Build any scale workflows with the [Fused Python SDK](python-sdk/overview.md) and [Workbench webapp](workbench/overview.md), and integrate them into your stack with the [Fused Hosted API](hosted-api/overview.md).


![alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/ecosystem_diagram.png)

## Patterns

User Defined Functions (UDFs) are building blocks of serverless geospatial operations that integrate across the stack. They connect frameworks such as Planetary Computer, Google Earth Engine, Big Query, Snowflake, and DuckDB, as well as cloud-native datasets such as NASA, NOAA, US Census, and Overture. With Fused, users write, share, or discover UDFs that turn into live HTTP endpoints that load their output into any tools that can call an API.

The `@fused.udf` decorator is used to define a Python function as a UDF. This simplified example illustrates the concept:

```python
@fused.udf
def my_function():
    ...
    return df
```

Keep these fundamentals in mind as you work with UDFs.

- [@fused.udf](core_concepts/#fusedudf): The UDF decorator prepares the UDF to be deployed as a serverless function that can be invoked through HTTP requests.
- [@fused.cache](core_concepts/#caching): UDFs can import from any Python library or custom helper modules, and cache the output of helper functions with the cache decorator.
- [Tile or File](core_concepts/#tile-vs-file-udfs): There's two types of UDF: `Tile` loads data as a collection of tiles at various zoom levels that make up a complete map, and `File` loads a single output object.
- [Return types](core_concepts/#return-types): UDFs can return any serializable data object. Note that for the output to render on a map, it should be a raster or vector type.


## Connect with the community

Write, share, or discover UDFs across the Fused ecosystem.

<div class="grid cards" markdown>

-   [:fontawesome-brands-github: __GitHub__](https://github.com/fusedio/udfs/tree/main)

-   [:fontawesome-brands-discord: __Discord__](https://bit.ly/fusedslack)

-   [:fontawesome-brands-linkedin: __LinkedIn__](https://www.linkedin.com/company/fusedio/)

-   [:fontawesome-brands-twitter: __Twitter__](https://twitter.com/Fused_io)


</div>

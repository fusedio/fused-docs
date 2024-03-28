# Retool

Supercharge your team's Retool apps with serverless geospatial operations! ⚡

This guide shows how to create a [custom Retool component](https://docs.retool.com/apps/web/guides/components/custom) using the [Mapbox GL JS](https://docs.mapbox.com/mapbox-gl-js/example/) library to display vector tiles from a custom tile server provided by Fused. 

You'll first generate a signed UDF URL then introduce it into a custom map component that can input and output data across other Retool components.

## 1. Generate a signed URL for a UDF

First, on Workbench, create and save a UDF that successfully renders in `Tile` mode. Under the "Settings" tab, click "Share" to [generate a signed URL](/basics/core-concepts/#generate-endpoints-with-workbench) that can be called via HTTP requests. 


Modify the generated `HTTP` URL to run as a [Tile](/core-concepts/#call-udfs-with-http-requests) by setting the `tiles/` path paramater, followed by templated `/{z}/{x}/{y}` path. You can optionally pass UDF parameters as UDF-encoded strings, which can be configured to change based on UI user input.


## 2. Create a custom Retool component


## 3. Pass data from a UI component to the map


## 4. Pass data from the map to a UI component

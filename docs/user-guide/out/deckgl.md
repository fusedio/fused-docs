---
title: DeckGL (HTML)
sidebar_label: DeckGL (HTML)
---

[DeckGL](https://deck.gl/) is a highly framework to create interactive map visualizations that handle large datasets.

This guide shows how to load data from Fused into DeckGL maps created from a single standalone HTML page with the following layer types:

- [H3HexagonLayer](/user-guide/out/deckgl/#h3hexagonlayer)
- [Vector Tile Layer](/user-guide/out/deckgl/#vector-tile-layers)
- [Raster Tile Layer](/user-guide/out/deckgl/#raster-tile-layers)

## 1. Generate a signed URL for a UDF

First create a UDF and [generate a HTTP endpoint](/core-concepts/run/#http-requests).

## 2. Create a DeckGL HTML map

Create an `.html` file following this template. This code creates a DeckGL map then introduces a layer that renders data from the specified Fused endpoint.


```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Fused DeckGL</title>
    <meta
      name="viewport"
      content="initial-scale=1,maximum-scale=1,user-scalable=no"
    />

    <script src="https://unpkg.com/@deck.gl/core@^9.0.0/dist.min.js"></script>
    <script src="https://unpkg.com/@deck.gl/layers@^9.0.0/dist.min.js"></script>
    <script src="https://unpkg.com/@deck.gl/geo-layers@^9.0.0/dist.min.js"></script>
    <script src="https://unpkg.com/@deck.gl/carto@^9.0.0/dist.min.js"></script>
    <script src="https://unpkg.com/h3-js"></script>
    <script src="https://unpkg.com/deck.gl@latest/dist.min.js"></script>
    <script src="https://api.mapbox.com/mapbox-gl-js/v3.2.0/mapbox-gl.js"></script>
    <link
      href="https://api.mapbox.com/mapbox-gl-js/v3.2.0/mapbox-gl.css"
      rel="stylesheet"
    />
    <style>
      body {
        width: 100vw;
        height: 100vh;
        margin: 0;
      }
    </style>
  </head>
  <body>
    <div id="map"></div>
    <script>
      const { DeckGL, H3HexagonLayer, GeoJsonLayer, BitmapLayer, TileLayer } = deck;

      new DeckGL({
        mapboxApiAccessToken:
          "pk.eyJ1IjoiZXN0b3JudWRhbWUiLCJhIjoiY2xneTh0Y3czMDczODNmcG11ZTNuazZvbSJ9.QFTdgqDlAFQKaJ_QLA35ew",
        mapStyle: "mapbox://styles/mapbox/dark-v10",
        initialViewState: {
          longitude: -122.417759,
          latitude: 37.776452,
          zoom: 12,
        },
        controller: true,
        layers: [
          new H3HexagonLayer({
            id: "H3HexagonLayer",
            data: "https://www.fused.io/server/v1/realtime-shared/f393efed9c75425365f2f00254d37cb15166e22fc5defabcc7ee6fd9e2d7a3b4/run/file?dtype_out_vector=json",
            extruded: true,
            getElevation: (d) => d.count,
            elevationScale: 20,
            filled: true,
            stroked: true,
            getFillColor: (d) => [255, (1 - d.count / 500) * 255, 0],
            getHexagon: (d) => d.hex,
            getLineColor: [255, 255, 255],
            getLineWidth: 2,
            lineWidthUnits: "pixels",
          }),
        ],
      });
    </script>
  </body>
</html>
```

### H3HexagonLayer

Create an [`H3HexagonLayer`](https://deck.gl/docs/api-reference/geo-layers/h3-hexagon-layer), which should look similar to this.

<iframe src="/img/deckgl_h3.html"  height="400px" width="100%" scrolling="no"></iframe>

```js
new H3HexagonLayer({
    id: "H3HexagonLayer",
    data: "https://www.fused.io/server/v1/realtime-shared/f393efed9c75425365f2f00254d37cb15166e22fc5defabcc7ee6fd9e2d7a3b4/run/file?dtype_out_vector=json",
    extruded: true,
    getElevation: (d) => d.count,
    elevationScale: 20,
    filled: true,
    stroked: true,
    getFillColor: (d) => [255, (1 - d.count / 500) * 255, 0],
    getHexagon: (d) => d.hex,
    getLineColor: [255, 255, 255],
    getLineWidth: 2,
    lineWidthUnits: "pixels",
}),
```

### Vector Tile Layer

Vector Tile layers are created by placing a [`GeoJsonLayer`](https://deck.gl/docs/api-reference/layers/geojson-layer) sublayer within a [`TileLayer`](https://deck.gl/docs/api-reference/geo-layers/tile-layer). Use the following snippet to introduce a vector layer, which should look similar to this.

The layer in the sample map comes from [Overture Buildings UDF](https://github.com/fusedio/udfs/tree/main/public/Overture_Maps_Example).

<iframe src="/img/deckgl_vector.html"  height="400px" width="100%" scrolling="no"></iframe>

```js
new TileLayer({
  // Use geojsonlayer inside of tilelayer. This is instead of MVT Layer, which has optimizations that can cause clipping when polygon extends beyond Tile area.
  id: "VectorTileLayer",
  data: "https://www.fused.io/server/v1/realtime-shared/3aadf7a892ace2f6efab8da9720f1da241fc4403e7722f501ab45503e094a13d/run/tiles/{z}/{x}/{y}?dtype_out_vector=geojson",
  maxZoom: 19,
  minZoom: 0,

  renderSubLayers: (props) => {
    const { boundingBox } = props.tile;

    return new GeoJsonLayer(props, {
      data: props.data,
      stroked: true,
      getLineColor: [0, 255, 10],
      getLineWidth: 10,
      getFillColor: [0, 40, 0, 0.5],
      getPointRadius: 4,
      getLineWidth: 5,
      pointRadiusUnits: "pixels",
      bounds: [
        boundingBox[0][0],
        boundingBox[0][1],
        boundingBox[1][0],
        boundingBox[1][1],
      ],
    });
  },
});
```

### Raster Tile Layer

Raster Tile layers are created by placing a [`BitmapLayer`](https://deck.gl/docs/api-reference/layers/bitmap-layer) sublayer within a [`TileLayer`](https://deck.gl/docs/api-reference/geo-layers/tile-layer). Use the following snippet to introduce a raster layer, which should look similar to this. The layer in the sample map comes from the [NAIP Tile UDF](https://github.com/fusedio/udfs/tree/main/public/NAIP_Tile_Example).

<iframe src="/img/deckgl_raster.html"  height="300px" width="100%" scrolling="no"></iframe>

```js
new TileLayer({
  id: "RasterTileLayer",
  data: "https://staging.fused.io/server/v1/realtime-shared/3a6030eb4fa9c70780bba1b62cdfffe2eca24745db78aba62ddd96ebb0f6e0cc/run/tiles/{z}/{x}/{y}?dtype_out_raster=png",
  maxZoom: 19,
  minZoom: 0,

  renderSubLayers: (props) => {
    const { boundingBox } = props.tile;

    return new BitmapLayer(props, {
      data: null,
      image: props.data,
      bounds: [
        boundingBox[0][0],
        boundingBox[0][1],
        boundingBox[1][0],
        boundingBox[1][1],
      ],
    });
  },
  pickable: true,
});
```

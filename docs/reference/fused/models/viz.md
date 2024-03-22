---
sidebar_label: viz
title: fused.models.viz
---

## VizLayerConfig Objects

```python
class VizLayerConfig(BaseModel)
```

#### root\_bboxes

Properties as defined on https://deck.gl/docs/api-reference/layers/geojson-layer

#### root\_bbox\_ids

Properties as defined on https://deck.gl/docs/api-reference/layers/text-layer

#### root\_points

Unused

#### root\_heatmap

Properties as defined on https://deck.gl/docs/api-reference/aggregation-layers/heatmap-layer

#### selection\_geojson

Properties as defined on https://nebula.gl/docs/api-reference/layers/editable-geojson-layer

#### data\_circles

Properties as defined on https://deck.gl/docs/api-reference/layers/scatterplot-layer

#### root\_bboxes\_selected

Properties as defined on https://deck.gl/docs/api-reference/layers/geojson-layer

#### data\_bboxes

Unused

#### data\_heatmap

Properties as defined on https://deck.gl/docs/api-reference/aggregation-layers/heatmap-layer

#### data\_solid

Properties as defined on https://deck.gl/docs/api-reference/layers/solid-polygon-layer

#### data\_path

Properties as defined on https://deck.gl/docs/api-reference/layers/path-layer

#### data\_text

Properties as defined on https://deck.gl/docs/api-reference/layers/text-layer

## VizConfig Objects

```python
class VizConfig(BaseModel)
```

Configuration for a dataset in the viz (debug) widget

#### name

Name to show for this dataset

#### show\_heatmap

Show materialized data as a heatmap instead of points (circles)

#### show\_bboxes

Show the bounding boxes of chunks

#### show\_bbox\_ids

Show the IDs of chunk bounding boxes (when show_bboxes is also True)

#### show\_data

Show this dataset

#### show\_tooltip

Allow selection of points in this dataset (e.g. for use with raster debugging)

#### selected\_columns

Columns that will be materialized by default

#### column\_names

Column names for specific uses, such as geographic location or point size scaling

## VizAppConfig Objects

```python
class VizAppConfig(BaseModel)
```

Configuration for the viz (debug) widget

## DatasetViz Objects

```python
class DatasetViz(BaseModel)
```

Configuration for visualizing a specific dataset

## DatasetVizV2 Objects

```python
class DatasetVizV2(BaseModel)
```

Configuration for visualizing a specific dataset


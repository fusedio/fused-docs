---
sidebar_label: common
title: fused.models.udf.common
---

## ChunkMetadata Objects

```python
class ChunkMetadata(BaseModel)
```

#### file\_id

The identifier of the file that contains this chunk.

#### chunk\_id

The identifier of this chunk inside the file.

#### bbox\_minx

The west-most coordinate of this bounding box.

#### bbox\_miny

The southern-most coordinate of this bounding box.

#### bbox\_maxx

The east-most coordinate of this bounding box.

#### bbox\_maxy

The northern-most coordinate of this bounding box.

#### sum\_area

The sum of all area of all geometries in this chunk.

!!! note

    Area is currently computed in the WGS84 coordinate system, so it should only be used as a heuristic.

#### sum\_length

The sum of all lengths of all geometries in this chunk.

!!! note

    Length is currently computed in the WGS84 coordinate system, so it should only be used as a heuristic.

#### sum\_area\_utm

The sum of all geometries&#x27; area in UTM

#### sum\_length\_utm

The sum of all geometries&#x27; length in UTM

#### num\_coords

The sum of the number of coordinates among all geometries in this chunk.

#### num\_rows

The number of rows in this chunk

#### to\_box

```python
def to_box() -> shapely.Polygon
```

Returns a Shapely polygon representing the bounding box of this chunk

## Chunk Objects

```python
class Chunk(BaseModel)
```

#### data

The data object contained within this chunk.

This will either be a [`pandas.DataFrame`][pandas.DataFrame],
[`geopandas.GeoDataFrame`][geopandas.GeoDataFrame], or
[`pyarrow.Table`][pyarrow.Table], depending on the type of user-defined function in
use.

#### metadata

The [ChunkMetadata][fused.models.udf.common.ChunkMetadata] describing this chunk.


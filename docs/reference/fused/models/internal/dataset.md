---
sidebar_label: dataset
title: fused.models.internal.dataset
---

## SampleStrategy Objects

```python
class SampleStrategy(str, Enum)
```

How to generate output samples

## EMPTY

Do not generate a sample

## FIRST\_CHUNK

The sample is from the first chunk

## GEO

Geographically sample

## DatasetOutputType Objects

```python
class DatasetOutputType(str, Enum)
```

## V2

Save as a table to a URL

## DatasetOutputBase Objects

```python
class DatasetOutputBase(BaseModel)
```

## save\_index

Whether to override saving the output index.

## sample\_strategy

How to generate output samples, or None for the default.

## overwrite

Whether the API should overwrite the output dataset if it already exists.

## DatasetOutputV2 Objects

```python
class DatasetOutputV2(DatasetOutputBase)
```

Output that writes a table to a URL

## url

Table URL to write to

## table

```python
@property
def table() -> Optional[str]
```

Returns the table name for this output

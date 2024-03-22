---
sidebar_label: dataset
title: fused.models.internal.dataset
---

## DatasetInput Objects

```python
class DatasetInput(DatasetInputBase)
```

(Deprecated) A class to describe a dataset to be used in a join or map operation

#### base\_path

The base path of the input dataset.

#### tables

The list of table names to fetch in the operation.

#### cache\_locally

Whether to cache all files from the input locally.

#### read\_sidecar\_files

Whether to read sidecar files from the input as part of the operation.

#### first\_n

Process only the first N files of the dataset. This is for debugging and benchmarking purposes.

Note that this can produce output tables that are missing files.

#### file\_sort\_field

When processing files, use this field on the metadata table to sort the files

## DatasetInputType Objects

```python
class DatasetInputType(str, Enum)
```

#### V2

Zip or Union operation

## DatasetInputV2Type Objects

```python
class DatasetInputV2Type(str, Enum)
```

#### ZIP

Append column-wise within partitions

#### UNION

Append partitions

## DatasetInputV2 Objects

```python
class DatasetInputV2(DatasetInputBase, FusedProjectAware)
```

#### first\_n

Process only the first N files of the dataset. This is for debugging and benchmarking purposes.

Note that this can produce output tables that are missing files.

#### file\_sort\_field

When processing files, use this field on the metadata table to sort the files

#### from\_table\_url

```python
@classmethod
def from_table_url(cls,
                   url: str,
                   *,
                   cache_locally: bool = False) -> DatasetInputV2
```

Create a DatasetInputV2 that reads a single table from a URL.

#### show

```python
def show(dataset_config: Optional[Union[Dict[str, Any], VizConfig]] = None,
         **kwargs) -> str
```

Visualize the input

**Arguments**:

- `dataset_config` - Customization of how to load and display the dataset.
- `**kwargs` - Will be passed through to the underlying API viz method.

## SampleStrategy Objects

```python
class SampleStrategy(str, Enum)
```

How to generate output samples

#### EMPTY

Do not generate a sample

#### FIRST\_CHUNK

The sample is from the first chunk

#### GEO

Geographically sample

## DatasetOutputType Objects

```python
class DatasetOutputType(str, Enum)
```

#### V2

Save as a table to a URL

## DatasetOutputBase Objects

```python
class DatasetOutputBase(BaseModel)
```

#### save\_index

Whether to override saving the output index.

#### sample\_strategy

How to generate output samples, or None for the default.

#### overwrite

Whether the API should overwrite the output dataset if it already exists.

## DatasetOutput Objects

```python
class DatasetOutput(DatasetOutputBase)
```

(Deprecated) Output that writes a table to a dataset

## DatasetOutputV2 Objects

```python
class DatasetOutputV2(DatasetOutputBase, FusedProjectAware)
```

Output that writes a table to a URL

#### url

Table URL to write to

#### to\_v1

```python
def to_v1() -> DatasetOutput
```

Converts this output object to a DatasetOutput (V1)

#### table

```python
@property
def table() -> Optional[str]
```

Returns the table name for this output


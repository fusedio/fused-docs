---
sidebar_label: job
title: fused.models.api.job
---

#### SYSTEM\_PARAMETER\_NAMES

Parameter names that will be provided by the Fused system

## JobStepConfig Objects

```python
class JobStepConfig(FusedBaseModel)
```

#### ignore\_chunk\_error

If `True`, continue processing even if some computations throw errors.

#### run\_remote

```python
def run_remote(output_table: Optional[str] = ...,
               instance_type: Optional[WHITELISTED_INSTANCE_TYPES] = None,
               *,
               region: str | None = None,
               disk_size_gb: int | None = None,
               additional_env: List[str] | None = None,
               image_name: Optional[str] = None,
               ignore_no_udf: bool = False,
               ignore_no_output: bool = False,
               validate_imports: Optional[bool] = None,
               overwrite: Optional[bool] = None) -> RunResponse
```

Execute this operation

**Arguments**:

- `output_table` - The name of the table to write to. Defaults to None.
- `instance_type` - The AWS EC2 instance type to use for the job. Acceptable strings are &quot;m5.large&quot;, &quot;m5.xlarge&quot;, &quot;m5.2xlarge&quot;, &quot;m5.4xlarge&quot;, &quot;r5.large&quot;, &quot;r5.xlarge&quot;, &quot;r5.2xlarge&quot;, &quot;r5.4xlarge&quot;. Defaults to None.
- `region` - The AWS region in which to run. Defaults to None.
- `disk_size_gb` - The disk size to specify for the job. Defaults to None.
- `additional_env` - Any additional environment variables to be passed into the job. Defaults to None.
- `image_name` - Custom image name to run. Defaults to None for default image.
  
- `ignore_no_udf` - Ignore validation errors about not specifying a UDF. Defaults to False.
- `ignore_no_output` - Ignore validation errors about not specifying output location. Defaults to False.

#### set\_output

```python
def set_output(table_or_url: Optional[str] = None,
               *,
               table: Optional[str] = None,
               url: Optional[str] = None,
               inplace: bool = False,
               overwrite: Optional[bool] = None) -> JobStepConfig
```

Update output tables on this operation

**Arguments**:

- `table_or_url` - Automatically set either `table` or `url` depending on whether this is a URL.
  

**Arguments**:

- `table` - The name of the table to use for output. This table name must be unique. Defaults to None.
- `url` - If set, the URL to write the table to. Overrides `table` and `base_path`.
- `inplace` - If True, modify and return this object. If False, modify and return a copy. Defaults to False.
- `overwrite` - If True, overwrite the output dataset if it already exists. Defaults to None to not update.
  

**Returns**:

  _description_

## PartitionJobStepConfig Objects

```python
class PartitionJobStepConfig(JobStepConfig)
```

Base class for partitioner steps (should not be instantiated directly)

#### input

The path to the input file(s) for partitioning.

#### output

Base path of the main output directory

#### output\_metadata

Base path of the fused output directory

#### partitioning\_maximum\_per\_file

Maximum value for `partitioning_method` to use per file. If `None`, defaults to _1/10th_ of the total value of `partitioning_method`. So if the value is `None` and `partitioning_method` is `"area"`, then each file will be have no more than 1/10th the total area of all geometries.

#### partitioning\_maximum\_per\_chunk

Maximum value for `partitioning_method` to use per chunk. If `None`, defaults to _1/100th_ of the total value of `partitioning_method`. So if the value is `None` and `partitioning_method` is `"area"`, then each file will be have no more than 1/100th the total area of all geometries.

## GDALOpenConfig Objects

```python
class GDALOpenConfig(BaseModel)
```

A class to define options for how to open files with GDAL.

#### open\_options

A dictionary of options passed in to GDAL for opening files.

#### layer

The layer of the input file to read from.

## GeospatialPartitionJobStepConfig Objects

```python
class GeospatialPartitionJobStepConfig(PartitionJobStepConfig)
```

#### drop\_out\_of\_bounds

Whether to drop points that are outside of the WGS84 valid bounds.

#### lonlat\_cols

Names of longitude, latitude columns to construct point geometries from.

This currently applies only to loading Parquet files.

If the original files are in a format such as CSV, pass the names of the longitude
and latitude columns in the GDALOpenConfig. If you pass those to GDALOpenConfig, do
not also pass names to lonlat_columns here.

#### partitioning\_method

The method used for deciding how to group geometries.

#### subdivide\_start

Geometries with greater area than this (in WGS84 degrees) will be subdivided.
Start area should be greater than or equal to stop area.

#### subdivide\_stop

This is the area that will stop continued subdivision of a geometry.
Stop area should be less than or equal to start area. Additionally stop area cannot
be zero, as that would cause infinite subdivision.

#### split\_identical\_centroids

Whether to split a partition that has identical centroids (such as if all geometries
in the partition are the same) if there are more such rows than defined in
&quot;partitioning_maximum_per_file&quot; and &quot;partitioning_maximum_per_chunk&quot;.

#### target\_num\_chunks

The target for the number of chunks if partitioning_maximum_per_file is None.

#### gdal\_config

Options to pass to GDAL for opening files.

#### run\_remote

```python
def run_remote(output_table: Optional[str] = ...,
               instance_type: Optional[WHITELISTED_INSTANCE_TYPES] = None,
               *,
               region: str | None = None,
               disk_size_gb: int | None = None,
               additional_env: List[str] | None = None,
               image_name: Optional[str] = None,
               ignore_no_udf: bool = False,
               ignore_no_output: bool = False,
               validate_imports: Optional[bool] = None,
               overwrite: Optional[bool] = None) -> RunResponse
```

Execute this operation

**Arguments**:

- `output_table` - The name of the table to write to. Defaults to None.
- `instance_type` - The AWS EC2 instance type to use for the job. Acceptable strings are &quot;m5.large&quot;, &quot;m5.xlarge&quot;, &quot;m5.2xlarge&quot;, &quot;m5.4xlarge&quot;, &quot;r5.large&quot;, &quot;r5.xlarge&quot;, &quot;r5.2xlarge&quot;, &quot;r5.4xlarge&quot;. Defaults to None.
- `region` - The AWS region in which to run. Defaults to None.
- `disk_size_gb` - The disk size to specify for the job. Defaults to None.
- `additional_env` - Any additional environment variables to be passed into the job. Defaults to None.
- `image_name` - Custom image name to run. Defaults to None for default image.
  
- `ignore_no_udf` - Ignore validation errors about not specifying a UDF. Defaults to False.
- `ignore_no_output` - Ignore validation errors about not specifying output location. Defaults to False.

## UdfJobStepConfig Objects

```python
class UdfJobStepConfig(JobStepConfig)
```

A job step of running a UDF.

#### set\_input

```python
def set_input(input: Optional[List[Any]],
              inplace: bool = False) -> UdfJobStepConfig
```

Set the input datasets on this operation

**Arguments**:

- `input` - A list of JSON-serializable objects to pass as input to the UDF, or None to run once with no arguments.
- `inplace` - If True, modify and return this object. If False, modify and return a copy. Defaults to False.

#### set\_udf

```python
def set_udf(udf: BaseUdf | dict | str,
            parameters: Optional[Dict[str, Any]] = None,
            replace_parameters: bool = False,
            inplace: bool = False) -> UdfJobStepConfig
```

Set a user-defined function on this operation

**Arguments**:

- `udf` - the representation of this UDF
- `parameters` - Parameters to set on the UDF. Defaults to None to not set parameters.
- `replace_parameters` - If True, unset any parameters not passed in parameters. Defaults to False.
- `inplace` - If True, modify and return this object. If False, modify and return a copy. Defaults to False.

#### run\_local

```python
def run_local(sample: Any | None = ...,
              validate_output: bool = False,
              validate_imports: Optional[bool] = None,
              **kwargs) -> UdfEvaluationResult
```

Run a UDF locally on sample data.

**Arguments**:

- `sample` - The sample input to pass to the UDF. Defaults to None.
- `validate_output` - If True, the output of the UDF is validated and schema is updated. If False,
  the output is returned as-is. Defaults to False.
- `**kwargs` - Additional keyword arguments to be passed to the UDF.
  

**Returns**:

  The output of the user-defined function (UDF) applied to the input data.
  

**Raises**:

  Any exceptions raised by the user-defined function (UDF) during its execution.

## MapJobStepConfig Objects

```python
class MapJobStepConfig(JobStepConfig)
```

#### udf

The UDF to run on this operation.

#### input

The dataset to map over.

#### output

How to save the map operation.

#### input\_metadata

```python
@property
def input_metadata() -> DatasetInputBase
```

Access the input metadata.

#### set\_input

```python
def set_input(input: Optional[CoerceableToDatasetInput] = None,
              *,
              inplace: bool = False) -> MapJobStepConfig
```

Set the input tables on this operation

**Arguments**:

- `input` - Input to read.
  

**Arguments**:

- `inplace` - If True, modify and return this object. If False, modify and return a copy. Defaults to False.

#### set\_udf

```python
def set_udf(udf: BaseUdf | dict | str,
            parameters: Optional[Dict[str, Any]] = None,
            replace_parameters: bool = False,
            inplace: bool = False) -> MapJobStepConfig
```

Set a user-defined function on this operation

**Arguments**:

- `udf` - the representation of this UDF
- `parameters` - Parameters to set on the UDF. Defaults to None to not set parameters.
- `replace_parameters` - If True, unset any parameters not passed in parameters. Defaults to False.
- `inplace` - If True, modify and return this object. If False, modify and return a copy. Defaults to False.

#### open\_output

```python
def open_output(**kwargs) -> Table
```

Opens the output of this operation

**Arguments**:

- `kwargs` - Additional arguments to pass to open
  

**Returns**:

  The Table that was generated by this operation

#### get\_sample

```python
def get_sample(file_id: str | int | None = None,
               chunk_id: int | None = None,
               n_rows: int | None = None,
               use_cache: bool = True) -> MapInput
```

Fetch a sample of this operation

**Arguments**:

- `file_id` - The identifier of this file. Defaults to None.
- `chunk_id` - The numeric index of the chunk within the file to fetch. Defaults to None.
- `n_rows` - The maximum number of rows to sample. Defaults to None for all rows in the chunk.
- `use_cache` - If True, use a cached sample if available. Defaults to True.
  

**Returns**:

  
  Sample data retrieved from the given file and chunk.

#### run\_local

```python
def run_local(file_id: str | int | None = None,
              chunk_id: int | None = None,
              n_rows: int | None = None,
              sample: MapInput | None = None,
              validate_output: bool = True,
              validate_imports: Optional[bool] = None,
              use_cache: bool = True,
              **kwargs) -> UdfEvaluationResult
```

Run a UDF locally on sample data.

**Arguments**:

- `file_id` _str or int or None, optional_ - Identifier for the file containing the data.
  Defaults to None, in which case a file is automatically chosen.
- `chunk_id` _int or None, optional_ - Identifier for the specific chunk of data within the file.
  Defaults to None, in which case a chunk is automatically chosen.
- `n_rows` - The maximum number of rows to sample from the left dataset. Defaults to None for all rows in the chunk.
- `sample` - If sample is passed, it is used instead of retrieving a sample.
- `validate_output` - If True, the output of the UDF is validated and schema is updated. If False,
  the output is returned as-is. Defaults to True.
- `use_cache` - If True, use a cached sample if available. Defaults to True.
- `**kwargs` - Additional keyword arguments to be passed to the UDF.
  

**Returns**:

  The output of the user-defined function (UDF) applied to the input data.
  

**Raises**:

  Any exceptions raised by the user-defined function (UDF) during its execution.

#### get\_output\_chunk

```python
def get_output_chunk(
    file_id: str | int | None = None,
    chunk_id: int | None = None
) -> Union[pa.Table, pd.DataFrame, gpd.GeoDataFrame]
```

Fetch a sample of the output of this operation

**Arguments**:

- `file_id` - The identifier of this file. Defaults to None.
- `chunk_id` - The numeric index of the chunk within the file to fetch. Defaults to None.
  

**Returns**:

  Sample data retrieved from the given file and chunk.

#### show

```python
def show(dataset_config: Optional[Union[Dict[str, Any], VizConfig]] = None,
         **kwargs) -> str
```

Visualize the map operation

**Arguments**:

- `dataset_config` - Customization of how to load and display the dataset.
- `**kwargs` - Will be passed through to the underlying API viz method.

## JoinJobStepConfig Objects

```python
class JoinJobStepConfig(JobStepConfig)
```

#### set\_input

```python
def set_input(input_left: Optional[CoerceableToDatasetInput] = None,
              input_right: Optional[CoerceableToDatasetInput] = None,
              *,
              inplace: bool = False) -> JoinJobStepConfig
```

Set the input tables on this operation

**Arguments**:

- `input_left` - The new left input
- `input_right` - The new right input
  

**Arguments**:

- `inplace` - If True, modify and return this object. If False, modify and return a copy. Defaults to False.

#### set\_udf

```python
def set_udf(udf: BaseUdf | dict | str,
            parameters: Optional[Dict[str, Any]] = None,
            replace_parameters: bool = False,
            inplace: bool = False) -> JoinJobStepConfig
```

Set a user-defined function on this operation

**Arguments**:

- `udf` - the representation of this UDF
- `parameters` - Parameters to set on the UDF. Defaults to None to not set parameters.
- `replace_parameters` - If True, unset any parameters not passed in parameters. Defaults to False.
- `inplace` - If True, modify and return this object. If False, modify and return a copy. Defaults to False.

#### open\_output

```python
def open_output(**kwargs) -> Table
```

Opens the output of this operation

**Arguments**:

- `kwargs` - Additional arguments to pass to open
  

**Returns**:

  The Table that was generated by this operation

#### get\_sample

```python
def get_sample(file_id: str | int | None = None,
               chunk_id: int | None = None,
               n_rows: int | None = None,
               use_cache: bool = True) -> JoinInput
```

Fetch a sample of this operation

**Arguments**:

- `file_id` - The identifier of this file. Defaults to None.
- `chunk_id` - The numeric index of the chunk within the file to fetch. Defaults to None.
- `n_rows` - The maximum number of rows to sample from the left dataset. Defaults to None for all rows in the chunk.
- `use_cache` - If True, use a cached sample if available. Defaults to True.
  

**Returns**:

  
  Sample data retrieved from the given file and chunk.

#### run\_local

```python
def run_local(file_id: str | int | None = None,
              chunk_id: int | None = None,
              n_rows: int | None = None,
              sample: JoinInput | None = None,
              validate_output: bool = True,
              validate_imports: Optional[bool] = None,
              use_cache: bool = True,
              **kwargs) -> UdfEvaluationResult
```

Run a UDF locally on sample data.

**Arguments**:

- `file_id` _str or int or None, optional_ - Identifier for the file containing the data.
  Defaults to None, in which case a file is automatically chosen.
- `chunk_id` _int or None, optional_ - Identifier for the specific chunk of data within the file.
  Defaults to None, in which case a chunk is automatically chosen.
- `n_rows` - The maximum number of rows to sample from the left dataset. Defaults to None for all rows in the chunk.
- `sample` - If sample is passed, it is used instead of retrieving a sample.
- `validate_output` - If True, the output of the UDF is validated and schema is updated. If False,
  the output is returned as-is. Defaults to True.
- `use_cache` - If True, use a cached sample if available. Defaults to True.
- `**kwargs` - Additional keyword arguments to be passed to the UDF.
  

**Returns**:

  The output of the user-defined function (UDF) applied to the input data.
  

**Raises**:

  Any exceptions raised by the user-defined function (UDF) during its execution.

#### get\_output\_chunk

```python
def get_output_chunk(
    file_id: str | int | None = None,
    chunk_id: int | None = None
) -> Union[pa.Table, pd.DataFrame, gpd.GeoDataFrame]
```

Fetch a sample of the output of this operation

**Arguments**:

- `file_id` - The identifier of this file. Defaults to None.
- `chunk_id` - The numeric index of the chunk within the file to fetch. Defaults to None.
  

**Returns**:

  Sample data retrieved from the given file and chunk.

#### show

```python
def show(dataset_config_left: Optional[Union[Dict[str, Any],
                                             VizConfig]] = None,
         dataset_config_right: Optional[Union[Dict[str, Any],
                                              VizConfig]] = None,
         app_config: Optional[Union[Dict[str, Any], VizAppConfig]] = None,
         **kwargs) -> str
```

Visualize the join operation

**Arguments**:

- `dataset_config_left` - Customization of how to load and display the left dataset.
- `dataset_config_right` - Customization of how to load and display the right dataset.
- `app_config` - Customization of the app.
- `**kwargs` - Will be passed through to the underlying API show method.

## JoinSinglefileJobStepConfig Objects

```python
class JoinSinglefileJobStepConfig(JobStepConfig)
```

#### set\_input

```python
def set_input(input_left: Optional[CoerceableToDatasetInput] = None,
              input_right: Optional[str] = None,
              *,
              inplace: bool = False) -> JoinSinglefileJobStepConfig
```

Set the input tables on this operation

All arguments except for input_right apply to the left dataset.

**Arguments**:

- `input_left` - URL of the left table to read.
- `input_right` - URL of the right dataset file. Defaults to None for no update.
  

**Arguments**:

- `inplace` - If True, modify and return this object. If False, modify and return a copy. Defaults to False.

#### set\_udf

```python
def set_udf(udf: BaseUdf | dict | str,
            parameters: Optional[Dict[str, Any]] = None,
            replace_parameters: bool = False,
            inplace: bool = False) -> JoinSinglefileJobStepConfig
```

Set a user-defined function on this operation

**Arguments**:

- `udf` - the representation of this UDF
- `parameters` - Parameters to set on the UDF. Defaults to None to not set parameters.
- `replace_parameters` - If True, unset any parameters not passed in parameters. Defaults to False.
- `inplace` - If True, modify and return this object. If False, modify and return a copy. Defaults to False.

#### open\_output

```python
def open_output(**kwargs) -> Table
```

Opens the output of this operation

**Arguments**:

- `kwargs` - Additional arguments to pass to open
  

**Returns**:

  The Table that was generated by this operation

#### get\_sample

```python
def get_sample(file_id: str | int | None = None,
               chunk_id: int | None = None,
               n_rows: int | None = None,
               use_cache: bool = True) -> JoinSingleFileInput
```

Fetch a sample of this operation

**Arguments**:

- `file_id` - The identifier of this file. Defaults to None.
- `chunk_id` - The numeric index of the chunk within the file to fetch. Defaults to None.
- `n_rows` - The maximum number of rows to sample from the left dataset. Defaults to None for all rows in the chunk.
- `use_cache` - If True, use a cached sample if available. Defaults to True.
  

**Returns**:

  
  Sample data retrieved from the given file and chunk.

#### run\_local

```python
def run_local(file_id: str | int | None = None,
              chunk_id: int | None = None,
              n_rows: int | None = None,
              sample: JoinSingleFileInput | None = None,
              validate_output: bool = True,
              validate_imports: Optional[bool] = None,
              use_cache: bool = True,
              **kwargs) -> UdfEvaluationResult
```

Run a UDF locally on sample data.

**Arguments**:

- `file_id` _str or int or None, optional_ - Identifier for the file containing the data.
  Defaults to None, in which case a file is automatically chosen.
- `chunk_id` _int or None, optional_ - Identifier for the specific chunk of data within the file.
  Defaults to None, in which case a chunk is automatically chosen.
- `n_rows` - The maximum number of rows to sample from the left dataset. Defaults to None for all rows in the chunk.
- `sample` - If sample is passed, it is used instead of retrieving a sample.
- `validate_output` - If True, the output of the UDF is validated and schema is updated. If False,
  the output is returned as-is. Defaults to True.
- `use_cache` - If True, use a cached sample if available. Defaults to True.
- `**kwargs` - Additional keyword arguments to be passed to the UDF.
  

**Returns**:

  The output of the user-defined function (UDF) applied to the input data.
  

**Raises**:

  Any exceptions raised by the user-defined function (UDF) during its execution.

#### get\_output\_chunk

```python
def get_output_chunk(
    file_id: str | int | None = None,
    chunk_id: int | None = None
) -> Union[pa.Table, pd.DataFrame, gpd.GeoDataFrame]
```

Fetch a sample of the output of this operation

**Arguments**:

- `file_id` - The identifier of this file. Defaults to None.
- `chunk_id` - The numeric index of the chunk within the file to fetch. Defaults to None.
  

**Returns**:

  Sample data retrieved from the given file and chunk.

#### show

```python
def show(dataset_config: Optional[Union[Dict[str, Any], VizConfig]] = None,
         **kwargs) -> str
```

Visualize the operation

**Arguments**:

- `dataset_config` - Customization of how to load and display the dataset.
- `**kwargs` - Will be passed through to the underlying API viz method.

## JobConfig Objects

```python
class JobConfig(FusedBaseModel)
```

#### name

The name of the job.

#### steps

The individual steps to run in sequence in the job.

#### metadata

User defined metadata. Any metadata values must be JSON serializable.

#### run\_remote

```python
def run_remote(instance_type: Optional[WHITELISTED_INSTANCE_TYPES] = None,
               *,
               region: str | None = None,
               disk_size_gb: int | None = None,
               additional_env: List[str] | None = None,
               image_name: Optional[str] = None,
               ignore_no_udf: bool = False,
               ignore_no_output: bool = False,
               validate_imports: Optional[bool] = None,
               **kwargs) -> RunResponse
```

Execute an operation

**Arguments**:

- `region` - The AWS region in which to run. Defaults to None.
- `instance_type` - The AWS EC2 instance type to use for the job. Acceptable strings are &quot;m5.large&quot;, &quot;m5.xlarge&quot;, &quot;m5.2xlarge&quot;, &quot;m5.4xlarge&quot;, &quot;r5.large&quot;, &quot;r5.xlarge&quot;, &quot;r5.2xlarge&quot;, &quot;r5.4xlarge&quot;. Defaults to None.
- `disk_size_gb` - The disk size to specify for the job. Defaults to None.
- `additional_env` - Any additional environment variables to be passed into the job, each in the form KEY=value. Defaults to None.
- `image_name` - Custom image name to run. Defaults to None for default image.


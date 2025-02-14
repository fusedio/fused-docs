---
sidebar_label: schema
title: models.schema
toc_max_heading_level: 5
unlisted: true
---

## BaseDataType Objects

```python
class BaseDataType()
```

A base class for Fused DataType objects

## GeoArrowWKB Objects

```python
class GeoArrowWKB(pa.ExtensionType)
```

A PyArrow extension type to store the &quot;geoarrow.wkb&quot; name on a binary column.

## PrimitiveDataType Objects

```python
class PrimitiveDataType(BaseDataType, str, Enum)
```

An enumeration of data types that can be used in columns.

#### Geometry

WKB-encoded geometry as a Binary DataType

#### to\_arrow

```python
def to_arrow() -> pa.DataType
```

Convert this type to a [`pyarrow.DataType`][pyarrow.DataType].

#### from\_arrow

```python
@classmethod
def from_arrow(cls, dtype: pa.DataType) -> PrimitiveDataType
```

Construct this from a [`pyarrow.DataType`][pyarrow.DataType].

#### from\_numpy\_type\_class

```python
@classmethod
def from_numpy_type_class(cls, dtype: Type[np.generic]) -> PrimitiveDataType
```

Construct this from a [`numpy.generic`][numpy.generic] instance.

#### from\_numpy\_type

```python
@classmethod
def from_numpy_type(cls, dtype: np.generic) -> PrimitiveDataType
```

Construct this from a [`numpy.generic`][numpy.generic] instance.

#### from\_numpy\_dtype

```python
@classmethod
def from_numpy_dtype(cls, dtype: np.dtype) -> PrimitiveDataType
```

Construct this from a [`numpy.dtype`][numpy.dtype] instance.

#### from\_pandas\_type

```python
@classmethod
def from_pandas_type(
        cls, dtype: "pd.api.extensions.ExtensionDtype") -> PrimitiveDataType
```

Construct this from a [pandas dtype][pandas.api.extensions.ExtensionDtype] instance.

## TimestampType Objects

```python
class TimestampType(BaseDataType, BaseModel)
```

#### from\_string

```python
@classmethod
def from_string(cls, s: str) -> TimestampType
```

Parse from a string type description

**Examples**:

    ```py
    s = "Timestamp[ms]"
    TimestampType.from_string(s)
    ```
  
    ```py
    s = "Timestamp[ms, America/New_York]"
    TimestampType.from_string(s)
    ```

## ListType Objects

```python
class ListType(BaseDataType, BaseModel)
```

#### from\_string

```python
@classmethod
def from_string(cls, s: str) -> ListType
```

Parse from a string type description

**Examples**:

    ```py
    s = "List[Float32]"
    ListType.from_string(s)
    ```

## LargeListType Objects

```python
class LargeListType(BaseDataType, BaseModel)
```

#### from\_string

```python
@classmethod
def from_string(cls, s: str) -> LargeListType
```

Parse from a string type description

**Examples**:

    ```py
    s = "LargeList[Uint8]"
    LargeListType.from_string(s)
    ```

## FixedSizeListType Objects

```python
class FixedSizeListType(BaseDataType, BaseModel)
```

#### from\_string

```python
@classmethod
def from_string(cls, s: str) -> FixedSizeListType
```

Parse from a string type description

There should be two items in the bracket. The first should be the inner type.
The second should be the number of inner elements of the fixed size list.

**Examples**:

    ```py
    s = "FixedSizeList[Uint8, 4]"
    FixedSizeListType.from_string(s)
    ```

## FixedSizeBinaryType Objects

```python
class FixedSizeBinaryType(BaseDataType, BaseModel)
```

#### from\_string

```python
@classmethod
def from_string(cls, s: str) -> FixedSizeBinaryType
```

Parse from a string type description

**Examples**:

    ```py
    s = "FixedSizeBinary[4]"
    FixedSizeBinaryType.from_string(s)
    ```

#### data\_type\_from\_arrow

```python
def data_type_from_arrow(dtype: pa.DataType) -> DataType
```

Construct this from a [`pyarrow.DataType`][pyarrow.DataType].

#### data\_type\_from\_string

```python
def data_type_from_string(s: str) -> DataType
```

Construct DataType from a string representation

## Field Objects

```python
class Field(BaseModel)
```

A description of a single column in a table.

#### name

The name of the column.

#### type

The [data type][fused.models.DataType] of this column.

#### nullable

Whether the column can have null values.

#### metadata

Optional metadata describing the column.

#### to\_arrow

```python
def to_arrow() -> pa.Field
```

Convert this to a [`pyarrow.Field`][pyarrow.Field].

#### from\_arrow

```python
@classmethod
def from_arrow(cls, field: pa.Field) -> Field
```

Construct this from a [`pyarrow.Field`][pyarrow.Field].

## Schema Objects

```python
class Schema(BaseModel)
```

A description of a table schema.

!!! info

    This schema mirrors the definition of a [`pyarrow.Schema`][pyarrow.Schema]
    object.

#### fields

A list of [`fields`][fused.models.Field] describing the columns in this table.

The ordering of the field descriptors must match the actual ordering of the columns
in the table.

#### metadata

Optional metadata describing the table.

#### to\_arrow

```python
def to_arrow() -> pa.Schema
```

Convert this to a [`pyarrow.Schema`][pyarrow.Schema].

#### empty

```python
@classmethod
def empty(cls) -> Schema
```

Returns a Schema with no fields.

#### is\_empty

```python
@property
def is_empty() -> bool
```

True if this schema has no fields and no metadata.

#### from\_arrow

```python
@classmethod
def from_arrow(cls, schema: pa.Schema) -> Schema
```

Construct this from a [`pyarrow.Schema`][pyarrow.Schema].

#### from\_dataframe

```python
@classmethod
def from_dataframe(cls, df: Union["pd.DataFrame",
                                  "gpd.GeoDataFrame"]) -> Schema
```

Infer a schema from a [`pandas.DataFrame`][pandas.DataFrame].

#### from\_dict

```python
@classmethod
def from_dict(cls, d: Dict[str, Any]) -> Schema
```

Create a schema from a key-value dictionary.

**Returns**:

  A Schema object
  

**Examples**:

    ```py
    columns = {
        'column1': np.uint8,
        'column2': str,
    }
    schema = Schema.from_dict(columns)
    ```

#### from\_parquet

```python
@classmethod
def from_parquet(cls, file: Union[str, Path, IO[bytes]]) -> Schema
```

Construct a Schema from a Parquet file

**Arguments**:

- `file` - Parquet file to parse as schema.
  

**Returns**:

  Schema inferred from Parquet file

#### from\_string

```python
@classmethod
def from_string(cls, str: str) -> Schema
```

Parse a schema from a string, which may be in several forms.

The string may either contain JSON, or a &quot;command-line&quot; form of specifying a schema
where fields are specified as `name:type`, like so: `field1:Int32 field2:List[String]`

```
column1:String column2:Float64
```

Nested types can be defined using square bracket syntax, where the nested type is inside the outer type.
For example, a list of strings:

```
column1:List[String]
```

A list of uint8s where each list has exactly two elements:

```
"column2:FixedSizeList[Uint8, 2]"
```

A list of floats with capacity of &gt; 2^32 elements:

```
column3:LargeList[Float64]
```

4 bytes per element:

```
column4:FixedSizeBinary[4]
```

A timestamp stored as seconds:

```
column5:Timestamp[s]
```

A timestamp stored as seconds, with timezone:

```
"column6:Timestamp[s, America/New_York]"
```


#### to\_string

```python
def to_string() -> str
```

Returns a string form of this schema, which will be parseable by `from_string`.

#### update

```python
def update(other: Schema) -> Schema
```

Update this schema using fields from another schema.

Fields are updated by name from the other schema. The fields in this schema will
stay in the same order. All field names in the other schema must exist in this
schema.

**Arguments**:

- `other` - the schema with which to update this schema
  

**Returns**:

  A new Schema object

#### get\_field

```python
def get_field(name: str) -> Optional[Field]
```

Returns the field in this schema with the specified name, or None.

**Arguments**:

- `name` - The name of the field.
  

**Returns**:

  The Field object, or None if no field with that name was found.


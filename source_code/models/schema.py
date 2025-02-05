from __future__ import annotations

import inspect
import json
import re
import shlex
import warnings
from enum import Enum
from pathlib import Path
from typing import IO, TYPE_CHECKING, Any, Dict, List, Literal, Optional, Type, Union

if TYPE_CHECKING:
    import geopandas as gpd
    import pandas as pd

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
from pydantic import BaseModel
from pydantic import Field as PydanticField
from pydantic import StrictInt, field_validator

from fused._optional_deps import GPD_GEODATAFRAME, HAS_GEOPANDAS
from fused.warnings import FusedDefaultWarning, FusedReservedWarning, FusedWarning

INDEX_COLUMN_NAME = "fused_index"
GEOARROW_NAME = "geoarrow.wkb"


class BaseDataType:
    """A base class for Fused DataType objects"""

    pass


class GeoArrowWKB(pa.ExtensionType):
    """A PyArrow extension type to store the "geoarrow.wkb" name on a binary column."""

    # This is derived from docs here:
    # https://arrow.apache.org/docs/python/generated/pyarrow.ExtensionType.html
    def __init__(self):
        pa.ExtensionType.__init__(self, pa.binary(), GEOARROW_NAME)

    def __arrow_ext_serialize__(self):
        # since we don't have a parameterized type, we don't need extra
        # metadata to be deserialized
        return b""

    @classmethod
    def __arrow_ext_deserialize__(self, storage_type, serialized):
        # return an instance of this subclass given the serialized
        # metadata.
        return GeoArrowWKB()


try:
    pa.register_extension_type(GeoArrowWKB())
except pa.ArrowKeyError:
    pass


class PrimitiveDataType(BaseDataType, str, Enum):
    """An enumeration of data types that can be used in columns."""

    Null = "null"
    Bool = "Bool"
    Int8 = "Int8"
    Int16 = "Int16"
    Int32 = "Int32"
    Int64 = "Int64"
    Uint8 = "Uint8"
    Uint16 = "Uint16"
    Uint32 = "Uint32"
    Uint64 = "Uint64"
    Float16 = "Float16"
    Float32 = "Float32"
    Float64 = "Float64"
    Date32 = "Date32"
    Date64 = "Date64"
    String = "String"
    LargeString = "LargeString"
    Binary = "Binary"
    LargeBinary = "LargeBinary"
    Geometry = "Geometry"
    """WKB-encoded geometry as a Binary DataType"""

    def __str__(self) -> str:
        return self.value

    def to_arrow(self) -> pa.DataType:
        """Convert this type to a [`pyarrow.DataType`][pyarrow.DataType]."""

        if self == PrimitiveDataType.Null:
            return pa.null()
        if self == PrimitiveDataType.Bool:
            return pa.bool_()
        if self == PrimitiveDataType.Int8:
            return pa.int8()
        if self == PrimitiveDataType.Int16:
            return pa.int16()
        if self == PrimitiveDataType.Int32:
            return pa.int32()
        if self == PrimitiveDataType.Int64:
            return pa.int64()
        if self == PrimitiveDataType.Uint8:
            return pa.uint8()
        if self == PrimitiveDataType.Uint16:
            return pa.uint16()
        if self == PrimitiveDataType.Uint32:
            return pa.uint32()
        if self == PrimitiveDataType.Uint64:
            return pa.uint64()
        if self == PrimitiveDataType.Float16:
            return pa.float16()
        if self == PrimitiveDataType.Float32:
            return pa.float32()
        if self == PrimitiveDataType.Float64:
            return pa.float64()
        if self == PrimitiveDataType.Date32:
            return pa.date32()
        if self == PrimitiveDataType.Date64:
            return pa.date64()
        if self == PrimitiveDataType.String:
            return pa.string()
        if self == PrimitiveDataType.LargeString:
            return pa.large_string()
        if self == PrimitiveDataType.Binary:
            return pa.binary()
        if self == PrimitiveDataType.LargeBinary:
            return pa.large_binary()
        if self == PrimitiveDataType.Geometry:
            return GeoArrowWKB()

        raise ValueError(f"unexpected type {self=}")

    @classmethod
    def from_arrow(cls, dtype: pa.DataType) -> PrimitiveDataType:
        """Construct this from a [`pyarrow.DataType`][pyarrow.DataType]."""
        if isinstance(dtype, pa.ExtensionType):
            if dtype.extension_name == GEOARROW_NAME:
                return cls.Geometry

            raise ValueError(f"Unknown extension type {dtype.extension_name}")

        if pa.types.is_null(dtype):
            return cls.Null
        if pa.types.is_boolean(dtype):
            return cls.Bool
        if pa.types.is_int8(dtype):
            return cls.Int8
        if pa.types.is_int16(dtype):
            return cls.Int16
        if pa.types.is_int32(dtype):
            return cls.Int32
        if pa.types.is_int64(dtype):
            return cls.Int64
        if pa.types.is_uint8(dtype):
            return cls.Uint8
        if pa.types.is_uint16(dtype):
            return cls.Uint16
        if pa.types.is_uint32(dtype):
            return cls.Uint32
        if pa.types.is_uint64(dtype):
            return cls.Uint64
        if pa.types.is_float16(dtype):
            return cls.Float16
        if pa.types.is_float32(dtype):
            return cls.Float32
        if pa.types.is_float64(dtype):
            return cls.Float64
        if pa.types.is_date32(dtype):
            return cls.Date32
        if pa.types.is_date64(dtype):
            return cls.Date64
        if pa.types.is_string(dtype):
            return cls.String
        if pa.types.is_large_string(dtype):
            return cls.LargeString
        if pa.types.is_binary(dtype):
            return cls.Binary
        if pa.types.is_large_binary(dtype):
            return cls.LargeBinary

        assert False, f"unimplemented type {dtype}"

    @classmethod
    def from_numpy_type_class(cls, dtype: Type[np.generic]) -> PrimitiveDataType:
        """Construct this from a [`numpy.generic`][numpy.generic] instance."""

        assert issubclass(
            dtype, np.generic
        ), f"Expected dtype to be a subclass of np.generic, got {dtype}"

        return cls.from_arrow(pa.from_numpy_dtype(dtype))

    @classmethod
    def from_numpy_type(cls, dtype: np.generic) -> PrimitiveDataType:
        """Construct this from a [`numpy.generic`][numpy.generic] instance."""

        assert isinstance(dtype, np.generic)
        return cls.from_arrow(pa.from_numpy_dtype(dtype))

    @classmethod
    def from_numpy_dtype(cls, dtype: np.dtype) -> PrimitiveDataType:
        """Construct this from a [`numpy.dtype`][numpy.dtype] instance."""

        assert isinstance(dtype, np.dtype)
        return cls.from_numpy_type_class(dtype.type)

    @classmethod
    def from_pandas_type(
        cls, dtype: "pd.api.extensions.ExtensionDtype"
    ) -> PrimitiveDataType:
        """Construct this from a [pandas dtype][pandas.api.extensions.ExtensionDtype] instance."""
        import pandas as pd

        pandas_df = pd.DataFrame({"col": pd.Series(dtype=dtype)})
        pyarrow_schema = pa.Schema.from_pandas(pandas_df, preserve_index=False)
        return cls.from_arrow(pyarrow_schema.field("col").type)

    @classmethod
    def from_python_type(cls, dtype: Type[object]) -> PrimitiveDataType:
        if dtype is float:
            return PrimitiveDataType.Float64

        if dtype is int:
            return PrimitiveDataType.Int64

        if dtype is str:
            return PrimitiveDataType.String

        if dtype is bool:
            return PrimitiveDataType.Bool

        raise TypeError(f"Expected {dtype} to be a builtin python type")


class TimestampType(BaseDataType, BaseModel):
    type: Literal["Timestamp"] = "Timestamp"
    unit: Literal["s", "ms", "us", "ns"]
    tz: Optional[str] = None

    def __str__(self) -> str:
        if self.tz is not None:
            return f"{self.type}[{self.unit}, {self.tz}]"

        return f"{self.type}[{self.unit}]"

    def to_arrow(self) -> pa.TimestampType:
        return pa.timestamp(unit=self.unit, tz=self.tz)

    @classmethod
    def from_arrow(cls, dtype: pa.TimestampType) -> TimestampType:
        return TimestampType(unit=dtype.unit, tz=dtype.tz)

    @classmethod
    def from_string(cls, s: str) -> TimestampType:
        """Parse from a string type description

        Examples:
            ```py
            s = "Timestamp[ms]"
            TimestampType.from_string(s)
            ```

            ```py
            s = "Timestamp[ms, America/New_York]"
            TimestampType.from_string(s)
            ```

        """
        start = "Timestamp["
        end = "]"
        assert s.startswith(start)
        assert s.endswith(end)
        inner_s = s[len(start) : -len(end)]
        split = inner_s.split(",", maxsplit=1)
        if len(split) == 1:
            unit = split[0]
            return TimestampType(unit=unit.strip())  # type: ignore

        else:
            assert len(split) == 2
            unit, tz = split
            return TimestampType(unit=unit.strip(), tz=tz.strip())  # type: ignore


class ListType(BaseDataType, BaseModel):
    type: Literal["List"] = "List"
    element_type: DataType

    def __str__(self) -> str:
        return f"{self.type}[{self.element_type}]"

    def to_arrow(self) -> pa.ListType:
        value_type = self.element_type.to_arrow()
        return pa.list_(value_type)

    @classmethod
    def from_arrow(cls, dtype: pa.ListType) -> ListType:
        return ListType(element_type=data_type_from_arrow(dtype.value_type))

    @classmethod
    def from_string(cls, s: str) -> ListType:
        """Parse from a string type description

        Examples:
            ```py
            s = "List[Float32]"
            ListType.from_string(s)
            ```
        """
        start = "List["
        end = "]"
        assert s.startswith(start)
        assert s.endswith(end)
        inner_s = s[len(start) : -len(end)]
        return ListType(element_type=data_type_from_string(inner_s))


class LargeListType(BaseDataType, BaseModel):
    type: Literal["LargeList"] = "LargeList"
    element_type: DataType

    def __str__(self) -> str:
        return f"{self.type}[{self.element_type}]"

    def to_arrow(self) -> pa.LargeListType:
        value_type = self.element_type.to_arrow()
        return pa.large_list(value_type)

    @classmethod
    def from_arrow(cls, dtype: pa.LargeListType) -> LargeListType:
        return LargeListType(element_type=data_type_from_arrow(dtype.value_type))

    @classmethod
    def from_string(cls, s: str) -> LargeListType:
        """Parse from a string type description

        Examples:
            ```py
            s = "LargeList[Uint8]"
            LargeListType.from_string(s)
            ```
        """
        start = "LargeList["
        end = "]"
        assert s.startswith(start)
        assert s.endswith(end)
        inner_s = s[len(start) : -len(end)]
        return LargeListType(element_type=data_type_from_string(inner_s))


class FixedSizeListType(BaseDataType, BaseModel):
    type: Literal["FixedSizeList"] = "FixedSizeList"
    element_type: DataType
    inner_size: StrictInt

    def __str__(self) -> str:
        return f"{self.type}[{self.element_type}, {self.inner_size}]"

    def to_arrow(self) -> pa.FixedSizeListType:
        value_type = self.element_type.to_arrow()
        return pa.list_(value_type, self.inner_size)

    @classmethod
    def from_arrow(cls, dtype: pa.FixedSizeListType) -> FixedSizeListType:
        return FixedSizeListType(
            element_type=data_type_from_arrow(dtype.value_type),
            inner_size=dtype.list_size,
        )

    @classmethod
    def from_string(cls, s: str) -> FixedSizeListType:
        """Parse from a string type description

        There should be two items in the bracket. The first should be the inner type.
        The second should be the number of inner elements of the fixed size list.

        Examples:
            ```py
            s = "FixedSizeList[Uint8, 4]"
            FixedSizeListType.from_string(s)
            ```
        """
        start = "FixedSizeList["
        end = "]"
        assert s.startswith(start)
        assert s.endswith(end)

        regex = r",\s*(\d+)\]$"
        match = re.search(regex, s)
        assert match
        inner_size = int(match.group(1))
        inner_str = s[len(start) : match.span(0)[0]]
        return FixedSizeListType(
            element_type=data_type_from_string(inner_str), inner_size=inner_size
        )


class FixedSizeBinaryType(BaseDataType, BaseModel):
    type: Literal["FixedSizeBinary"] = "FixedSizeBinary"
    byte_width: StrictInt

    def __str__(self) -> str:
        return f"{self.type}[{self.byte_width}]"

    def to_arrow(self) -> pa.FixedSizeBinaryType:
        return pa.binary(self.byte_width)

    @classmethod
    def from_arrow(cls, dtype: pa.FixedSizeBinaryType) -> FixedSizeBinaryType:
        return FixedSizeBinaryType(byte_width=dtype.byte_width)

    @classmethod
    def from_string(cls, s: str) -> FixedSizeBinaryType:
        """Parse from a string type description

        Examples:
            ```py
            s = "FixedSizeBinary[4]"
            FixedSizeBinaryType.from_string(s)
            ```
        """
        start = "FixedSizeBinary["
        end = "]"
        assert s.startswith(start)
        assert s.endswith(end)

        regex = r"^FixedSizeBinary\[(\d+)\]$"
        match = re.search(regex, s)
        assert match
        byte_width = int(match.group(1))
        return FixedSizeBinaryType(byte_width=byte_width)


class StructType(BaseDataType, BaseModel):
    type: Literal["Struct"] = "Struct"
    fields: List[Field]

    def to_arrow(self) -> pa.DataType:
        return pa.struct([field.to_arrow() for field in self.fields])

    @classmethod
    def from_arrow(cls, dtype: pa.DataType) -> StructType:
        parsed_fields: List[Field] = []
        for i in range(dtype.num_fields):
            parsed_fields.append(Field.from_arrow(dtype.field(i)))

        return StructType(fields=parsed_fields)

    @classmethod
    def from_string(cls, s: str) -> StructType:
        raise NotImplementedError

    def __str__(self) -> str:
        field_strs = [f"{field.name}:{field.type}" for field in self.fields]
        # We use a semicolon for structs to make parsing easier, since each internal
        # data type can have their own comma characters, and we don't know how many
        # struct fields will exist.
        inner_str = "; ".join(field_strs)
        return f"{self.type}[{inner_str}]"


DataType = Union[
    PrimitiveDataType,
    TimestampType,
    ListType,
    LargeListType,
    FixedSizeListType,
    FixedSizeBinaryType,
    StructType,
]


def data_type_from_arrow(dtype: pa.DataType) -> DataType:
    """Construct this from a [`pyarrow.DataType`][pyarrow.DataType]."""
    if isinstance(dtype, pa.ExtensionType):
        if dtype.extension_name == GEOARROW_NAME:
            return PrimitiveDataType.Geometry

        raise ValueError(f"Unknown extension type {dtype.extension_name}")

    if pa.types.is_null(dtype):
        return PrimitiveDataType.Null
    if pa.types.is_boolean(dtype):
        return PrimitiveDataType.Bool
    if pa.types.is_int8(dtype):
        return PrimitiveDataType.Int8
    if pa.types.is_int16(dtype):
        return PrimitiveDataType.Int16
    if pa.types.is_int32(dtype):
        return PrimitiveDataType.Int32
    if pa.types.is_int64(dtype):
        return PrimitiveDataType.Int64
    if pa.types.is_uint8(dtype):
        return PrimitiveDataType.Uint8
    if pa.types.is_uint16(dtype):
        return PrimitiveDataType.Uint16
    if pa.types.is_uint32(dtype):
        return PrimitiveDataType.Uint32
    if pa.types.is_uint64(dtype):
        return PrimitiveDataType.Uint64
    if pa.types.is_float16(dtype):
        return PrimitiveDataType.Float16
    if pa.types.is_float32(dtype):
        return PrimitiveDataType.Float32
    if pa.types.is_float64(dtype):
        return PrimitiveDataType.Float64
    if pa.types.is_date32(dtype):
        return PrimitiveDataType.Date32
    if pa.types.is_date64(dtype):
        return PrimitiveDataType.Date64
    if pa.types.is_string(dtype):
        return PrimitiveDataType.String
    if pa.types.is_large_string(dtype):
        return PrimitiveDataType.LargeString
    if pa.types.is_binary(dtype):
        return PrimitiveDataType.Binary
    if pa.types.is_large_binary(dtype):
        return PrimitiveDataType.LargeBinary
    if pa.types.is_timestamp(dtype):
        return TimestampType.from_arrow(dtype)
    if pa.types.is_list(dtype):
        return ListType.from_arrow(dtype)
    if pa.types.is_large_list(dtype):
        return LargeListType.from_arrow(dtype)
    if pa.types.is_fixed_size_list(dtype):
        return FixedSizeListType.from_arrow(dtype)
    if pa.types.is_fixed_size_binary(dtype):
        return FixedSizeBinaryType.from_arrow(dtype)
    if pa.types.is_struct(dtype):
        return StructType.from_arrow(dtype)

    # Hack: for now, cast decimal data types to float64
    if pa.types.is_decimal(dtype):
        return PrimitiveDataType.Float64

    warnings.warn(
        FusedDefaultWarning(f"unimplemented type {dtype}; defaulting to String")
    )
    # Cast default type to string??
    return PrimitiveDataType.String


def data_type_from_string(s: str) -> DataType:
    """Construct DataType from a string representation"""
    if s in ("str", "string"):
        return PrimitiveDataType.String

    try:
        return PrimitiveDataType(s)

    except ValueError:
        pass

    # If the string is not found in the PrimitiveDataType enum, first try to parse it
    # using numpy
    try:
        numpy_dtype = np.dtype(s)
        return PrimitiveDataType.from_numpy_dtype(np.dtype(numpy_dtype))
    except TypeError:
        pass

    if s.startswith("Timestamp"):
        return TimestampType.from_string(s)

    if s.startswith("List"):
        return ListType.from_string(s)

    if s.startswith("LargeList"):
        return LargeListType.from_string(s)

    if s.startswith("FixedSizeList"):
        return FixedSizeListType.from_string(s)

    if s.startswith("FixedSizeBinary"):
        return FixedSizeBinaryType.from_string(s)

    if s.startswith("Struct"):
        return StructType.from_string(s)

    raise ValueError(f"unimplemented type: {s}")


class Field(BaseModel):
    """A description of a single column in a table."""

    name: str
    """The name of the column."""

    type: DataType
    """The [data type][fused.models.DataType] of this column."""

    nullable: bool = True
    """Whether the column can have null values."""

    metadata: Optional[Dict[str, str]] = None
    """Optional metadata describing the column."""

    @field_validator("type")
    @classmethod
    def coerce_null_type_to_string(cls, v):
        if v == PrimitiveDataType.Null:
            return PrimitiveDataType.String

        return v

    def to_arrow(self) -> pa.Field:
        """Convert this to a [`pyarrow.Field`][pyarrow.Field]."""

        return pa.field(
            name=self.name,
            type=self.type.to_arrow(),
            nullable=self.nullable,
            metadata=self.metadata,
        )

    @classmethod
    def from_arrow(cls, field: pa.Field) -> Field:
        """Construct this from a [`pyarrow.Field`][pyarrow.Field]."""

        parsed_metadata: Dict[str, str] = {}
        if field.metadata:
            for key, value in field.metadata.items():
                parsed_metadata[key.decode()] = value.decode()

        return cls(
            name=field.name,
            type=data_type_from_arrow(field.type),
            nullable=field.nullable,
            metadata=parsed_metadata or None,
        )

    @field_validator("type", mode="before")
    @classmethod
    def coerce_type(cls, v):
        import pandas as pd

        # For numpy, most people pass around numpy _classes_ as the type
        # Note: passing a class instance to issubclass will error
        if inspect.isclass(v) and issubclass(v, np.generic):
            return PrimitiveDataType.from_numpy_type_class(v)

        # This is rare, it would be a scalar instance of a numpy type
        if isinstance(v, np.generic):
            return PrimitiveDataType.from_numpy_type(v)

        if isinstance(v, np.dtype):
            return PrimitiveDataType.from_numpy_dtype(v)

        if isinstance(v, pd.api.extensions.ExtensionDtype):
            return PrimitiveDataType.from_pandas_type(v)

        if any(v is python_type for python_type in [float, int, str, bool]):
            return PrimitiveDataType.from_python_type(v)

        if isinstance(v, str):
            return data_type_from_string(v)

        return v


# Note: this section needs to happen _after_ all recursive references have been defined
Field.model_rebuild()
TimestampType.model_rebuild()
ListType.model_rebuild()
LargeListType.model_rebuild()
FixedSizeListType.model_rebuild()
FixedSizeBinaryType.model_rebuild()
StructType.model_rebuild()


class Schema(BaseModel):
    """A description of a table schema.

    !!! info

        This schema mirrors the definition of a [`pyarrow.Schema`][pyarrow.Schema]
        object.
    """

    fields: List[Field] = PydanticField(default_factory=list)
    """A list of [`fields`][fused.models.Field] describing the columns in this table.

    The ordering of the field descriptors must match the actual ordering of the columns
    in the table.
    """

    metadata: Optional[Dict[str, str]] = None
    """Optional metadata describing the table."""

    def to_arrow(self) -> pa.Schema:
        """Convert this to a [`pyarrow.Schema`][pyarrow.Schema]."""

        return pa.schema([field.to_arrow() for field in self.fields], self.metadata)

    @classmethod
    def empty(cls) -> Schema:
        """Returns a Schema with no fields."""
        return cls(fields=[])

    @property
    def is_empty(self) -> bool:
        """True if this schema has no fields and no metadata."""
        return not len(self.fields) and not self.metadata

    @classmethod
    def from_arrow(cls, schema: pa.Schema) -> Schema:
        """Construct this from a [`pyarrow.Schema`][pyarrow.Schema]."""

        parsed_fields: List[Field] = []
        for field in schema:
            parsed_fields.append(Field.from_arrow(field))

        parsed_metadata: Dict[str, str] = {}
        if schema.metadata:
            for key, value in schema.metadata.items():
                parsed_metadata[key.decode()] = value.decode()

        return cls(fields=parsed_fields, metadata=parsed_metadata)

    @classmethod
    def from_dataframe(cls, df: Union["pd.DataFrame", "gpd.GeoDataFrame"]) -> Schema:
        """Infer a schema from a [`pandas.DataFrame`][pandas.DataFrame]."""
        if HAS_GEOPANDAS and isinstance(df, GPD_GEODATAFRAME):
            import geopandas as gpd

            # Remove the geometry column so that pa.Schema.from_pandas succeeds
            geometry_column_index = list(df.columns).index(df._geometry_column_name)
            non_geo_columns = [
                name for name in df.columns if name != df._geometry_column_name
            ]
            non_geospatial_schema = cls.from_dataframe(df[non_geo_columns])
            non_geospatial_schema.fields.insert(
                geometry_column_index,
                Field(name=df._geometry_column_name, type=PrimitiveDataType.Geometry),
            )

            from geopandas.io.arrow import _create_metadata

            # We must create the standard geo metadata, because it should be written even
            # if some chunk is not processed (e.g. in inner join.) We remove the bbox in that
            # case because it will be wrong if copied to some other chunk.
            try:
                if gpd.__version__ < "1":
                    geo_metadata = _create_metadata(df, schema_version=None)
                else:
                    # Internal API changed around GeoPandas 1.0
                    geo_metadata = _create_metadata(
                        df,
                        geometry_encoding={df._geometry_column_name: "WKB"},
                        schema_version=None,
                    )

                if "bbox" in geo_metadata["columns"][df._geometry_column_name]:
                    # May not be present if e.g. the column is empty of all values
                    del geo_metadata["columns"][df._geometry_column_name]["bbox"]

                non_geospatial_schema.metadata["geo"] = json.dumps(geo_metadata)
            except Exception as e:
                warnings.warn(FusedWarning(f"Failed to reparse geo metadata: {e}"))

            return non_geospatial_schema

        pyarrow_schema = pa.Schema.from_pandas(df, preserve_index=False)
        pyarrow_schema = pyarrow_schema.remove_metadata()

        # The fused index column should not be specified on the schema because it is an
        # index, not a column to be saved.
        fused_index_idx = pyarrow_schema.get_field_index(INDEX_COLUMN_NAME)
        if fused_index_idx >= 0:
            pyarrow_schema = pyarrow_schema.remove(fused_index_idx)

        return cls.from_arrow(pyarrow_schema)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> Schema:
        """Create a schema from a key-value dictionary.

        Returns:
            A Schema object

        Examples:
            ```py
            columns = {
                'column1': np.uint8,
                'column2': str,
            }
            schema = Schema.from_dict(columns)
            ```

        """
        fields: List[Field] = []
        for name, dtype in d.items():
            field = Field(name=name, type=dtype)
            fields.append(field)

        return cls(fields=fields)

    @classmethod
    def from_parquet(cls, file: Union[str, Path, IO[bytes]]) -> Schema:
        """Construct a Schema from a Parquet file

        Args:
            file: Parquet file to parse as schema.

        Returns:
            Schema inferred from Parquet file
        """
        schema = pq.read_schema(file)
        return cls.from_arrow(schema)

    @classmethod
    def from_string(cls, str: str) -> Schema:
        """Parse a schema from a string, which may be in several forms.

        The string may either contain JSON, or a "command-line" form of specifying a schema
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

        A list of floats with capacity of > 2^32 elements:

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
        """
        if str.lstrip().startswith("{"):
            return cls.model_validate_json(str)

        split = shlex.split(str, comments=True)

        if len(split) == 0:
            return Schema()

        parsed_fields: List[Field] = []
        for field in split:
            split = field.split(":", maxsplit=1)
            if len(split) == 1:
                raise NotImplementedError()

            name = split[0]
            if name.startswith("-"):
                warnings.warn(
                    FusedReservedWarning(
                        f"Field names should not begin with '-': {name}"
                    )
                )
            dtype = split[1]
            parsed_field = Field(name=name, type=dtype)  # type: ignore
            parsed_fields.append(parsed_field)

        return Schema(fields=parsed_fields)

    def to_string(self) -> str:
        """Returns a string form of this schema, which will be parseable by `from_string`."""
        # Check if any field needs to be customized beyond what the CLI form would have.
        any_field_has_metadata = any(
            [(f.metadata or not f.nullable) for f in self.fields]
        )
        if self.metadata or any_field_has_metadata:
            # The command-line form below does not support encoding metadata
            return self.model_dump_json()

        field_strs: List[str] = []
        for field in self.fields:
            field_descriptor = f"{field.name}:{field.type}"
            field_strs.append(f"{shlex.quote(field_descriptor)}")

        return " ".join(field_strs)

    def update(self, other: Schema) -> Schema:
        """Update this schema using fields from another schema.

        Fields are updated by name from the other schema. The fields in this schema will
        stay in the same order. All field names in the other schema must exist in this
        schema.

        Args:
            other: the schema with which to update this schema

        Returns:
            A new Schema object
        """
        new_metadata = {}
        left_metadata = self.metadata or {}
        right_metadata = other.metadata or {}
        new_metadata.update(left_metadata)
        left_metadata.update(right_metadata)

        left_fields = self.fields
        right_fields = other.fields

        left_field_names = {field.name for field in left_fields}
        right_field_names = {field.name for field in right_fields}
        extra_right_field_names = right_field_names.difference(left_field_names)
        if extra_right_field_names:
            error_msg = (
                f"{', '.join(extra_right_field_names)}"
                " found in right schema but not in left schema"
            )
            raise ValueError(error_msg)

        right_field_mapping = {field.name: field for field in right_fields}

        new_fields = []
        for left_field in left_fields:
            right_field = right_field_mapping.get(left_field.name)
            if right_field is not None:
                new_fields.append(right_field)
            else:
                new_fields.append(left_field)

        return Schema(fields=new_fields, metadata=new_metadata)

    def get_field(self, name: str) -> Optional[Field]:
        """Returns the field in this schema with the specified name, or None.

        Args:
            name: The name of the field.

        Returns:
            The Field object, or None if no field with that name was found."""
        for field in self.fields:
            if field.name == name:
                return field

        return None

    @field_validator("fields")
    @classmethod
    def validate_fields(cls, v: List[Field]):
        assert len(v) == len({field.name for field in v}), "Field names must be unique"
        return v

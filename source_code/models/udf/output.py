import warnings
from typing import Any, Optional

import numpy as np
import pyarrow as pa
from pydantic import (
    BaseModel,
    ConfigDict,
    ValidationInfo,
    field_validator,
    model_validator,
)

from fused._optional_deps import GPD_GEODATAFRAME, HAS_GEOPANDAS
from fused.warnings import FusedUdfWarning

from ..schema import INDEX_COLUMN_NAME, Schema


class Output(BaseModel):
    skip_fused_index_validation: bool = False
    data: Any = None
    table_schema: Optional[Schema] = None
    # TODO: sidecar_output can be a path too, right?
    sidecar_output: Optional[bytes] = None

    @field_validator("data", mode="before")
    @classmethod
    def coerce_none_to_empty_dataframe(cls, v):
        import pandas as pd

        if v is None:
            v = pd.DataFrame({"fused_index": pd.Series([], dtype=np.uint32)})

        return v

    @field_validator("data")
    @classmethod
    def validate_data(cls, v, info: ValidationInfo):
        if info.data.get("skip_fused_index_validation", False):
            return v

        import pandas as pd

        fused_index_msg = "`fused_index` must be a column in `output.data`."
        if isinstance(v, pd.DataFrame):
            assert "fused_index" in v.columns, fused_index_msg

        elif isinstance(v, pa.Table):
            assert "fused_index" in v.column_names, fused_index_msg

        return v

    def validate_data_with_schema(self, *, strict: bool = False):
        if strict:
            raise NotImplementedError

    model_config = ConfigDict(arbitrary_types_allowed=True, validate_assignment=True)


class PandasOutput(Output):
    data: Any
    """The output DataFrame or GeoDataFrame."""

    table_schema: Schema
    """A schema describing the output table."""

    @model_validator(mode="before")
    @classmethod
    def initialize_table_schema(cls, values):
        """If table_schema is not passed, initialize one from the data argument"""
        if values.get("table_schema") is None:
            assert "data" in values, "`data` was not passed into PandasOutput"
            values["table_schema"] = Schema.from_dataframe(values["data"])

        return values

    def validate_data_with_schema(self, *, strict: bool = False):
        super().validate_data_with_schema(strict=strict)
        if not self.skip_fused_index_validation:
            assert (
                INDEX_COLUMN_NAME in self.data.columns
            ), f"`{INDEX_COLUMN_NAME}` should be a column on `output.data`"

            # if fused index is wrong type, it's an error (or warning?)
            index_dtype = self.data[INDEX_COLUMN_NAME].dtype
            if index_dtype.kind == "i" or index_dtype.kind == "u":
                if (self.data[INDEX_COLUMN_NAME] < 0).any():
                    # This only makes sense for signed
                    warnings.warn(
                        FusedUdfWarning(
                            f"`{INDEX_COLUMN_NAME}` has negative values, which may cause errors."
                        )
                    )
            else:
                warnings.warn(
                    FusedUdfWarning(
                        f"Expected `{INDEX_COLUMN_NAME}` to be an integer, but it was {index_dtype}"
                    )
                )

        # if there's any difference between field names in the schema and the df names,
        # error
        field_names = {field.name for field in self.table_schema.fields}
        field_names.add(INDEX_COLUMN_NAME)

        df_column_diff = set([str(x) for x in self.data.columns]).difference(
            field_names
        )
        if df_column_diff:
            raise ValueError(
                f"Additional columns specified that were not in the schema: {', '.join(df_column_diff)}"
            )

        if HAS_GEOPANDAS and isinstance(self.data, GPD_GEODATAFRAME):
            # Remove geometry before validating
            non_geo_columns = [
                name
                for name in self.data.columns
                if name != self.data._geometry_column_name
            ]
            non_geo_df = self.data[non_geo_columns]

            non_geo_schema = Schema(
                fields=[
                    field
                    for field in self.table_schema.fields
                    if field.name != self.data._geometry_column_name
                ]
            )

            pa.Table.from_pandas(non_geo_df, schema=non_geo_schema.to_arrow())

        else:
            # Lax parsing; this allows anything where pyarrow _can_ cast between the two
            # types. For example this allows Uint64 -> Float64, but not Uint64 ->
            # String.
            # If validated, this should not error
            pa.Table.from_pandas(self.data, schema=self.table_schema.to_arrow())

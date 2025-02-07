from __future__ import annotations

import warnings
from pathlib import Path
from typing import (
    Any,
    BinaryIO,
    Dict,
    Iterable,
    Literal,
    Optional,
    Sequence,
    Union,
    overload,
)

from pydantic import Field, PrivateAttr, RootModel
from typing_extensions import Annotated

from fused.models.schema import Schema
from fused.models.udf.base_udf import (
    METADATA_FUSED_ID,
    METADATA_FUSED_SLUG,
    BaseUdf,
    UdfType,
)
from fused.warnings import FusedUdfWarning

from .._inplace import _maybe_inplace


class GeoPandasUdfV2(BaseUdf):
    """A user-defined function that operates on [`geopandas.GeoDataFrame`s][geopandas.GeoDataFrame]."""

    type: Literal[UdfType.GEOPANDAS_V2] = UdfType.GEOPANDAS_V2
    table_schema: Optional[Schema] = None
    """The [`Schema`][fused.models.Schema] describing the output of this UDF.
    """

    entrypoint: str
    """Name of the function within the code to invoke."""

    parameters: Dict[str, Any] = Field(default_factory=dict)
    """Parameters to pass into the entrypoint."""

    _parameter_list: Optional[Sequence[str]] = PrivateAttr(None)
    original_headers: Optional[str] = None

    _nested_callable = PrivateAttr(None)  # TODO : Find out type

    def set_parameters(
        self,
        parameters: Dict[str, Any],
        replace_parameters: bool = False,
        inplace: bool = False,
    ) -> "GeoPandasUdfV2":
        """Set the parameters on this UDF.

        Args:
            parameters: The new parameters dictionary.
            replace_parameters: If True, unset any parameters not in the parameters argument. Defaults to False.
            inplace: If True, modify this object. If False, return a new object. Defaults to True.
        """
        ret = _maybe_inplace(self, inplace)
        new_parameters = (
            parameters
            if replace_parameters
            else {
                **ret.parameters,
                **parameters,
            }
        )
        ret.parameters = new_parameters
        return ret

    def eval_schema(self, inplace: bool = False) -> "GeoPandasUdfV2":
        """Reload the schema saved in the code of the UDF.

        Note that this will evaluate the UDF function.

        Args:
            inplace: If True, update this UDF object. Otherwise return a new UDF object (default).
        """
        from fused._udf.execute_v2 import execute_for_decorator

        new_udf = execute_for_decorator(self)
        assert isinstance(
            new_udf, GeoPandasUdfV2
        ), f"UDF has unexpected type: {type(new_udf)}"
        ret = _maybe_inplace(self, inplace)
        ret.table_schema = new_udf.table_schema
        ret._parameter_list = new_udf._parameter_list
        return ret

    def run_local(
        self,
        sample: Any | None = ...,
        *,
        inplace: bool = False,
        validate_output: bool = False,
        validate_imports: Optional[bool] = None,
        **kwargs,
    ) -> "UdfEvaluationResult":  # ruff: noqa: F821
        """Evaluate this UDF against a sample.

        Args:
            sample: Sample (from `get_sample`) to execute against.
            inplace: If True, update this UDF object with schema information. (default)
        """
        from fused._udf.execute_v2 import execute_against_sample
        from fused.models.udf._eval_result import (  # ruff: noqa: F401
            UdfEvaluationResult,
        )

        ret = _maybe_inplace(self, inplace)
        sample_list = [] if sample is Ellipsis else [sample]
        return execute_against_sample(
            udf=ret,
            input=sample_list,
            validate_output=validate_output,
            validate_imports=validate_imports,
            **kwargs,
        )

    def to_file(self, where: Union[str, Path, BinaryIO], *, overwrite: bool = False):
        """Write the UDF to disk or the specified file-like object.

        The UDF will be written as a Zip file.

        Args:
            where: A path to a file or a file-like object.

        Keyword Args:
            overwrite: If true, overwriting is allowed.
        """
        job = self()
        job.export(where, how="zip", overwrite=overwrite)

    def to_directory(self, where: Union[str, Path], *, overwrite: bool = False):
        """Write the UDF to disk as a directory (folder).

        Args:
            where: A path to a directory.

        Keyword Args:
            overwrite: If true, overwriting is allowed.
        """
        job = self()
        job.export(where, how="local", overwrite=overwrite)

    # List of data input is passed - run that
    @overload
    def __call__(self, *, arg_list: Iterable[Any], **kwargs) -> UdfJobStepConfig:
        ...

    # Nothing is passed - run the UDF once
    @overload
    def __call__(self, *, arg_list: None = None, **kwargs) -> UdfJobStepConfig:
        ...

    def __call__(
        self, *, arg_list: Optional[Iterable[Any]] = None, **kwargs
    ) -> Union[UdfJobStepConfig,]:
        """Create a job from this UDF.

        Args:
            arg_list: A list of records to pass in to the UDF as input.
        """
        # cyclic dependency if imported at top-level
        from fused.models.api.job import UdfJobStepConfig

        with_params = self.model_copy()
        # TODO: Consider using with_parameters here, and validating that "context" and other reserved parameter names are not being passed.
        new_parameters = {**kwargs}
        if new_parameters:
            with_params.parameters = new_parameters

        if arg_list is not None and not len(arg_list):
            warnings.warn(
                FusedUdfWarning(
                    "An empty `arg_list` was passed in, no calls to the UDF will be made."
                )
            )

        return UdfJobStepConfig(
            udf=with_params,
            input=arg_list,
        )


EMPTY_UDF = GeoPandasUdfV2(
    name="EMPTY_UDF", code="", entrypoint="", table_schema=Schema(fields=[])
)

AnyBaseUdf = Annotated[GeoPandasUdfV2, Field(..., discriminator="type")]


class RootAnyBaseUdf(RootModel[AnyBaseUdf]):
    pass


def load_udf_from_response_data(data: dict) -> RootAnyBaseUdf:
    """Return a UDF from an HTTP response body, adding in metadata if necessary"""

    udf = RootAnyBaseUdf.model_validate_json(data["udf_body"]).root
    # Restore metadata fields if they were not already present
    if not udf._get_metadata_safe(METADATA_FUSED_ID) and "id" in data:
        udf._set_metadata_safe(METADATA_FUSED_ID, data["id"])
    if not udf._get_metadata_safe(METADATA_FUSED_SLUG) and "slug" in data:
        udf._set_metadata_safe(METADATA_FUSED_SLUG, data["slug"])
    return udf

import ast
import inspect
import warnings
from textwrap import dedent
from typing import Any, Callable, Dict, List, Optional, Sequence, Union

from fused._udf.state import (
    decorator_src_override,
    decorator_udf_override,
    noop_decorators,
)
from fused.models import Schema
from fused.models.udf import Header
from fused.models.udf.udf import GeoPandasUdfV2
from fused.warnings import (
    FusedIgnoredWarning,
    FusedPythonVersionWarning,
    FusedTypeWarning,
    FusedUdfWarning,
)

RESERVED_UDF_PARAMETERS = {
    "self",
    "arg_list",
    "output_table",
}
"""Set of UDF parameter names that should not be used because they will cause conflicts
when instantiating the UDF to a job."""

UDF_RUN_KWARGS = {"x", "y", "z"}
"""Set of UDF keyword arguments that are also parameters to udf.run(), which would cause the
user's UDF arguments to be clobbered."""


def _extract_parameter_list(func: Callable, num_positional_args: int) -> List[str]:
    parameter_list: List[str] = []

    signature = inspect.signature(func)
    for param_idx, param in enumerate(signature.parameters.values()):
        # Don't check certain
        is_reserved_positional_param = (param_idx == 0 and param.name == "dataset") or (
            param_idx == 1 and param.name == "right"
        )
        if param.name in RESERVED_UDF_PARAMETERS and not is_reserved_positional_param:
            warnings.warn(
                FusedUdfWarning(
                    f'Parameter named "{param}" is reserved and may cause conflicts. If you want to set the Fused option with the same name, provide it when instantiating the UDF but not in the parameter list.'
                )
            )

        if (
            param.kind
            in [inspect.Parameter.KEYWORD_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD]
            and param.name in UDF_RUN_KWARGS
        ):
            warnings.warn(
                FusedIgnoredWarning(
                    f'Parameter named "{param}" for UDF "{func.__name__}" is reserved and will be clobbered when calling fused.run(). Reserved parameters for fused.run() include {UDF_RUN_KWARGS}'
                )
            )

        if param_idx < num_positional_args:
            # This is one of the first args for getting the input data
            continue

        if param.kind in [
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.VAR_POSITIONAL,
        ]:
            warnings.warn(
                FusedUdfWarning(
                    f"Positional-only argument (name {param.name}, kind {param.kind}) cannot be specified in UDFs"
                )
            )
        elif param.kind != inspect.Parameter.VAR_KEYWORD:
            # Must be a keyword only parameter
            # This parameter must be specified: if param.default is not inspect._empty:
            # TODO: This parameter_list is not used at all, instead the signature is called below.
            parameter_list.append(param.name)

    return list(signature.parameters.keys())


# Note: If the signature of this function changes, the signature of the
# specialized versions of it below must also change. This pattern is used
# so that the internal function can be reused (pass in different _udf_cls),
# but the type hinting in e.g. VS Code is correct. Importantly, this type
# hinting includes the keyword parameters. Otherwise the way to express
# the type to VS Code is either not possible or too complicated.
def _udf_internal(
    fn: Optional[Callable] = None,
    *,
    _udf_cls: type[GeoPandasUdfV2],
    _num_positional_args: int,
    schema: Union[Schema, Dict, str, None] = None,
    name: Union[str, None] = None,
    default_parameters: Optional[Dict[str, Any]] = None,
    headers: Optional[Sequence[Union[str, Header]]] = None,
):
    def _internal_decorator_wrapper(func):
        if noop_decorators.get():
            return func

        entrypoint = func.__name__
        fn_name = name or entrypoint

        _src = decorator_src_override.get() or inspect.getsource(func)
        _src = dedent(_src)
        # src = _strip_decorators(_src)
        _src, original_headers = _strip_decorator_params(_src)

        src = _src

        parameter_list = _extract_parameter_list(
            func, num_positional_args=_num_positional_args
        )

        table_schema = schema  # may be null
        if table_schema is not None:
            if isinstance(table_schema, str):
                table_schema = Schema.from_string(table_schema)
            elif isinstance(table_schema, Schema):
                warnings.warn(
                    FusedTypeWarning(
                        "Passing table_schema as type Schema may not work on the backend. Instead pass a JSON string literal."
                    )
                )
            elif not isinstance(table_schema, Schema):
                # Schema really should not be of type Schema, since that cannot be
                # run on the backend.
                table_schema = Schema.model_validate(table_schema)

        resolved_headers = headers
        override_udf = decorator_udf_override.get()
        if override_udf and override_udf.headers:
            # model_dump is needed because the headers are really the wrong type
            resolved_headers = [h.model_dump() for h in override_udf.headers]

        new_udf = _udf_cls(
            code=src.strip("\n"),
            name=fn_name,
            entrypoint=entrypoint,
            table_schema=table_schema,
            parameters=default_parameters or {},
            headers=resolved_headers,
            original_headers=original_headers,
        )
        new_udf._parameter_list = parameter_list
        new_udf._nested_callable = func
        return new_udf

    if fn is not None:
        return _internal_decorator_wrapper(fn)
    else:
        return _internal_decorator_wrapper


# Specializations of _udf_internal. Note we return Callable so that type hinting
# is right when using "@fused.udf()" -- but this does mean it's wrong when
# using "@fused.udf".
def udf(
    fn: Optional[Callable] = None,
    *,
    schema: Union[Schema, Dict, None] = None,
    name: Optional[str] = None,
    default_parameters: Optional[Dict[str, Any]] = None,
    headers: Optional[Sequence[Union[str, Header]]] = None,
) -> Callable[..., GeoPandasUdfV2]:
    """A decorator that transforms a function into a Fused UDF.

    Args:
        schema: The schema for the DataFrame returned by the UDF. The schema may be either
            a string (in the form `"field_name:DataType field_name2:DataType"`, or as JSON),
            as a Python dictionary representing the schema, or a `Schema` model object.

            Defaults to None, in which case a schema must be evaluated by calling `run_local`
            for a job to be able to write output. The return value of `run_local` will also
            indicate how to include the schema in the decorator so `run_local` does not need
            to be run again.
        name: The name of the UDF object. Defaults to the name of the function.
        default_parameters: Parameters to embed in the UDF object, separately from the arguments
            list of the function. Defaults to None for empty parameters.
        headers: A list of files to include as modules when running the UDF. For example,
            when specifying `headers=['my_header.py']`, inside the UDF function it may be
            referenced as:

            ```py
            import my_header
            my_header.my_function()
            ```

            Defaults to None for no headers.
    Returns:
        A callable that represents the transformed UDF. This callable can be used
        within GeoPandas workflows to apply the defined operation on geospatial data.

    Examples:
        To create a simple UDF that calls a utility function to calculate the area of geometries in a GeoDataFrame:

        ```py
        @fused.udf
        def udf(bbox, table_path="s3://fused-asset/infra/building_msft_us"):
            ...
            gdf = table_to_tile(bbox, table=table_path)
            return gdf
        ```
    """
    return _udf_internal(
        fn=fn,
        _udf_cls=GeoPandasUdfV2,
        _num_positional_args=2,
        schema=schema,
        name=name,
        default_parameters=default_parameters,
        headers=headers,
    )


def _strip_decorator_params(src: str) -> str:
    """Remove all parameter from decorator declaration."""
    # TODO: use ast by line number to not use ast.unparse

    # TODO: This requires Python 3.9 because ast.unparse was exposed in that release.
    # https://docs.python.org/3/whatsnew/3.9.html#ast We may be able to backport it?
    if not hasattr(ast, "unparse"):
        warnings.warn(
            FusedPythonVersionWarning(
                "Decorators will not be removed from UDF source because ast.unparse is not available in this version of Python"
            )
        )
        return src, ""

    tree = ast.parse(src)

    original_headers = ""
    changes_made = False

    def remove_params_from_decorator(node):
        if isinstance(node, ast.Call):
            if (
                isinstance(node.func, ast.Attribute)
                and node.func.value.id == "fused"
                and node.func.attr == "udf"
            ):
                for each_keyword in node.keywords:
                    if each_keyword.arg == "headers":
                        nonlocal original_headers, changes_made
                        original_headers = ast.unparse(each_keyword.value)
                        changes_made = True
                node.keywords = []
        return node

    # Remove parameters from the fused decorator definition
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            new_decorators = []
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Call):
                    new_decorators.append(remove_params_from_decorator(decorator))
                else:
                    new_decorators.append(decorator)

    if changes_made:
        modified_src = ast.unparse(tree)

        return modified_src, original_headers
    else:
        # Avoid unparsing if not absolutely necessary. This is because of e.g.
        # PEP 701 causing differences between Python 3.11/3.12 rendering of f-strings.
        return src, ""

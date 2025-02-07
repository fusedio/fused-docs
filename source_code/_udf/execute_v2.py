import ast
import inspect
import time
import warnings
from contextlib import ExitStack
from textwrap import dedent, indent
from typing import Any, Callable, Dict, Optional

import pandas as pd

import fused
from fused._udf.context import ExecutionContextProtocol, context
from fused._udf.state import decorator_src_override_context, noop_decorators_context
from fused.core._impl._exec_globals_impl import make_exec_globals
from fused.models.schema import Schema
from fused.models.udf import EMPTY_UDF, AnyBaseUdf
from fused.models.udf._eval_result import UdfEvaluationResult
from fused.models.udf.output import Output, PandasOutput
from fused.warnings import FusedWarning


def _add_special_kwargs(
    fn: Callable,
    args: Dict[str, Any],
    output: Output,
    context: ExecutionContextProtocol,
):
    signature = inspect.signature(fn)
    param_names = signature.parameters.keys()
    # note: we don't check that this is a kwarg on the function, so if it's the first parameter it could cause
    # a call failure.
    if "output" in param_names:
        args["output"] = output
    if "context" in param_names:
        args["context"] = context

    return args


def execute_against_sample(
    udf: AnyBaseUdf,
    input: Any,
    update_schema: bool = True,
    validate_output: bool = True,
    validate_imports: Optional[bool] = None,
    **kwargs,
) -> UdfEvaluationResult:
    from fused._udf.args import coerce_arg

    if udf is EMPTY_UDF:
        raise ValueError("Empty UDF cannot be evaluated. Use `set_udf` to set a UDF.")

    output = Output()
    try:
        # Define custom function in environment

        # Wrap cell in a function
        # This is believed to fix scoping issues with closures and list comprehensions
        # See also https://stackoverflow.com/a/2749806,
        # https://stackoverflow.com/q/38318370
        # {cell_text} is not itself indented because we need to make sure that every
        # line of {cell_text} is indented, not just the first.
        FN_RESULT_NAME = "__fused_fn_result"
        wrapped_cell = """\
            def __fused_exec():
            {cell_text}

                return {entrypoint}

            {FN_RESULT_NAME} = __fused_exec()
            """
        original_src = udf.code
        src = dedent(wrapped_cell).format(
            cell_text=indent(dedent(original_src), " " * 4),
            entrypoint=udf.entrypoint,
            FN_RESULT_NAME=FN_RESULT_NAME,
        )

        exec_locals = {}
        exec_globals = make_exec_globals()

        # Validate import stamements correspond to valid modules
        validate_imports_whitelist(udf, validate_imports=validate_imports)

        with ExitStack() as stack:
            stack.enter_context(noop_decorators_context(True))

            # Add headers to sys.meta_path
            if udf.headers is not None:
                for header in udf.headers:
                    stack.enter_context(header._register_custom_finder())

            exec(src, exec_globals, exec_locals)

            _fn = exec_locals[FN_RESULT_NAME]

            kwargs_to_pass = {**udf.parameters, **kwargs}
            _add_special_kwargs(
                _fn, args=kwargs_to_pass, output=output, context=context
            )
            signature = inspect.signature(_fn)
            reformatted_kwargs_to_pass = {
                key: coerce_arg(arg, signature.parameters[key])
                for key, arg in kwargs_to_pass.items()
                # If this corresponds to a parameter on the UDF, then pass it in.
                # Otherwise, simply ignore it.
                if key in signature.parameters and key != "input"
            }

            args_to_pass = (
                input.as_udf_args() if hasattr(input, "as_udf_args") else input
            )
            positional_params = list(signature.parameters.values())
            positional_param_names = list(signature.parameters.keys())
            reformatted_args_to_pass = [
                coerce_arg(arg, positional_params[i])
                for i, arg in enumerate(args_to_pass)
                # If this corresponds to a parameter on the UDF, then pass it in.
                # Otherwise, simply ignore it.
                if positional_param_names[i] != "input"
            ]

            # Run UDF
            time_start = time.perf_counter()
            _output = _fn(*reformatted_args_to_pass, **reformatted_kwargs_to_pass)
            time_end = time.perf_counter()
            time_taken_seconds = time_end - time_start

            if not validate_output:
                return _output

            if _output is not None:
                output.data = _output

    except Exception:
        raise

    new_output = _transform_output(output=output)

    if new_output is None:
        # TODO: Assumes table_schema is present, which doesn't match type
        if udf.table_schema not in [None, {}, Schema()]:
            warnings.warn(
                FusedWarning(
                    "UDF is configured with a schema but returns `None`. An empty schema was set for this execution."
                )
            )

        return UdfEvaluationResult(
            data=None,
            sidecar=None,
            udf=udf,
            table_schema={},
            time_taken_seconds=time_taken_seconds,
        )

    # Validate the dataframe after assigning it to the output variable in user_ns
    # so the user can inspect the output if anything is wrong.
    new_output.validate_data_with_schema()

    if update_schema and udf.table_schema is None:
        udf.table_schema = new_output.table_schema

    return UdfEvaluationResult(
        data=new_output.data,
        sidecar=new_output.sidecar_output,
        udf=udf,
        table_schema=new_output.table_schema,
        time_taken_seconds=time_taken_seconds,
    )


def execute_for_decorator(udf: AnyBaseUdf) -> AnyBaseUdf:
    """Evaluate a UDF for the purpose of getting the UDF object out of it."""
    # Define custom function in environment

    # This is a stripped-down version of execute_against_sample, above.

    FN_RESULT_NAME = "__fused_fn_result"
    wrapped_cell = """\
        def __fused_exec():
        {cell_text}

            return {entrypoint}

        {FN_RESULT_NAME} = __fused_exec()
        """
    original_src = udf.code
    src = dedent(wrapped_cell).format(
        cell_text=indent(dedent(original_src), " " * 4),
        entrypoint=udf.entrypoint,
        FN_RESULT_NAME=FN_RESULT_NAME,
    )

    exec_locals = {}
    exec_globals = make_exec_globals()

    with ExitStack() as stack:
        stack.enter_context(decorator_src_override_context(original_src))

        # Add headers to sys.meta_path
        if udf.headers is not None:
            for header in udf.headers:
                stack.enter_context(header._register_custom_finder())

        exec(src, exec_globals, exec_locals)

        _fn = exec_locals[FN_RESULT_NAME]

        return _fn


def _transform_output(output: Output) -> PandasOutput:
    # TODO: Support PyArrow
    if isinstance(output, PandasOutput):
        return output

    if isinstance(output.data, pd.DataFrame):
        # Force all column names to be strings
        output.data.columns = [str(x) for x in output.data.columns]

        # Note that we don't pass a _new_ schema argument here
        # - If the user defined a schema onto output.table_schema, that will be
        #   preserved.
        # - If the user did not define output.table_schema, then output.table_schema
        #   will be None, and PandasOutput will default to a schema inferred from
        #   the DataFrame.
        return PandasOutput(
            data=output.data,
            table_schema=output.table_schema,
            sidecar_output=output.sidecar_output,
            skip_fused_index_validation=output.skip_fused_index_validation,
        )
    elif output.data is None:
        return None

    raise TypeError(f"Unexpected result type {type(output.data)}")


def validate_imports_whitelist(
    udf: AnyBaseUdf, validate_imports: Optional[bool] = None
):
    # Skip import validation if the option is set
    if not fused.options.default_validate_imports and validate_imports is not True:
        return

    # Skip import validation if not logged in
    if not fused.api.AUTHORIZATION.is_configured():
        return

    from fused._global_api import get_api

    # Get the dependency whitelist from the cached API endpoint
    api = get_api()
    package_dependencies = api.dependency_whitelist()

    # Initialize a list to store the import statements
    import_statements = []

    # Parse the source code into an AST
    tree = ast.parse(udf.code)

    # Traverse the AST to find import statements
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                import_statements.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module_name = node.module
            import_statements.append(module_name)

    # Check for unavailable modules
    header_modules = [header.module_name for header in udf.headers]
    fused_modules = ["fused"]  # assume fused is always available
    available_modules = (
        list(package_dependencies["dependency_whitelist"].keys())
        + header_modules
        + fused_modules
    )
    unavailable_modules = []
    for import_statement in import_statements:
        if import_statement.split(".", 1)[0] not in available_modules:
            unavailable_modules.append(import_statement)

    if unavailable_modules:
        raise ValueError(
            f"The following imports in the UDF might not be available: {repr(unavailable_modules)}. Please check the UDF headers and imports and try again."
        )

    # TODO: check major versions for some packages

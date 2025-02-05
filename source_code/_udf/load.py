import ast
import inspect
import re
import warnings
from pathlib import Path
from types import ModuleType
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

import requests

from fused._options import options as OPTIONS
from fused._str_utils import is_url
from fused.models import Schema
from fused.models.udf import Header
from fused.models.udf._udf_registry import UdfRegistry
from fused.models.udf.udf import GeoPandasUdfV2
from fused.warnings import FusedDefaultWarning

DECORATOR_NAMES = "udf"


def _detect_function_name(src: str) -> Optional[str]:
    parsed = ast.parse(src)

    found_function_name: Optional[str] = None
    show_warning = False

    for node in ast.iter_child_nodes(parsed):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Check if the function has decorators
            if node.decorator_list:
                # Find Fused decorator from the function
                for decorator in node.decorator_list:
                    new_found_function_name: Optional[str] = None
                    if isinstance(decorator, ast.Call):
                        if decorator.func.attr in DECORATOR_NAMES:
                            new_found_function_name = node.name
                    elif isinstance(decorator, ast.Attribute):
                        if decorator.attr in DECORATOR_NAMES:
                            # This is just in case there are no parens on the decorator.
                            new_found_function_name = node.name

                    if new_found_function_name:
                        if found_function_name:
                            show_warning = True
                        else:
                            found_function_name = new_found_function_name

    if show_warning:
        warnings.warn(
            FusedDefaultWarning(f"Loading the first UDF ({found_function_name})")
        )

    return found_function_name


def _detect_table_schema(src: str, function_name: str) -> Optional[str]:
    parsed = ast.parse(src)

    for node in ast.iter_child_nodes(parsed):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Check if the function has decorators
            if node.name == function_name and node.decorator_list:
                # Find Fused decorator from the function
                for decorator in node.decorator_list:
                    if isinstance(decorator, ast.Call):
                        if decorator.func.attr in DECORATOR_NAMES:
                            for keyword in decorator.keywords:
                                if keyword.arg == "schema":
                                    if isinstance(keyword.value, ast.Str):
                                        return keyword.value.value
                                    elif isinstance(keyword.value, ast.Dict):
                                        if keyword.value.keys is None or not len(
                                            keyword.value.keys
                                        ):
                                            # Empty dictionary, special case
                                            return {}
                                    warnings.warn(
                                        FusedDefaultWarning(
                                            "A table schema was present but it could not be parsed. Use `eval_schema` to evaluate it."
                                        )
                                    )
                            return None
                    elif isinstance(decorator, ast.Attribute):
                        if decorator.attr in DECORATOR_NAMES:
                            # This is just in case there are no parens on the decorator.
                            return None

    return None


def _detect_parameters(src: str) -> Tuple[Dict[str, Any], List[str]]:
    def extract_arg_type(node):
        if isinstance(node, ast.Str):
            return node.s
        elif isinstance(node, ast.Tuple):
            return tuple(extract_arg_type(item) for item in node.elts)
        elif isinstance(node, ast.List):
            return [extract_arg_type(item) for item in node.elts]
        elif isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.Dict):
            return {k.s: extract_arg_type(v) for k, v in zip(node.keys, node.values)}

    try:
        parsed_ast = ast.parse(src)
    except SyntaxError:
        parsed_ast = ast.parse(repr(src))

    # Find and extract parameters
    params = []
    for node in ast.walk(parsed_ast):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for arg in node.args.args:
                params.append(arg.arg)
            break

    # Find and extract default values
    defaults = []
    for node in ast.walk(parsed_ast):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for default in node.args.defaults:
                defaults.append(extract_arg_type(default))
            break

    # Create a dictionary with parameters and their default values
    return dict(zip(params[-len(defaults) :], defaults)), params


def load_udf(
    udf_paths: Sequence[str],
    *,
    parameters: Optional[Dict[str, Any]] = None,
    content_type: Optional[str] = None,
    load_schema: bool = True,
    header_paths: Optional[Sequence[Header]] = None,
) -> UdfRegistry:
    """
    Load UDF(s) in a UdfRegistry object.

    Args:
        udf_paths: The paths to the UDF source code files or URLs.
            If provided as a list, it loads and registers multiple UDFs as a UdfRegistry.
        function: The name of the UDF function to load.
        parameters: A dictionary of parameters to be passed to the UDF.
        table_schema: The schema of the input data table.
        content_type: The content type of the UDF source, e.g., "file", "py", or "url".
        load_schema: Whether to automatically detect and load the table schema.
        header_paths: A sequence of headers for the UDF.

    Returns:
        UdfRegistry or UDF: Returns a UdfRegistry containing registered UDFs.

    Raises:
    - ValueError: If multiple UDFs with the same name are found in a list of UDF paths.
    - AssertionError: If an unsupported content type is provided.

    Examples:
        Load multiple UDFs from a list of files and register them in a UdfRegistry:

        ```py
        load_udf(udf_paths=["udf1.py", "udf2.py"], header_paths=["header.py"])
        load_udf("my_udf.py", function="my_function", content_type="file")
        ```
    """
    if not isinstance(udf_paths, list):
        udf = _load_udfs_from_file(
            udf_paths=udf_paths,
            parameters=parameters,
            content_type=content_type,
            load_schema=load_schema,
            header_paths=header_paths,
        )
        if isinstance(udf, UdfRegistry):
            return udf
        else:
            return UdfRegistry({udf.name: udf})
    else:
        udfs = {}
        for udf_path in udf_paths:
            udf = _load_udfs_from_file(
                udf_path,
                parameters=parameters,
                content_type=content_type,
                load_schema=load_schema,
                header_paths=header_paths,
            )

            # If the returned object is already a registry, just return it.
            if isinstance(udf, UdfRegistry):
                return udf
            if udf.name not in udfs:
                udfs[udf.name] = udf
            else:
                raise ValueError(
                    f"Multiple UDFs with the same name ({udf.name}) are not allowed."
                )
        return UdfRegistry(udfs)


def _load_udfs_from_file(
    udf_paths: str,
    function: Optional[str] = None,
    *,
    parameters: Optional[Dict[str, Any]] = None,
    table_schema: Union[Dict[str, Any], Schema, str, None] = None,
    content_type: Optional[str] = None,
    load_schema: bool = True,
    header_paths: Optional[Sequence[Header]] = None,
) -> Union[UdfRegistry, GeoPandasUdfV2]:
    """
    Load UDF(s) from a single source.

    Parameters:
    - udf_paths (str): The path to the UDF source code files or URLs.
    - function (str, optional): The name of the UDF function to load.
    - parameters (dict, optional): A dictionary of parameters to be passed to the UDF.
    - table_schema (dict, Schema, str, or None, optional): The schema of the input data table.
    - content_type (str, optional): The content type of the UDF source, e.g., "file", "py", or "url".
    - load_schema (bool, optional): Whether to automatically detect and load the table schema.
    - header_paths (Sequence[Header], optional): A sequence of headers for the UDF.

    Returns:
    - UdfRegistry or UDF: Returns an instantiated UDF object or a UdfRegistry if multiple UDFs
      were found.

    Raises:
    - ValueError: If multiple UDFs with the same name are found in a list of UDF paths.
    - AssertionError: If an unsupported content type is provided.
    """
    src = None
    _is_url = False

    if content_type == "url" or (content_type is None and is_url(udf_paths)):
        _is_url = True
    elif content_type is None or content_type == "file":
        udf_paths = Path(udf_paths)
    elif content_type == "py":
        src = udf_paths
    else:
        assert (
            False
        ), f'Unknown content type: {content_type}. Should be one of "file", "py".'

    if isinstance(udf_paths, Path):
        src = Path(udf_paths).read_text("utf-8")
    elif isinstance(udf_paths, ModuleType):
        if function:
            assert hasattr(udf_paths, function), "Could not find function on object."
        src = inspect.getsource(udf_paths)
    elif _is_url:
        r = requests.get(udf_paths, timeout=OPTIONS.request_timeout)
        r.raise_for_status()
        src = r.text
    else:
        pass
        # assert False, f"Unknown type to load from: {type(udf_paths)}"

    assert src, "No source provided"

    # If the source file contains multiple UDFs
    udfs = _find_udfs(src)
    if len(udfs.items()) > 1:
        # TODO: Update return type hint
        return load_udf(
            udf_paths=list(udfs.values()),
            header_paths=header_paths,
            load_schema=load_schema,
            content_type="py",
        )

    function = function if function else _detect_function_name(src)

    if table_schema:
        table_schema = table_schema
    elif load_schema:
        table_schema = _detect_table_schema(src, function)
    else:
        raise ValueError("No table schema provided and `load_schema` is False.")

    if isinstance(table_schema, str):
        table_schema = Schema.from_string(table_schema)
    elif table_schema is not None and not isinstance(table_schema, Schema):
        table_schema = Schema.model_validate(table_schema)

    # Set param headers on code string headers
    if header_paths:
        src = _replace_headers(src, header_paths)
    else:
        # If no `header_paths` but `src` contains headers, raise an error
        src_headers = _get_src_headers(src)
        if src_headers:
            raise ValueError(
                f"`load_udf` requires the `headers` parameter to be specified because the UDF source file specifies headers as `headers={src_headers}`."
            )

    _parameters, _parameter_list = _detect_parameters(src)
    new_udf = GeoPandasUdfV2(
        code=udfs[function].strip("\n"),  # UDF src without imports
        name=function,
        entrypoint=function,
        table_schema=table_schema,
        parameters=parameters or _parameters,
        headers=header_paths or [],
    )

    new_udf._parameter_list = _parameter_list
    return new_udf


def _find_udfs(src):
    fused_udf_functions = {}
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Call) and isinstance(
                    decorator.func, ast.Attribute
                ):
                    # Handle @fused.udf()
                    func = decorator.func
                elif isinstance(decorator, ast.Attribute):
                    # Handle @fused.udf
                    func = decorator
                else:
                    # If neither of the above, skip. This handles decorators internal to the udf.
                    continue
                if func.value.id == "fused" and func.attr == "udf":
                    # Get the code of the function, starting at the decorator.
                    start_lineno = decorator.lineno - 1
                    end_lineno = node.end_lineno
                    function_code = "\n".join(src.splitlines()[start_lineno:end_lineno])
                    fused_udf_functions[node.name] = function_code
    return fused_udf_functions


def _replace_headers(src: str, header_paths) -> str:
    def dict_from_file_paths(file_paths):
        file_dict = {}
        for file_path in file_paths:
            if isinstance(file_path, str):
                file_name = Path(file_path).stem
                file_dict[file_name] = file_path
            else:
                # TODO: Phase out
                file_dict[file_path.module_name + ".py"] = file_path
        return file_dict

    def replace_headers(src, header_paths):
        new_headers = str(header_paths)

        # Regex to match the headers parameter
        pattern = r"headers=\[[^\]]+\]"

        # Use regex to find and replace the headers value in the code
        return re.sub(pattern, f"headers={new_headers}", src)

    src_headers = _get_src_headers(src)
    if not src_headers:
        if header_paths:
            # warnings.warn(
            #     "Ignoring header specified in `load_udf` because UDF declaration does not specify header.",
            #     FusedDefaultWarning,
            # )
            pass
        else:
            return src

    # Assert that all headers in original UDF code are passed of the provided headers
    for src_header in set(dict_from_file_paths(src_headers).keys()):
        if src_header not in list(dict_from_file_paths(header_paths).keys()):
            ValueError(
                "The header {src_header} in UDF code do not match the headers provided."
            )
    return replace_headers(src, header_paths)


def _get_src_headers(src):
    # Regex to match the headers parameter
    pattern = r"headers=\s*\[([\s\S]*?)\]"

    # Use regex to find and extract the headers value
    match = re.search(pattern, src)

    # If a match is found, extract and split the headers into an array
    if match:
        return [header.strip("\"' ,\n\t") for header in match.group(1).split(",")]
    else:
        return []

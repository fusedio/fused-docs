import ast
from typing import Optional

from ..internal import DatasetOutputV2


def stringify_named_params(params):
    return [k + "=" + repr(v) for k, v in params.items()]


def structure_params(params, separator=", "):
    return separator.join([param for param in params])


def stringify_headers(headers):
    if not headers:
        return "[]"
    else:
        for header in headers:
            if hasattr(header, "source_file"):
                delattr(header, "source_file")
        return str(headers)


def stringify_output(output) -> Optional[str]:
    if isinstance(output, DatasetOutputV2):
        return repr(output.url) if output.url is not None else None

    return repr(output)


def extract_parameters(src):
    # Parse the input string into an AST (Abstract Syntax Tree)
    parsed_ast = ast.parse(src)

    all_parameters = []
    named_parameters = {}

    # Find all function definitions in the AST
    function_defs = [
        node
        for node in ast.walk(parsed_ast)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    # Assume the first function is the target function
    target_function = function_defs[0]

    for arg in target_function.args.args:
        param_name = arg.arg
        # named_parameters[param_name] = None  # Initialize with None
        all_parameters.append(param_name)

    for keyword in target_function.args.kwonlyargs:
        param_name = keyword.arg
        # named_parameters[param_name] = None  # Initialize with None

    for param, default in zip(
        target_function.args.args[
            len(target_function.args.args) - len(target_function.args.defaults) :
        ],
        target_function.args.defaults,
    ):
        # Extract the default value if it's a string, number, or None
        # TODO: Handle more types
        if isinstance(
            default,
            (
                ast.Str,
                ast.Num,
                ast.NameConstant,
                ast.Tuple,
                ast.List,
                ast.Dict,
                ast.Set,
            ),
        ):
            named_parameters[param.arg] = ast.literal_eval(default)

    positional_parameters = [
        param for param in all_parameters if param not in named_parameters
    ]

    return positional_parameters, named_parameters

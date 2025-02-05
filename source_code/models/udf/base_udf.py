from __future__ import annotations

import ast
import json
import warnings
from enum import Enum
from functools import cached_property
from io import IOBase
from pathlib import PurePath
from textwrap import dedent, indent
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Iterable,
    Literal,
    Optional,
    Sequence,
    Tuple,
    Union,
)
from uuid import UUID

import requests
from pydantic import BaseModel, ConfigDict, RootModel, field_validator

from fused._formatter.udf import fused_header_repr, fused_udf_repr
from fused._options import options as OPTIONS
from fused.models.base import UserMetadataType
from fused.models.udf.header import Header
from fused.warnings import FusedWarning

from .._codegen import (
    extract_parameters,
    stringify_headers,
    stringify_named_params,
    structure_params,
)
from .._inplace import _maybe_inplace

if TYPE_CHECKING:
    from fused.models.api import UdfAccessToken, UdfAccessTokenList


METADATA_FUSED_ID = "fused:id"
METADATA_FUSED_SLUG = "fused:slug"
METADATA_FUSED_EXPLORER_TAB = "fused:explorerTab"


class HeaderSequence(RootModel[Sequence[Header]]):
    def _repr_html_(self) -> str:
        return fused_header_repr(self)

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __setitem__(self, item, value):
        self.root[item] = value

    def __len__(self):
        return len(self.root)


class AttrDict(dict):
    """Dictionary where keys can also be accessed as attributes"""

    def __getattribute__(self, __name: str) -> Any:
        try:
            return super().__getattribute__(__name)
        except AttributeError:
            if __name in self:
                return self[__name]
            else:
                raise

    def __dir__(self) -> Iterable[str]:
        return self.keys()


class UdfType(str, Enum):
    GEOPANDAS_V2 = "geopandas_v2"


class BaseUdf(BaseModel):
    name: Optional[str] = None
    type: Literal[UdfType.GEOPANDAS_V2]
    code: str
    headers: Union[HeaderSequence, Sequence[Header], None] = None
    metadata: UserMetadataType = None

    @field_validator("headers", mode="before")
    @classmethod
    def _process_headers(cls, headers):
        processed_headers = []
        if headers is not None:
            for header in headers:
                if isinstance(header, str):
                    module_name = PurePath(header).name.split(".", maxsplit=1)[0]
                    processed_headers.append(
                        Header.from_code(module_name=module_name, source_file=header)
                    )
                elif (
                    isinstance(header, dict)
                    and header.get("source_file")
                    and not header.get("source_code")
                ):  # headers = {'source_file': 'header.py', 'module_name': 'header'}
                    source_file = header["source_file"]
                    module_name = header.get(
                        "module_name",
                        PurePath(source_file).name.split(".", maxsplit=1)[0],
                    )
                    processed_headers.append(
                        Header.from_code(
                            module_name=module_name,
                            source_file=source_file,
                        )
                    )
                else:
                    processed_headers.append(header)

        return processed_headers

    @field_validator("code", mode="before")
    @classmethod
    def udf_is_str(cls, v):
        if isinstance(v, IOBase):
            # Handle passing in a file as the code
            v.seek(0)
            data = v.read()
            if isinstance(data, str):
                return data
            elif isinstance(data, bytes):
                return data.decode("utf-8")
            else:
                raise ValueError("Expected string or bytes from the file")

        return v

    @classmethod
    def from_gist(cls, gist_id: str):
        """Create a Udf from a GitHub gist."""
        # TODO: if a versioned gist, taking the last / won't work as that will be the
        # version, not the gist id.
        if "/" in gist_id:
            gist_id = gist_id.split("/")[-1]

        url = f"https://api.github.com/gists/{gist_id}"
        r = requests.get(url, timeout=OPTIONS.request_timeout)
        r.raise_for_status()

        files: dict = r.json()["files"]

        obj = {}
        # TODO: Update expected files schema
        assert "code.py" in files.keys()
        assert "parameters.json" in files.keys()

        obj["code"] = _fetch_gist_content(files, "code.py")

        if "table_schema.json" in files.keys():
            table_schema_text = _fetch_gist_content(files, "parameters.json")
            obj["table_schema"] = json.loads(table_schema_text)

        parameters_text = _fetch_gist_content(files, "parameters.json")
        parameters = json.loads(parameters_text)
        obj.update(parameters)

        return cls.model_validate(obj)

    def to_fused(
        self,
        slug: Optional[str] = ...,
        over_id: Union[str, UUID, None] = None,
        as_new: Optional[bool] = None,
        inplace: bool = True,
    ):
        """
        Save this UDF on the Fused service.

        Args:
            slug: ID to refer to this UDF as in URLs.
            over_id: ID to save the UDF over.
            as_new: If True, force saving this UDF as new.
            inplace: If True (default), update the UDF object with the new saved ID.
        """
        from fused._global_api import get_api

        backend_id = (
            str(over_id) if over_id else self._get_metadata_safe(METADATA_FUSED_ID)
        )
        if backend_id is None or as_new:
            assert (
                as_new is not False
            ), "Cannot detect ID to save over, so as_new cannot be False."
            backend_id = None

        ret = _maybe_inplace(self, inplace)

        if slug is Ellipsis:
            # If the user didn't specify a name to save as, determine the name
            # to save as here.
            slug = ret._get_metadata_safe(METADATA_FUSED_SLUG)
            if not slug:
                # No metadata-determined name, so use the regular name of the
                # UDF.
                slug = ret.name

        if slug and slug != ret.name:
            # If we are setting the name of the UDF, it is important to set the
            # name on the UDF body itself, because that is what Workbench will read
            ret.name = slug

        api = get_api()
        result = api.save_udf(
            udf=ret,
            slug=slug,
            id=backend_id,
        )
        new_id = result["id"]

        ret._set_metadata_safe(METADATA_FUSED_ID, new_id)
        return ret

    def delete_saved(self, inplace: bool = True):
        from fused._global_api import get_api

        backend_id = self._get_metadata_safe(METADATA_FUSED_ID)
        assert backend_id is not None, "No saved UDF ID found in metadata."

        api = get_api()
        api.delete_saved_udf(
            id=backend_id,
        )

        ret = _maybe_inplace(self, inplace)
        # ret.metadata must be non None because we read the backend ID from there
        ret.metadata.pop(METADATA_FUSED_ID)
        return ret

    def create_access_token(
        self,
        *,
        client_id: Union[str, Ellipsis, None] = ...,
        cache: bool = True,
        metadata_json: Optional[Dict[str, Any]] = None,
        enabled: bool = True,
    ) -> UdfAccessToken:
        from fused._global_api import get_api

        # If there is a backend ID, locate this UDF by the backend ID rather than by its name
        backend_id = self._get_metadata_safe(METADATA_FUSED_ID)
        assert (
            backend_id is not None
        ), "No saved UDF ID found in metadata. Save the UDF to Fused first with `.to_fused` and then create the access token."

        api = get_api()
        return api.create_udf_access_token(
            udf_id=backend_id,
            client_id=client_id,
            cache=cache,
            metadata_json=metadata_json,
            enabled=enabled,
        )

    def get_access_tokens(self) -> UdfAccessTokenList:
        from fused._global_api import get_api
        from fused.models.api import UdfAccessTokenList

        # If there is a backend ID, locate this UDF by the backend ID rather than by its name
        backend_id = self._get_metadata_safe(METADATA_FUSED_ID)
        assert (
            backend_id is not None
        ), "No saved UDF ID found in metadata. Save the UDF to Fused first with `.to_fused` and then create the access token."

        api = get_api()
        all_tokens = api.get_udf_access_tokens(max_requests=None)

        return UdfAccessTokenList(
            [token for token in all_tokens if token.udf_id == backend_id]
        )

    def _repr_html_(self) -> str:
        return fused_udf_repr(self)

    def _get_metadata_safe(
        self, key: str, default: Optional[Any] = None
    ) -> Optional[str]:
        if self.metadata is not None:
            return self.metadata.get(key, default)
        else:
            return None

    def _set_metadata_safe(self, key: str, value: Any):
        if self.metadata is None:
            self.metadata = {}

        self.metadata[key] = value

    def _generate_code(
        self, include_imports=True, headerfile=False
    ) -> Tuple[str, Sequence[str]]:
        def _extract_fn(src: str) -> Union[ast.FunctionDef, ast.AsyncFunctionDef]:
            # TODO: handle Header objects in header param
            parsed_ast = ast.parse(src)

            # Find all function definitions in the AST
            function_defs = [
                node
                for node in ast.walk(parsed_ast)
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            ]

            # first function (assume it's the target function)
            return function_defs[0]

        def _extract_fn_body(
            function_def: Union[ast.FunctionDef, ast.AsyncFunctionDef], src: str
        ) -> str:
            target_function_body = function_def.body
            # Reconstruct the source code of the function body
            line_start = target_function_body[0].lineno - 1
            line_end = target_function_body[-1].end_lineno
            target_function_body_lines = [
                line for line in src.splitlines()[line_start:line_end]
            ]
            target_function_body_str = "\n".join(target_function_body_lines)

            return target_function_body_str

        # Derive parameters
        positional_parameters, named_parameters = extract_parameters(self.code)

        _params_fn_original = positional_parameters + stringify_named_params(
            named_parameters
        )
        # String: Imports
        str_imports = (
            "\n".join(
                [
                    "import fused",
                    "from fused.models.udf import Header",
                ]
            )
            + "\n\n"
        )
        # String: UDF header - Replace Header with file reference
        header_files = []
        processed_headers = []
        # TODO: do this conversion as part of header attribute
        for header in self.headers:
            if isinstance(header, Header):
                if headerfile:
                    filename = header.module_name + ".py"
                    processed_headers.append(filename)

                else:
                    processed_headers.append(header)
                # Create a file magic string
                header_files.append(header._generate_cell_code())

            else:
                processed_headers.append(header)

        _headers = (
            stringify_headers(processed_headers) if headerfile else processed_headers
        )
        _schema = repr(self.table_schema.to_string()) if self.table_schema else '""'
        params_decorator = [f"\n    headers={_headers}", f"\n    schema={_schema}\n"]
        str_udf_header = (
            f"@fused.udf({structure_params(params_decorator, separator=',')})"
        )
        # String: Function header
        fn = _extract_fn(self.code)
        str_async = "async " if isinstance(fn, ast.AsyncFunctionDef) else ""
        str_fn_header = f"{str_async}def {self.entrypoint}({structure_params(_params_fn_original)}):"
        # String: Function body
        str_fn_body = dedent(_extract_fn_body(fn, src=self.code))

        str_udf = f"""
{str_udf_header}
{str_fn_header}
{indent(str_fn_body,  " " * 4)}
"""
        if include_imports:
            str_udf = str_imports + str_udf
        return str_udf.strip("\n"), header_files

    def render(self):
        from IPython import get_ipython
        from IPython.core.inputsplitter import IPythonInputSplitter

        # Get the current IPython instance.
        ipython = get_ipython()
        if ipython is None:
            raise RuntimeError("This function can only be used in a Jupyter Notebook.")

        # Create an instance of IPythonInputSplitter.
        splitter = IPythonInputSplitter()

        # Generate code string and split into lines.
        lines = self._generate_code()[0].strip().split("\n")

        # Set the content of the subsequent cell with.
        ipython.set_next_input(splitter.transform_cell("\n".join(lines)))

    @property
    def utils(self):
        return self._cached_utils

    @cached_property
    def _cached_utils(self):
        if len(self.headers) == 0:
            raise ValueError("UDF does not have a utils module")
        if len(self.headers) > 1:
            raise ValueError("UDF has multiple header modules")
        if self.headers[0].module_name != "utils":
            warnings.warn(
                FusedWarning(
                    f"Accessing header module {self.headers[0].module_name} under the name utils"
                ),
            )
        # TODO: Even though this might have already been evaluated, we have to evaluate it again now
        # It is at least cached

        vals = self.headers[0]._exec()

        return AttrDict(vals)

    model_config = ConfigDict(exclude={"utils"})


def _fetch_gist_content(gist_files_dict: Dict, fname: str) -> str:
    gist_data = gist_files_dict[fname]

    if gist_data["truncated"]:
        full_url = gist_data["raw_url"]
        full_r = requests.get(full_url, timeout=OPTIONS.request_timeout)
        full_r.raise_for_status()
        return full_r.text
    else:
        return gist_data["content"]

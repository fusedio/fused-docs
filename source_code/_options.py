import os
import warnings
from pathlib import Path
from typing import List, Optional, Tuple, Union

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    StrictStr,
    field_serializer,
    field_validator,
)

from ._global_api import reset_api
from .warnings import FusedIgnoredWarning, FusedImportWarning

DEV_DEFAULT_BASE_URL = "http://localhost:8783/v1"
PROD_DEFAULT_BASE_URL = "https://www.fused.io/server/v1"
PREVIEW_DEFAULT_BASE_URL = "https://www-preview.fused.io/server/v1"
STAGING_DEFAULT_BASE_URL = "https://www-staging.fused.io/server/v1"


OPTIONS_PATH = Path("~/.fused/settings.toml").expanduser()
"""First choice for where to find settings"""
OPTIONS_JSON_PATH = Path("~/.fused/settings.json").expanduser()
"""Second choice for where to find settings"""


class OptionsBaseModel(BaseModel):
    def __dir__(self) -> List[str]:
        # Provide method name lookup and completion. Only provide 'public'
        # methods.
        # This enables autocompletion
        # Pydantic methods to remove in __dir__
        PYDANTIC_METHODS = {
            "Config",
            "construct",
            "copy",
            "from_orm",
            "json",
            "parse_file",
            "parse_obj",
            "schema",
            "schema_json",
            "update_forward_refs",
            "validate",
            "model_validate",
            "model_dump_json",
        }

        normal_dir = {
            name
            for name in dir(type(self))
            if (not name.startswith("_") and name not in PYDANTIC_METHODS)
        }
        pydantic_fields = set(self.model_fields.keys())
        return sorted(normal_dir | pydantic_fields)

    def _repr_html_(self) -> str:
        # Circular import because the repr needs the options
        from fused._formatter.formatter_options import fused_options_repr

        return fused_options_repr(self)


class AuthOptions(OptionsBaseModel):
    authorize_url: str = "https://dev-tjcykxcetrz6bps6.us.auth0.com/authorize"
    """The authorize URL is used for the initial login flow. This is intended to be opened in
    the user's web browser for them to sign in."""

    oauth_token_url: str = "https://dev-tjcykxcetrz6bps6.us.auth0.com/oauth/token"
    """The token url is used for programmatic access to generate access and refresh tokens."""

    logout_url: str = "https://dev-tjcykxcetrz6bps6.us.auth0.com/oidc/logout"

    # The client id, client secret, and audience identifies a specific application and API
    client_id: str = "CXiwKZQmmyo0rqXZY7pzBgfsF7AL2A9l"
    client_secret: str = (
        "FVNz012KgNmqITYnCCOM8Q1Nt81W_DO4SeCRgVsftREKTWpzZU522nia5TdSNv8h"
    )
    audience: str = "fused-python-api"

    local_redirect_url: str = "http://localhost:3000"
    """This redirect uri is passed to the authorize URL as a url parameter. This localhost
    uri is used to intercept the "code" generated from the authorization"""

    scopes: List[str] = ["openid", "email", "name", "offline_access"]
    """The offline_access scope is necessary to be able to fetch refresh tokens
    The other scopes are useful to access identifying information in the retrieved JWT"""

    credentials_path: str = "~/.fused/credentials"
    """The path where the refresh token is saved on disk. Will be user-expanded to resolve ~."""


class ShowOptions(OptionsBaseModel):
    """Options for showing debug information"""

    open_browser: Optional[StrictBool] = None
    """Whether to open a local browser window for debug information"""
    show_widget: Optional[StrictBool] = None
    """Whether to show debug information in an IPython widget"""

    format_numbers: Optional[StrictBool] = None
    """Whether to format numbers in object reprs"""

    materialize_virtual_folders: StrictBool = True
    """Whether to automatically materialize virtual project folders in reprs"""


def _cache_directory() -> Path:
    mount_path = Path("/mount")
    # Cache in mounted drive if available & writable, else cache in /tmp
    if mount_path.exists() and os.access(mount_path, os.W_OK):
        base_path = mount_path
    else:
        base_path = Path("/tmp")
    return base_path / "cached_data"


class Options(OptionsBaseModel):
    base_url: str = PROD_DEFAULT_BASE_URL
    """Fused API endpoint"""

    auth: AuthOptions = Field(default_factory=AuthOptions)
    """Options for authentication."""

    show: ShowOptions = Field(default_factory=ShowOptions)
    """Options for object reprs and how data are shown for debugging."""

    max_workers: int = 16
    """Maximum number of threads, when multithreading requests"""

    request_timeout: Union[Tuple[float, float], float, None] = 120
    """Request timeout for the Fused service

    May be set to a tuple of connection timeout and read timeout"""

    realtime_client_id: Optional[StrictStr] = None
    """Client ID for realtime service."""

    save_user_settings: StrictBool = True
    """Save per-user settings such as credentials and environment IDs."""

    default_udf_run_engine: Optional[StrictStr] = None
    """Default engine to run UDFs, one of: `local`, `realtime`, `batch`."""

    default_validate_imports: StrictBool = False
    """Default for whether to validate imports in UDFs before `run_local`,
    `run_batch`."""

    prompt_to_login: StrictBool = False
    """Automatically prompt the user to login when importing Fused."""

    no_login: StrictBool = False
    """If set, Fused will not attempt to login automatically when needed."""

    pyodide_async_requests: StrictBool = False
    """If set, Fused is being called inside Pyodide and should use pyodide
    for async HTTP requests."""

    cache_directory: Path = Field(default_factory=_cache_directory)
    """ The base directory for storing cached results """

    @field_serializer("cache_directory")
    def _serialize_cache_directory(self, path: Path, _info) -> str:
        return str(path)

    @field_validator("base_url")
    @classmethod
    def _validate_base_url(cls, v):
        reset_api()
        return v

    @property
    def base_web_url(self):
        if self.base_url == STAGING_DEFAULT_BASE_URL:
            return "https://staging.fused.io"
        elif self.base_url == PREVIEW_DEFAULT_BASE_URL:
            return "https://preview.fused.io"

        return "https://www.fused.io"

    def save(self):
        """Save Fused options to `~/.fused/settings.toml`. They will be automatically
        reloaded the next time fused-py is imported.
        """
        try:
            import rtoml

            OPTIONS_PATH.parent.mkdir(parents=True, exist_ok=True)
            # None (null) will not be serialized correctly in toml, so exclude it.
            # Any option which can be None should be None by default. Some open options
            # don't do this; should be updated to not be Optional.
            rtoml.dump(
                self.model_dump(exclude_none=True, exclude_defaults=True), OPTIONS_PATH
            )
        except ImportError:
            warnings.warn(
                FusedImportWarning("rtoml is not installed so options are not saved")
            )

    def _to_toml(self) -> str:
        try:
            import rtoml

            return rtoml.dumps(
                self.model_dump(exclude_none=True, exclude_defaults=True)
            )
        except ImportError:
            warnings.warn(
                FusedImportWarning("rtoml is not installed so options are not saved")
            )

    model_config = ConfigDict(validate_assignment=True)


def _load_options():
    if OPTIONS_PATH.exists():
        try:
            import rtoml

            return Options.model_validate(rtoml.load(OPTIONS_PATH))
        except:  # noqa E722
            warnings.warn(
                FusedIgnoredWarning(
                    f"Settings file {OPTIONS_PATH} exists but could not be loaded."
                )
            )

    if OPTIONS_JSON_PATH.exists():
        try:
            import json

            with open(OPTIONS_JSON_PATH, "r") as json_file:
                return Options.model_validate(json.load(json_file))
        except:  # noqa E722
            warnings.warn(
                FusedIgnoredWarning(
                    f"Settings file {OPTIONS_JSON_PATH} exists but could not be loaded."
                )
            )

    return Options()


options = _load_options()
"""List global configuration options.

This object contains a set of configuration options that control global behavior of the library. This object can be used to modify the options.

Examples:
    Change the `request_timeout` option from its default value to 120 seconds:
    ```py
    fused.options.request_timeout = 120
    ```
"""


def env(environment_name: str):
    """Set the environment."""
    if environment_name == "dev":
        _env = DEV_DEFAULT_BASE_URL
    elif environment_name == "stg":
        _env = STAGING_DEFAULT_BASE_URL
    elif environment_name == "prod":
        _env = PROD_DEFAULT_BASE_URL
    elif environment_name == "pre":
        _env = PREVIEW_DEFAULT_BASE_URL
    else:
        raise ValueError("Available options are `dev`, `stg`, `prod`, and `pre`.")

    setattr(options, "base_url", _env)

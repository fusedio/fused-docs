from __future__ import annotations

import shutil
import time
import uuid
import warnings
from functools import lru_cache
from io import SEEK_END, SEEK_SET
from pathlib import Path
from tempfile import TemporaryFile
from typing import (
    TYPE_CHECKING,
    Any,
    BinaryIO,
    Dict,
    Iterable,
    List,
    Literal,
    Optional,
    Sequence,
    Union,
    overload,
)

if TYPE_CHECKING:
    import geopandas as gpd
    import pandas as pd

import requests

import fused
import fused.models.request as request_models
from fused._auth import AUTHORIZATION
from fused._deserialize_parquet import parquet_to_df
from fused._global_api import set_api, set_api_class
from fused._optional_deps import HAS_PANDAS, PD_DATAFRAME
from fused._options import (
    DEV_DEFAULT_BASE_URL,
    PROD_DEFAULT_BASE_URL,
    STAGING_DEFAULT_BASE_URL,
)
from fused._options import options as OPTIONS
from fused._request import raise_for_status
from fused._str_utils import detect_passing_local_file_as_str
from fused.models.api import (
    JobConfig,
    JobStepConfig,
    ListDetails,
    UdfAccessToken,
    UdfAccessTokenList,
)
from fused.models.internal import Jobs, RunResponse
from fused.models.internal.job import CoerceableToJobId, _object_to_job_id
from fused.models.request import WHITELISTED_INSTANCE_TYPES
from fused.models.udf._udf_registry import UdfRegistry
from fused.models.udf.base_udf import METADATA_FUSED_EXPLORER_TAB
from fused.models.udf.udf import AnyBaseUdf, load_udf_from_response_data
from fused.warnings import (
    FusedIgnoredWarning,
    FusedNonProductionWarning,
    FusedOnPremWarning,
    FusedWarning,
)

UDF_LOCAL_SERVER_URL = "http://127.0.0.1:8000"


def _detect_upload_length(data: Union[bytes, BinaryIO]) -> int:
    if hasattr(data, "tell") and hasattr(data, "seek"):
        # Looks like an IO, try to get size that way
        data.seek(0, SEEK_END)
        length = data.tell()
        # Reset to beginning
        data.seek(0, SEEK_SET)
        return length

    return len(data)


def resolve_udf_server_url(
    client_id: Optional[str] = None, *, base_url: Optional[str] = None
) -> str:
    if client_id == "_local" or OPTIONS.realtime_client_id == "_local":
        return UDF_LOCAL_SERVER_URL

    if client_id and client_id.endswith("-staging"):
        return f"{base_url or STAGING_DEFAULT_BASE_URL}/realtime/{client_id}"

    if client_id is None:
        api = FusedAPI()
        client_id = api._automatic_realtime_client_id()

        if client_id is None:
            raise ValueError("Failed to detect realtime client ID")

    return f"{base_url or OPTIONS.base_url}/realtime/{client_id}"


class FusedAPI:
    """API for running jobs in the Fused service."""

    base_url: str

    def __init__(
        self,
        *,
        base_url: Optional[str] = None,
        set_global_api: bool = True,
        credentials_needed: bool = True,
    ):
        """Create a FusedAPI instance.

        Keyword Args:
            base_url: The Fused instance to send requests to. Defaults to `https://www.fused.io/server/v1`.
            set_global_api: Set this as the global API object. Defaults to True.
            credentials_needed: If True, automatically attempt to log in. Defaults to True.
        """
        if credentials_needed:
            AUTHORIZATION.initialize()
        base_url = base_url or OPTIONS.base_url

        self.base_url = base_url
        self._check_is_prod()

        if set_global_api:
            set_api(self)

    def _check_is_prod(self):
        if self.base_url in [STAGING_DEFAULT_BASE_URL, DEV_DEFAULT_BASE_URL]:
            warnings.warn(
                FusedNonProductionWarning(
                    "FusedAPI is connected to a development environment"
                )
            )
        elif self.base_url != PROD_DEFAULT_BASE_URL:
            warnings.warn(
                FusedOnPremWarning("FusedAPI is connected to an on-prem environment")
            )

    def download_table_bbox(
        self,
        path: str,
        minx: float,
        miny: float,
        maxx: float,
        maxy: float,
        n_rows: Optional[int] = None,
        columns: Optional[List[str]] = None,
        clip: bool = True,
        buffer: Optional[float] = None,
    ) -> Union["pd.DataFrame", "gpd.GeoDataFrame"]:
        url = f"{self.base_url}/table/download/bbox"

        params = request_models.GetTableBboxRequest(
            path=path,
            bbox_minx=minx,
            bbox_miny=miny,
            bbox_maxx=maxx,
            bbox_maxy=maxy,
            n_rows=n_rows,
            columns=columns,
            clip=clip,
            buffer=buffer,
        )

        self._check_is_prod()
        r = requests.get(
            url=url,
            params=params.model_dump(),
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return parquet_to_df(r.content)

    def start_job(
        self,
        config: Union[JobConfig, JobStepConfig],
        *,
        instance_type: Optional[WHITELISTED_INSTANCE_TYPES] = None,
        region: Optional[str] = None,
        disk_size_gb: Optional[int] = None,
        additional_env: Optional[Sequence[str]] = ("FUSED_CREDENTIAL_PROVIDER=ec2",),
        image_name: Optional[str] = None,
    ) -> RunResponse:
        """Execute an operation

        Args:
            config: the configuration object to run in the job.

        Keyword Args:
            instance_type: The AWS EC2 instance type to use for the job. Acceptable strings are "m5.large", "m5.xlarge", "m5.2xlarge", "m5.4xlarge", "r5.large", "r5.xlarge", "r5.2xlarge", "r5.4xlarge". Defaults to None.
            region: The AWS region in which to run. Defaults to None.
            disk_size_gb: The disk size to specify for the job. Defaults to None.
            additional_env: Any additional environment variables to be passed into the job, each in the form KEY=value. Defaults to None.
            image_name: Custom image name to run. Defaults to None for default image.
        """
        url = f"{self.base_url}/run"

        if isinstance(config, JobStepConfig):
            config = JobConfig(steps=[config])

        body = {"config": config.model_dump()}
        if additional_env:
            body["additional_env"] = additional_env
        if image_name:
            body["image_name"] = image_name

        params = request_models.StartJobRequest(
            region=region,
            instance_type=instance_type,
            disk_size_gb=disk_size_gb,
        )

        self._check_is_prod()
        r = requests.post(
            url=url,
            params=params.model_dump(),
            json=body,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return RunResponse.model_validate_json(r.content)

    def save_udf(
        self,
        udf: AnyBaseUdf,
        slug: Optional[str] = None,
        id: Optional[str] = None,
        allow_public_read: bool = False,
        allow_public_list: bool = False,
    ) -> UdfRegistry:
        url = f"{self.base_url}/udf/by-id/{id}" if id else f"{self.base_url}/udf/new"
        body = request_models.SaveUdfRequest(
            slug=slug,
            udf_body=udf.model_dump_json(),
            udf_type=request_models.UdfType.auto,
            allow_public_read=allow_public_read,
            allow_public_list=allow_public_list,
        )

        self._check_is_prod()
        r = requests.post(
            url=url,
            json=body.model_dump(),
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        # TODO: body
        return r.json()

    def delete_saved_udf(self, id: str):
        url = f"{self.base_url}/udf/by-id/{id}"

        self._check_is_prod()
        r = requests.delete(
            url=url,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        # TODO: body
        return r.json()

    def _get_udf(
        self,
        email_or_handle_or_id: str,
        slug: Optional[str] = None,
    ):
        if slug is None:  # first arg is id
            slug = email_or_handle_or_id
            email = self._whoami()["email"]
            url = f"{self.base_url}/udf/by-user-email/{email}/by-slug/{slug}"
        else:
            if "@" in email_or_handle_or_id:  # all valid email addresses contain @
                url = f"{self.base_url}/udf/by-user-email/{email_or_handle_or_id}/by-slug/{slug}"
            else:
                url = f"{self.base_url}/udf/by-user-handle/{email_or_handle_or_id}/by-slug/{slug}"

        r = requests.get(
            url=url,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return r.json()

    def _get_udf_by_id(self, id: str):
        url = f"{self.base_url}/udf/by-id/{id}"
        r = requests.get(
            url=url,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return r.json()

    def _get_public_udf(
        self,
        id: str,
    ):
        url = f"{self.base_url}/udf/public/by-slug/{id}"

        r = requests.get(
            url=url,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return r.json()

    def _get_code_by_url(self, url: str):
        req_url = f"{self.base_url}/code-proxy/by-url"

        r = requests.get(
            url=req_url,
            params={
                "url": url,
            },
            headers=self._generate_headers(credentials_needed=False),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return r.json()

    def get_udfs(
        self,
        n: int = 5,
        *,
        skip: int = 0,
        per_request: int = 25,
        max_requests: Optional[int] = 1,
        by: Literal["name", "id", "slug"] = "name",
        whose: Literal["self", "public", "community", "team"] = "self",
    ):
        request_count = 0
        has_content = True
        udfs = []

        assert per_request >= 0

        while has_content:
            if whose == "self":
                url = f"{self.base_url}/udf/self"
            elif whose == "public" or whose == "community":
                url = f"{self.base_url}/udf/public"
            elif whose == "team":
                url = f"{self.base_url}/udf/exec-env/self"
            else:
                raise ValueError(
                    'Invalid value for `whose`, should be one of: "self", "public", "community", "team"'
                )

            params = request_models.ListUdfsRequest(
                skip=skip,
                limit=per_request,
            )
            skip += per_request

            r = requests.get(
                url=url,
                params=params.model_dump(),
                headers=self._generate_headers(),
                timeout=OPTIONS.request_timeout,
            )
            raise_for_status(r)
            udfs_this_request = r.json()
            if udfs_this_request:
                udfs.extend(udfs_this_request)
            else:
                has_content = False

            request_count += 1
            if len(udfs) >= n or (
                max_requests is not None and request_count == max_requests
            ):
                break

        deserialized_udfs = {}
        for udf in udfs:
            if "udf_body" in udf and udf["udf_body"]:
                try:
                    deserialized_udf = load_udf_from_response_data(udf)
                    udf_id = (
                        deserialized_udf.name
                        if by == "name"
                        else (
                            udf["id"]
                            if by == "id"
                            else (udf["slug"] if by == "slug" else None)
                        )
                    )

                    filtered_public_udf = (
                        whose == "public"
                        and deserialized_udf._get_metadata_safe(
                            METADATA_FUSED_EXPLORER_TAB
                        )
                        == "community"
                    ) or (
                        whose == "community"
                        and deserialized_udf._get_metadata_safe(
                            METADATA_FUSED_EXPLORER_TAB
                        )
                        != "community"
                    )

                    if udf_id is not None and not filtered_public_udf:
                        deserialized_udfs[udf_id] = deserialized_udf
                except Exception as e:
                    warnings.warn(
                        FusedWarning(
                            f"UDF {udf['slug']} ({udf['id']}) could not be deserialized: {e}"
                        ),
                    )
        return UdfRegistry(deserialized_udfs)

    def get_udf_access_tokens(
        self,
        n: Optional[int] = None,
        *,
        skip: int = 0,
        per_request: int = 25,
        max_requests: Optional[int] = 1,
        _whose: Literal["self", "all"] = "self",
    ) -> UdfAccessTokenList:
        request_count = 0
        has_content = True
        tokens = []

        assert per_request >= 0

        while has_content:
            url = f"{self.base_url}/udf-access-token/{_whose}"

            params = request_models.ListUdfAccessTokensRequest(
                skip=skip,
                limit=per_request,
            )
            skip += per_request

            r = requests.get(
                url=url,
                params=params.model_dump(),
                headers=self._generate_headers(),
                timeout=OPTIONS.request_timeout,
            )
            raise_for_status(r)
            tokens_this_request = r.json()
            if tokens_this_request:
                tokens.extend(tokens_this_request)
            else:
                has_content = False

            request_count += 1
            if n is not None and (
                len(tokens) >= n
                or (max_requests is not None and request_count == max_requests)
            ):
                break

        tokens_deserialized = UdfAccessTokenList()
        for token in tokens:
            token_deserialized = UdfAccessToken.model_validate(token)
            token_deserialized.udf_email = self._whoami()["email"]
            tokens_deserialized.append(token_deserialized)

        return tokens_deserialized

    def get_udf_access_token(
        self,
        token: Union[str, UdfAccessToken],
    ) -> UdfAccessToken:
        if isinstance(token, UdfAccessToken):
            token = token.token
        url = f"{self.base_url}/udf-access-token/by-token/{token}"

        r = requests.get(
            url=url,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        token_obj = UdfAccessToken.model_validate_json(r.content)
        token_obj.udf_email = self._whoami()["email"]
        token_obj.udf_slug = self._get_udf_by_id(token_obj.udf_id)["slug"]
        return token_obj

    def delete_udf_access_token(
        self,
        token: Union[str, UdfAccessToken],
    ) -> UdfAccessToken:
        if isinstance(token, UdfAccessToken):
            token = token.token
        url = f"{self.base_url}/udf-access-token/by-token/{token}"

        r = requests.delete(
            url=url,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        token_obj = UdfAccessToken.model_validate_json(r.content)
        token_obj.udf_email = self._whoami()["email"]
        token_obj.udf_slug = self._get_udf_by_id(token_obj.udf_id)["slug"]
        return token_obj

    def update_udf_access_token(
        self,
        token: Union[str, UdfAccessToken],
        *,
        client_id: Optional[str] = None,
        cache: Optional[bool] = None,
        metadata_json: Optional[Dict[str, Any]] = None,
        enabled: Optional[bool] = None,
    ) -> UdfAccessToken:
        if isinstance(token, UdfAccessToken):
            token = token.token
        url = f"{self.base_url}/udf-access-token/by-token/{token}"

        body = request_models.UpdateUdfAccessTokenRequest(
            client_id=client_id,
            cache=cache,
            metadata_json=metadata_json,
            enabled=enabled,
        ).model_dump()  # type: ignore

        r = requests.post(
            url=url,
            json=body,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        token_obj = UdfAccessToken.model_validate_json(r.content)
        token_obj.udf_email = self._whoami()["email"]
        token_obj.udf_slug = self._get_udf_by_id(token_obj.udf_id)["slug"]
        return token_obj

    def create_udf_access_token(
        self,
        udf_email_or_name_or_id: Optional[str] = None,
        /,
        udf_name: Optional[str] = None,
        *,
        udf_email: Optional[str] = None,
        udf_id: Optional[str] = None,
        client_id: Union[str, Ellipsis, None] = ...,
        cache: bool = True,
        metadata_json: Optional[Dict[str, Any]] = None,
        enabled: bool = True,
    ) -> UdfAccessToken:
        """
        Create a token for running a UDF. The token allows anyone who has it to run
        the UDF, with the parameters they choose. The UDF will run under your environment.

        The token does not allow running any other UDF on your account.

        Args:
            udf_email_or_name_or_id: A UDF ID, email address (for use with udf_name), or UDF name.
            udf_name: The name of the UDF to create the token for.

        Keyword Args:
            udf_email: The email of the user owning the UDF, or, if udf_name is None, the name of the UDF.
            udf_id: The backend ID of the UDF to create the token for.
            client_id: If specified, overrides which realtime environment to run the UDF under.
            cache: If True, UDF tiles will be cached.
            metadata_json: Additional metadata to serve as part of the tiles metadata.json.
            enable: If True, the token can be used.
        """
        if udf_id is not None:
            if (
                udf_name is not None
                or udf_email is not None
                or udf_email_or_name_or_id is not None
            ):
                warnings.warn(
                    FusedIgnoredWarning(
                        "All other ways of specifying the UDF are ignored in favor of udf_id."
                    ),
                )
                udf_name = None
                udf_email = None
        elif udf_name is not None:
            if udf_email_or_name_or_id is not None:
                if udf_email is not None:
                    warnings.warn(
                        FusedIgnoredWarning(
                            "All other ways of specifying the UDF are ignored in favor of the first argument and udf_name."
                        ),
                    )
                udf_email = udf_email_or_name_or_id
        elif udf_email_or_name_or_id is not None:
            if udf_name is not None:
                udf_email = udf_email_or_name_or_id
            else:
                # Need to figure out what exactly the first argument is and how it specifies a UDF
                is_valid_uuid = True
                try:
                    uuid.UUID(udf_email_or_name_or_id)
                except ValueError:
                    is_valid_uuid = False
                if is_valid_uuid:
                    udf_id = udf_email_or_name_or_id
                elif "/" in udf_email_or_name_or_id:
                    udf_email, udf_name = udf_email_or_name_or_id.split("/", maxsplit=1)
                else:
                    udf_name = udf_email_or_name_or_id
                    udf_email = self._whoami()["email"]
        else:
            raise ValueError("No UDF specified to create an access token for.")

        if client_id is Ellipsis:
            client_id = self._automatic_realtime_client_id()

        if client_id is Ellipsis:
            raise ValueError("Failed to detect realtime client ID")

        url = f"{self.base_url}/udf-access-token/new"

        metadata_json = metadata_json or {}

        body = request_models.CreateUdfAccessTokenRequest(
            udf_email=udf_email,
            udf_slug=udf_name,
            udf_id=udf_id,
            client_id=client_id,
            cache=cache,
            metadata_json=metadata_json,
            enabled=enabled,
        ).model_dump()  # type: ignore

        r = requests.post(
            url=url,
            json=body,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        token_obj = UdfAccessToken.model_validate_json(r.content)
        token_obj.udf_email = self._whoami()["email"]
        token_obj.udf_slug = self._get_udf_by_id(token_obj.udf_id)["slug"]
        return token_obj

    def get_secret_value(
        self,
        key: str,
        client_id: Optional[str] = None,
    ) -> str:
        """Retrieve a secret value from the Fused service."""
        if client_id is None:
            client_id = self._automatic_realtime_client_id()

        if client_id is None:
            raise ValueError("Failed to detect realtime client ID")

        url = f"{resolve_udf_server_url(client_id=client_id, base_url=self.base_url)}/api/v1/secrets/{key}"

        r = requests.get(
            url=url,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return r.json()

    def set_secret_value(
        self,
        key: str,
        value: str,
        client_id: Optional[str] = None,
    ) -> str:
        """Set a secret value on the Fused service."""
        if client_id is None:
            client_id = self._automatic_realtime_client_id()

        if client_id is None:
            raise ValueError("Failed to detect realtime client ID")

        body = request_models.UpdateSecretRequest(value=value).model_dump()
        url = f"{resolve_udf_server_url(client_id=client_id, base_url=self.base_url)}/api/v1/secrets/{key}"

        r = requests.put(
            url=url,
            json=body,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return r.json()

    def delete_secret_value(
        self,
        key: str,
        client_id: Optional[str] = None,
    ) -> str:
        """Delete a secret value on the Fused service."""
        if client_id is None:
            client_id = self._automatic_realtime_client_id()

        if client_id is None:
            raise ValueError("Failed to detect realtime client ID")

        url = f"{resolve_udf_server_url(client_id=client_id, base_url=self.base_url)}/api/v1/secrets/{key}"

        r = requests.delete(
            url=url,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return r.json()

    def list_secrets(
        self,
        client_id: Optional[str] = None,
    ) -> Iterable[str]:
        """List available secret values on the Fused service.

        This may also be used to retrieve all secrets."""
        if client_id is None:
            client_id = self._automatic_realtime_client_id()

        if client_id is None:
            raise ValueError("Failed to detect realtime client ID")

        url = f"{resolve_udf_server_url(client_id=client_id, base_url=self.base_url)}/api/v1/secrets"

        r = requests.get(
            url=url,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return r.json().keys()

    def get_jobs(
        self,
        n: int = 5,
        *,
        skip: int = 0,
        per_request: int = 25,
        max_requests: Optional[int] = 1,
    ) -> Jobs:
        """Get the job history.

        Args:
            n: The number of jobs to fetch. Defaults to 5.

        Keyword Args:
            skip: Where in the job history to begin. Defaults to 0, which retrieves the most recent job.
            per_request: Number of jobs per request to fetch. Defaults to 25.
            max_requests: Maximum number of requests to make. May be None to fetch all jobs. Defaults to 1.

        Returns:
            The job history.
        """
        request_count = 0
        has_content = True
        jobs = []
        original_skip = skip

        assert per_request >= 0

        while has_content:
            url = f"{self.base_url}/job/self"

            params = request_models.ListJobsRequest(
                skip=skip,
                limit=per_request,
            )
            skip += per_request

            r = requests.get(
                url=url,
                params=params.model_dump(),
                headers=self._generate_headers(),
                timeout=OPTIONS.request_timeout,
            )
            raise_for_status(r)
            jobs_this_request = r.json()
            if jobs_this_request:
                jobs.extend(jobs_this_request)
            else:
                has_content = False

            request_count += 1
            if len(jobs) >= n or (
                max_requests is not None and request_count == max_requests
            ):
                break

        return Jobs(
            jobs=jobs[:n],
            n=n,
            skip=original_skip,
            per_request=per_request,
            max_requests=max_requests,
        )

    def get_job_config(self, job: CoerceableToJobId) -> JobConfig:
        job_id = _object_to_job_id(job)
        url = f"{self.base_url}/job/by-id/{job_id}/config"

        r = requests.get(
            url=url,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
            allow_redirects=False,
        )
        raise_for_status(r)

        redirect_location = r.headers["location"]

        r2 = requests.get(
            url=redirect_location,
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r2)

        return JobConfig.model_validate_json(r2.content)

    def get_status(self, job: CoerceableToJobId) -> RunResponse:
        """Fetch the status of a running job

        Args:
            job: the identifier of a job or a `RunResponse` object.

        Returns:
            The status of the given job.
        """
        job_id = _object_to_job_id(job)
        url = f"{self.base_url}/run/by-id/{job_id}"

        r = requests.get(
            url=url,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return RunResponse.model_validate_json(r.content)

    def get_logs(
        self,
        job: CoerceableToJobId,
        since_ms: Optional[int] = None,
    ) -> List[Any]:
        """Fetch logs for a job

        Args:
            job: the identifier of a job or a `RunResponse` object.
            since_ms: Timestamp, in milliseconds since epoch, to get logs for. Defaults to None for all logs.

        Returns:
            Log messages for the given job.
        """
        job_id = _object_to_job_id(job)
        url = f"{self.base_url}/logs/{job_id}"
        params = {}
        if since_ms is not None:
            params["since_ms"] = since_ms
        r = requests.get(
            url=url,
            params=params,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return r.json()

    def tail_logs(
        self,
        job: CoerceableToJobId,
        refresh_seconds: float = 1,
        sample_logs: bool = True,
        timeout: Optional[float] = None,
        get_logs_retries: int = 1,
    ):
        """Continuously print logs for a job

        Args:
            job: the identifier of a job or a `RunResponse` object.
            refresh_seconds: how frequently, in seconds, to check for new logs. Defaults to 1.
            sample_logs: if true, print out only a sample of logs. Defaults to True.
            timeout: if not None, how long to continue tailing logs for. Defaults to None for indefinite.
            get_logs_retries: Number of additional retries for log requests. Defaults to 1.
        """
        # TODO: Move this to the RunResponse object
        start_time = time.time()
        job = self.get_status(job)
        print(f"Logs for: {job.job_id}")

        def _tail_get_logs(
            job: RunResponse, since_ms: Optional[int] = None
        ) -> List[Any]:
            for _ in range(get_logs_retries + 1):
                try:
                    return self.get_logs(job, since_ms=since_ms)
                except requests.exceptions.RequestException:
                    # TODO: Don't use bare except
                    print("Server did not respond with logs")
                    # TODO: Backoff strategy
                    time.sleep(refresh_seconds)
            raise ValueError("Server did not respond with logs")

        r = _tail_get_logs(job)
        if job.status not in ["running", "pending"]:
            print(f"Job is not running ({job.status})")
            return

        if len(r) == 0:
            print("Configuring packages and waiting for logs...")
            while len(r) == 0:
                time.sleep(refresh_seconds)
                r = _tail_get_logs(job)
                if timeout is not None and time.time() - start_time > timeout:
                    raise TimeoutError("Timed out waiting for logs")

        last_message: Optional[str] = None
        last_since_ms: Optional[int] = None
        while True:
            time.sleep(refresh_seconds)
            r = _tail_get_logs(job, since_ms=last_since_ms)
            # If any results -- there may be none because we are filtering them with since_ms
            if len(r):
                current_message: str = r[-1]["message"]
                if last_message != current_message:
                    # If the most recent log line has changed, print it out
                    last_message = current_message
                    last_since_ms = r[-1]["timestamp"]

                    if sample_logs:
                        print(current_message.rstrip())
                    else:
                        for message in r:
                            print(message["message"].rstrip())

            if "ERROR" in current_message or self.get_status(job).status != "running":
                # Try to detect exit scenarios: an error has occured and the job will stop,
                # or the job is no longer in a running state.
                return

            if timeout is not None and time.time() - start_time > timeout:
                raise TimeoutError("Timed out")

    def wait_for_job(
        self,
        job: CoerceableToJobId,
        poll_interval_seconds: float = 5,
        timeout: Optional[float] = None,
    ) -> RunResponse:
        """Block the Python kernel until the given job has finished

        Args:
            job: the identifier of a job or a `RunResponse` object.
            poll_interval_seconds: How often (in seconds) to poll for status updates. Defaults to 5.
            timeout: The length of time in seconds to wait for the job. Defaults to None.

        Raises:
            TimeoutError: if waiting for the job timed out.

        Returns:
            The status of the given job.
        """
        # TODO: Move this to the RunResponse object
        start_time = time.time()
        status = self.get_status(job)
        while not status.terminal_status:
            time.sleep(poll_interval_seconds)
            status = self.get_status(job)
            if timeout is not None and time.time() - start_time > timeout:
                raise TimeoutError("Timed out waiting for job")
        return status

    def cancel_job(self, job: CoerceableToJobId) -> RunResponse:
        """Cancel an existing job

        Args:
            job: the identifier of a job or a `RunResponse` object.

        Returns:
            A new job object.
        """
        job_id = _object_to_job_id(job)
        url = f"{self.base_url}/run/by-id/{job_id}/cancel"

        self._check_is_prod()
        r = requests.post(
            url=url,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return RunResponse.model_validate_json(r.content)

    def _whoami(self) -> Any:
        """
        Returns information on the currently logged in user
        """
        url = f"{self.base_url}/user/self"

        r = requests.get(
            url=url,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return r.json()

    def _list_realtime_instances(self, *, whose: str = "self") -> List[Any]:
        """
        Returns information about available realtime instances
        """
        url = f"{self.base_url}/realtime-instance"
        if whose == "self":
            url += "/available"
        else:
            assert whose == "public", "whose must be 'public' or 'self'"

        r = requests.get(
            url=url,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return r.json()

    def _automatic_realtime_client_id(self) -> Optional[str]:
        client_id = OPTIONS.realtime_client_id
        if client_id is None:
            instances = self._list_realtime_instances()
            if len(instances):
                instances = sorted(
                    instances,
                    key=lambda instance: instance.get("preference_rank", 0),
                    reverse=True,
                )
                client_id = instances[0]["client_id"]
            if OPTIONS.save_user_settings and client_id:
                OPTIONS.realtime_client_id = client_id

        return client_id

    @overload
    def list(self, path: str, *, details: Literal[True]) -> List[ListDetails]:
        ...

    @overload
    def list(self, path: str, *, details: Literal[False] = False) -> List[str]:
        ...

    def list(
        self, path: str, *, details: bool = False, client_id: Optional[str] = None
    ):
        list_request_url = f"{self.base_url}/files/list{'-details' if details else ''}"

        params = request_models.ListPathRequest(path=path).model_dump()
        if client_id is None:
            client_id = self._automatic_realtime_client_id()
        if client_id:
            params["client_id"] = client_id

        r = requests.get(
            url=list_request_url,
            params=params,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        result = r.json()
        if details:
            result = [ListDetails.model_validate(detail) for detail in result]
        return result

    def delete(
        self,
        path: str,
        max_deletion_depth: Union[int, Literal["unlimited"]] = 2,
        *,
        client_id: Optional[str] = None,
    ) -> bool:
        delete_request_url = f"{self.base_url}/files/delete"

        params = request_models.DeletePathRequest(
            path=path,
            max_deletion_depth=max_deletion_depth,
        ).model_dump()
        if client_id is None:
            client_id = self._automatic_realtime_client_id()
        if client_id:
            params["client_id"] = client_id

        r = requests.delete(
            url=delete_request_url,
            params=params,
            json="{}",
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return r.json()

    def _resolve(
        self,
        path: str,
    ) -> List[str]:
        resolve_request_url = f"{self.base_url}/files/resolve"

        params = request_models.ResolvePathRequest(
            path=path,
        )

        r = requests.post(
            url=resolve_request_url,
            params=params.model_dump(),
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return r.json()

    def get(self, path: str, *, client_id: Optional[str] = None) -> bytes:
        get_request_url = f"{self.base_url}/files/get"

        params = request_models.GetPathRequest(path=path).model_dump()
        if client_id is None:
            client_id = self._automatic_realtime_client_id()
        if client_id:
            params["client_id"] = client_id

        r = requests.get(
            url=get_request_url,
            params=params,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
            allow_redirects=True,
        )
        raise_for_status(r)
        return r.content

    def download(
        self,
        path: str,
        local_path: Union[str, Path],
        *,
        client_id: Optional[str] = None,
    ) -> None:
        get_request_url = f"{self.base_url}/files/get"

        params = request_models.GetPathRequest(path=path).model_dump()
        if client_id is None:
            client_id = self._automatic_realtime_client_id()
        if client_id:
            params["client_id"] = client_id

        r = requests.get(
            url=get_request_url,
            params=params,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
            allow_redirects=True,
            stream=True,
        )
        raise_for_status(r)
        with open(local_path, "wb") as f:
            shutil.copyfileobj(r.raw, f)

    def sign_url(self, path: str, *, client_id: Optional[str] = None) -> str:
        sign_request_url = f"{self.base_url}/files/sign"

        params = request_models.SignPathRequest(path=path).model_dump()
        if client_id is None:
            client_id = self._automatic_realtime_client_id()
        if client_id:
            params["client_id"] = client_id

        r = requests.get(
            url=sign_request_url,
            params=params,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return r.json()

    def sign_url_prefix(
        self, path: str, *, client_id: Optional[str] = None
    ) -> Dict[str, str]:
        sign_prefix_request_url = f"{self.base_url}/files/sign_prefix"

        params = request_models.SignPathRequest(path=path).model_dump()
        if client_id is None:
            client_id = self._automatic_realtime_client_id()
        if client_id:
            params["client_id"] = client_id

        r = requests.get(
            url=sign_prefix_request_url,
            params=params,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return r.json()

    def upload(self, path: str, data: Union[bytes, BinaryIO]) -> None:
        """Upload a binary blob to a cloud location"""
        return self._upload_signed(path=path, data=data)

    def _upload_tmp(self, extension: str, data: Union[bytes, BinaryIO]) -> str:
        """Upload a binary blob to a temporary cloud location, and return the new URL"""
        return self._upload_tmp_signed(extension=extension, data=data)

    def _upload_signed(
        self,
        path: str,
        data: Union[bytes, BinaryIO],
        *,
        client_id: Optional[str] = None,
    ) -> None:
        """Upload a binary blob to a cloud location"""
        upload_url = f"{self.base_url}/files/sign-upload"

        params = request_models.SignUploadRequest(
            path=path, content_length=_detect_upload_length(data)
        ).model_dump()
        if client_id is None:
            client_id = self._automatic_realtime_client_id()
        if client_id:
            params["client_id"] = client_id

        r = requests.get(
            url=upload_url,
            params=params,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        signed_post = r.json()

        r2 = requests.post(
            url=signed_post["url"],
            data=signed_post["fields"],
            files={"file": data},
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r2)

    def _upload_tmp_signed(
        self,
        extension: str,
        data: Union[bytes, BinaryIO],
        *,
        client_id: Optional[str] = None,
    ) -> str:
        """Upload a binary blob to a temporary cloud location, and return the new URL"""
        upload_temp_url = f"{self.base_url}/files/sign-upload-temp"

        params = request_models.SignUploadTempRequest(
            extension=extension, content_length=_detect_upload_length(data)
        ).model_dump()
        if client_id is None:
            client_id = self._automatic_realtime_client_id()
        if client_id:
            params["client_id"] = client_id

        r = requests.get(
            url=upload_temp_url,
            params=params,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        sign_details = r.json()

        signed_post = sign_details["signed_post"]
        r2 = requests.post(
            url=signed_post["url"],
            data=signed_post["fields"],
            files={"file": data},
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r2)

        return sign_details["storage_url"]

    def _upload_direct(
        self,
        path: str,
        data: Union[bytes, BinaryIO],
        *,
        client_id: Optional[str] = None,
    ) -> None:
        """Upload a binary blob to a cloud location"""
        upload_url = f"{self.base_url}/files/upload"

        params = request_models.UploadRequest(path=path).model_dump()
        if client_id is None:
            client_id = self._automatic_realtime_client_id()
        if client_id:
            params["client_id"] = client_id

        r = requests.put(
            url=upload_url,
            params=params,
            headers=self._generate_headers(
                {"Content-Type": "application/octet-stream"}
            ),
            data=data,
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)

    def _upload_tmp_direct(
        self,
        extension: str,
        data: Union[bytes, BinaryIO],
        *,
        client_id: Optional[str] = None,
    ) -> str:
        """Upload a binary blob to a temporary cloud location, and return the new URL"""
        upload_temp_url = f"{self.base_url}/files/upload-temp"

        params = request_models.UploadTempRequest(extension=extension).model_dump()
        if client_id is None:
            client_id = self._automatic_realtime_client_id()
        if client_id:
            params["client_id"] = client_id

        r = requests.post(
            url=upload_temp_url,
            params=params,
            headers=self._generate_headers(
                {"Content-Type": "application/octet-stream"}
            ),
            data=data,
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return r.json()

    def _upload_local_input(
        self, input: Union[str, Path, List[Union[str, Path]], "gpd.GeoDataFrame"]
    ) -> Union[str, List[str]]:
        """Upload local input (in-memory DataFrame or path to local file(s)).

        If uploaded, return a URL to it. Otherwise return input unchanged.
        """
        # in-memory (Geo)DataFrame
        if HAS_PANDAS and isinstance(input, PD_DATAFRAME):
            with TemporaryFile() as tmp:
                input.to_parquet(tmp)
                tmp.seek(0, SEEK_SET)
                input = self._upload_tmp(extension="parquet", data=tmp)
                return input

        # local file path(s)
        def _upload_path(input_path: Path) -> str:
            with open(input_path, "rb") as f:
                extension = input_path.name.rsplit(".", 1)[-1]
                uploaded_input = self._upload_tmp(extension=extension, data=f)
            return uploaded_input

        if isinstance(input, (str, Path)):
            input = detect_passing_local_file_as_str(input)
            if isinstance(input, Path):
                return _upload_path(input)
            else:
                # not a local file path, return as is
                return input
        elif isinstance(input, list):
            uploaded_inputs = []
            for input_path in input:
                input_path = detect_passing_local_file_as_str(input_path)
                if isinstance(input_path, Path):
                    uploaded_inputs.append(_upload_path(input_path))
                else:
                    uploaded_inputs.append(input_path)
            return uploaded_inputs
        else:
            raise TypeError(f"Unsupported input type: {type(input)}")

    def _health(self) -> bool:
        """Check the health of the API backend"""
        r = requests.get(f"{self.base_url}/health", timeout=OPTIONS.request_timeout)
        raise_for_status(r)
        return True

    def auth_token(self) -> str:
        """
        Returns the current user's Fused environment (team) auth token
        """
        url = f"{self.base_url}/execution-env/token"

        r = requests.get(
            url=url,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return r.json()

    def _generate_headers(
        self,
        headers: Optional[Dict[str, str]] = None,
        *,
        credentials_needed: bool = True,
    ) -> Dict[str, str]:
        if headers is None:
            headers = {}

        common_headers = {
            "Fused-Py-Version": fused.__version__,
            **headers,
        }

        if AUTHORIZATION.is_configured() or credentials_needed:
            common_headers[
                "Authorization"
            ] = f"{AUTHORIZATION.credentials.auth_scheme} {AUTHORIZATION.credentials.access_token}"

        return common_headers

    @lru_cache
    def dependency_whitelist(self) -> str:
        sign_request_url = f"{self.base_url}/internal/dependency-whitelist"
        r = requests.get(
            url=sign_request_url,
            headers=self._generate_headers(),
            timeout=OPTIONS.request_timeout,
        )
        raise_for_status(r)
        return r.json()


set_api_class(FusedAPI)

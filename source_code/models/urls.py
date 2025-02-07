from typing import Union

from pydantic import FileUrl, UrlConstraints
from pydantic_core import SchemaValidator, Url, core_schema
from typing_extensions import Annotated

S3Url = Annotated[Url, UrlConstraints(allowed_schemes=["s3"])]
GCSUrl = Annotated[Url, UrlConstraints(allowed_schemes=["gs"])]
FusedIntermediaryUrl = Annotated[
    Url, UrlConstraints(allowed_schemes=["fused_intermediary"])
]
FusedTeamUrl = Annotated[Url, UrlConstraints(allowed_schemes=["fd"])]


DatasetUrl = Union[S3Url, GCSUrl, FileUrl, FusedIntermediaryUrl, FusedTeamUrl]

dataset_url_schema = core_schema.url_schema()
dataset_url_schema_validator = SchemaValidator(dataset_url_schema)

from __future__ import annotations

from enum import Enum
from typing import Literal, Optional
from urllib.parse import urlparse

from pydantic import BaseModel, Field, StrictBool, StrictStr
from typing_extensions import Annotated

from fused._str_utils import append_url_part


class SampleStrategy(str, Enum):
    """How to generate output samples"""

    EMPTY = "empty"
    """Do not generate a sample"""
    FIRST_CHUNK = "first_chunk"
    """The sample is from the first chunk"""
    GEO = "geo"
    """Geographically sample"""


class DatasetOutputType(str, Enum):
    V2 = "v2"
    """Save as a table to a URL"""


class DatasetOutputBase(BaseModel):
    type: Literal[None, "v2"]

    save_index: Optional[StrictBool] = None
    """Whether to override saving the output index."""

    sample_strategy: Optional[SampleStrategy] = None
    """How to generate output samples, or None for the default."""

    overwrite: bool = False
    """Whether the API should overwrite the output dataset if it already exists."""

    def from_str(
        s: Optional[str], project_url: Optional[str] = None
    ) -> AnyDatasetOutput:
        try:
            parsed = urlparse(s)
            if parsed.scheme:
                output = DatasetOutputV2(url=s)
                output._project_url = project_url
                return output
        except (ValueError, TypeError, AttributeError):
            pass

        if project_url is not None:
            url = append_url_part(project_url, s) if s is not None else None
            output = DatasetOutputV2(url=url)
            output._project_url = project_url
            return output

        if s is None:
            return DatasetOutputV2()

        # Parsing as URL failed
        raise ValueError("failed to parse URL")


class DatasetOutputV2(DatasetOutputBase):
    """Output that writes a table to a URL"""

    type: Literal["v2"] = "v2"

    url: Optional[StrictStr] = None
    """Table URL to write to"""

    @property
    def table(self) -> Optional[str]:
        """Returns the table name for this output"""
        if self.url:
            return self.url.rstrip("/").rsplit("/", maxsplit=1)[1]
        return None


AnyDatasetOutput = Annotated[
    DatasetOutputV2,
    Field(..., discriminator="type"),
]

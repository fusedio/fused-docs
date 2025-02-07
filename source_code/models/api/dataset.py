from __future__ import annotations

from typing import Optional, Tuple

from pydantic import ConfigDict

from fused.models.api.job import AnyJobStepConfig
from fused.models.base import FusedBaseModel
from fused.models.udf.udf import AnyBaseUdf

from ..request import WHITELISTED_INSTANCE_TYPES


class JobMetadata(FusedBaseModel):
    ec2_instance_type: Optional[WHITELISTED_INSTANCE_TYPES] = None
    """The EC2 instance this job is run on."""

    step_config: AnyJobStepConfig
    time_taken: Optional[float] = None
    """The time taken for the job, if known."""

    job_id: Optional[str] = None
    """The fused id for the job."""

    @property
    def job(self) -> AnyJobStepConfig:
        """The job step config that created this table."""
        return self.step_config

    @property
    def udf(self) -> Optional[AnyBaseUdf]:
        """The user-defined function that created this table."""
        if hasattr(self.step_config, "udf"):
            return self.step_config.udf

        return None

    @property
    def udf_code(self) -> Optional[str]:
        """The code string of the user-defined function that created this table."""
        udf = self.udf
        if udf is not None:
            return udf.code

        return None

    @property
    def inputs(self) -> Tuple:
        """The datasets that were combined to create this table."""
        if hasattr(self.step_config, "input"):
            return (self.step_config.input,)

    # We ignore extra keys because some keys are only useful for the backend
    model_config = ConfigDict(extra="ignore")

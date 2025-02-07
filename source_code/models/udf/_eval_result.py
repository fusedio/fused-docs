from typing import Any, List, Optional, Union

from pydantic import BaseModel, ConfigDict

from fused._formatter.formatter_eval_result import fused_eval_result_repr
from fused.models.schema import Schema
from fused.models.udf import AnyBaseUdf


class UdfEvaluationResult(BaseModel):
    data: Any = None
    sidecar: Optional[bytes] = None

    udf: Optional[AnyBaseUdf] = None
    table_schema: Optional[Schema] = None

    time_taken_seconds: float

    stdout: Optional[str] = None
    stderr: Optional[str] = None
    has_exception: bool = False
    exception_class: Optional[str] = None
    error_message: Optional[str] = None
    error_lineno: Optional[int] = None

    def _repr_html_(self) -> str:
        return fused_eval_result_repr(self)

    model_config = ConfigDict(arbitrary_types_allowed=True)


class MultiUdfEvaluationResult(BaseModel):
    udf_results: List[Union[UdfEvaluationResult, Any]]

    def _repr_html_(self) -> str:
        # Aggregate reprs
        result_reprs = [
            udf_result._repr_html_()
            if hasattr(udf_result, "_repr_html_")
            else repr(udf_result)
            for udf_result in self.udf_results
        ]
        return "<br><br>".join(result_reprs)

    model_config = ConfigDict(arbitrary_types_allowed=True)

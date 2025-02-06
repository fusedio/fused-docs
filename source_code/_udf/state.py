from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fused.models.udf import AnyBaseUdf


noop_decorators: ContextVar[bool] = ContextVar("noop_decorator", default=False)
decorator_src_override: ContextVar[str | None] = ContextVar(
    "decorator_src_override", default=None
)
decorator_udf_override: ContextVar[AnyBaseUdf | None] = ContextVar(
    "decorator_udf_override", default=None
)


@contextmanager
def noop_decorators_context(val: bool):
    token = noop_decorators.set(val)
    try:
        yield token
    finally:
        noop_decorators.reset(token)


# Provides the UDF's code to the fused.udf decorator via the global context (above).
#
# Injecting the UDF code back inside the run function.
@contextmanager
def decorator_src_override_context(val: str):
    token = decorator_src_override.set(val)
    try:
        yield token
    finally:
        decorator_src_override.reset(token)


@contextmanager
def decorator_udf_override_context(udf: AnyBaseUdf):
    token = decorator_udf_override.set(udf)
    try:
        yield token
    finally:
        decorator_udf_override.reset(token)

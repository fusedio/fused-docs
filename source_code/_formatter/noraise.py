import warnings
from typing import Any, Callable, Optional

from fused.warnings import FusedWarning


def noraise(
    fn: Optional[Callable] = None,
    *,
    incompat_version_message: Optional[str] = None,
    message: Optional[str] = None,
    default: Optional[Any] = None,
):
    rendered_message = "Failed, and no additional information is available."
    if message:
        rendered_message = message
    elif incompat_version_message:
        rendered_message = f"{incompat_version_message}. You may have an incompatible version of fused-py -- try upgrading to latest."

    def _internal_noraise_wrapper(func):
        def _internal_noraise(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:  # noqa: E722
                warnings.warn(FusedWarning(rendered_message))
                return default

        return _internal_noraise

    if fn is not None:
        return _internal_noraise_wrapper(fn)
    else:
        return _internal_noraise_wrapper

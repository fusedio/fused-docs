from typing import Callable, Optional


def _noop_udf_internal(
    fn: Optional[Callable] = None,
    **kwargs,
):
    if fn is not None:
        return fn
    else:
        return lambda fn2: fn2


udf = _noop_udf_internal

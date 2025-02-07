import base64
import functools
import hashlib
import inspect
import os
import pickle
import types
from typing import Any, Awaitable, Callable, Optional, TypeVar

from loguru import logger

from fused._options import options as OPTIONS


def _serialize_code(code: types.CodeType) -> bytes:
    func_code_bytes = base64.b64encode(code.co_code)

    # Introduce variable values into hash.
    func_const_values = [
        # Embedded lambdas must be serialized, same as the overall function
        (
            _serialize_code(const)
            if isinstance(const, types.CodeType)
            else str(const).encode("utf-8")
        )
        for const in code.co_consts
    ]
    # Names must be serialized as otherwise referenced names (min vs max) would not
    # affect cache key.
    func_name_values = [name.encode("utf-8") for name in code.co_names]

    return b"".join(
        [
            func_code_bytes,
            *func_const_values,
            *func_name_values,
        ]
    )


def _serialize_function_defaults(func: Callable) -> bytes:
    parts = []

    if func.__defaults__ is not None:
        for d in func.__defaults__:
            parts.append(_hashify(d).encode("utf-8"))

    if func.__kwdefaults__ is not None:
        for key, value in func.__kwdefaults__.items():
            parts.append(f"{key}{_hashify(value)}".encode("utf-8"))

    return b"".join(parts)


def _hashify(func) -> str:
    hash_object = hashlib.sha256()
    try:
        if hasattr(func, "__fused_cached_fn"):
            return _hashify(func.__fused_cached_fn)
        elif callable(func):
            hash_object.update(_serialize_code(func.__code__))
            # Caution! The defaults and args do not go into the same part of the cache key!
            hash_object.update(_serialize_function_defaults(func))
        else:
            hash_object.update(str(func).encode("utf-8"))
        return hash_object.hexdigest()
    except Exception as e:
        logger.warning(f"Error Hashing {e}")
        return ""


def _cache(
    func: Callable,
    *args,
    reset: bool = False,
    path: str = "tmp",
    retry: bool = True,
    **kwargs,
):
    path = path.strip("/")

    # Cache directory
    # TODO: consider udf name in path once available from Fused global context
    path = OPTIONS.cache_directory / path
    path.mkdir(parents=True, exist_ok=True)

    # Pop reserved `_cache_id`kwarg
    _cache_id = kwargs.pop("_cache_id", None)

    try:
        # TODO: ignore `_`

        # 1. Hashify function
        id = _hashify(func)

        # 2. Hashify args
        for v in args:
            id += "_" + _hashify(v)

        # 3. Hashify kwargs
        for k in kwargs:
            id += k + _hashify(kwargs[k])

        # 4. Hashify _cache_id
        id += _hashify(_cache_id)

        # 5. Hashify composite id
        id = _hashify(id)

        path_file = path / f"data_{id}"

        if not os.path.exists(path_file) or reset:
            with open(path_file, "wb") as f:
                data = func(*args, **kwargs)
                pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
                return data
        else:
            try:
                with open(path_file, "rb") as f:
                    data = pickle.load(f)

                    print(f"{func.__qualname__} was cached")
                    return data
            except Exception:
                logger.debug("Cache not found, retrying.")
                if retry:
                    with open(path_file, "wb") as f:
                        data = func(*args, **kwargs)
                        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
                        return data
                else:
                    return None
    except Exception as e:
        logger.info(f"Error Caching {e}")
        raise e


async def _cache_async(
    func: Callable,
    *args,
    reset: bool = False,
    path: str = "tmp",
    retry: bool = True,
    **kwargs,
):
    path = path.strip("/")

    # Cache directory
    # TODO: consider udf name in path once available from Fused global context
    path = OPTIONS.cache_directory / path
    path.mkdir(parents=True, exist_ok=True)

    # Pop reserved `_cache_id`kwarg
    _cache_id = kwargs.pop("_cache_id", None)

    try:
        # TODO: ignore `_`

        # 1. Hashify function
        id = _hashify(func)

        # 2. Hashify args
        for v in args:
            id += "_" + _hashify(v)

        # 3. Hashify kwargs
        for k in kwargs:
            id += k + _hashify(kwargs[k])

        # 4. Hashify _cache_id
        id += _hashify(_cache_id)

        # 5. Hashify composite id
        id = _hashify(id)

        path_file = path / f"data_{id}"

        if not os.path.exists(path_file) or reset:
            with open(path_file, "wb") as f:
                data = await func(*args, **kwargs)
                pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
                return data
        else:
            try:
                with open(path_file, "rb") as f:
                    data = pickle.load(f)

                    print(f"{func.__qualname__} was cached")
                    return data
            except Exception:
                logger.debug("Cache not found, retrying.")
                if retry:
                    with open(path_file, "wb") as f:
                        data = await func(*args, **kwargs)
                        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
                        return data
                else:
                    return None
    except Exception as e:
        logger.info(f"Error Caching {e}")
        raise e


def _cache_internal(func, **decorator_kwargs):
    def decorator(func):
        _path = decorator_kwargs.get("path", "tmp")

        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def wrapper_async(*args, **kwargs):
                return await _cache_async(func, *args, path=_path, **kwargs)

            wrapper_async.__fused_cached_fn = func

            return wrapper_async
        else:

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return _cache(func, *args, path=_path, **kwargs)

            wrapper.__fused_cached_fn = func

            return wrapper

    if callable(func):  # w/o args
        return decorator(func)
    else:  # w/ args
        return decorator


def cache(
    func: Optional[Callable[..., Any]] = None, **kwargs: Any
) -> Callable[..., Any]:
    """Decorator to cache the return value of a function.

    This function serves as a decorator that can be applied to any function
    to cache its return values. The cache behavior can be customized through
    keyword arguments.

    Args:
        func (Callable, optional): The function to be decorated. If None, this
            returns a partial decorator with the passed keyword arguments.
        **kwargs: Arbitrary keyword arguments that are passed to the internal
            caching mechanism. These could specify cache size, expiration time,
            and other cache-related settings.

    Returns:
        Callable: A decorator that, when applied to a function, caches its
        return values according to the specified keyword arguments.

    Examples:

        Use the `@cache` decorator to cache the return value of a function in a custom path.

        ```py
        @cache(path="/tmp/custom_path/")
        def expensive_function():
            # Function implementation goes here
            return result
        ```

        If the output of a cached function changes, for example if remote data is modified,
        it can be reset by running the function with the `reset` keyword argument. Afterward,
        the argument can be cleared.

        ```py
        @cache(path="/tmp/custom_path/", reset=True)
        def expensive_function():
            # Function implementation goes here
            return result
        ```
    """
    return _cache_internal(func=func, **kwargs)


T = TypeVar("T")


def cache_call(func: Callable[..., T], *args: Any, **kwargs: Any) -> T:
    """Directly calls a function with caching.

    This function directly calls the provided function with the given arguments
    and keyword arguments, caching its return value. The cache used depends on
    the implementation of the `_cache` function.

    Args:
        func (Callable): The function to call and cache its result.
        *args: Positional arguments to pass to the function.
        **kwargs: Keyword arguments to pass to the function.

    Returns:
        The cached return value of the function.

    Raises:
        Exception: Propagates any exception raised by the function being called
        or the caching mechanism.
    """
    return _cache(func, *args, **kwargs)


async def cache_call_async(
    func: Callable[..., Awaitable[T]], *args: Any, **kwargs: Any
) -> T:
    """Asynchronously calls a function with caching.

    Similar to `cache_call`, but for asynchronous functions. This function
    awaits the provided async function, caches its return value, and then
    returns it. The specifics of the caching mechanism depend on the
    implementation of `_cache_async`.

    Args:
        func (Callable): The asynchronous function to call and cache its result.
        *args: Positional arguments to pass to the async function.
        **kwargs: Keyword arguments to pass to the async function.

    Returns:
        The cached return value of the async function.

    Raises:
        Exception: Propagates any exception raised by the async function being
        called or the caching mechanism.

    Examples:
        async def fetch_data(param):
            # Async function implementation goes here
            return data

        # Usage
        result = await cache_call_async(fetch_data, 'example_param')
    """
    return await _cache_async(func, *args, **kwargs)

---
sidebar_label: _cache
title: fused.core._cache
---

## cache

```python showLineNumbers
def cache(func: Optional[Callable[..., Any]] = None,
          **kwargs: Any) -> Callable[..., Any]
```

Decorator to cache the return value of a function.

This function serves as a decorator that can be applied to any function
to cache its return values. The cache behavior can be customized through
keyword arguments.

**Arguments**:

- `func` _Callable, optional_ - The function to be decorated. If None, this
  returns a partial decorator with the passed keyword arguments.
- `**kwargs` - Arbitrary keyword arguments that are passed to the internal
  caching mechanism. These could specify cache size, expiration time,
  and other cache-related settings.


**Returns**:

- `Callable` - A decorator that, when applied to a function, caches its
  return values according to the specified keyword arguments.


**Examples**:


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

## cache\_call

```python showLineNumbers
def cache_call(func: Callable[..., T], *args: Any, **kwargs: Any) -> T
```

Directly calls a function with caching.

This function directly calls the provided function with the given arguments
and keyword arguments, caching its return value. The cache used depends on
the implementation of the `_cache` function.

**Arguments**:

- `func` _Callable_ - The function to call and cache its result.
- `*args` - Positional arguments to pass to the function.
- `**kwargs` - Keyword arguments to pass to the function.


**Returns**:

  The cached return value of the function.


**Raises**:

- `Exception` - Propagates any exception raised by the function being called
  or the caching mechanism.

## cache\_call\_async

```python showLineNumbers
async def cache_call_async(func: Callable[..., Awaitable[T]], *args: Any,
                           **kwargs: Any) -> T
```

Asynchronously calls a function with caching.

Similar to `cache_call`, but for asynchronous functions. This function
awaits the provided async function, caches its return value, and then
returns it. The specifics of the caching mechanism depend on the
implementation of `_cache_async`.

**Arguments**:

- `func` _Callable_ - The asynchronous function to call and cache its result.
- `*args` - Positional arguments to pass to the async function.
- `**kwargs` - Keyword arguments to pass to the async function.


**Returns**:

  The cached return value of the async function.


**Raises**:

- `Exception` - Propagates any exception raised by the async function being
  called or the caching mechanism.


**Examples**:

  ```py
  async def fetch_data(param):
  # Async function implementation goes here
  return data

  # Usage
  result = await cache_call_async(fetch_data, 'example_param')
  ```

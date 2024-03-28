---
sidebar_label: _options
title: fused._options
---

## OpenOptions Objects

```python
class OpenOptions(OptionsBaseModel)
```

Options for opening tables and projects.

## fetch\_samples

Whether to automatically fetch samples when opening tables

## fetch\_table\_metadata

Whether to automatically fetch table metadata when opening projects

## fetch\_minimal\_table\_metadata

Whether to fetch only a minimal set of table metadata when opening projects

## auto\_refresh\_project

Automatically refresh project objects when accessing a key that is not present locally

## ShowOptions Objects

```python
class ShowOptions(OptionsBaseModel)
```

Options for showing debug information

## open\_browser

Whether to open a local browser window for debug information

## show\_widget

Whether to show debug information in an IPython widget

## format\_numbers

Whether to format numbers in object reprs

## materialize\_virtual\_folders

Whether to automatically materialize virtual project folders in reprs

## CacheOptions Objects

```python
class CacheOptions(OptionsBaseModel)
```

Options for caching samples

## enable

Whether to enable caching

## Options Objects

```python
class Options(OptionsBaseModel)
```

## base\_url

Fused API endpoint

## open

Options for `fused.open_table` and `fused.open_project`.

## show

Options for object reprs and how data are shown for debugging.

## cache

Options for caching data fused-py can retrieve, such as
the sample for `run_local`.

## max\_workers

Maximum number of threads, when multithreading requests

## request\_timeout

Request timeout for the Fused service

May be set to a tuple of connection timeout and read timeout

## realtime\_client\_id

Client ID for realtime service.

## save\_user\_settings

Save per-user settings such as credentials and environment IDs.

## default\_udf\_run\_engine

Default engine to run UDFs, one of: `local`, `realtime`, `batch`.

## default\_validate\_imports

Default for whether to validate imports in UDFs before `run_local`,
`run_batch`.

## save

```python
def save()
```

Save Fused options to `~/.fused/settings.toml`. They will be automatically
reloaded the next time fused-py is imported.

## options

List global configuration options.

This object contains a set of configuration options that control global behavior of the library. This object can be used to modify the options.

**Examples**:

  Change the `request_timeout` option from its default value to 120 seconds:
    ```py
    fused.options.request_timeout = 120
    ```

## set\_option

```python
def set_option(option_name: str, option_value: Any)
```

Sets the value of a configuration option.

This function updates the global `options` object with a new value for a specified option.
It supports setting values for nested options using dot notation. For example, if the
`options` object has a nested structure, you can set a value for a nested attribute
by specifying the option name in the form "parent.child".

**Arguments**:

- `option_name` - A string specifying the name of the option to set. This can be a simple
  attribute name or a dot-separated path for nested attributes.
- `option_value` - The new value to set for the specified option. This can be of any type
  that is compatible with the attribute being set.
  

**Raises**:

- `AttributeError` - If the specified attribute path is not valid, either because a part
  of the path does not exist or the final attribute cannot be set with
  the provided value.
  

**Examples**:

  Set the `request_timeout` top-level option to 120 seconds:
    ```py
    set_option('request_timeout', 120)
    ```

## \_env

```python
def _env(environment_name: str)
```

Set the environment.


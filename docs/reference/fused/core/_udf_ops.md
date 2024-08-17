---
sidebar_label: _udf_ops
title: fused.core._udf_ops
---

## load\_udf\_from\_fused

```python
def load_udf_from_fused(email_or_id: str,
                        id: Optional[str] = None,
                        *,
                        cache_key: Any = None) -> BaseUdf
```

Download the code of a UDF, to be run inline.

**Arguments**:

- `email_or_id` - Email of the UDF's owner, or name of the UDF to import.
- `id` - Name of the UDF to import. If only the first argument is provided, the current user's email will be used.
- `cache_key` - Additional cache key for busting the UDF cache.

## load\_udf\_from\_github

```python
def load_udf_from_github(url: str, *, cache_key: Any = None) -> BaseUdf
```

Download the code of a UDF, to be run inline.

**Arguments**:

- `email_or_id` - Email of the UDF's owner, or name of the UDF to import.
- `id` - Name of the UDF to import. If only the first argument is provided, the current user's email will be used.
- `cache_key` - Additional cache key for busting the UDF cache.

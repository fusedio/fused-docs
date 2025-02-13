---
sidebar_label: base_udf
title: models.udf.base_udf
toc_max_heading_level: 5
unlisted: true
---

## AttrDict Objects

```python
class AttrDict(dict)
```

Dictionary where keys can also be accessed as attributes

## BaseUdf Objects

```python
class BaseUdf(BaseModel)
```

#### from\_gist

```python
@classmethod
def from_gist(cls, gist_id: str)
```

Create a Udf from a GitHub gist.

#### to\_fused

```python
def to_fused(slug: Optional[str] = ...,
             over_id: Union[str, UUID, None] = None,
             as_new: Optional[bool] = None,
             inplace: bool = True)
```

Save this UDF on the Fused service.

**Arguments**:

- `slug` - ID to refer to this UDF as in URLs.
- `over_id` - ID to save the UDF over.
- `as_new` - If True, force saving this UDF as new.
- `inplace` - If True (default), update the UDF object with the new saved ID.


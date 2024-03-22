---
sidebar_label: header
title: fused.models.udf.header
---

## Header Objects

```python
class Header(BaseModel)
```

A header represents a reusable source module included with a UDF.

#### module\_name

The name by which the header may be imported

#### source\_code

The code of the header module

#### source\_file

The name of the original source file

#### from\_code

```python
@classmethod
def from_code(cls,
              module_name: str,
              source_file: str,
              source: Literal["disk", "url"] = "disk")
```

Read a header from a location.

**Arguments**:

- `module_name` - The name by which the module may be imported
- `source_file` - Where to read from
- `source` - Source type, must be `"disk"` (read a file from disk) or `"url"` (read a file from URL)


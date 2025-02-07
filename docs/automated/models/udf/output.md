---
sidebar_label: output
title: models.udf.output
toc_max_heading_level: 5
unlisted: true
---

## PandasOutput Objects

```python
class PandasOutput(Output)
```

#### data

The output DataFrame or GeoDataFrame.

#### table\_schema

A schema describing the output table.

#### initialize\_table\_schema

```python
@model_validator(mode="before")
@classmethod
def initialize_table_schema(cls, values)
```

If table_schema is not passed, initialize one from the data argument


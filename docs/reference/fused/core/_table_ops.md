---
sidebar_label: _table_ops
title: fused.core._table_ops
---

## get\_chunks\_metadata

```python
def get_chunks_metadata(url: str) -> gpd.GeoDataFrame
```

Returns a GeoDataFrame with each chunk in the table as a row.

**Arguments**:

- `url` - URL of the table.

## get\_chunk\_from\_table

```python
def get_chunk_from_table(
        url: str,
        file_id: Union[str, int, None],
        chunk_id: Optional[int],
        *,
        columns: Optional[Iterable[str]] = None) -> gpd.GeoDataFrame
```

Returns a chunk from a table and chunk coordinates.

This can be called with file_id and chunk_id from `get_chunks_metadata`.

**Arguments**:

- `url` - URL of the table.
- `file_id` - File ID to read.
- `chunk_id` - Chunk ID to read.


**Arguments**:

- `columns` - Read only the specified columns.

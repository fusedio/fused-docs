from typing import TYPE_CHECKING, Iterable, Optional, Union

from ._impl._table_ops_impl import get_chunk_from_table as _get_chunk_from_table
from ._impl._table_ops_impl import get_chunks_metadata as _get_chunks_metadata

if TYPE_CHECKING:
    import geopandas as gpd


def get_chunks_metadata(url: str) -> "gpd.GeoDataFrame":
    """Returns a GeoDataFrame with each chunk in the table as a row.

    Args:
        url: URL of the table.
    """
    return _get_chunks_metadata(url)


def get_chunk_from_table(
    url: str,
    file_id: Union[str, int, None],
    chunk_id: Optional[int],
    *,
    columns: Optional[Iterable[str]] = None,
) -> "gpd.GeoDataFrame":
    """Returns a chunk from a table and chunk coordinates.

    This can be called with file_id and chunk_id from `get_chunks_metadata`.

    Args:
        url: URL of the table.
        file_id: File ID to read.
        chunk_id: Chunk ID to read.

    Keyword Args:
        columns: Read only the specified columns.
    """
    return _get_chunk_from_table(
        url=url,
        file_id=file_id,
        chunk_id=chunk_id,
        columns=columns,
    )

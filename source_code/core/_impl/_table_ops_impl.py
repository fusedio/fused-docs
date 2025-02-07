import base64
from io import BytesIO
from typing import TYPE_CHECKING, Iterable, Optional, Union

if TYPE_CHECKING:
    import geopandas as gpd


def _normalize_url(url: str) -> str:
    if url.endswith("/"):
        return url[:-1]
    return url


def get_chunks_metadata(url: str) -> "gpd.GeoDataFrame":
    """Returns a GeoDataFrame with each chunk in the table as a row.

    Args:
        url: URL of the table.
    """
    import geopandas as gpd
    import pandas as pd
    import pyarrow.parquet as pq
    import shapely

    url = _normalize_url(url) + "/_sample"

    with pq.ParquetFile(url) as file:
        # do not use pq.read_metadata as it may segfault in versions >= 12 (tested on 15.0.1)
        sample_metadata = file.metadata

    if (
        b"fused:format_version" not in sample_metadata.metadata.keys()
        or sample_metadata.metadata[b"fused:format_version"] != b"5"
    ):
        raise ValueError(
            "Dataset does not have Fused metadata or it is an incompatible version."
        )

    metadata_bytes = sample_metadata.metadata[b"fused:_metadata"]
    metadata_bytes = base64.decodebytes(metadata_bytes)
    metadata_bio = BytesIO(metadata_bytes)
    df = pd.read_parquet(metadata_bio)
    geoms = shapely.box(
        df["bbox_minx"], df["bbox_miny"], df["bbox_maxx"], df["bbox_maxy"]
    )
    return gpd.GeoDataFrame(df, geometry=geoms, crs="EPSG:4326")


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
    """
    import geopandas as gpd
    import geopandas.io.arrow
    import pyarrow.parquet as pq

    if file_id is None:
        data = gpd.read_parquet(url)
    else:
        url = _normalize_url(url) + f"/{file_id}.parquet"

        with pq.ParquetFile(url) as file:
            if chunk_id is not None:
                table = file.read_row_group(chunk_id, columns=columns)
            else:
                table = file.read(columns=columns)

            if b"geo" in table.schema.metadata:
                data = geopandas.io.arrow._arrow_to_geopandas(table)
            else:
                data = table.to_pandas()

    if isinstance(data, (gpd.GeoDataFrame, gpd.GeoSeries)):
        if data.crs is None:
            data = data.set_crs(4326)
    return data

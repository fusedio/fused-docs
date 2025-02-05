from io import BytesIO
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    import geopandas as gpd
    import pandas as pd


def parquet_to_df(b: bytes) -> Union["pd.DataFrame", "gpd.GeoDataFrame"]:
    try:
        import geopandas as gpd

        return gpd.read_parquet(BytesIO(b))
    except:  # noqa: E722
        import pandas as pd

        return pd.read_parquet(BytesIO(b))

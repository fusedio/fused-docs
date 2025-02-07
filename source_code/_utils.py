from typing import Any, Union

from fused.core._impl._udf_ops_impl import get_step_config_from_server

from .core._impl._reimports import AttrDict


class _PublicUtils:
    """
    A class designed to dynamically access utils of public UDFs, fetching their configuration
    from the server.

    Methods:
        __init__(self, cache_key: Any = None): Initializes the _Public instance with an optional cache key.
        __getattribute__(self, key: str) -> Union[Any, AttrDict]: Attempts to access class attributes, falling back to fetching the attribute's configuration from a server if not found.
        __getitem__(self, key: str) -> AttrDict: Fetches the configuration for the given key from a server and returns a utility object for execution.
    """

    def __init__(self, cache_key: Any = None):
        """
        Initializes the _Public instance with an optional cache key.

        Parameters:
            cache_key (Any, optional): A key used for caching purposes. Defaults to None.
        """
        self._cache_key = cache_key

    def __getattribute__(self, key: str) -> Union[Any, AttrDict]:
        try:
            return super().__getattribute__(key)
        except AttributeError:
            try:
                return self[key]
            # Note that we need to raise an AttributeError, **not a KeyError** so that
            # IPython's _repr_html_ works here
            except KeyError:
                raise AttributeError(
                    f"object of type {type(self).__name__} has no attribute {key}"
                ) from None

    def __getitem__(self, key: str) -> AttrDict:
        step_config = get_step_config_from_server(
            email_or_handle=None,
            slug=key,
            cache_key=self._cache_key,
            _is_public=True,
        )

        return step_config.udf.utils


utils = _PublicUtils()
"""
A module to access utility functions located in the UDF called "common".

They can be imported by other UDFs with `common = fused.public.common`. They contain common operations such as:
- read_shape_zip
- url_to_arr
- get_collection_bbox
- read_tiff_pc
- table_to_tile
- rasterize_geometry


Examples:

    This example shows how to access the `geo_buffer` function from the `common` UDF.
    ```python
    import fused
    import geopandas as gpd

    gdf = gpd.read_file('https://www2.census.gov/geo/tiger/TIGER_RD18/STATE/11_DISTRICT_OF_COLUMBIA/11/tl_rd22_11_bg.zip')
    gdf_buffered = fused.public.common.geo_buffer(gdf, 10)
    ```

    This example shows how to load a table with `table_to_tile`, which efficiently loads a table by filtering and adjusting based on the provided bounding box (bbox) and zoom level.
    ```python
    table_path = "s3://fused-asset/infra/census_bg_us"
    gdf = fused.public.common.table_to_tile(
        bbox, table_path, use_columns=["GEOID", "geometry"], min_zoom=12
    )
    ```

    This example shows how to use `rasterize_geometry` to place an input geometry within an image array.
    ```python
    geom_masks = [
        rasterize_geometry(geom, arr.shape[-2:], transform) for geom in gdf.geometry
    ]
    ```

Public UDFs are listed at https://github.com/fusedio/udfs/tree/main/public
"""

import inspect
import json
import uuid
from io import StringIO
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Union, get_args, get_origin

try:
    from types import UnionType
except ImportError:
    # compatibility with Python 3.9
    UnionType = type(Union[int, str])

import geopandas as gpd
import mercantile
import pandas as pd
import shapely

if TYPE_CHECKING:
    from fused.types import Bbox, TileGDF, TileXYZ


FALSE_CASEFOLDED = "false".casefold()
GEOJSON_CRS = 4326


def _parse_bbox(val: str) -> Union[list, gpd.GeoDataFrame]:
    deserialized = json.loads(val)
    if isinstance(deserialized, list):
        return deserialized
    return gpd.GeoDataFrame.from_features(deserialized, crs=GEOJSON_CRS)


def _parse_to_gdf(val: Any) -> gpd.GeoDataFrame:
    if isinstance(val, gpd.GeoDataFrame):
        return val
    elif isinstance(val, str):
        deserialized = json.loads(val)
        if isinstance(deserialized, list):
            return gpd.GeoDataFrame(
                {}, geometry=[shapely.box(*deserialized)], crs=GEOJSON_CRS
            )
        return gpd.GeoDataFrame.from_features(deserialized, crs=GEOJSON_CRS)
    raise NotImplementedError(f"Not sure how to convert type `{val}` to GeoDataFrame")


def _parse_to_df(val: Any) -> pd.DataFrame:
    if isinstance(val, pd.DataFrame):
        return val
    elif isinstance(val, str):
        return pd.read_json(StringIO(val))
    raise NotImplementedError(f"Not sure how to convert type `{val}` to DataFrame")


def convert_to_tile_gdf(val: Any, add_xyz: bool = True) -> "TileGDF":
    if isinstance(val, str):
        val = _parse_bbox(val)
    if isinstance(val, list):
        val = gpd.GeoDataFrame({}, geometry=[shapely.box(*val)], crs=GEOJSON_CRS)
    if isinstance(val, gpd.GeoDataFrame):
        if add_xyz and not all(c in val.columns for c in ["x", "y", "z"]):
            tile = mercantile.bounding_tile(*val.total_bounds)
            val = val.assign(x=tile.x, y=tile.y, z=tile.z)
            val = val[["x", "y", "z", "geometry"]]
        return val

    raise NotImplementedError(f"Not sure how to convert type `{val}` to TileGDF")


def convert_to_tile_xyz(val: Any) -> "TileXYZ":
    if isinstance(val, str):
        val = _parse_bbox(val)
    if isinstance(val, gpd.GeoDataFrame):
        if all(c in val.columns for c in ["x", "y", "z"]):
            return mercantile.Tile(*val.iloc[0][["x", "y", "z"]])
        else:
            return mercantile.bounding_tile(*val.total_bounds)
    if isinstance(val, list):
        return mercantile.bounding_tile(*val)
    raise NotImplementedError(f"not sure how to convert type `{val}` to TileXYZ")


def convert_to_bbox(val: Any) -> "Bbox":
    if isinstance(val, str):
        val = _parse_bbox(val)
    if isinstance(val, list):
        return shapely.box(*val)
    if isinstance(val, gpd.GeoDataFrame):
        return shapely.box(*val.total_bounds)
    raise NotImplementedError(f"not sure how to convert type `{val}` to Bbox")


def _resolve_annotation(annotation):
    if annotation is inspect._empty:
        return annotation

    origin = get_origin(annotation)
    if origin is not None:
        if origin is Union or origin is UnionType:
            args = get_args(annotation)
            # Handle Optional and (x | None)
            if len(args) == 2:
                if args[0] is type(None):
                    return args[1]
                if args[1] is type(None):
                    return args[0]
            # TODO, handle e.g. Union types. Look into using Pydantic for this. Leave as is for now.
        else:
            return origin
    return annotation


def coerce_arg(val: Any, param: inspect.Parameter) -> Any:
    # Needed due to circular import issue
    from fused.types import Bbox, TileGDF, TileXYZ, ViewportGDF

    # TODO: perhaps use https://docs.python.org/3/library/typing.html#typing.get_type_hints
    annotation = _resolve_annotation(param.annotation)
    if annotation is inspect._empty:
        return val

    # Temporary solution for properly handling non-stdlib annotations
    if isinstance(annotation, str):
        if "GeoDataFrame" in annotation:
            annotation = gpd.GeoDataFrame
        elif "DataFrame" in annotation:
            annotation = pd.DataFrame

    if annotation is int:
        if isinstance(val, str):
            # base 0 will cause the integer to be interpreted as a integer literal similar to how
            # code would be read. Possible improvement to help handle 0x...:
            # https://docs.python.org/3/library/functions.html#int
            # Only strings should be passed in to `int` if the base is passed too. Integers and so
            # on will not be converted correctly.
            return int(val, base=10)
        return int(val)
    if annotation is float:
        return float(val)
    if annotation is bool:
        if isinstance(val, str) and val.casefold() == FALSE_CASEFOLDED:
            return False
        return bool(val)
    if annotation in [list, dict, List, Dict, Iterable] and isinstance(val, str):
        return json.loads(val)
    if annotation is tuple:
        return tuple(json.loads(val))
    if annotation is uuid.UUID:
        return uuid.UUID(val)
    if annotation in [TileGDF, ViewportGDF]:
        return convert_to_tile_gdf(val, add_xyz=annotation is TileGDF)
    if annotation is TileXYZ:
        return convert_to_tile_xyz(val)
    if annotation is Bbox:
        return convert_to_bbox(val)
    if annotation is gpd.GeoDataFrame:
        # load as geojson
        return _parse_to_gdf(val)
    if annotation is pd.DataFrame:
        # load as json
        return _parse_to_df(val)

    # Unknown, fall back to not doing anything with it
    return val

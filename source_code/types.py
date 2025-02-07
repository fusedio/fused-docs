from typing import TYPE_CHECKING, Optional, TypeVar

if TYPE_CHECKING:
    import geopandas as gpd
    import mercantile
    import shapely

TileXYZ = TypeVar("TileXYZ", bound="mercantile.Tile")
TileGDF = TypeVar("TileGDF", bound="gpd.GeoDataFrame")
ViewportGDF = TypeVar("ViewportGDF", bound="gpd.GeoDataFrame")
Bbox = TypeVar("Bbox", bound="shapely.geometry.polygon.Polygon")


class UdfRuntimeError(RuntimeError):
    def __init__(self, *args, child_exception_class: Optional[str] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.child_exception_class = child_exception_class

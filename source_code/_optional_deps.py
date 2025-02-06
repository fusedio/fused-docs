try:
    import pandas as pd

    HAS_PANDAS = True
    PD_DATAFRAME = pd.DataFrame
except ImportError:
    HAS_PANDAS = False
    PD_DATAFRAME = None

try:
    import geopandas as gpd

    HAS_GEOPANDAS = True
    GPD_GEODATAFRAME = gpd.GeoDataFrame
except ImportError:
    HAS_GEOPANDAS = False
    GPD_GEODATAFRAME = None

try:
    import mercantile

    HAS_MERCANTILE = True
    MERCANTILE_TILE = mercantile.Tile
except ImportError:
    HAS_MERCANTILE = False
    MERCANTILE_TILE = None

try:
    import shapely

    HAS_SHAPELY = True
    SHAPELY_POLYGON = shapely.geometry.polygon.Polygon
except ImportError:
    HAS_SHAPELY = False
    SHAPELY_POLYGON = None

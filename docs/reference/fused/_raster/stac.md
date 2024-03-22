---
sidebar_label: stac
title: fused._raster.stac
---

#### stac\_from\_tiff\_list

```python
def stac_from_tiff_list(tiff_list: Sequence[str],
                        *,
                        input_datetime: Optional[Iterable[datetime]] = None,
                        id: Optional[Iterable[str]] = None,
                        collection: Optional[str] = None,
                        asset_name: str = "asset",
                        naive: bool = False,
                        max_workers: Optional[int] = None) -> gpd.GeoDataFrame
```

Construct a STAC GeoDataFrame from a list of GeoTIFF urls.

**Arguments**:

- `tiff_list` - input paths.
  

**Arguments**:

- `input_datetime` - datetime associated with the item. Defaults to None.
- `id` - id to assign to the item (default to the source basename). Defaults to None.
- `collection` - name of collection the item belongs to. Defaults to None.
- `asset_name` - asset name in the Assets object. Defaults to &quot;asset&quot;.
- `naive` - When True, this function will only read geometry information for the _first_ item in the list and copy geometry information to the others. Defaults to False.
  

**Returns**:

  a GeoDataFrame with containing the description of STAC items

#### stac\_from\_stac\_list

```python
def stac_from_stac_list(stac_list: Sequence[Dict]) -> gpd.GeoDataFrame
```

Construct a STAC GeoDataFrame from a list of STAC Items.

**Arguments**:

- `stac_list` - input STAC Items.
  

**Returns**:

  a GeoDataFrame with containing the description of STAC items


---
sidebar_label: signer
title: fused._raster.signer
---

#### create\_href\_mapping

```python
def create_href_mapping(
        stac_gdf: Union[Dataset, gpd.GeoDataFrame],
        signer: Callable[[str], str],
        asset_names: Optional[Sequence[str]] = None) -> Dict[str, str]
```

Create an href mapping given a STAC GeoDataFrame and a lambda signer

**Arguments**:

- `stac_gdf` - A GeoDataFrame representing STAC Items
- `signer` - A function applied on each asset href.
- `asset_names` - The keys in the assets dictionary to sign. Defaults to None, in which case it signs all assets.
  

**Returns**:

  A dict mapping from original asset hrefs to signed asset hrefs.


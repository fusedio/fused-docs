import json
from tempfile import NamedTemporaryFile


def deserialize_tiff(content: bytes):
    import rasterio
    import rioxarray
    import xarray as xr

    with NamedTemporaryFile(prefix="udf_result", suffix=".tiff") as ntmp:
        with open(ntmp.name, "wb") as f:
            f.write(content)
        with rasterio.open(ntmp.name) as dataset:
            rda = rioxarray.open_rasterio(
                dataset,
                masked=True,
            )
            metadata = dataset.tags(ns="fused")
        orig_type = metadata.get("orig_type")
        if orig_type == "numpy.ndarray":
            data = rda.values
            if len(json.loads(metadata["shape"])) < rda.ndim:
                data = data.squeeze()
            if "bounds" in metadata:
                bounds = json.loads(metadata["bounds"])
                data = (data, bounds)
        elif orig_type == "xarray.DataArray":
            data = rda
        else:
            key = metadata.get("key") or "image"
            data = xr.Dataset({key: rda})
    return data

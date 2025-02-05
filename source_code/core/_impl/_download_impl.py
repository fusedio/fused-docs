def data_path() -> str:
    # TODO: Allow overriding in OPTIONS
    return "/tmp/fused"


def filesystem(protocol: str, **storage_options):
    from urllib.parse import urlparse

    import fsspec
    from fsspec.implementations.dirfs import DirFileSystem

    from fused.api._public_api import get_api

    if protocol == "fd":
        # fused team directory
        api = get_api()
        if hasattr(api, "_resolve"):
            root = api._resolve("fd://")
            root_parsed = urlparse(root)
            return DirFileSystem(
                path=root, fs=fsspec.filesystem(root_parsed.scheme, **storage_options)
            )
        else:
            raise ValueError("Could not determine root of Fused team directory")
    return fsspec.filesystem(protocol, **storage_options)


def _download_requests(url: str) -> bytes:
    import requests

    # this function is shared
    response = requests.get(url, headers={"User-Agent": ""})
    response.raise_for_status()
    return response.content


def _download_signed(url: str) -> bytes:
    from fused.api._public_api import get_api

    api = get_api()
    return _download_requests(api.sign_url(url))


def _download_s3(url: str) -> bytes:
    try:
        return _download_signed(url)
    except:  # noqa E722
        s3 = filesystem("s3")
        with s3.open(url, "rb") as f:
            return f.read()


def _download_gcs(url: str) -> bytes:
    try:
        return _download_signed(url)
    except:  # noqa E722
        gcs = filesystem("gs")
        with gcs.open(url, "rb") as f:
            return f.read()

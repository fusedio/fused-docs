import os
import time
from pathlib import Path
from typing import Callable

from ._impl._download_impl import (
    _download_gcs,
    _download_requests,
    _download_s3,
    data_path,
)


def create_path(path: str, mkdir: bool = True) -> str:
    # Deprecated name...
    return file_path(file_path=path, mkdir=mkdir)


def file_path(file_path: str, mkdir: bool = True) -> str:
    """Creates a directory in a predefined temporary directory.

    This gives users the ability to manage directories during the execution of a UDF. It takes a relative file_path,
    creates the corresponding directory structure, and returns its absolute path.

    This is useful for UDFs that temporarily store intermediate results as files,
    such as when writing intermediary files to disk when processing large datasets.
    file_path ensures that necessary directories exist.

    Args:
        file_path: The file path to locate.
        mkdir: If True, create the directory if it doesn't already exist. Defaults to True.

    Returns:
        The located file path.
    """
    # TODO: Move this onto the context object or use the context object
    # TODO: Return Path objects rather than converting to str
    global_path = data_path() + "/"

    tmp = file_path.split("/")
    if tmp[-1].rfind(".") < 0:
        folder = Path(global_path + "/" + file_path)
    else:
        folder = Path(global_path + "/" + "/".join(tmp[:-1]))
    if mkdir:
        folder.mkdir(parents=True, exist_ok=True)
    return str(Path(global_path + "/" + file_path))


def download(url: str, file_path: str) -> str:
    """Download a file.

    May be called from multiple processes with the same inputs to get the same result.

    Fused runs UDFs from top to bottom each time code changes. This means objects in the UDF are recreated each time, which can slow down a UDF that downloads files from a remote server.

    💡 Downloaded files are written to a mounted volume shared across all UDFs in an organization. This means that a file downloaded by one UDF can be read by other UDFs.

    Fused addresses the latency of downloading files with the download utility function. It stores files in the mounted filesystem so they only download the first time.

    💡 Because a Tile UDF runs multiple chunks in parallel, the download function sets a signal lock during the first download attempt, to ensure the download happens only once.

    Args:
        url: The URL to download.
        file_path: The local path where to save the file.

    Returns:
        The function downloads the file only on the first execution, and returns the file path.

    Examples:
        ```python
        @fused.udf
        def geodataframe_from_geojson():
            import geopandas as gpd
            url = "s3://sample_bucket/my_geojson.zip"
            path = fused.core.download(url, "tmp/my_geojson.zip")
            gdf = gpd.read_file(path)
            return gdf
        ```

    """
    from urllib.parse import urlparse

    from loguru import logger

    file_path = file_path.strip("/")

    # Cache in mounted drive if available & writable, else cache in /tmp
    base_path = data_path()

    # Download directory
    file_full_path = Path(base_path) / file_path
    file_full_path.parent.mkdir(parents=True, exist_ok=True)

    def _download():
        parsed_url = urlparse(url)
        logger.debug(f"Downloading {url} -> {file_full_path}")

        if parsed_url.scheme == "s3":
            content = _download_s3(url)
        elif parsed_url.scheme == "gs":
            content = _download_gcs(url)
        else:
            if parsed_url.scheme not in ["http", "https"]:
                logger.debug(f"Unexpected URL scheme {parsed_url.scheme}")
            content = _download_requests(url)

        with open(file_full_path, "wb") as file:
            file.write(content)

    _run_once(signal_name=file_path, fn=_download)

    return file_full_path


def _run_once(signal_name: str, fn: Callable) -> None:
    """Run a function once, waiting for another process to run it if in progress.

    Args:
        signal_key: A relative key for signalling done status. Files are written using `file_path` and this key to deduplicate runs.
        fn: A function that will be run once.
    """
    from loguru import logger

    path_in_progress = Path(file_path(signal_name + ".in_progress"))
    path_done = Path(file_path(signal_name + ".done"))
    path_error = Path(file_path(signal_name + ".error"))

    def _wait_for_file_done():
        logger.debug(f"Waiting for {signal_name}")
        while not path_done.exists() and not path_error.exists():
            time.sleep(1)
        if path_error.exists():
            os.remove(str(path_in_progress))
            os.remove(str(path_error))
            raise ValueError(f"{signal_name} failed in another chunk. Try again.")
        logger.info(f"already cached ({signal_name}).")

    if path_in_progress.is_file():
        _wait_for_file_done()
    else:
        try:
            with open(path_in_progress, "x") as file:
                file.write("requesting")
        except FileExistsError:
            _wait_for_file_done()
            return
        logger.debug(f"Running fn -> {signal_name}")

        try:
            fn()
        except:
            with open(path_error, "w") as file:
                file.write("done")
            raise

        with open(path_done, "w") as file:
            file.write("done")
        logger.info(f"waited successfully ({signal_name}).")

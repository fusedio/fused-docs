---
id: changelog
title: Changelog
tags: [Changelog]
sidebar_position: 8
---
# Changelog

## v1.5.3 (2024-04-08) :duck:

- Improved compatibility with DuckDB requesting data from shared UDFs.
- Geocoder in Workbench now supports coordinates and H3 cell IDs.
- GeoDataFrame arguments to UDFs can be passed as bounding boxes.
- The package ibis was upgraded to 8.0.0.
- Utils modules no longer need to import fused.

## v1.5.2 (2024-04-01) :tanabata_tree:

- File browser can now preview images like TIFFs, JPEGs, PNGs, and more.
- Users can now open Parquet files with DuckDB directly from the file browser.

## v1.5.0 (2024-03-25) :open_file_folder:

- The upload view in Workbench now shows a file browser.
- Users can now preview files in the file browser using a default UDF.

## v1.4.1 (2024-03-19) :speech_balloon:

- UDFs now support typed function annotations.
- Introduced special types  `fused.types.TileXYZ`, `fused.types.TileGDF`, `fused.types.Bbox`.
- Workbench now autodetects Tile or File outputs based on typing.
- Added button to Workbench to autodelect UDF parameters based on typing.

## v1.1.1 (2024-01-17) :dizzy:

- Renamed `fused.utils.run_realtime` and `fused.utils.run_realtime_xyz` to `fused.utils.run_file` amd `fused.utils.run_tile`.
- Removed `fused.utils.run_once`.

## v1.1.0 (2024-01-08) :rocket:

- Added functions to run the UDFs realtime.

## v1.1.0-rc2 (2023-12-11) :bug:

- Added `fused.utils.get_chunk_from_table`.
- Fixed bugs in loading and saving UDFs with custom metadata and headers.

## v1.1.0-rc0 (2023-11-29) :cloud:

- Added cloud load and save of UDFs.
- `target_num_files` is replaced by `target_num_chunks` in the ingest API.
- Standardize how a decorator's headers are preprocesses to set `source_code` key.
- Fixed a bug loading UDFs from a job.

## v1.0.3 (2023-11-7) :bowtie:

_Getting chunks_

- Added `fused.utils.get_chunks_metadata` to get the metadata GeoDataFrame for a table.
- `run_local` now passes a copy of the input data into the UDF, to avoid accidentally persisting state between runs.
- `instance_type` is now shown in more places for running jobs.
- Fixed a bug where `render()`ing UDFs could get cut off.
- Fixed a bug with defining a UDF that contained an internal `@contextmanager`.

## v1.0.2 (2023-10-26) :up:

_Uploading files_

- Added `fused.upload` for uploading files to Fused storage.
- Added a warning for UDF parameter names that can cause issues.
- Fixed some dependency validation checks incorrectly failing on built in modules.

## v1.0.1 (2023-10-19) :ant:

- Added `ignore_chunk_error` flag to jobs.
- Added warning when sidecar table names are specified but no matching table URL is provided.
- Fixed reading chunks when sidecars are requested but no sidecar file is present.
- Upgraded a dependency that was blocking installation on Colab.

## v1.0.0 (2023-10-13) :ship:

_Shipping dependencies_

- Added `image_name` to `run_remote` for customizing the set of dependencies used.
- Added `fused.delete` for deleting files or tables.
- Renamed `output_main` and `output_fused` to `output` and `output_metadata` respectively in ingestion jobs.
- Adjusted the default instance type for `run_remote`.
- Fixed `get_dataframe` sometimes failing.
- Improved tab completion for `fused.options` and added a repr.
- Fixed a bug where more version migration messages were printed.
- Fixed a bug when saving `fused.options`.

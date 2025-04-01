---
id: changelog
title: Changelog
tags: [Changelog]
sidebar_position: 8
---

# Changelog

## v1.16.2 (2025-04-01)

**[`fused-py`](/python-sdk/)**

- It is now possible to return dictionaries of objects from a UDF, for example a dictionary of a raster numpy array, a DataFrame, and a string.
- Whitespace in a UDF will be considered when determining whether to return cached data.
- Fixed calling `fused.run` in [large jobs](/core-concepts/run-udfs/run_large/).

**[Workbench](/workbench/)**

- Added experimental AI agent builder.
- Workbench will now prompt you to replace an existing UDF when adding the same UDF (by name) from the catalog.
- Added ability to upload an entire collection.
- Fixed saving collections with empty names.

[Visualization](/workbench/udf-builder/styling/):
- Added a H3-only visualization preset.
- Fixed a bug where changing TileLayer visualization type could result in a crash.

[App Builder](/workbench/app-builder/app-overview/):
- Updated the runtime.

## v1.16.0 (2025-03-27)

**[`fused-py`](/python-sdk/)**

- The result object of running in `batch` now has `logs_url` property.
- Fixed `fused.submit` raising an error if some run failed.

**[Workbench](/workbench/)**

- Added a Download UDFs button for downloading an entire collection.
- Results will show a message at the top if UDF execution was cached.
- Non-visible UDFs will have a different highlight color on them in the UDF list.
- Collections will show as modified if the order of UDFs has been changed.
- Fixes for Collections saving the ordering and visibility of UDFs.
- Fixed the Team Jobs page in Workbench crashing in some cases.

**Shared tokens**

- Shared token URLs can be called with an arbitrary (ignored) file extension in the URL.

## v1.15.0 (2025-03-20)

**[`fused-py`](/python-sdk/)**

- Loading UDFs now behaves like importing a Python module, and attributes defined on the UDF can be accessed.
- The `fused.submit()` keyword `wait_on_result` has been renamed to `collect`, with a default of `collect=True` returning the collected results (pass `collect=False` to get the JobPool object to inspect individual results).
- New UDFs default to using `fused.types.Bounds`.
- Upgraded `duckdb` to v1.2.1.
- UDFs can now return simple types like `str`, `int`, `float`, `bool`, and so on.
- Files in `/mount/` can be listed through the API.
- UDFs from publicly accessible GitHub repositories can be loaded through `fused.load`.
- `fused.load` now supports loading a UDF from a local .py file or directory
- The `x`, `y` and `z` aren't protected arguments when running a UDF anymore (previously protected to pass X/Y/Z mercantile tiles).

**[Workbench](/workbench/)**

New:
- Added a new account page and redesigned preferences page.
- You can now customize the code formatter settings (available under Preferences > Editor preferences).
- UDFs can optionally be shared with their code when creating a share token.

General:
- Moved shared token page to bottom left bar, and adjusted the icons.
- The ordering of UDFs in collections is now saved.

[App Builder](/workbench/app-builder/app-overview/):
- Updated app list UI.
- Fixed bugs with shared apps showing the wrong URL in the browser.

## v1.14.0 (2025-02-25)

v1.14.0 introduces a lot of new changes across `fused-py` and Workbench

**[`fused-py`](/python-sdk/)**

- Introducing [`fused.submit()`](/python-sdk/top-level-functions/#submit) method for multiple job run
- Improvement to [UDF caching](/core-concepts/cache/#caching-a-udf)
    - All UDFs are now cached for 90 days by default
    - Ability to customize the age of cached data & UDFs with the new [`cache_max_age`](/core-concepts/cache/#defining-your-cache-lifetime-cache_max_age) argument when defining UDFs, running UDFs or when caching regular Python functions
- `pandas` & `geopandas` are now optional for running non-spatial UDF locally
- Removed hardcoded `nodata=0` value for serializing raster data

**[Workbench](/workbench/)**

New:
- Introducing [Collections](/workbench/udf-builder/collections/) to organize & aggregate UDFs together
- Redesigned "Share" button & page: All the info you need to share your UDFs to your team or the world

General:
- Improvements to Navigation in [Command Pallette](/user-guide/best-practices/workbench-best-practices/#using-keyboard-shortcuts-command-palette). Try it out in Workbench by doing `Cmd + K` (`Ctrl + K` on Windows / Linux)
- Autocomplete now works with `Tab` in [Code Editor](/workbench/udf-builder/code-editor/) with `Tab`
- Added a Delete Button in the Shared Tokens page (under [Account page](/workbench/account/))
- Ability to upload images for UDF Preview in [Settings Page](/workbench/udf-builder/code-editor/#settings)
- Adding “Fullscreen” toggle in [Map View](/workbench/udf-builder/map/)
- Improved `colorContinuous` in [Visualize Tab](/workbench/udf-builder/styling/)
- Allowing users to configure public/team access scopes for share tokens 
- No longer able to edit UDF & App name in read-only mode
- Fixing job loading logs

[File Explorer](/workbench/file-explorer/):
- Download directories as `zip`
- Adding favorites to file path input search results 
- Ability to open `.parquet` files with Kepler.gl


## v1.13.0 (2025-01-22)

- Fixed shared UDFs not respecting the Cache Enabled setting.
- Added a cache TTL (time-to-live) setting when running a UDF via a shared token endpoint.
- Tags you or your team have already used will be suggested when editing a UDF's tags.
- Team UDFs will be shown as read-only in Workbench, similar to Public UDFs.
- File Explorer shows deletion in progress.
- File Explorer can accept more S3 URLs, and uses `/mount/` instead of `/mnt/cache`.
- UDF Builder will no longer select a UDF when clicking to hide it.
- Fixed how Push to Github chooses the directory within a repository to push to.
- Fixed the browser location bar in Workbench updating on a delay.
- Fixed writing Shapefile or GPKG files to S3.
- (Beta) New [fusedio/apps](https://github.com/fusedio/apps) repository for public Fused Apps.
- Navigating to Team UDFs or Saved UDFs in the UDF Catalog will now prompt for login.
- Fixed the "Select..." environment button in Workbench settings.
- UDF Builder will no longer replace all unaccepted characters with `_` (underscore).
- Fixed loading team UDFs when running a UDF with a shared token.
- Batch jobs that use `print` will now have that output appear in the job logs.
- Apps in the shared token list show an app icon.
- Removed some deprecated batch job options.
- Installed `vega-datasets` package.

## v1.12.0 (2025-01-10)

- (Beta) Added an App catalog in Workbench, and a new type of URL for sharing apps.
- Added `/mount` as an alias for `/mnt/cache`.
- More consistently coerce the type of inputs to UDFs.
- Added more visualization presets to UDF builder in Workbench.
- Fixed an issue where the tab icon in Workbench could unintentionally change.
- Fixed bugs in Workbench File Explorer for `/mnt/cache` when browsing directories with many files.
- Fixed bugs in `fused` Python API not being able to list all files that should be accessible.
- Fixed bugs in the Github integration, command palette, and file explorer in Workbench.
- Fixed bugs in caching some UDF outputs.
- The shareable URL for public and community UDFs will now show in the settings tab for those UDFs.
- UDFs can customize their data return with `Response` objects.

## v1.11.9 (2024-12-19)

- Accounts now have a *handle* assigned to them, which can be used when loading UDFs and pushing to community UDFs
- Account handle can be changed once by the user (for more changes please contact the Fused team.)
- Added a command palette to the Workbench, which can be opened with Cmd-k or Ctrl-k.
- When creating a PR for a community UDF or to update a public UDF, it will be under your account if you log in to Fused with Github.
- Bug fixes for pushing to Github, e.g. when pushing a saved UDF, and for listing the Fused bot account as an author.
- Batch (`run_remote`) jobs can call back to the Fused API.
- Team UDFs can be pinned to the end of the featured list.
- Speed improvements in ingestion.
- Ingestion will detect `.pq` files as Parquet.
- Format code shortcut in Workbench is shown in the keyboard shortcut list and command palette.
- Workbench will hide the map tooltip when dragging the map by default.
- Workbench will now look for a `hexLayer` visualization preset for tabular results that do not contain `geometry`.
- Workbench file explorer can now handle larger lists of files.
- Fix for browsing disk cache (`/mnt/cache`) in Workbench file explorer.
- Teams with multiple realtime instances can now set one as their default.
- Fix for saving UDFs with certain names. Workbench will show more descriptive error messages in more cases for issues saving UDFs.

## v1.11.8 (2024-12-04)

- New File Explorer interface, with support for managing Google Cloud Storage (GCS) and `/mnt/cache` files.
- Workbench will show an error when trying to save a UDF with a duplicate name.
- Fixed a few bugs with Github integration, including the wrong repository being selected by default when creating a PR.
- Updated `fsspec` and `pyogrio` packages.

## v1.11.7 (2024-11-27)

- Decluttered the interface on mobile browsers by default.
- Fixed redo (Cmd-Shift-z or Ctrl-Shift-z) sometimes being bound to the wrong key.
- Tweaked the logic for showing the selected object in Workbench.

## v1.11.6 (2024-11-26)

- Added Format with Black (Alt+Shift+f) to Workbench.
- Fix the CRS of DataFrame's returned by get_chunk_from_table.
- Added a human readable ID to batch jobs.
- Fused will send an email when a batch job finishes.
- Fix for opening larger files in Kepler.gl.
- Fix for accessing UDFs in a team.
- Improved messages for UDF recursion, UDF geometry arguments, and returning geometry columns.
- Adjusted the UDF list styling and behavior in Workbench.
- Fix for secrets in shared tokens.

## v1.11.5 (2024-11-20)

- Show message for keyword arguments in UDFs that are reserved.
- Added reset kernel button.
- Workbench layers apply visualization changes immediately when the map is paused.
- Show the user that started a job for the team jobs list.
- Fix for running nested UDFs with utils modules.
- Fix for returning xarray results from UDFs.
- Fix for listing files from within UDFs.
- Upgraded to GeoPandas v1.

## v1.8.0 (2024-06-25) :package:

- Added Workbench tour for first-time users.
- Undo history is now saved across UDFs and persists through reloads.
- Added autocomplete when writing UDFs in Workbench.
- Added `colorBins`, `colorCategories`, and `colorContinuous` functions to Workbench's Visualize tab.
- Migrated SDK to Pydantic v2 for improved data validation and serialization.
- Fixed a bug causing NumPy dependency conflicts.

## v1.7.0 (2024-06-04) :bird:

- Execution infrastructure updates.
- Update DuckDB package to v1.0.0.
- Improve responsivity of Workbench allotments.
- Crispen Workbench UI.

## v1.6.1 (2024-05-06) :guardsman:

_GitHub integration_

- Updates to team GitHub integration.
- Users are now able to create shared UDF token from a team UDF both in Workbench and Python SDK.

## v1.6.0 (2024-04-30) :checkered_flag:

- The Workbench file explorer now shows UDFs contributed by community members.
- Team admins can now set up a GitHub repository with UDFs that their team members can access from Workbench.

## v1.5.4 (2024-04-15) :telescope:

- Button to open slice of data in Kepler.gl.
- Minor UI design and button placement updates.

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
- Added button to Workbench to autodetect UDF parameters based on typing.

## v1.1.1 (2024-01-17) :dizzy:

- Renamed `fused.utils.run_realtime` and `fused.utils.run_realtime_xyz` to `fused.utils.run_file` amd `fused.utils.run_tile`.
- Removed `fused.utils.run_once`.

## v1.1.0 (2024-01-08) :rocket:

- Added functions to run the UDFs realtime.

## v1.1.0-rc2 (2023-12-11) :bug:

- Added `fused.utils.get_chunk_from_table`.
- Fixed bugs in loading and saving UDFs with custom metadata and headers.

## v1.1.0-rc0 (2023-11-29) :cloud:

- Added cloud load and save UDFs.
- `target_num_files` is replaced by `target_num_chunks` in the ingest API.
- Standardize how a decorator's headers are preprocesses to set `source_code` key.
- Fixed a bug loading UDFs from a job.

## v1.0.3 (2023-11-7) :sweat_drops:

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
- Fixed some dependency validation checks incorrectly failing on built-in modules.

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
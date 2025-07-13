---
id: changelog
title: Changelog
tags: [Changelog]
sidebar_position: 8
---

# Changelog

## v1.21.0 (2025-07-11)

**[`fused-py`](/python-sdk/)**

New Features:
- Added `fused.api.resolve`.
- Added `fused.api.team_info`.
- IPython magics now load automatically.
- When running a large (batch) job, it is now possible to specify the job's name.
- Upgraded xarray to 2025.4.0, DuckDB to 1.3.2, and H3 to 4.3.0.
- The `fd://` filesystem scheme will automatically be registered with `fsspec`.
- UDFs that return HTML will be loaded as `str` objects from `fused.run`.
- Saved UDFs have a `catalog_url` property.
- `npy` output format is now supported for numpy (raster) return values.
- Arrow-compatible return values are now accepted.
- `fused.cache` will detect changes to referenced UDFs.
- `fused.run` accepts `verbose` keyword.

Bug Fixes:
- Fixed bugs with `Udf.render` on some IPython versions.
- Fixed bugs with `repr`s for access tokens and UDFs.
- Fixed calling `fused.run` with UDF objects and `sync=False`.
- Renamed the UDF class to `Udf`.
- Removed some unused and deprecated code.
- Fixed bugs with `fused.cache` showing as not found, having stale files, or not passing arguments through.
- Removed the `n` keyword argument from `get_udfs` and `get_apps`.
- Fixed bugs with HEAD requests to UDF endpoint.
- `fused.submit` will warn about conflicting arguments.
- `/tmp/` size has been increased in realtime instances.
- `fused.api.list` and related functions supports `/mount` paths.
- Improved the performance of GitHub sync.
- Changed defaults for `JobPool.cancel` and fixed a bug where it would continue to retry.
- Fixed bugs with `JobPool.df` and UDF runs that result in exceptions.
- Fixed encoding URL paths in `fused.api.download` and related functions.

**[Workbench](/workbench/)**

New Features:
- Added AI editing and AI chat capabilities in the UDF builder.
- Workbench will now show how much time was taken on each line of a UDF.
- Added new Dashboard builder mode (experimental).
- Added new Table data view mode.
- GitHub integration has a new page and is no longer beta.
- Fused apps uses a newer version of Streamlit and Stlite.
- Added a menu item to take a screenshot in higher-than-screen resolution.
- Added type-to-filter in File Explorer.
- File Explorer can be browsed without logging in.
- File Explorer now shows a summary of the current directory.
- File preview UDFs can now be specified with regular expressions.
- Cmd+Click on shared tokens will now take you to the UDF catalog.

Bug Fixes:
- Results panel shows when memory usage is unknown.
- Share code is more consistent with the selected output format.
- Fixed bugs with read-only app UI.
- The large data warning will now show in File Explorer as well when applicable.
- Fixed bugs with app/UDF catalog layout and sorting.
- Adjusted the UI for visualization settings and parameters in the UDF list.
- Reordered menu items in File Explorer.
- Cursor position will be remembered when switching between UDFs.
- Share tokens that are already shown on the page are no longer redacted.
- GitHub integration remembers relevant open PRs better.
- Map tooltip can now be scrolled.

## v1.20.1 (2025-06-09)

**[`fused-py`](/python-sdk/)**

New Features:
- Added `fused.api.resolve` and `fused.api.team_info`.
- IPython magics will automatically be loaded when importing `fused`.
- `run_remote` (batch jobs) can now accept a job name.

Bug Fixes:
- Fixed the `render` method of UDF objects.
- Fixed access tokens for apps being rendered in IPython.
- Fixed calling `fused.run(udf, sync=False)` with UDF objects.
- Removed some deprecated fields and arguments.

**[Workbench](/workbench/)**

- Workbench will now show the amount of time taken in UDF functions as a heatmap.
- Memory bars in the Results panel will show when usage is unknown.
- Update how shared token URLs are generated for different output formats.
- Updated stlite to 0.82.0.

## v1.20.0 (2025-06-03)

**[`fused-py`](/python-sdk/)**

New Features:
- Running a UDF with engine `local` will cache similarly to how it would when running on `remote` (supporting `cache_max_age` to control the caching).
- Large (batch) jobs will be in a Pending state if they cannot start immediately.
- UDFs can now accept `**kwargs` parameters, which will always be passed in as strings.
- `@fused.cache` has a new `cache_verbose` option. If set to `True` (default), it prints a message when a cached result is returned.
- `@fused.cache` renamed the `reset` parameter to `cache_reset`. The existing `reset` parameter is deprecated.
- Some file listing APIs like `fused.api.list` will work for public buckets when on free accounts.
- `fused.load` accepts `import_globals` (default `True`) for controlling importing UDF globals. Also, when globals cannot be imported, a warning is emitted instead of an exception.

Bug Fixes:
- Clarified login-needed message in Fused Apps.
- Fixed bugs with `@fused.cache` results not being ready.
- Fixed bugs with `@fused.cache` not detecting changes in the cached function.
- Loading a UDF from a file will autodetect the UDF function name.
- Fixed bugs with returning GeoDataFrames that do not contain geometry.
- Fixed calling `to_fused` on an app.

**[Workbench](/workbench/)**

- A message will appear above the UDF body when parameters are set in the UDF list.
- A lock icon will be shown next to read-only UDFs and Apps in Workbench.
- When pushing UDFs to GitHub, the preview image will be pushed to a public URL so that the README in GitHub is rendered correctly.
- When pushing UDFs to GitHub, Workbench will assign the PR to you if possible.
- It is now possible to delete UDFs and Apps directly from the catalog.
- Added a "Reload Collection" button. This pulls all latest version of UDF currently in your Collection.
- Workbench will minimize more changes from the PRs it creates on GitHub.
- "Open in Kepler.gl" supports H3 (string) data.
- The visibility button for a Fused App will now reset the app.
- A new Reset 3D View button is added to the UDF Builder map, and the keyboard shortcut has been updated to `Cmd+Shift+UpArrow` on MacOS (`Ctrl+Shift_UpArrow` on Windows / Linux).
- Workbench will show the current environment name above the map by default.
- Workbench will remember which UDF was selected when reopening the page.
- Adjusted which UDF mode label is shown when automatically detecting the UDF mode.
- Fixed some bugs with dynamic output mode.
- UI updates for the Pull Changes (history) and Push Changes views, including showing the README file in both views.
- Drag&Drop UDF into Workbench now works on the entire tab
- Added a button to download usage table in the Profile view.
- Fixed some visual bugs with light mode.
- File Explorer will no longer show file opener UDFs saved on your personal catalog, and will clarify when file opener UDFs are from your team catalog.

## v1.19.0 (2025-05-19)

**[`fused-py`](/python-sdk/)**

Breaking changes:
- [Large (batch) jobs](/core-concepts/run-udfs/run_large/) have been updated to pass parameters into the UDF the same way as other UDF runs. For compatibility, if the parameters passed into the job do not correspond with the parameters, a dictionary parameter is passed into the UDF instead. This will be deprecated and removed in a future release.
- The `context` and [`bbox`](/core-concepts/filetile/#legacy-bbox-object) parameters to a UDF are no longer treated as special.
- Python 3.9 support, which was previously deprecated, is now removed. The minimum Python version for the `fused` package is now 3.10.

New Features:
- PyArrow upgraded to version 16.0.
- Ingestion now supports input files without extensions, and filters out files with `.` or `_` prefix.
- `cache=False` is now a shortcut for disabling cache, e.g. `cache_max_age=0`.
- UDFs now support parameters annotated as `shapely.Geometry` or `shapely.Polygon`.
- [`fused.load`](/python-sdk/top-level-functions/#fusedload) now support loading UDFs from Github Pull Request URLs.
- Added a timeout parameter for `fused.api.upload`.
- Fused API functions now support `/mount` without `file://` prefix.
- `fused.api.download` now supports downloading files from `/mount`.
- `fused.api.list` now supports listing an individual file under `/mount`.
- `max_deletion_depth` in `fused.api.delete` default changed from 2 to 3.

Bug Fixes
- Fixed pickling UDF objects.
- Fixed UDF equality checks not conforming to Python specifications.
- Many fixes to ensure compatibility between the `fused` module available on PyPI and the `fused` module within the Fused backend.
- Fixed returning `pd.Timestamp` objects.
- Fixed bugs with handling of stdout if the UDF is async.
- Fixed bugs with UDF object `repr` in Jupyter.
- Fixed [`@fused.cache`](/core-concepts/cache/#caching-any-python-function-fusedcache) in [Fused Apps](/workbench/app-builder/).
- Fixed "multiple auth mechanisms" error when retrieving job results.
- Fixed deserialization of GeoDataFrame without geometry column.
- Fixed cases where UDFs would be indented when run.
- Various stability and performance updates, including new self-healing capabilities on the Fused backend.

**[Workbench](/workbench/)**

- Upgraded Streamlit in apps to 1.44.
- [Fused Apps](/workbench/app-builder/) is no longer "beta".
- [Fused Apps](/workbench/app-builder/) will now highlight syntax errors.
- [Fused Apps](/workbench/app-builder/) will now autocomplete the `fused` module correctly.
- "Changes pending" in the map has been renamed to "Running" and now shows the time elapsed without needing to hover over it.
- UDF builder tooltips have been refreshed, it is now possible to click on data on the map to pin the tooltip on screen. Pinned tooltips show how many data records were under the mouse and allow paging through them.
- Workbench can now highlight H3 hexagons on click.
- Workbench can now detect decimal H3 indexes and Cmd+Click works on them.
- `udf://` URLs in Workbench now entirely overwrite parameters of the selected UDF.
- Fixed UDF builder showing partially updated map states for Tile UDFs.
- Collections catalog can now be sorted.
- Fixed a bug where Workbench would not detect newly added utils on UDFs.
- Parameters and Visualization sections are now styled slightly differently to make it easier to pick out your UDFs.
- Renamed Visualization "Surprise me" button to "Preset".
- Fixed a visual bug with the job status.
- Updated the share UDF and share app pages.
- Fixed bugs with UDF or app catalog showing the wrong content.
- Renamed "History" to "Pull Changes" and updated styling of that page.
- Fixed Pull Changes not showing diffs if utils had been added or deleted.
- Fixed Workbench showing the original Github link for forked UDFs.
- Workbench code editors will now remember scroll position.
- Clicking the viewport location label will now copy it.

## v1.18.0 (2025-04-28)

**[`fused-py`](/python-sdk/)**

Breaking changes:
- `fused.submit` now raises an error by default, if there is any run erroring

New Features:
- It is now possible set the cache storage location with `@fused.cache(storage=...)`.
- `@fused.cache` can now exclude arguments from the cache key.
- `@fused.cache` uses Pandas' own way of hashing DataFrames.
- Added storage argument to `fused.file_path(storage=...)`.
- Large jobs now pick up AWS credentials more consistently.
- Auth redirect can dynamically select the port when logging in locally.
- `udf.to_fused` will show the diff when UDF name conflicts with an existing UDF.
- `fused.load` can load by the unique UDF ID again.
- UDFs can be run by username and UDF name in addition to email and UDF name. (ex: `fused.run(user@team.com/my_cool_udf)`). 
- Preview images can now be specified in-directory in Github.
- Adjusted UDF caching behavior for performance.

Bug Fixes
- Fixed behavior when loading and running UDFs with code outside of the UDF function.
- Fixed `fused.api.list` being incompatible with some async stacks.
- Fixed a bug where strings inside UDFs would get extra spaces added to them.
- Shared tokens can be created by a team account.
- Fixed a bug that could occur where Fused would try to duplicate index column names of the returned DataFrame.
- Fixed various bugs when a UDF closes `stdout`.
- Fixed a bug where `fused.run` would not return printed messages from a UDF.
- Fixed a bug where `fused.load` would crash on very large strings.
- Fixed various bugs with exporting UDFs from within fused-py.
- Fixed a bug where `partitioning_schema_input` would not be found when ingesting.
- Fixed a bug where UDFs might import incorrectly when several pushes happen in quick succession in a linked Github repo.

**[Workbench](/workbench/)**

- `File (Viewport)` renamed to `Single (Viewport)`.
- Added `Single (Parameter)` UDF type that behaves like `Single (Viewport)` but does not pass the viewport bounds.
- File Explorer will show a per-user home favourite.
- Your UDF list will now sync across different browser tabs.
- Preference toggles are added to the Command Palette.
- The share page has been redesigned.
- Collections catalog page now shows the UDF in a given Collection by hovering over them.
- When adding a duplicate UDF to Workbench, you will be prompted to duplicate or replace it.
- Memory usage for UDFs can be found in the results panel (once displaying memory usage was been turned on in Preferences)
- Workbench will indicate that UDF runs were cached in all circumstances.
- The public map page is now compatible with any public-readable shared token.
- Added `udf://name?param=value` URL support to Workbench.
- Reduced the size of metadata diffs generated by Workbench when pushing to Github.
- Various performance improvements.
- Fixes for various UI layout bugs.

## v1.17.0 (2025-04-10)

**[`fused-py`](/python-sdk/)**

- Team UDFs can be loaded or run by specifying the name "team", as in: `fused.load("team/udf_name")`
- `Udf.to_fused` supports overwriting the UDF when saving.
- Added `fused.api.enable_gcs()` to configure using the Google Cloud Platform secret specified in Fused secret manager.
- `@fused.cache` locking mechanism has changed and will not allow multiple concurrent runs.
- Upgraded DuckDB to v1.2.2.
- Running a saved UDF by token or name will now also show the logs, including print statements and error tracebacks.
- All functions interacting with the Fused server will now retry automatically, by default 3 times.
- Python 3.9 support is deprecated. The next release of `fused` will require Python 3.10+.
- Deprecated `fused_batch` module is removed.

**[Workbench](/workbench/)**

- Cached UDF runs will show the original logs.
- "Change output parameters" in the Share UDF screen shows all detected parameters.
- Added a copy viewport bounds button in the Results panel.
- Improved the performance of the catalog screen.
- Fixed the job page showing times in inconsistent time zones.

[App Builder](/workbench/app-builder/app-overview/):
- Deprecated `fused_app` module is removed.

## v1.16.3 (2025-04-03)

**[`fused-py`](/python-sdk/)**

- It is now possible to return general `list`s and `tuple`s from UDFs. (Note: a tuple of a raster and bounds will be treated as a raster return type.)

**[Workbench](/workbench/)**

- Workbench will now prompt you when loading large UDF results that could slow down or overwhelm your browser. The threshold for this prompt is configurable in your Workbench preferences.
- Fixed bugs with loading large UDF results.
- UDF list will show an error if a UDF has an empty name.
- Fixed running some public UDFs in Workbench.

## v1.16.2 (2025-04-01)

**[`fused-py`](/python-sdk/)**

- It is now possible to return dictionaries of objects from a UDF, for example a dictionary of a raster numpy array, a DataFrame, and a string.
- Whitespace in a UDF will be considered as changes when determining whether to return cached data. (a UDF with different whitespace will be rerun rather than cached)
- Fixed calling `fused.run` in [large jobs](/core-concepts/run-udfs/run_large/).

**[Workbench](/workbench/)**

- Added experimental AI agent builder.
- Workbench will now prompt you to replace an existing UDF when adding the same UDF (by name) from the catalog.
- Added ability to download & upload an entire collection.
- Fixed saving collections with empty names.

[Visualization](/workbench/udf-builder/styling/):
- Added an H3-only visualization preset.
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

- Introducing [`fused.submit()`](/python-sdk/top-level-functions/#fusedsubmit) method for multiple job run
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
- Improvements to Navigation in [Command Pallette](/core-concepts/best-practices/workbench-best-practices/#using-keyboard-shortcuts-command-palette). Try it out in Workbench by doing `Cmd + K` (`Ctrl + K` on Windows / Linux)
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
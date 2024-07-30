export const PYARROW_URL =
  "/pyarrow/pyarrow-17.0.0-cp312-cp312-pyodide_2024_0_wasm32.whl";

/** Requirements to install by default on Pyodide */
export const DEFAULT_APP_REQUIREMENTS = [
  // Needed by fused_app.py:
  PYARROW_URL,
  "pyodide-unix-timezones", // needed by pyarrow
  "geopandas",
  "requests",
  "xarray",
  "yarl",
  // Commonly used in product:
  "pydeck",
];

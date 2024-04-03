# DuckDB (Parquet)

[DuckDB](https://duckdb.org/) is an open source, in-process, analytical database. It is popular for fast, local queries over in memory datasets. DuckDB supports several of the output formats that Fused can serve, and in particular it has great support for Parquet files.

To load data from Fused, you'll first generate a signed UDF URL.

## 1. Generate a signed URL for a UDF

First, on Workbench, create and save a UDF that successfully renders in `File` mode. Under the "Settings" tab, click "Share" to [generate a signed URL](/basics/core-concepts/#generate-endpoints-with-workbench) that can be called via HTTP requests. 

Modify the generated `HTTP` URL to set `dtype_out_vector` to `parquet`. You can optionally pass UDF parameters as URL-encoded strings, which can be configured to change based on query input.

## 2. Install and load `httpfs`

To load Parquet files from remote endpoints from within DuckDB, you can install the `httpfs` extension. This is an official DuckDB extension and will be automatically downloaded if needed.

```sql
INSTALL httpfs;
LOAD httpfs;
```

## 3. Query using `read_parquet`

Now you can make a query using the UDF URL, with the dtype_out_vector set to `parquet`:

```sql
select *
from read_parquet('https://www.fused.io/server/v1/realtime-shared/221aa65f3d96f1a320ed0f4eea0d320724c0ddc0c75cbf70df711def11e2ecc5/run/file?dtype_out_vector=parquet');
```

You can pass parameters into the URL from the query:

```sql
select *
from read_parquet('https://www.fused.io/server/v1/realtime-shared/221aa65f3d96f1a320ed0f4eea0d320724c0ddc0c75cbf70df711def11e2ecc5/run/file?dtype_out_vector=parquet&resolution=13');
```

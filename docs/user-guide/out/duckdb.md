# DuckDB

[DuckDB](https://duckdb.org/) is an open source, in-process, analytical database. Its can natively read several of output formats that Fused HTTP Endpoints return.


## 1. Generate a signed URL for a UDF

First create a UDF and generate an [HTTP endpoint](/core-concepts/run/#http-requests).

## 2. Install and load `httpfs`

To load Parquet files from remote endpoints from within DuckDB, you can install the `httpfs` extension.

```sql
INSTALL httpfs;
LOAD httpfs;
```

## 3. Query using `read_parquet`

Now you can make a query using the UDF URL, with the dtype_out_vector set to `parquet`:

```sql
SELECT *
FROM read_parquet('https://www.fused.io/server/v1/realtime-shared/221aa65f3d96f1a320ed0f4eea0d320724c0ddc0c75cbf70df711def11e2ecc5/run/file?dtype_out_vector=parquet');
```

You can pass parameters into the URL from the query:

```sql
SELECT *
FROM read_parquet('https://www.fused.io/server/v1/realtime-shared/221aa65f3d96f1a320ed0f4eea0d320724c0ddc0c75cbf70df711def11e2ecc5/run/file?dtype_out_vector=parquet&resolution=13');
```

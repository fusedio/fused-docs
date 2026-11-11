# Query a dataset over HTTP: `GET /h3/query`

Every indexed dataset is served by `GET /h3/query` on its environment's server, the way to read it from outside a UDF. The base URL is `https://www.fused.io/server/v1` on production; in Python, `fused.options.base_url` gives the current environment's. The response is Parquet. Every parameter and error: https://docs.fused.io/rest-api/h3. Partition and index: https://docs.fused.io/skills/H3.md.

```bash
curl -G "https://www.fused.io/server/v1/h3/query" \
  --data-urlencode "path=s3://fused-asset/data/nyc311/" \
  -d min_lng=-73.990 -d min_lat=40.750 -d max_lng=-73.980 -d max_lat=40.758 \
  --data-urlencode 'partition={"month": "2025-12"}' \
  -d columns=hex -d columns=complaint_type \
  -o nyc311.parquet
```

Expect HTTP 200 and 752 rows with columns `hex`, `complaint_type`.

- **Selectors:** the same as `fused.h3.query` (https://docs.fused.io/skills/h3/query.md), as URL parameters: a box (`min_lng`, `min_lat`, `max_lng`, `max_lat`), `lat` and `lng`, `cell`, or `hex_min` and `hex_max`. Narrow with `time_min`/`time_max`, `partition` and `partition_range` (JSON objects), and repeat `columns=` per column.
- **Credentials:** a public `s3://` dataset needs none. For the user's own dataset add `-H "Authorization: Bearer $FUSED_ACCESS_TOKEN"` with a token from `fused.api.access_token()`; without it the endpoint returns 403.
- **Paging:** when more rows remain, the response has an `X-Fused-Next-Cursor` header. Send it back as `cursor=` with the same query until there is none.
- **Errors:** the body is JSON with a `detail` message. Read it, fix the request, then retry.
- **Browser:** the endpoint allows cross-origin requests, so a web page can `fetch` it and parse the Parquet, for example with hyparquet.

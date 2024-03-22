---
id: overview
title: Overview
tags: [Overview, Hosted API]
sidebar_position: 0
---

# Hosted API overview

UDFs saved on Fused cloud can be called as HTTP endpoints.

This section shows how to generate and make authenticated calls to these endpoints, and the "integrations" section shows examples of how to use them to integrate with your team's most important tools.

Using the Fused Hosted API supercharges your stack with the ability to trigger and load the output of any scale workflows. API calls automatically provision serverless compute resources to run workflows in parallel using advanced caching and geo partitioning - without your team needing to spend time on setup.

Endpoints created with Fused Hosted API seamlessly integrate with tools such as:

- Tile-based maps: Simply pass the endpoint into tile-based maps such as open source JavaScript tools (e.g. leaflet, Deck.gl, and Kepler.gl), proprietary web-based apps (such as Felt and Foursquare Studio), or desktop based tools such as ArcGIS, ESRI, and QGIS.
- Apps that make HTTP requests: Load data into low-code app builders such as Streamlit & Retool.
- Apps that render embeddable maps: Embed responsive maps to significantly enhance the utility and interactivity of documentation sites and apps, such as Notion.

Read on to learn how.

## Introduction

This section describes how to create a UDF endpoint either in Workbench or with the Fused Python SDK, and how to authenticate requests to call the endpoint.

Endpoints can be called with "private" or "shared" authentication tokens. They are created as follows:


## Get an account's private token

Python environments where the authentication flow completed successfully store a credentials key in the default location ` ~/.fused/credentials`. Calls to UDFs from those environments will use that key, unless a token for a different account is explicitly set in the call. Making calls to endpoints from a non-authenticated environment will need the authenticated account's access token, which can be retrieved with the following commands.

```python
from fused._auth import CREDENTIALS

CREDENTIALS.credentials.access_token
```


:::danger

Note that the "private" token can access all UDFs and should be kept private. The recommended approach is instead to use "shared" tokens with tightly scoped permissions, as detailed below.

Remember that tokens are tied to the account that created them and requests to their corresponding endpoints will accrue charges on that account.
:::


This is how to call UDF endpoints via HTTP requests with the token.

```bash
curl -XGET https://app.fused.io/server/v1/realtime-shared/$SHARED_TOKEN/run/file
```

## Create and manage shared tokens (recommended)

Shared tokens are tightly scoped to a single UDF, and can easily be revoked. Creating a shared token for a UDF returns a token object that, among other attributes, contains the token as a string and sample endpoint URLs.

This is how to to call UDF endpoints in Python with signed token URLs.
```python
from fused.api import FusedAPI
api = FusedAPI()

token_object = api.create_udf_access_token(udf_email="user@fused.io", udf_name="caltrain_live_location")
output = fused.core.run_shared_file(token=token_object.token, my_param="...")
```

### Manage shared tokens

Fetch a specific UDF token object using its unique token string:
```python
token_object = api.get_udf_access_token(token=token.token)
```

Fetch all UDF tokens:
```python
token_objects = api.get_udf_access_tokens()
```

Update a specific UDF token using its unique token string:
```python
token_object = api.update_udf_access_token(token=token.token, enabled=True)
```

Delete a specific UDF token using its unique token string:
```python
api.delete_udf_access_token(token=token.token, enabled=True)
```


Similarly, signed URLs endpoints can be created that can be called from another application via HTTP requests.

### Single File HTTP endpoints

Single file HTTP endpoints are suitable for handling individual requests, ideal for scenarios where a single resource is required, such as loading data into [Google Sheets](/hosted-api/integrations/google_sheets/).


```python
from fused.api import FusedAPI
api = FusedAPI()

# URL for single call
api.create_udf_access_token(udf_email="user@fused.io", udf_name="caltrain_live_location").get_file_url()
```

### Tile HTTP endpoints

Tile HTTP endpoints are designed for serving map applications that consume Tiles, such as [Lonboard](/hosted-api/integrations/lonboard/) or [geemap](/hosted-api/integrations/geemap/).

```python
from fused.api import FusedAPI
api = FusedAPI()

# URL for XYZ tiles
api.create_udf_access_token(udf_email="user@fused.io", udf_name="caltrain_live_location").get_tile_url()
```

## Call UDF endpoints

The Fused Python SDK exposes methods to call UDFs. In Python environments authenticated to Fused, the UDF be called or imported in these 3 ways:


Call UDF and return its output:

```python
output = fused.core.run_file("user@fused.io", "caltrain_live_location")
```

Call UDF asynchronously and return its output:
```python
output = await fused.core.run_file_async("user@fused.io", "caltrain_live_location")
```

Import as a UDF object:
```python
my_udf = fused.core.load_udf_from_fused("user@fused.io", "caltrain_live_location")
```

:::note
Did you know UDFs can also call other UDFs? It's an easy way to chain UDFs together or even run jobs in parallel.
:::
Other environments can call the UDF endpoint via HTTP requests and receive its output in the response body.

```bash
curl -XGET "https://app.fused.io/server/v1/realtime/fused/api/v1/run/udf/saved/user@fused.io/caltrain_live_location?dtype_out_raster=png&dtype_out_vector=parquet" -H "Authorization: Bearer $ACCESS_TOKEN"
```



:::note
Once you save a UDF in workbench, the "Settings" tab of the editor will show the above as snippets you can easily copy to use the UDF from different environments.

![alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/snippets_caltrain.png)
:::
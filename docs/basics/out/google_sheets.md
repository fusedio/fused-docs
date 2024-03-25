# Google Sheets

The Google Sheets `importData` command imports data at from a given url in `.csv` format. You can use it to load data from a UDF into a cell.


## Step 1: Create a UDF in Fused Hosted API

Create a UDF that returns a table then save it on Workbench to automatically create an endpoint.

This example retrieves Caltrain live location data from GTFS realtime feed, and returns it as a dataframe.

```python
@fused.udf
def udf(bbox=None):
    import requests
    import pandas as pd

    r = requests.get(f'https://www.caltrain.com/files/rt/vehiclepositions/CT.json')
    j = r.json()
    df = pd.json_normalize(j['Entities'])
    return df
```

## Step 2: Create a URL for the UDF

Now, [create a signed Tile HTTP endpoint](/docs/hosted-api/hosted-api-overview#tile-http-endpoints) for the UDF.

The generated URL should look like this:

```bash
https://app-staging.fused.io/server/v1/realtime-shared/ccd781317018362a6966c9f12b27e95f1fe2fd88ff339de90eb9ac35b87cf439/run/file
```

Append this query parameter to the end of the URL to structure the response as a CSV type: `?dtype_out_vector=csv`.

## Step 3: Call the UDF in a cell

Now that you have the UDF live on Fused Hosted API and a URL to call it, you're ready to import data into Google Sheets. In the cell where you want your data to appear, use the `importData` function with the URL of your UDF. The syntax is as follows:

```
=importData("https://app-staging.fused.io/server/v1/realtime-shared/ccd781317018362a6966c9f12b27e95f1fe2fd88ff339de90eb9ac35b87cf439/run/file?dtype_out_vector=csv")
```

When you enter this formula into a cell, Google Sheets will call your UDF, and the returned dataframe will be automatically populated in the spreadsheet.

![alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/gifs/google_sheets.gif)

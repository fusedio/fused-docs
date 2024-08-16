# Excel

Microsoft Excel can import data from a given URL in `.csv` format. You can use this to load data from a UDF into an Excel sheet.


## 1. Create a UDF in Fused Hosted API

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


## 2. Create a URL for the UDF

Now, [create a signed Tile HTTP endpoint](/basics/core-concepts/#generate-endpoints-with-workbench) for the UDF.

Append this query parameter to the end of the URL to structure the response as a CSV type: `?dtype_out_vector=csv`.

The generated URL should look like this:

`https://www.fused.io/server/v1/realtime-shared/ccd781317018362a6966c9f12b27e95f1fe2fd88ff339de90eb9ac35b87cf439/run/file?dtype_out_vector=csv`



## 3. Import Data to Excel

Open Excel, then click the `Data` tab in the top ribbon. Click `From Web`.

![alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/gifs/excel_start.png)

In the From Web dialog box, paste in the URL from your UDF, and click `OK`.

![alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/gifs/excel_load.png)

A preview of the data will be shown. Click `Load` to import the data to your Excel sheet. Optionally, you can click `Transform` to transform the data if needed.

![alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/gifs/excel_preview.png)

Your data from Fused will now be loaded to a new Excel sheet.

![alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/gifs/excel_loaded.png)


**_Note:_** The desktop version of Microsoft Excel is required. Microsoft Excel Online does not support loading data from web sources.

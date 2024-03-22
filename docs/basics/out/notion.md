---
search:
  boost: 10
---

# Notion integration

Embed responsive maps into your Notion pages to significantly enhance the utility and interactivity of your documentation, project plans, internal apps, or any other type of content you manage within Notion.

![alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/a_notion.png)

To render a map into a Notion page you'll embed an HTML map that you can host on AWS S3.

## Step 1. Generate a signed URL for a UDF

First, on Workbench, create and save a UDF that successfully renders in `Tile` mode. Under the "Settings" tab, click "Share" to generate a signed URL that enables running the specific URL via HTTP requests. Copy the generated `HTTP` URL which you will use in the next step.

![Alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/snippets_share.png)


## Step 2. Create a Leaflet HTML map

On your local system, create a `.html` file following the template below.

### Vector map

If rendering a vector map, ensure the URL string is suffixed with `?dtype_out_vector=mvt` and use the following lines to render it as a `vectorGrid` layer.

```html
const url = `https://www.fused.io/server/v1/realtime-shared/******/run/tiles/{z}/{x}/{y}?dtype_out_vector=mvt`
L.vectorGrid.protobuf(mvtUrl, {}).addTo(map);
```

### Raster map
If rendering a vector map, ensure the URL string is suffixed with `?dtype_out_raster=png` and use the following lines to render it as a `tileLayer`.

```html
const url = `https://www.fused.io/server/v1/realtime-shared/******/run/tiles/{z}/{x}/{y}?dtype_out_raster=png`
L.tileLayer(url, {maxZoom: 19}).addTo(map);
```

This template uses the Leaflet javascript package to create a map, and introduces a basemap `tileLayer` and a custom `vectorGrid` layer. Modify accordingly.

```html
<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="initial-scale=1,maximum-scale=1,user-scalable=no" />
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script src="https://unpkg.com/leaflet.vectorgrid@latest/dist/Leaflet.VectorGrid.bundled.js"></script>
    <style>
      #map {position: absolute; top: 0; right: 0; bottom: 0; left: 0;}
    </style>
  </head>
  <body>
    <div id="map">
    </div>
    <script>
      const map = L.map('map').setView([0, 0], 1);
      // Basemap
      L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>'
      }).addTo(map);

      // Vector map
      const url = `https://app.fused.io/server/v1/realtime-shared/********/run/tiles/{z}/{x}/{y}?dtype_out_vector=mvt`;
      L.vectorGrid.protobuf(url, {}).addTo(map);
    </script>
  </body>
</html>
```


## Step 3. Upload the HTML file to S3

Upload the `.html` file to an S3 bucket and set public access permissions. Get the object's URL, which you'll embed into Notion in the next step.

A sample object URL looks like this:

```
https://fused-magic.s3.us-west-2.amazonaws.com/username/notion_test_map.html
```


## Step 4. Embed the map into Notion

Click the `+` that appears when you hover on a new line and select embed, or simply type `/embed`. Paste the map's URL in the menu that appears.

![Alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/gifs/notion2.gif)

[This Notion Page](https://fusedio.notion.site/Demo-Overture-Dataset-Technical-Documentation-8b4138aa56a8483890a93febcc2f2f7f) shows what a sample Notion page looks like with an embedded map.

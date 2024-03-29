# Mapbox (HTML)

Bring your apps to life with embedded responsive maps that dynamically respond to user input.


This guide shows how to create a web map using the [Mapbox GL JS](https://docs.mapbox.com/mapbox-gl-js/example/) library to display vector or raster tiles from a custom tile server provided by Fused. 

You'll first generate a signed UDF URL and render it on an HTML map. You can then use the HTML map in a low-code app like Retool or render it as an `iframe` in an app such as Notion.

## 1. Generate a signed URL for a UDF

First, on Workbench, create and save a UDF that successfully renders in `Tile` mode. Under the "Settings" tab, click "Share" to [generate a signed URL](/basics/core-concepts/#generate-endpoints-with-workbench) that can be called via HTTP requests. 


Modify the generated `HTTP` URL to run as a [Tile](/core-concepts/#call-udfs-with-http-requests) by setting the `tiles/` path paramater, followed by templated `/{z}/{x}/{y}` path. You can optionally pass UDF parameters as UDF-encoded strings, which can be configured to change based on UI user input.


## 2. Create a Mapbox HTML map

Create an `.html` file following this template. This code creates a mapbox map, adds a source, then a layer that renders data from that source. This is a basic example. Read on to see how to configure vector and raster layers.

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Add a vector tile source</title>
<meta name="viewport" content="initial-scale=1,maximum-scale=1,user-scalable=no">
<link href="https://api.mapbox.com/mapbox-gl-js/v3.2.0/mapbox-gl.css" rel="stylesheet">
<script src="https://api.mapbox.com/mapbox-gl-js/v3.2.0/mapbox-gl.js"></script>
<style>
body { margin: 0; padding: 0; }
#map { position: absolute; top: 0; bottom: 0; width: 100%; }
</style>
</head>
<body>
<div id="map"></div>
<script>
	mapboxgl.accessToken = 'pk.eyJ1IjoiZXN0b3JudWRhbWUiLCJhIjoiY2xneTh0Y3czMDczODNmcG11ZTNuazZvbSJ9.QFTdgqDlAFQKaJ_QLA35ew';
    const map = new mapboxgl.Map({
        container: 'map',
        // Choose from Mapbox's core styles, or make your own style with Mapbox Studio
        style: 'mapbox://styles/mapbox/dark-v10',
        zoom: 13,
        center: [-122.447303, 37.753574]
    });

    // Optionally, pass parameters to the tile source
    const model = {
        theme: 'building'
    }

    map.on('load', () => {
        map.addSource('fused-vector-source', {
            'type': 'vector',
            'tiles': [ // Vector Tile URL that returns mvt (https://docs.mapbox.com/data/tilesets/guides/vector-tiles-standards/)
                `https://www.fused.io/server/v1/realtime-shared/55ffe996fc2bd635cde3beda7e2632005e228798a1ef333297240b86af7d12a4/run/tiles/{z}/{x}/{y}?dtype_out_vector=mvt&type=${model.theme}`
            ],
            'minzoom': 6,
            'maxzoom': 14
        });
        map.addLayer(
            {
                'id': 'fused-vector-layer', // Layer ID
                'type': 'line',
                'source': 'fused-vector-source', // ID of the tile source created above
                'source-layer': 'udf', // Important! The source-layer name is 'udf' for all Fused vector tiles
                'layout': {
                    'line-cap': 'round',
                    'line-join': 'round'
                },
                'paint': {
                    'line-opacity': 0.6,
                    'line-color': 'rgb(53, 175, 109)',
                    'line-width': 2
                }
            }
        );
    })
</script>

</body>
</html>

```

### Vector layers

Use the following snippet to introduce a vector layer, which should look similar to this. The layer in the sample map comes from [Overture Buildings UDF](https://github.com/fusedio/udfs/tree/main/public/Overture_Maps_Example).

<iframe src="/img/mapbox_vector.html"  height="300px" width="100%" scrolling="no"></iframe>

```html
<script>
    map.addSource('fused-vector-source', {
        'type': 'vector',
        'tiles': [ // Vector Tile URL that returns mvt (https://docs.mapbox.com/data/tilesets/guides/vector-tiles-standards/)
            `https://www.fused.io/server/v1/realtime-shared/55ffe996fc2bd635cde3beda7e2632005e228798a1ef333297240b86af7d12a4/run/tiles/{z}/{x}/{y}?dtype_out_vector=mvt&type=${model.theme}`
        ],
        'minzoom': 6,
        'maxzoom': 14
    });
    map.addLayer(
        {
            'id': 'fused-vector-layer', // Layer ID
            'type': 'line',
            'source': 'fused-vector-source', // ID of the tile source created above
            'source-layer': 'udf', // Important! The source-layer name is 'udf' for Fused vector tiles
            'layout': {
                'line-cap': 'round',
                'line-join': 'round'
            },
            'paint': {
                'line-opacity': 0.6,
                'line-color': 'rgb(53, 175, 109)',
                'line-width': 2
            }
        }
    );
</script>
```

### Raster layers

Use the following snippet to introduce a raster layer, which should look similar to this. The layer in the sample map comes from the [Solar Irradiance UDF](https://github.com/fusedio/udfs/tree/main/public/Solar_Irradiance).

<iframe src="/img/mapbox_raster.html"  height="300px" width="100%" scrolling="no"></iframe>

```html
<script>
    map.addSource('fused-irradiation-source', {
        'type': 'raster',
        'tiles': [ // Raster Tile URL that returns png
            'https://www.fused.io/server/v1/realtime-shared/af0bc71e64075233b731f316988b323ac28658059db9e87388393fe187752501/run/tiles/{z}/{x}/{y}?dtype_out_raster=png'
        ],
        'tileSize': 256,
        'minzoom': 10,
        'maxzoom': 18
    });
    map.addLayer(
        {
            'id': 'wms-test-layer',
            'type': 'raster',
            'source': 'fused-irradiation-source',
            'paint': {}
        },
        'building' // Place layer under labels, roads and buildings.
    ); 
</script>
```



# Retool

Run Fused UDFs from Retool.

This guide shows how to create a [custom Retool component](https://docs.retool.com/apps/web/guides/components/custom) using the [Mapbox GL JS](https://docs.mapbox.com/mapbox-gl-js/example/) library to render vector tiles.

You'll first generate a signed UDF URL then introduce it into a custom map component that can input and output data across other Retool components.

## 1. Create an HTML map

Create a mapbox `.html` map following this [tutorial](/user-guide/out/mapbox/).

## 2. Create a custom Retool component

In a Retool app, create a custom Retool component. In the `IFrame Code` box, paste the code Mapbox HTML map created in the first step.

![alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/retool-1.png)

It's that easy. The following two sections show how to interchange data with the map component you just created. That's a bit more elaborate, but you're in good hands.

## 3. Pass data from a UI component to the map (optional)

Create a component that accepts user input which will be passed as a query parameter to the Fused endpoint.

This example uses a `select` component. Add options to the component - in this case `building`, `water`, and `place` because in the sample UDF these are passed in the `type` parameter to select different "theme" layers of the Overture dataset.

![alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/retool-2.png)

In Retool custom components, variables are passed through the Model. The IFrame code receives updates from Retool via a subcribe function. The Retool docs further explain how to [pass data to your custom component](https://docs.retool.com/apps/web/guides/components/custom#pass-data-to-your-custom-component).

In the custom component's `Model` box, paste a snippet like this one to pass data from the `select` component.

```json
{
  "theme": {{select1.value}}
}
```

Now subscribe the sections of code that will make use of the model values by wrapping all map components within a `window.Retool.subscribe` function. In this example, the value of `model.theme` is passed to a query parameter via string interpolation. When the value changes in the UI element, the value will update for the map.

```js
window.Retool.subscribe(function (model) {

    const map = new mapboxgl.Map({
        ...
    });

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
            ...
        );
    })
})
```

The result should look like this.

![alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/gifs/retool_in.gif)

## 4. Pass data from the map to a UI component (optional)

Passing data from the map component to another Retool component follows a similar process. This example introduces a drawing tool to draw custom polygons on the preceding map, then pass the polygons' geojson to a `jsonExplorer` Retool component.

First, update the custom component's model to include a `data` key with an empty dictionary as a value. This is where the map component will pass data.

```json
{
  "theme": {{select1.value}},
  "data": {}
}
```

Then, introduce these headers and snippet to the map IFrame.

```html
<script src="https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-draw/v1.2.1/mapbox-gl-draw.js"></script>
<link rel="stylesheet" href="https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-draw/v1.2.1/mapbox-gl-draw.css" type="text/css">
```

This is a [MapboxDraw](https://github.com/mapbox/mapbox-gl-draw) component. Ensure it's wrapped within the same `window.Retool.subscribe` function introduced in step 3 so Retool updates the `data` field when a change in the draw component triggers the `updateData` function.

```js
var draw = new MapboxDraw({
    displayControlsDefault: false,
    controls: {
        polygon: true,
        trash: true
    }
});
map.addControl(draw);

map.on('draw.create', updateData);
map.on('draw.delete', updateData);
map.on('draw.update', updateData);

function updateData(e) {
    var data = draw.getAll();
    window.Retool.modelUpdate({ data })
}
```

Finally, create a `jsonExplorer` component with the following value `{{customComponent1.model.data}}` which will receive the GeoJSON when a polygon is drawn on the map.

![alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/gifs/retool_out.gif)

This GeoJSON can be used in subsequent operations. For example, it could be passed as a parameter to downstream UDF calls as explained [here](/user-guide/out/http/#with-a-geojson).

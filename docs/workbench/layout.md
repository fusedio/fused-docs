---
search:
  boost: 10
---

# Workbench Layout

The Fused Workbench is styled like the familiar IDE format - so developers feel right at home. Just like an IDE, the main interface is the code editor. However, Workbench takes it to the next level by deeply integrating the code editor to the adjacent [deck.gl](http://deck.gl) map and expanding their joint capabilities in significant ways.

On the Workbench, developers rapidly iterate on UDFs and instantly see the effect of their code on the map. The immediacy is a result of strategic data partitioning and caching, which enables Fused to interactively load, process, and view any size datasets.

![Alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/image-17.png)

## UDF Editor

### Code Editor

The UDF Editor is where developers author UDFs. They can write Python to explore and analyze geospatial data of any size interactively.

![Alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/image-1.png)

#### Auto, Tile, and File

A UDF can set to render its outputs on Workbench as a Tile or File - or autodetect between the two based on parameters. The choice depends on the nature of data the UDF will return. New UDFs are set to autodetect by default, and the kind can be changed in the top-right dropdown of the code editor.

<!-- You can read more about the difference between the two types of outputs in the [core concepts section](/core_concepts/#tile-vs-file-udfs). -->

<!-- ![alt text](image.png) -->

:::note
Because a UDF can be called as either File or Tile, Workbench must explicitly know how to render their output. When a UDF is configured as "Auto", Workbench automatically handles the output as Tile if it statically checks that the types `fused.types.TileXYZ`, `fused.types.TileGDF`, or `fused.types.Bbox` are used in the UDF. Otherwise, it assumes File.

Note that the "Auto" setting is specific and applicable only to the Workbench UI. UDFs called via `fused-py` or HTTP requests run as Tile only if a parameter specifies the Tile geometry. 

:::

#### Toolbar

The toolbar atop the editor is where buttons to configure, save, duplicate, download, and delete UDFs are located. Clicking “Download” saves the present state of the UDF code and module locally as a `.zip` file that can be loaded with the Python SDK or shared with others so they can import into their workbench.

![Alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/image-34.png)


#### Error indicator

Sifting through error logs to debug failed multi-hour jobs is a persistent and recurring annoyance of working with large datasets and data orchestrators. The Fused Workbench is desiged with sound developer experience in mind. As such, the UDF code editor immediately highlights errors in the code, so developers can flow and focus on what matters.

![Alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/gifs/editor_error.gif)



### Module


As UDFs grow in complexity, it's useful to modularize the code to make it reusable and composable. It's also a good practice to keep only the essential "business logic" in the decorated UDF function - this makes it easy to know what a UDF does at a glance.

With this in mind, a Fused UDF can optionally import Python objects from its acompanying module, with an import statement as if importing from a Python package. In the Workbench, the "module" code editor tab is the place for helper functions and other associated Python objects for the UDF to import. Keep in mind that the module's name is configurable in order to avoid naming collisions.

In this example, UDF imports the function `arr_to_plasma` from its module, which is named `utils`. The function contains support logic the UDF uses it to transform an array.

```python
@fused.udf
def udf(bbox):
    from utils import arr_to_plasma
    ...
    return arr_to_plasma(arr.values, min_max=(0, .8))
```

![Alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/image-33.png)

#### Exporting modules

A module goes wherever its UDF goes.

This means that when a user saves, exports, shares, or uploads a UDF, the code for the module and for the UDF stays together and the import statement works the same. For example, clicking "Download" on a UDF downloads a `.zip` file containing a `.py` file for each with both the module and the UDF code.

> 💡 Note: At the moment, UDFs in the Workbench have a single module. To support advanced use cases, the Python SDK support multiple modules per UDF.


### Visualization


A layer is a geo visualization that made up of the UDF's Python code, the output of its execution, and associated visual configurations like color, line width, etc. In the Workbench, layers have a 1:1 relationship with UDFs.

#### Powered by deck.gl

Fused maps data (a vector or raster output from a UDF) as a stack of visual layers. To display it, Fused uses the industry standard [deck.gl TileLayer](https://deck.gl/docs/api-reference/geo-layers/tile-layer) - an open source, high-performance data visualization framework. This means users can feel right at home with programmatic control of each aspect of rendering.

![Alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/image-7.png)

#### Style layers

Layers are highly customizable. Developers can edit the code to transform the underlying data to show on the map, then edit what it looks like.

The visualization configuration uses **[@deck.gl/json](https://deck.gl/docs/api-reference/json/conversion-reference)** to implement a **[TileLayer](https://deck.gl/docs/api-reference/geo-layers/tile-layer)** with a **[GeoJsonLayer](https://deck.gl/docs/api-reference/layers/geojson-layer)** sublayer.

For example, the visualization json for a vector tile layer that dynamically sets `LineColor` properties from a GeoDataFrame (line `18`), might look like this.

![Alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/image-5.png)

### Settings


The settings tab is where each UDF can be configured. This section provides quick access to caching and to metadata associated with discoverability and the UDF's profile card.


![Alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/image-27.png)

#### Cache

UDFs run code remotely and return outputs to the browser over the network. Consequently, the map may feel sloggy if UDFs return a large data volume. To resolve this, users can enable caching to store the UDF's returned data in S3.

> 💡 Note that when a UDF's cache is enabled, its output data is stored by default in a Fused-managed S3 bucket. Fused is serious about giving users full control over where their data is stored. Get in touch to set your own bucket.

![Alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/image-28.png)

#### Snippets

Once a user creates a UDF in the Workbench, they can use snippets to call it and load its output it into other workflows. The "Snippets" section shows copyable commands to trigger the UDF from within a Python environment or bash.

By default, UDFs can only be called by user account that creates them. This can be done with the snippets below.

![Alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/snippets2.png)

It's also possible to generate signed tokens that allow anyone with the token to call the UDF. These tokens can be revoked.

![Alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/gifs/sign_url.gif)





#### Default parameter values

UDFs can be called with the parameters they explicitly define. Typed parameters can be set manually or automatically inferred within workbench, then used to trigger parametrized UDF runs via API. It's also possible to set predefined values that appear as options.

![Alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/gifs/parameters.gif)

#### Default view state

Setting a default view state on a published or shared UDF helps users navigate to a default viewport. That viewport can optionally be enabled and configured in this section. These values can be set manually or automatically by clicking "Set current map view".

![Alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/default_view_state.png)

UDFs with the default view state enabled show a "Zoom to layer" button. Clicking it sets the viewport to the preconfigured state.


![Alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/gifs/zoom_to_layer.gif)

#### Image preview

A URL of the image to show for the UDF preview thumbnail. This can be set to any remote address that is open to the public. Fused recommends S3.

![Alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/image-30.png)

#### Tags

Tags relevant to the UDF to make it easy to find in the Explorer search.

![Alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/image-31.png)

#### Description

It's good practice to document UDFs with a brief description of their purpose, code, and datasets they import Markdown text box to include general information about the UDF. The markdown supports links, code blocks, and headers.

![Alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/image-32.png)


## Navigation


### UDF Explorer

Clicking the "Add UDF" button on the navbar opens the UDF Explorer.

![Alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/image-20.png)

The Explorer is the one-stop-shop to browse personal and public UDFs, upload UDF zip files, and create new UDFs.


![Alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/image-19.png)

### UDF List

Users can create, delete, reorder, show/hide, and save layers on the UDF list.

Clicking a layer will make it the “active” layer and bring up its associated code in the right-hand editor. From there, clicking on the “visualization” tab will bring up the editor to style the layer.

![Alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/image-6.png)

If a UDF renders an output specific to a location, or has "default view state" enabled, clicking the "zoom to layer" icon will quickly pan the viewport to the area of interest. This is useful when switching between UDFs and to get context when opening a UDF a colleague shared.


![Alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/gifs/zoom_to_layer.gif)

### Preferences

The gear icon on the navbar contains global preferences. These toggle show/hide workbench sections, set the runtime environment, set the app's color theme, and show the user available keyboard shortcuts.

![Alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/image-18.png)

#### Save the Workbench session state [EXPERIMENTAL]

While debugging, it might be useful to download or restore the Workbench's configuration. To this end, the Workbench session's state can be downloaded as a JSON file. When the file is uploaded to a Fused Workbench, the app will reinstate the session.

![Alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/restore_session.png)


## Map

As developers iterate on UDFs and conduct exploratory data analysis, the interactive Deck.gl map gives them immediate feedback of the effect the code has on the data. This powerful feature reduces iteration time and increases productivity. As a developer zooms and moves the map between points of interest, Fused automatically runs the UDF code on the tiles shown in the viewport.

![Alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/gifs/viewport_sf.gif)

This means that a data scientist can instantly visualize the output of a complex geospatial operations - then run at any scale without engineering heavy-lifting.

As an example, this image shows the output of a UDF that calculates the shortest path from census block groups to nearby hospitals, colored by travel distance. Loading the original census data is slow, and route planning operations are cumbersome on distributed compute systems, but Fused's caching and parallelization immediately gets the data to the screen, so analysts can ask deeper questions on the spot.

![Alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/gabe_sf_route.png)

#### Toolbar

As developers interact with the map to inspect the UDF's results, they will find powerful utilities along the edges of the viewport. On the top left, they can click a toggle button to pause or resume the execution of the UDF code. Hitting pause on execution is useful to extensively edit a UDF or to glance at adjacent areas without rendering the layer for them.

> 💡 Tip: The viewport tilts and rotates via `CMD` + Click, then drag.

![Alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/map_toolbar.png)

### Sidebar

The sidebar on the top-right of the map also furnishes powerful utilities. These include a geocoder to direct the viewport to searched locations, a selector to change the basemap, a button to capture screenshots of the viewport, and toggles to enable a tooltip and fullscreen mode.

![Alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/gifs/map_toolbar_v7.gif)

### Debugger

As you write a UDF in Workbench, you might want information about the data that renders - or fails to render - in a particular area of the viewport.

Whether you are looking to determine the attributes of a specific rendered pixel or determine why no data is showing, you can inspect the map with the interactive debugger.

To enable it, simply click on the area of the map you want to inspect. To tuck it away, click "Clear debug selection" in the bottom right-hand menu, or select another UDF.


![Alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/gifs/viewport_debugger.gif)

If data renders successfully, the attribute values and coordinates of the selected point will appear in the "Selected Object" tab in the Results pane.

Otherwise, if there's an error, the error code and associated information will appear.

## Results

Exploratory data analysis is characterized by logs & print statements, previewing intermediary outputs, and sifting through error logs. The results section is designed with the developer in mind - it dynamically surfaces only the information that is relevant at each moment. It shows content related to the UDF execution in 4 tabs which include `stderr` and `stdout` logs, and specifics about the present tile.

> 💡 All UDF logs associated with or resulting from user code are ephemeral. They are passed to the frontend for debugging purposes, but are not persisted anywhere.

#### Toolbar

The toolbar atop the Results pane is where buttons to download the viewport data and UDF response objecs.

### Stdout

The "Stdout" tab shows the UDF's `stdout`, which includes logs or print statements. Its toolbar has buttons to download the stdout as a text file and the results as a GeoJSON, when applicable.

![Alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/image-21.png)

> 💡 Pro-tip: Within the result box, `CMD` + Click on a URL opens it in a new tab.


### Errors

The "Errors" tab contains the `stderr` trace if the UDF execution raises an error, and the toolbar has a button to download it. This helps developers debug UDF code.

![Alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/image-22.png)


### Selected Object

This tab shows a GeoJSON of the object that is selected on the map.

![Alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/image-23.png)


### Request Details

For Tile UDFs, this last tab shows a JSON with the `bbox` XYZ index and bounds.

![Alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/image-24.png)

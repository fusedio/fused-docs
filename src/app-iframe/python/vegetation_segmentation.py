import streamlit as st
# Sidebar sliders for parameters
# st.header("Model Parameters")

available_indices = [
    'VARI: Visible Atmospherically Resistant Index',  # Visible Atmospherically Resistant Index
    'GLI: Green Leaf Index',  # Green Leaf Index
    'RGRI: Red-Green Ratio Index (>0.9 for buildings)',  # Red-Green Ratio Index
    # 'ExG: Excess Green Index',     # Excess Green Index
    # 'NGRDI: Normalized Green-Red Difference Index',    # Normalized Green-Red Difference Index
]

selected_name = st.selectbox("Select Vegetation Index", available_indices)
index_method = available_indices.index(selected_name)

# Slider for morphological kernel size
index_min, index_max = st.slider("Thresholding Index Values",
                                 min_value=0.0,
                                 max_value=1.0,
                                 value=(0.1, 0.9),
                                 step=0.01)
mask = st.checkbox("Show Mask", value=True)
st.components.v1.html(f"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Fused DeckGL</title>
    <meta
      name="viewport"
      content="initial-scale=1,maximum-scale=1,user-scalable=no"
    />

    <script src="https://unpkg.com/@deck.gl/core@^9.0.0/dist.min.js"></script>
    <script src="https://unpkg.com/@deck.gl/layers@^9.0.0/dist.min.js"></script>
    <script src="https://unpkg.com/@deck.gl/geo-layers@^9.0.0/dist.min.js"></script>
    <script src="https://unpkg.com/@deck.gl/carto@^9.0.0/dist.min.js"></script>
    <script src="https://unpkg.com/h3-js"></script>
    <script src="https://unpkg.com/deck.gl@latest/dist.min.js"></script>
    <script src="https://api.mapbox.com/mapbox-gl-js/v3.2.0/mapbox-gl.js"></script>
    <link
      href="https://api.mapbox.com/mapbox-gl-js/v3.2.0/mapbox-gl.css"
      rel="stylesheet"
    />
    <style>
      body {{
        width: 100vw;
        height: 100vh;
        margin: 0;
      }}
    </style>
  </head>
  <body>
    <div id="map"></div>
    <script>
      const {{ DeckGL, H3HexagonLayer, GeoJsonLayer, BitmapLayer, TileLayer }} = deck;

      new DeckGL({{
        // mapboxApiAccessToken:
        //   "pk.eyJ1IjoiZXN0b3JudWRhbWUiLCJhIjoiY2xneTh0Y3czMDczODNmcG11ZTNuazZvbSJ9.QFTdgqDlAFQKaJ_QLA35ew",
        // mapStyle: "mapbox://styles/mapbox/dark-v10",
        initialViewState: {{
          longitude: -122.837838,
          latitude: 49.291155,
          zoom: 16,
        }},
        controller: true,
        layers: [
          new TileLayer({{
            id: "base",
            data: "https://www.fused.io/server/v1/realtime-shared/fsh_2YDT4gAuNEasD4CWu6Mave/run/tiles/{{z}}/{{x}}/{{y}}?dtype_out_raster=png&index_min={index_min}&index_max={index_max}&index_method={index_method}&return_mask=False",
            maxZoom: 25,
            minZoom: 0,

            renderSubLayers: props => {{
              const {{boundingBox}} = props.tile;
            
              return new BitmapLayer(props, {{
                data: null,
                image: props.data,
                bounds: [boundingBox[0][0], boundingBox[0][1], boundingBox[1][0], boundingBox[1][1]]
              }});
            }},
          }}),
          new TileLayer({{
            id: "data",
            data: "https://www.fused.io/server/v1/realtime-shared/fsh_2YDT4gAuNEasD4CWu6Mave/run/tiles/{{z}}/{{x}}/{{y}}?dtype_out_raster=png&index_min={index_min}&index_max={index_max}&index_method={index_method}&return_mask={mask}",
            maxZoom: 25,
            minZoom: 0,

            renderSubLayers: props => {{
              const {{boundingBox}} = props.tile;
            
              return new BitmapLayer(props, {{
                data: null,
                image: props.data,
                bounds: [boundingBox[0][0], boundingBox[0][1], boundingBox[1][0], boundingBox[1][1]]
              }});
            }},
          }}),
        ],
      }});
    </script>
  </body>
</html>
""",
                      height=600)

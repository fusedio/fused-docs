import streamlit as st
import folium
from folium.plugins import Draw
from streamlit_folium import st_folium
import requests
import json
import pandas as pd
import io
import urllib.parse
import plotly.graph_objects as go
import base64
import numpy
import time

# Constants
MONTHS = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]
GREY_COLORS = ["#FFFFFF", "#CCCCCC", "#999999", "#666666", "#333333", "#333333"]


def encode_geojson(geojson):
    json_string = json.dumps(geojson, separators=(",", ":"))
    return urllib.parse.quote(json_string)


def make_api_call(geojson, h3_size=5):
    url = "https://www.fused.io/server/v1/realtime-shared/fsh_2YYNSXQCEZnERzYB10OZ3b/run/file"
    params = {
        "dtype_out_raster": "tiff",
        "dtype_out_vector": "csv",
        "geojson": encode_geojson(geojson),
        "h3_size": h3_size,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.content
    else:
        return f"Error: {response.status_code}, {response.text}"


def generate_html_content(rainfall_data, center_lat, center_lon):
    rainfall_array_json = json.dumps(rainfall_data)
    rainfall_array_encoded = urllib.parse.quote(rainfall_array_json)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Vector Tile Map with Similarity-based Color Gradient and Tooltip</title>
        <meta name="viewport" content="initial-scale=1,maximum-scale=1,user-scalable=no">
        <link href="https://api.mapbox.com/mapbox-gl-js/v2.14.1/mapbox-gl.css" rel="stylesheet">
        <script src="https://api.mapbox.com/mapbox-gl-js/v2.14.1/mapbox-gl.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/chroma-js/2.4.2/chroma.min.js"></script>
        <style>
            body {{ margin: 0; padding: 0; }}
            #map {{ position: absolute; top: 0; bottom: 0; width: 100%; }}
            .mapboxgl-popup {{
                max-width: 400px;
                font: 12px/20px 'Helvetica Neue', Arial, Helvetica, sans-serif;
            }}
            #legend {{
                position: absolute;
                bottom: 20px;
                right: 20px;
                background: rgba(255, 255, 255, 0.8);
                padding: 10px;
                border-radius: 3px;
            }}
            #stopwatch {{
                position: absolute;
                top: 10px;
                left: 10px;
                background: rgba(255, 255, 255, 0.8);
                padding: 5px 10px;
                border-radius: 3px;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div id="map"></div>
        <div id="legend"></div>
        <div id="stopwatch">Loading time: 0.00s</div>
        <script>
            let startTime;
            let stopwatchInterval;
            let isTimerRunning = false;
            let tilesLoading = 0;
            let completionTimeout;

            function startStopwatch() {{
                if (!isTimerRunning) {{
                    startTime = Date.now();
                    stopwatchInterval = setInterval(updateStopwatch, 10);
                    isTimerRunning = true;
                    document.getElementById('stopwatch').textContent = 'Loading time: 0.00s';
                }}
            }}

            function stopStopwatch() {{
                if (isTimerRunning) {{
                    clearInterval(stopwatchInterval);
                    isTimerRunning = false;
                    const finalTime = ((Date.now() - startTime) / 1000).toFixed(2);
                    document.getElementById('stopwatch').textContent = `Loading time: ${{finalTime}}s (Completed)`;
                }}
            }}

            function updateStopwatch() {{
                const elapsedTime = (Date.now() - startTime) / 1000;
                document.getElementById('stopwatch').textContent = `Loading time: ${{elapsedTime.toFixed(2)}}s`;
            }}

            function resetAndStartStopwatch() {{
                clearTimeout(completionTimeout);
                if (isTimerRunning) {{
                    clearInterval(stopwatchInterval);
                    isTimerRunning = false;
                }}
                tilesLoading = 0;
                startStopwatch();
            }}

            function scheduleStopwatch() {{
                clearTimeout(completionTimeout);
                completionTimeout = setTimeout(() => {{
                    stopStopwatch();
                }}, 1000);
            }}

            mapboxgl.accessToken = 'pk.eyJ1IjoibWlsaW5kc29uaSIsImEiOiJjbDRjc2ZxaTgwMW5hM3Bqbmlka3VweWVkIn0.AM0QzfbGzUZc04vZ6o2uaw';
            const map = new mapboxgl.Map({{
                container: 'map',
                style: 'mapbox://styles/mapbox/dark-v10',
                zoom: 7,
                center: [{center_lon}, {center_lat}]
            }});

            const popup = new mapboxgl.Popup({{
                closeButton: false,
                closeOnClick: false
            }});

            const colorScale = chroma.scale(['#FF0000', '#FF6600', '#FFFF00', '#00FF00', '#0000FF'])
            .mode('lch').domain([0, 0.25, 0.5, 0.75, 1]);

            map.on('load', () => {{
                map.addSource('fused-vector-source', {{
                    'type': 'vector',
                    'tiles': [
                        'https://www.fused.io/server/v1/realtime-shared/fsh_3bVC7EFJLhSFVJqeuk1pcM/run/tiles/{{z}}/{{x}}/{{y}}?dtype_out_vector=mvt&input_array={rainfall_array_encoded}'
                    ],
                    'minzoom': 3,
                    'maxzoom': 14
                }});

                map.addLayer({{
                    'id': 'fused-vector-layer',
                    'type': 'fill',
                    'source': 'fused-vector-source',
                    'source-layer': 'udf',
                    'paint': {{
                        'fill-color': [
                            'interpolate',
                            ['linear'],
                            ['get', 'similarity'],
                            0, colorScale(0).hex(),
                            0.25, colorScale(0.25).hex(),
                            0.5, colorScale(0.5).hex(),
                            0.75, colorScale(0.75).hex(),
                            1, colorScale(1).hex()
                        ],
                        'fill-opacity': 0.7
                    }}
                }});

                resetAndStartStopwatch();

                map.on('sourcedata', (e) => {{
                    if (e.isSourceLoaded && e.sourceId === 'fused-vector-source') {{
                        tilesLoading = Math.max(0, tilesLoading - 1);
                        if (tilesLoading === 0) {{
                            scheduleStopwatch();
                        }}
                    }}
                }});

                map.on('dataloading', (e) => {{
                    if (e.sourceId === 'fused-vector-source') {{
                        tilesLoading++;
                        resetAndStartStopwatch();
                    }}
                }});

                map.on('idle', () => {{
                    if (tilesLoading === 0 && isTimerRunning) {{
                        scheduleStopwatch();
                    }}
                }});

                map.on('movestart', () => {{
                    resetAndStartStopwatch();
                }});
                
                map.on('mousemove', 'fused-vector-layer', (e) => {{
                    if (e.features.length > 0) {{
                        const feature = e.features[0];
                        const coordinates = e.lngLat;

                        let popupContent = '<h3>Feature Properties:</h3>';
                        for (const property in feature.properties) {{
                            popupContent += `<strong>${{property}}:</strong> ${{feature.properties[property]}}<br>`;
                        }}

                        popup.setLngLat(coordinates).setHTML(popupContent).addTo(map);
                    }}
                }});

                map.on('mouseleave', 'fused-vector-layer', () => {{
                    popup.remove();
                }});

                const legend = document.getElementById('legend');
                const gradientSteps = 5;
                for (let i = 0; i <= gradientSteps; i++) {{
                    const step = i / gradientSteps;
                    const color = colorScale(step).hex();
                    legend.innerHTML += `<div style="background: ${{color}}; width: 20px; height: 20px; display: inline-block;"></div>`;
                }}
                legend.innerHTML += '<br>Low Similarity <span style="float: right;">High Similarity</span>';
            }});

            map.on('error', (e) => {{
                console.error('Mapbox GL JS error:', e);
                stopStopwatch();
                document.getElementById('stopwatch').textContent += ' (Error)';
            }});
        </script>
    </body>
    </html>
    """
    return html_content


def main():
    st.set_page_config(layout="wide")
    st.title("Twin City App")

    # Initialize session state
    if "api_result" not in st.session_state:
        st.session_state.api_result = None
    if "drawn_shape" not in st.session_state:
        st.session_state.drawn_shape = None
    if "rainfall_data" not in st.session_state:
        st.session_state.rainfall_data = None

    # Create a layout container
    with st.container(border=True):
        col1, col2 = st.columns([3, 2])

        with col1:
            st.subheader("Location Selector")
            # Initialize map
            m = folium.Map(
                location=[37.7749, -122.4194], tiles="cartodbdark_matter", zoom_start=5
            )
            draw = Draw(
                export=True,
                position="topleft",
                draw_options={
                    "polyline": False,
                    "polygon": True,
                    "circle": False,
                    "marker": False,
                    "circlemarker": False,
                    "rectangle": True,
                },
            )
            m.add_child(draw)
            output = st_folium(m, width=None, height=400)

            if output["all_drawings"] is not None and output["all_drawings"]:
                st.session_state.drawn_shape = output["all_drawings"][-1]

        with col2:
            st.subheader("Parameter Selection 📊")
            parameter = st.selectbox("Select Parameter", ["Precipitation"])

            if st.session_state.drawn_shape is not None:
                if st.button("Get Data"):
                    with st.spinner("Fetching and processing data..."):
                        # Fetch data
                        geojson_for_api = {
                            "type": "Polygon",
                            "coordinates": st.session_state.drawn_shape["geometry"][
                                "coordinates"
                            ],
                        }
                        st.session_state.api_result = make_api_call(geojson_for_api)

                        # Process and display results
                        if isinstance(st.session_state.api_result, bytes):
                            try:
                                csv_data = io.StringIO(
                                    st.session_state.api_result.decode("utf-8")
                                )
                                df = pd.read_csv(csv_data)

                                if "rainfall" in df.columns and isinstance(
                                    df["rainfall"].iloc[0], str
                                ):
                                    df["rainfall"] = df["rainfall"].apply(eval)

                                if "rainfall" in df.columns:
                                    # Multiply by 10 and round off the rainfall data
                                    st.session_state.rainfall_data = [
                                        round(x * 10) for x in df["rainfall"].iloc[0]
                                    ]
                                    chart_data = pd.DataFrame(
                                        {
                                            "Month": MONTHS,
                                            "Rainfall": st.session_state.rainfall_data,
                                        }
                                    )

                                    st.bar_chart(
                                        chart_data.set_index("Month")["Rainfall"]
                                    )
                            except Exception as e:
                                st.error(f"Error parsing API response: {str(e)}")
                        else:
                            st.error(st.session_state.api_result)

    # Display Hex-Similarity Map if rainfall data is available
    if st.session_state.rainfall_data is not None:
        st.subheader("Hex-Similarity Map")
        # Fixed coordinates for New York City
        new_york_lat, new_york_lon = 40.7128, -74.0060
        html_content = generate_html_content(
            st.session_state.rainfall_data, new_york_lat, new_york_lon
        )
        encoded_content = base64.b64encode(html_content.encode()).decode()

        st.components.v1.iframe(
            f"data:text/html;base64,{encoded_content}",
            width=None,
            height=600,
            scrolling=True,
        )


if __name__ == "__main__":
    main()

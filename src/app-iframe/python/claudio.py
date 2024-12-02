import micropip
import streamlit as st
import streamlit.components.v1 as components

await micropip.install(["geopandas", "fused"])
from datetime import datetime, timedelta

import fused

# Title for the app
st.title("🚗 Trip Simulation: _Downtown Lima_")

# Define the start of today
today = datetime.now()
start_date = datetime(today.year, today.month, today.day)

# Slider to select a time during today
start_hour = st.sidebar.slider(
    "Select a 15-minute timeslot",
    min_value=start_date,
    max_value=start_date + timedelta(hours=24) - timedelta(minutes=15),
    value=start_date + timedelta(hours=8),
    format="HH:mm",
    step=timedelta(minutes=15),
)

# Format the times to pass to Fused
end_hour = start_hour + timedelta(minutes=15)
start_hour_str = start_hour.strftime("%Y-%m-%d %H:%M:%S")
end_hour_str = end_hour.strftime("%Y-%m-%d %H:%M:%S")

# Display the times for confirmation
st.sidebar.markdown(
    f"**Timeslot:** {start_hour.strftime('%H:%M')} to {end_hour.strftime('%H:%M')}"
)

gdf = fused.run("UDF_Simple_Trips_Gen_Lima", start_hour=start_hour, end_hour=end_hour)

if "path" in gdf.columns:
    gdf["path"] = gdf["path"].astype(str)

number_of_lines = len(gdf)

geojson = gdf.to_json()

html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Delhi Metro Map</title>
    <link href="https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.css" rel="stylesheet">
    <script src="https://api.mapbox.com/mapbox-gl-js/v3.7.0/mapbox-gl.js"></script>
    <script src="https://unpkg.com/@turf/turf@6/turf.min.js"></script>
    <style>
        body {{ margin: 0; padding: 0; }}
        #map {{ position: absolute; top: 0; bottom: 0; width: 100%; }}
        .title {{
            position: absolute;
            top: 20px;
            left: 20px;
            background: rgba(0, 0, 0, 0.8);
            padding: 15px;
            border-radius: 8px;
            color: white;
            font-family: 'Arial', sans-serif;
            z-index: 1;
            box-shadow: 0 0 20px rgba(255, 255, 255, 0.2);
        }}
    </style>
</head>
<body>
    <div id="map"></div>
    <div class="title">
        <h2 style="margin: 0;"># Trips: {number_of_lines}</h2>
    </div>
    <script>
        mapboxgl.accessToken = 'pk.eyJ1IjoibWlsaW5kc29uaSIsImEiOiJjbDRjc2ZxaTgwMW5hM3Bqbmlka3VweWVkIn0.AM0QzfbGzUZc04vZ6o2uaw';

        const map = new mapboxgl.Map({{
            container: 'map',
            style: 'mapbox://styles/mapbox/dark-v11',
            center: [-77.10, -12.0262542],
            zoom: 11,
            pitch: 45,
            bearing: -17.6
        }});

        map.addControl(new mapboxgl.NavigationControl());

        const colors = {{
            'work': '#FF0000',
            'home': '#00FF00'
        }};

        function createPointOnLine(line, distance) {{
            return turf.along(turf.lineString(line), distance);
        }}

        map.on('load', () => {{
            // Add the metro lines source
            map.addSource('metro-lines', {{
                type: 'geojson',
                data: {geojson}
            }});

            // Add a thicker background line for better visibility
            map.addLayer({{
                'id': 'metro-lines-background',
                'type': 'line',
                'source': 'metro-lines',
                'paint': {{
                    'line-color': '#ffffff',
                    'line-width': 5,
                    'line-opacity': 0.2
                }}
            }});

            // Base solid line
            map.addLayer({{
                'id': 'metro-lines-base',
                'type': 'line',
                'source': 'metro-lines',
                'paint': {{
                    'line-color': [
                        'match',
                        ['get', 'Name'],
                        ...Object.entries(colors).flat()
                    ],
                    'line-width': 3,
                    'line-opacity': 0.8
                }}
            }});

            // Outer glow for the line
            map.addLayer({{
                'id': 'metro-lines-glow',
                'type': 'line',
                'source': 'metro-lines',
                'paint': {{
                    'line-color': [
                        'match',
                        ['get', 'Name'],
                        ...Object.entries(colors).flat()
                    ],
                    'line-width': 6,
                    'line-blur': 3,
                    'line-opacity': 0.4
                }}
            }});

            // Add dashed line overlay for additional visual interest
            map.addLayer({{
                'id': 'metro-lines-dash',
                'type': 'line',
                'source': 'metro-lines',
                'paint': {{
                    'line-color': [
                        'match',
                        ['get', 'Name'],
                        ...Object.entries(colors).flat()
                    ],
                    'line-width': 2,
                    'line-opacity': 0.6,
                    'line-dasharray': [2, 4]
                }}
            }});

            const features = {geojson}.features;
            features.forEach((feature, idx) => {{
                const processLine = (coordinates, lineIdx = null) => {{
                    const idSuffix = lineIdx !== null ? `-${{lineIdx}}` : '';
                    const lineString = turf.lineString(coordinates);
                    const lineLength = turf.length(lineString);
                    const lineColor = colors[feature.properties.route_type] || '#FFFFFF';

                    // Create point source
                    map.addSource(`point-${{idx}}${{idSuffix}}`, {{
                        'type': 'geojson',
                        'data': createPointOnLine(coordinates, 0)
                    }});

                    // Largest glow
                    map.addLayer({{
                        'id': `point-glow-large-${{idx}}${{idSuffix}}`,
                        'source': `point-${{idx}}${{idSuffix}}`,
                        'type': 'circle',
                        'paint': {{
                            'circle-radius': 20,
                            'circle-color': lineColor,
                            'circle-opacity': 0.15,
                            'circle-blur': 1
                        }}
                    }});

                    // Medium glow
                    map.addLayer({{
                        'id': `point-glow-medium-${{idx}}${{idSuffix}}`,
                        'source': `point-${{idx}}${{idSuffix}}`,
                        'type': 'circle',
                        'paint': {{
                            'circle-radius': 10,
                            'circle-color': lineColor,
                            'circle-opacity': 0.3,
                            'circle-blur': 0.5
                        }}
                    }});

                    // Core point
                    map.addLayer({{
                        'id': `point-core-${{idx}}${{idSuffix}}`,
                        'source': `point-${{idx}}${{idSuffix}}`,
                        'type': 'circle',
                        'paint': {{
                            'circle-radius': 4,
                            'circle-color': '#FFFFFF',
                            'circle-opacity': 1
                        }}
                    }});

                    function animate(timestamp) {{
                        const duration = 8000;
                        const progress = (timestamp % duration) / duration;
                        const distance = progress * lineLength;

                        const point = createPointOnLine(coordinates, distance);
                        map.getSource(`point-${{idx}}${{idSuffix}}`).setData(point);

                        requestAnimationFrame(animate);
                    }}

                    animate(0);
                }};

                if (feature.geometry.type === 'MultiLineString') {{
                    feature.geometry.coordinates.forEach((line, lineIdx) => {{
                        processLine(line, lineIdx);
                    }});
                }} else {{
                    processLine(feature.geometry.coordinates);
                }}
            }});

            // Auto-zoom to show the selected line(s)
            const bounds = new mapboxgl.LngLatBounds();
            features.forEach(feature => {{
                if (feature.geometry.type === 'MultiLineString') {{
                    feature.geometry.coordinates.forEach(line => {{
                        line.forEach(coord => bounds.extend(coord));
                    }});
                }} else {{
                    feature.geometry.coordinates.forEach(coord => bounds.extend(coord));
                }}
            }});
            map.fitBounds(bounds, {{ padding: 50 }});
        }});
    </script>
</body>
</html>
"""

st.markdown(
    """
    <style>
        .stApp {
            background-color: #0a0a0a;
        }
        .css-18e3th9 {
            padding-top: 0;
        }
        .css-1d391kg {
            padding-top: 1rem;
        }
    </style>
""",
    unsafe_allow_html=True,
)

components.html(html_content, height=800)

#!/usr/bin/env python3
"""
Mini-Web Interactive Map Generator
===================================

Generates an educational interactive map of US federal administrative districts
optimized for web hosting and civics education.
"""

import folium
from folium import plugins
import geopandas as gpd
import json
from pathlib import Path
from map_config import MAP_CONFIG, LAYERS, BRANCH_INFO


class EducationalMapGenerator:
    """Generate educational interactive map with district layers"""

    def __init__(self, output_file='index.html'):
        """
        Initialize the map generator

        Parameters:
        -----------
        output_file : str
            Output HTML filename
        """
        self.output_file = output_file
        self.map = None
        self.script_dir = Path(__file__).parent

    def create_base_map(self):
        """Create base Folium map"""
        print("Creating base map...")

        self.map = folium.Map(
            location=MAP_CONFIG['center'],
            zoom_start=MAP_CONFIG['zoom_start'],
            tiles=MAP_CONFIG['tiles'],
            min_zoom=MAP_CONFIG.get('min_zoom', 3),
            max_zoom=MAP_CONFIG.get('max_zoom', 10),
            prefer_canvas=True,  # Better performance
        )

        # Add fullscreen button
        plugins.Fullscreen(
            position='topright',
            title='Fullscreen View',
            title_cancel='Exit Fullscreen',
            force_separate_button=True
        ).add_to(self.map)

        print("✓ Base map created")

    def add_educational_sidebar(self):
        """Add educational information sidebar to the map"""
        print("Adding educational sidebar...")

        sidebar_html = """
        <div id="edu-sidebar" style="
            position: fixed;
            top: 10px;
            left: 10px;
            width: 350px;
            max-height: calc(100vh - 120px);
            background: white;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            overflow-y: auto;
            z-index: 1000;
        ">
            <h2 style="
                margin: 0 0 15px 0;
                color: #2c3e50;
                font-size: 22px;
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
            ">US Federal Districts</h2>

            <p style="
                margin: 0 0 15px 0;
                color: #555;
                font-size: 14px;
                line-height: 1.6;
            ">
                An educational map showing how the federal government divides the United States
                for administrative purposes across the three branches of government.
            </p>

            <!-- Address Search Section -->
            <div id="search-section" style="margin-bottom: 20px; padding: 15px; background: #f8f9fa; border-radius: 8px; border: 2px solid #3498db;">
                <h3 style="
                    margin: 0 0 10px 0;
                    color: #2980b9;
                    font-size: 16px;
                ">📍 Find Your Districts</h3>
                <p style="margin: 0 0 10px 0; font-size: 12px; color: #666;">
                    Enter your address to discover all federal districts you live in:
                </p>
                <input type="text" id="address-input" placeholder="123 Main St, City, State" style="
                    width: 100%;
                    padding: 8px 12px;
                    border: 2px solid #ddd;
                    border-radius: 5px;
                    font-size: 14px;
                    margin-bottom: 10px;
                    box-sizing: border-box;
                ">
                <button id="search-btn" onclick="searchAddress()" style="
                    width: 100%;
                    padding: 10px;
                    background: linear-gradient(135deg, #3498db, #2ecc71);
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-size: 14px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: transform 0.2s;
                ">🔍 Find My Districts</button>
                <div id="search-status" style="
                    margin-top: 8px;
                    font-size: 12px;
                    color: #666;
                    display: none;
                "></div>
            </div>

            <!-- Results Panel (initially hidden) -->
            <div id="results-panel" style="
                display: none;
                margin-bottom: 20px;
                padding: 15px;
                background: #fff3cd;
                border-radius: 8px;
                border-left: 4px solid #ffc107;
                max-height: 400px;
                overflow-y: auto;
            ">
                <h3 style="
                    margin: 0 0 10px 0;
                    color: #856404;
                    font-size: 16px;
                ">Your Districts</h3>
                <div id="results-content"></div>
            </div>

            <div style="margin-bottom: 20px;">
                <h3 style="
                    margin: 0 0 10px 0;
                    color: #2980b9;
                    font-size: 16px;
                ">How to Use:</h3>
                <ul style="
                    margin: 0;
                    padding-left: 20px;
                    color: #555;
                    font-size: 13px;
                    line-height: 1.8;
                ">
                    <li>Enter your address above to find your districts</li>
                    <li>Click layer names in the control (top right) to show/hide</li>
                    <li>Click on regions to see district information</li>
                    <li>Use fullscreen button for better viewing</li>
                </ul>
            </div>

            <div id="branch-info" style="margin-top: 20px;">
                <h3 style="
                    margin: 0 0 10px 0;
                    color: #27ae60;
                    font-size: 16px;
                ">Three Branches of Government</h3>
                <div style="font-size: 12px; color: #555; line-height: 1.6;">
                    <div style="margin-bottom: 12px; padding: 10px; background: #e8f4f8; border-radius: 5px;">
                        <strong style="color: #2980b9;">⚖️ Judicial Branch</strong><br>
                        Interprets laws and ensures constitutional compliance.
                    </div>
                    <div style="margin-bottom: 12px; padding: 10px; background: #e8f8f0; border-radius: 5px;">
                        <strong style="color: #27ae60;">🏛️ Executive Branch</strong><br>
                        Enforces laws and administers federal programs.
                    </div>
                    <div style="margin-bottom: 12px; padding: 10px; background: #e8f0f8; border-radius: 5px;">
                        <strong style="color: #3498db;">🛡️ Military/Defense</strong><br>
                        Protects national security under civilian control.
                    </div>
                </div>
            </div>

            <div style="margin-top: 20px; padding-top: 15px; border-top: 1px solid #ddd;">
                <p style="margin: 0; font-size: 11px; color: #888;">
                    <strong>About:</strong> This map shows 10 key federal district systems
                    representing all three branches of government. Data has been simplified
                    for web performance while maintaining accuracy.
                </p>
            </div>
        </div>
        """

        self.map.get_root().html.add_child(folium.Element(sidebar_html))
        print("✓ Educational sidebar added")

    def create_educational_popup(self, properties, layer_config):
        """
        Create educational popup HTML for a feature

        Parameters:
        -----------
        properties : dict
            GeoJSON feature properties
        layer_config : dict
            Layer configuration including educational content

        Returns:
        --------
        str
            HTML content for popup
        """
        edu = layer_config.get('education', {})

        # Build popup HTML
        html = f"""
        <div style="font-family: Arial, sans-serif; min-width: 280px; max-width: 350px;">
            <h3 style="margin: 0 0 12px 0; color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 8px;">
                {edu.get('title', layer_config['name'])}
            </h3>

            <div style="margin-bottom: 12px; padding: 10px; background: #f8f9fa; border-radius: 5px;">
                <strong style="color: #555;">District Information:</strong><br>
        """

        # Add relevant properties
        for key, value in properties.items():
            if key.lower() not in ['shape_area', 'shape_leng', 'objectid', 'fid'] and value:
                html += f"""
                <div style="margin: 5px 0; font-size: 13px;">
                    <strong>{key}:</strong> {value}
                </div>
                """

        html += "</div>"

        # Add educational content
        if edu:
            html += f"""
            <div style="margin-top: 12px; padding: 10px; background: #fff3cd; border-radius: 5px; border-left: 4px solid #ffc107;">
                <div style="margin-bottom: 8px; font-size: 13px; line-height: 1.5;">
                    <strong style="color: #856404;">Purpose:</strong><br>
                    {edu.get('purpose', '')}
                </div>
            </div>

            <div style="margin-top: 10px; font-size: 12px; color: #666;">
                <div style="margin: 5px 0;">
                    <strong>Structure:</strong> {edu.get('structure', '')}
                </div>
                <div style="margin: 5px 0;">
                    <strong>Established:</strong> {edu.get('established', '')}
                </div>
            </div>

            <div style="margin-top: 10px; padding: 8px; background: #e7f3ff; border-radius: 5px; font-size: 12px;">
                <strong style="color: #0056b3;">Why This Matters:</strong><br>
                {edu.get('why_it_matters', '')}
            </div>
            """

        html += "</div>"
        return html

    def add_layer(self, layer_id, layer_config):
        """
        Add a layer to the map

        Parameters:
        -----------
        layer_id : str
            Layer identifier
        layer_config : dict
            Layer configuration from map_config.py
        """
        print(f"Adding layer: {layer_config['name']}")

        try:
            # Load GeoJSON
            file_path = self.script_dir / layer_config['file']
            if not file_path.exists():
                print(f"  ⚠️  File not found: {file_path}")
                return

            gdf = gpd.read_file(file_path)

            # Ensure WGS84
            if gdf.crs and gdf.crs.to_epsg() != 4326:
                gdf = gdf.to_crs(epsg=4326)

            # Clean up data - remove NaN values and convert non-serializable types
            for col in gdf.columns:
                if col != 'geometry':
                    # Convert to string to handle Timestamp and other types
                    gdf[col] = gdf[col].astype(str).fillna('')

            # Convert entire GeoDataFrame to GeoJSON
            geojson_data = json.loads(gdf.to_json())

            # Create popup function that generates HTML for each feature
            def create_popup_fn(feature):
                props = feature.get('properties', {})
                popup_html = self.create_educational_popup(props, layer_config)
                return folium.Popup(popup_html, max_width=400)

            # Add entire layer as single GeoJson with feature-specific popups
            folium.GeoJson(
                geojson_data,
                name=layer_config['name'],
                style_function=lambda x, style=layer_config['style']: style,
                highlight_function=lambda x, h_style=layer_config.get('highlight_style', {}): h_style,
                tooltip=folium.GeoJsonTooltip(
                    fields=list(geojson_data['features'][0]['properties'].keys()) if geojson_data.get('features') else [],
                    aliases=list(geojson_data['features'][0]['properties'].keys()) if geojson_data.get('features') else [],
                    localize=True
                ),
                popup=folium.GeoJsonPopup(
                    fields=list(geojson_data['features'][0]['properties'].keys()) if geojson_data.get('features') else [],
                    aliases=list(geojson_data['features'][0]['properties'].keys()) if geojson_data.get('features') else [],
                    localize=True,
                    labels=True
                ),
                show=layer_config.get('enabled_by_default', False),
            ).add_to(self.map)

            print(f"  ✓ Added {len(gdf)} features")

        except Exception as e:
            print(f"  ⚠️  Error: {e}")
            import traceback
            traceback.print_exc()

    def add_legend(self):
        """Add custom legend explaining district types"""
        print("Adding legend...")

        legend_html = """
        <div style="
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            font-family: Arial, sans-serif;
            font-size: 13px;
            z-index: 1000;
        ">
            <h4 style="margin: 0 0 10px 0; color: #2c3e50; font-size: 14px;">District Types</h4>
            <div style="margin: 5px 0;">
                <span style="display: inline-block; width: 20px; height: 15px; background: #4A90E2; margin-right: 8px; border: 1px solid #2C5AA0;"></span>
                Judicial Branch
            </div>
            <div style="margin: 5px 0;">
                <span style="display: inline-block; width: 20px; height: 15px; background: #51CF66; margin-right: 8px; border: 1px solid #2F9E44;"></span>
                Executive Branch
            </div>
            <div style="margin: 5px 0;">
                <span style="display: inline-block; width: 20px; height: 15px; background: #4DABF7; margin-right: 8px; border: 1px solid #1971C2;"></span>
                Military/Defense
            </div>
            <p style="margin: 10px 0 0 0; font-size: 11px; color: #666;">
                Use layer control (top right) to toggle layers
            </p>
        </div>
        """

        self.map.get_root().html.add_child(folium.Element(legend_html))
        print("✓ Legend added")

    def add_search_javascript(self):
        """Add JavaScript for address geocoding and district lookup"""
        print("Adding search functionality...")

        # Build layer data for JavaScript - including actual GeoJSON features
        layer_data = {}
        for layer_id, config in LAYERS.items():
            try:
                file_path = self.script_dir / config['file']
                if file_path.exists():
                    gdf = gpd.read_file(file_path)
                    if gdf.crs and gdf.crs.to_epsg() != 4326:
                        gdf = gdf.to_crs(epsg=4326)

                    # Clean NaN values and convert non-serializable types
                    for col in gdf.columns:
                        if col != 'geometry':
                            # Convert to string to handle Timestamp and other types
                            gdf[col] = gdf[col].astype(str).fillna('')

                    geojson_data = json.loads(gdf.to_json())

                    layer_data[config['name']] = {
                        'features': geojson_data.get('features', []),
                        'branch': config.get('branch', ''),
                        'education': config.get('education', {})
                    }
            except Exception as e:
                print(f"  Warning: Could not load {layer_id} for search: {e}")

        search_js = f"""
        <script>
        // Store search marker globally
        var searchMarker = null;
        var highlightLayer = null;
        var foliumMap = null;

        // Embedded layer data with actual GeoJSON features for searching
        var layerData = {json.dumps(layer_data)};

        // Find the Folium map object (it has a unique variable name)
        function getFoliumMap() {{
            if (foliumMap) return foliumMap;

            // Folium creates map variables like map_XXXXX
            for (var key in window) {{
                if (key.startsWith('map_') && window[key] instanceof L.Map) {{
                    foliumMap = window[key];
                    console.log('Folium map found:', key);
                    return foliumMap;
                }}
            }}
            return null;
        }}

        async function searchAddress() {{
            // Get the map reference
            const map = getFoliumMap();
            if (!map) {{
                alert('Map not ready yet. Please wait a moment and try again.');
                return;
            }}
            const addressInput = document.getElementById('address-input');
            const searchBtn = document.getElementById('search-btn');
            const searchStatus = document.getElementById('search-status');
            const resultsPanel = document.getElementById('results-panel');
            const resultsContent = document.getElementById('results-content');

            const address = addressInput.value.trim();

            if (!address) {{
                alert('Please enter an address');
                return;
            }}

            // Show loading state
            searchBtn.disabled = true;
            searchBtn.textContent = '🔍 Searching...';
            searchStatus.style.display = 'block';
            searchStatus.textContent = 'Geocoding address...';
            searchStatus.style.color = '#666';
            resultsPanel.style.display = 'none';

            try {{
                // Geocode using Nominatim (OpenStreetMap)
                const geocodeUrl = `https://nominatim.openstreetmap.org/search?format=json&q=${{encodeURIComponent(address)}}&countrycodes=us&limit=1`;

                const response = await fetch(geocodeUrl, {{
                    headers: {{
                        'User-Agent': 'Federal-Districts-Educational-Map/1.0'
                    }}
                }});

                if (!response.ok) {{
                    throw new Error('Geocoding service unavailable');
                }}

                const data = await response.json();

                if (data.length === 0) {{
                    searchStatus.textContent = '❌ Address not found. Try being more specific.';
                    searchStatus.style.color = '#e74c3c';
                    searchBtn.disabled = false;
                    searchBtn.textContent = '🔍 Find My Districts';
                    return;
                }}

                const lat = parseFloat(data[0].lat);
                const lon = parseFloat(data[0].lon);
                const displayName = data[0].display_name;

                searchStatus.textContent = '✓ Location found! Finding districts...';

                // Find containing districts
                const matchingDistricts = findContainingDistricts(lat, lon);

                // Display results
                displayResults(lat, lon, displayName, matchingDistricts);

                // Add/update marker
                if (searchMarker) {{
                    map.removeLayer(searchMarker);
                }}
                searchMarker = L.marker([lat, lon], {{
                    icon: L.icon({{
                        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
                        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
                        iconSize: [25, 41],
                        iconAnchor: [12, 41],
                        popupAnchor: [1, -34],
                        shadowSize: [41, 41]
                    }})
                }}).addTo(map);
                searchMarker.bindPopup(`<b>Your Location:</b><br>${{displayName}}<br><b>Districts:</b> ${{matchingDistricts.length}}`).openPopup();

                // Zoom to location
                map.setView([lat, lon], 8);

                searchStatus.style.display = 'none';

            }} catch (error) {{
                console.error('Search error:', error);
                searchStatus.textContent = '❌ Error: ' + error.message;
                searchStatus.style.color = '#e74c3c';
            }} finally {{
                searchBtn.disabled = false;
                searchBtn.textContent = '🔍 Find My Districts';
            }}
        }}

        function findContainingDistricts(lat, lon) {{
            const matching = [];

            // Search through embedded layer data instead of DOM
            for (const layerName in layerData) {{
                const layer = layerData[layerName];
                const features = layer.features || [];

                // Check each feature in this layer
                for (const feature of features) {{
                    if (feature.geometry && isPointInPolygon(lat, lon, feature.geometry)) {{
                        matching.push({{
                            layerName: layerName,
                            properties: feature.properties || {{}},
                            branch: layer.branch || 'Other',
                            education: layer.education || {{}}
                        }});
                    }}
                }}
            }}

            return matching;
        }}

        function isPointInPolygon(lat, lon, geometry) {{
            // Simple point-in-polygon test
            // For MultiPolygon, check all polygons
            if (geometry.type === 'MultiPolygon') {{
                for (let poly of geometry.coordinates) {{
                    if (testPolygon(lat, lon, poly[0])) return true;
                }}
                return false;
            }} else if (geometry.type === 'Polygon') {{
                return testPolygon(lat, lon, geometry.coordinates[0]);
            }}
            return false;
        }}

        function testPolygon(lat, lon, polygon) {{
            // Ray casting algorithm
            let inside = false;
            for (let i = 0, j = polygon.length - 1; i < polygon.length; j = i++) {{
                const xi = polygon[i][1], yi = polygon[i][0];
                const xj = polygon[j][1], yj = polygon[j][0];

                const intersect = ((yi > lon) !== (yj > lon))
                    && (lat < (xj - xi) * (lon - yi) / (yj - yi) + xi);
                if (intersect) inside = !inside;
            }}
            return inside;
        }}

        function displayResults(lat, lon, address, districts) {{
            const resultsPanel = document.getElementById('results-panel');
            const resultsContent = document.getElementById('results-content');

            if (districts.length === 0) {{
                resultsContent.innerHTML = `
                    <p style="margin: 0; color: #856404;">
                        No federal districts found at this location. This may be outside the US or in a data gap.
                    </p>
                `;
                resultsPanel.style.display = 'block';
                return;
            }}

            // Group by branch (branch is now directly in the district data)
            const byBranch = {{}};
            districts.forEach(d => {{
                const branch = d.branch || 'Other';
                if (!byBranch[branch]) byBranch[branch] = [];
                byBranch[branch].push(d);
            }});

            // Build HTML
            let html = `
                <div style="margin-bottom: 12px; padding: 10px; background: white; border-radius: 5px;">
                    <strong style="color: #856404;">📍 Location:</strong><br>
                    <span style="font-size: 12px;">${{address}}</span>
                </div>
                <p style="margin: 10px 0 15px 0; font-size: 13px; color: #856404;">
                    <strong>You are within ${{districts.length}} federal district(s):</strong>
                </p>
            `;

            // Judicial Branch
            if (byBranch['Judicial']) {{
                html += `
                    <div style="margin-bottom: 15px;">
                        <h4 style="margin: 0 0 8px 0; color: #2980b9; font-size: 14px;">⚖️ JUDICIAL BRANCH</h4>
                `;
                byBranch['Judicial'].forEach(d => {{
                    html += formatDistrictResult(d);
                }});
                html += '</div>';
            }}

            // Executive Branch
            if (byBranch['Executive']) {{
                html += `
                    <div style="margin-bottom: 15px;">
                        <h4 style="margin: 0 0 8px 0; color: #27ae60; font-size: 14px;">🏛️ EXECUTIVE BRANCH</h4>
                `;
                byBranch['Executive'].forEach(d => {{
                    html += formatDistrictResult(d);
                }});
                html += '</div>';
            }}

            // Military
            if (byBranch['Military']) {{
                html += `
                    <div style="margin-bottom: 15px;">
                        <h4 style="margin: 0 0 8px 0; color: #3498db; font-size: 14px;">🛡️ MILITARY/DEFENSE</h4>
                `;
                byBranch['Military'].forEach(d => {{
                    html += formatDistrictResult(d);
                }});
                html += '</div>';
            }}

            resultsContent.innerHTML = html;
            resultsPanel.style.display = 'block';

            // Scroll to results
            resultsPanel.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
        }}

        function formatDistrictResult(district) {{
            const props = district.properties;
            const edu = district.education || {{}};

            // Get primary identifier - check all possible name fields across datasets
            let identifier = props.NAME || props.name ||
                           props.DISTRICT || props.district ||
                           props.REGION || props.region ||
                           props.NAMELSAD ||
                           props.ADMU_NAME ||           // BLM Districts
                           props.COURT_NAME ||          // Bankruptcy Courts
                           props.CIRCUIT_NAME ||        // Courts of Appeals
                           props.DistrictName ||        // Coast Guard
                           props.EPAREGION ||           // EPA/FEMA/Education Regions
                           'Unknown';

            let html = `
                <div style="margin-bottom: 10px; padding: 8px; background: #f8f9fa; border-radius: 4px; border-left: 3px solid #3498db;">
                    <div style="font-size: 13px; font-weight: 600; color: #2c3e50; margin-bottom: 4px;">
                        ${{district.layerName}}
                    </div>
                    <div style="font-size: 12px; color: #555; margin-bottom: 6px;">
                        <strong>District:</strong> ${{identifier}}
                    </div>
            `;

            if (edu.purpose) {{
                html += `
                    <div style="font-size: 11px; color: #666; font-style: italic;">
                        ${{edu.purpose}}
                    </div>
                `;
            }}

            html += '</div>';
            return html;
        }}

        // Allow Enter key to trigger search
        document.addEventListener('DOMContentLoaded', function() {{
            const addressInput = document.getElementById('address-input');
            if (addressInput) {{
                addressInput.addEventListener('keypress', function(e) {{
                    if (e.key === 'Enter') {{
                        searchAddress();
                    }}
                }});
            }}
        }});
        </script>
        """

        self.map.get_root().html.add_child(folium.Element(search_js))
        print("✓ Search functionality added")

    def add_title(self):
        """Add title to the map"""
        title_html = """
        <div style="
            position: fixed;
            top: 10px;
            right: 60px;
            background: white;
            padding: 10px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            z-index: 999;
        ">
            <h1 style="
                margin: 0;
                font-size: 24px;
                color: #2c3e50;
                font-weight: 600;
            ">
                🗺️ US Federal Districts
                <span style="font-size: 14px; color: #7f8c8d; font-weight: normal;">
                    | Educational Map
                </span>
            </h1>
        </div>
        """

        self.map.get_root().html.add_child(folium.Element(title_html))

    def generate(self):
        """Generate the complete map"""
        print("\n" + "=" * 60)
        print("Educational Federal Districts Map Generator")
        print("=" * 60)

        # Create base map
        self.create_base_map()

        # Add title
        self.add_title()

        # Add educational sidebar
        self.add_educational_sidebar()

        # Add all layers
        print("\nAdding layers...")
        for layer_id, layer_config in LAYERS.items():
            self.add_layer(layer_id, layer_config)

        # Add layer control
        print("\nAdding layer control...")
        folium.LayerControl(
            position='topright',
            collapsed=False,
            autoZIndex=True,
        ).add_to(self.map)

        # Add legend
        self.add_legend()

        # Add search functionality
        self.add_search_javascript()

        # Save map
        output_path = self.script_dir / self.output_file
        print(f"\nSaving map to {output_path}...")
        self.map.save(str(output_path))

        # Get file size
        file_size_mb = output_path.stat().st_size / (1024 * 1024)

        print("\n" + "=" * 60)
        print("✅ MAP GENERATION COMPLETE!")
        print("=" * 60)
        print(f"Output file: {output_path}")
        print(f"File size: {file_size_mb:.2f} MB")
        print(f"\nTo view: open {self.output_file}")
        print("=" * 60)


def main():
    """Main execution"""
    generator = EducationalMapGenerator('index.html')
    generator.generate()


if __name__ == '__main__':
    main()

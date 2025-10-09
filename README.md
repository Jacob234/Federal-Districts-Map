# US Federal Districts - Educational Map (Mini-Web Version)

An interactive web map designed for civics education, showcasing how the US federal government divides the country for administrative purposes across the three branches of government.

## The only easy-to-access visualization of its kind on the internet
- overlays different administrative regions
- lets you see where you are situated within the federal gov's bureaucracy

## Future
- expand to more agencies
- add more educational aspects to learn about your districts and links to official resources
  

## 🎯 Purpose

This mini-web version is a streamlined, educational subset of the full [District-Maps project](../README.md), optimized for:
- **Static website hosting** (GitHub Pages, Netlify, personal websites)
- **Civics education** (students, teachers, general public)
- **Fast loading** (< 5MB total, optimized geometries)
- **Mobile accessibility** (responsive design)

## ✨ Features

### Educational Content
- **10 curated district systems** representing all three branches of government
- **In-depth descriptions** explaining each system's purpose and impact
- **Historical context** showing when and why each system was established
- **"Why It Matters"** sections connecting districts to everyday life

### Interactive Experience
- **Address Search** 🆕 - Find all federal districts for any US address
- **Layer toggle** - Show/hide different district systems
- **Click-to-learn** - Detailed popups with educational content
- **Color-coded branches** - Visual distinction between Judicial, Executive, and Military
- **Sidebar guide** - Always-visible instructions and branch information
- **Legend** - Clear explanation of district types
- **Geocoding** - Powered by OpenStreetMap/Nominatim (free, no API key)

### Technical Excellence
- **Optimized performance** - 97% file size reduction from source data
- **Mobile-responsive** - Works on all devices
- **Self-contained** - Single HTML file with embedded data
- **Client-side search** - No backend required, works on static hosts

## 📊 Included District Systems

### Judicial Branch (2 systems)
- **US Courts of Appeals Circuits** - 13 appellate court regions
- **US Bankruptcy Courts** - 90+ bankruptcy districts

### Executive Branch (7 systems)
- **FEMA Regions** - 10 emergency management regions
- **EPA Regions** - 10 environmental protection regions (foundational system)
- **Federal Reserve Districts** - 12 banking districts from 1913
- **Census Regions** - 4 major demographic regions
- **Census Divisions** - 9 sub-regions for detailed analysis
- **Department of Education Regions** - 10 administrative regions
- **BLM Districts** - Bureau of Land Management offices

### Military/Defense (1 system)
- **Coast Guard Districts** - 9 maritime defense regions

**Total**: 308 individual districts across 10 systems

## 🚀 Quick Start

### For Users (Viewing the Map)

1. **Download or host the files**:
   ```
   mini-web/
   ├── landing.html    # Introduction page
   ├── index.html      # Interactive map (5.29 MB)
   └── (data folder not needed after map generation)
   ```

2. **Open `landing.html` in a web browser**
   - Click "View Interactive Map" to explore
   - Or go directly to `index.html`

3. **Explore**:
   - **Try the address search!** Enter your address in the sidebar
   - See all federal districts you live in across all 10 systems
   - Use layer control (top right) to toggle systems
   - Click on regions for detailed information
   - Read the sidebar for branch explanations
   - Use fullscreen mode for better viewing

### Using Address Search 🆕

1. **Enter your address** in the search box in the left sidebar:
   - Example: `1600 Pennsylvania Ave, Washington, DC`
   - Example: `Times Square, New York, NY`
   - Example: `Golden Gate Bridge, San Francisco, CA`

2. **Click "Find My Districts"** or press Enter

3. **View your results**:
   - Map automatically zooms to your location
   - Red marker shows your address
   - Results panel displays ALL districts containing that location
   - Districts grouped by branch (Judicial/Executive/Military)
   - Educational information for each district

4. **Explore**:
   - Results are interactive - scroll through them
   - See the purpose and impact of each district
   - Learn why these districts matter to you
   - Try different addresses to compare

### For Developers (Regenerating the Map)

**Prerequisites**:
- Python 3.8+
- Virtual environment from parent project
- Source data from main project

**Generate map**:
```bash
cd mini-web
source ../venv/bin/activate
python generate_map.py
```

**Re-optimize data** (if source data changes):
```bash
python scripts/optimize_data.py
```

## 📁 Project Structure

```
mini-web/
├── landing.html              # Introduction/landing page
├── index.html                # Generated interactive map
├── README.md                 # This file
├── DEPLOYMENT.md             # Hosting instructions
│
├── generate_map.py           # Map generator script
├── map_config.py             # Layer configs with educational content
│
├── data/                     # Optimized GeoJSON files (2.84 MB)
│   ├── Courts_of_Appeals_Circuits.geojson
│   ├── Bankruptcy_Courts.geojson
│   ├── FEMA_Regions.geojson
│   ├── EPA_Regions.geojson
│   ├── Federal_Reserve_Districts.geojson
│   ├── Census_Regions.geojson
│   ├── Census_Divisions.geojson
│   ├── Education_Regions.geojson
│   ├── BLM_Districts.geojson
│   └── Coast_Guard_Districts.geojson
│
└── scripts/
    └── optimize_data.py      # Data optimization tool
```

## 🎓 Educational Use Cases

### For Students
- Understand the structure of the three branches of government
- See how federal services are organized geographically
- Learn about specific agencies and their roles
- Explore connections between districts and daily life

### For Teachers
- Visual aid for civics and government lessons
- Interactive exploration of federalism
- Real-world examples of administrative organization
- Discussion starter for separation of powers

### For General Public
- **Use address search to find YOUR districts!**
- Discover which federal districts you live in
- Understand federal emergency response organization
- Learn about the Federal Reserve system
- See how census data is organized

## 🔍 Address Search Feature

The mini-web version includes a powerful **address lookup** feature that makes civics education personal:

### How It Works

1. **Geocoding**: Converts your address to coordinates using OpenStreetMap/Nominatim
2. **Spatial Query**: Checks which district polygons contain that point
3. **Results Display**: Shows all matching districts grouped by branch
4. **Educational Context**: Includes purpose and impact for each district

### Example Searches

Try these addresses to see the feature in action:

- **White House**: `1600 Pennsylvania Ave, Washington, DC`
  - Judicial: DC Circuit Court of Appeals, DC Bankruptcy Court
  - Executive: FEMA Region 3, EPA Region 3, Federal Reserve District 5 (Richmond), etc.
  - Coast Guard: 5th District

- **Times Square**: `Times Square, New York, NY`
  - Judicial: 2nd Circuit Court of Appeals, Southern District of NY Bankruptcy
  - Executive: FEMA Region 2, EPA Region 2, Federal Reserve District 2 (New York), etc.
  - Coast Guard: 1st District

- **Golden Gate Bridge**: `Golden Gate Bridge, San Francisco, CA`
  - Judicial: 9th Circuit Court of Appeals, Northern District of CA Bankruptcy
  - Executive: FEMA Region 9, EPA Region 9, Federal Reserve District 12 (San Francisco), etc.
  - Coast Guard: 11th District

### Technical Details

- **No backend required** - Works entirely client-side
- **Free geocoding** - Uses Nominatim (OpenStreetMap)
- **Rate limits**: 1 request/second (automatic debouncing)
- **Privacy**: Address search is client-side only, not stored
- **Accuracy**: Point-in-polygon algorithm with ray-casting
- **Performance**: Results in < 1 second typically

### Limitations

- **US addresses only**: Search is restricted to US locations
- **Geocoding accuracy**: Depends on OpenStreetMap data quality
- **Rate limiting**: Wait 1 second between searches
- **Internet required**: Initial geocoding needs network connection

## 📈 Data Optimization

The mini-web version achieves dramatic file size reductions while maintaining accuracy:

| Dataset | Original | Optimized | Reduction |
|---------|----------|-----------|-----------|
| Census Divisions | 38.84 MB | 0.17 MB | 99.6% |
| Census Regions | 20.86 MB | 0.12 MB | 99.4% |
| Coast Guard | 15.70 MB | 0.16 MB | 99.0% |
| Federal Reserve | 6.76 MB | 0.46 MB | 93.2% |
| Courts of Appeals | 6.75 MB | 0.45 MB | 93.3% |
| FEMA Regions | 0.71 MB | 0.32 MB | 55.2% |
| *Total* | *~97 MB* | *2.84 MB* | *97.1%* |

**Optimization techniques**:
- Geometry simplification (0.005° - 0.02° tolerance)
- Removal of unnecessary attributes
- GeoJSON format compression
- Topology preservation

## 🌐 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed hosting instructions for:
- GitHub Pages
- Netlify
- Vercel
- Personal web servers

**TL;DR**: Upload `landing.html` and `index.html` to any static web host.

## 🔧 Customization

### Adding/Removing Layers

Edit `map_config.py`:
```python
LAYERS = {
    'new_layer': {
        'name': 'Display Name',
        'file': 'data/filename.geojson',
        'branch': 'Executive',
        'style': {...},
        'education': {...},
    },
}
```

### Changing Colors

Modify the `style` section in `map_config.py`:
```python
'style': {
    'fillColor': '#FF0000',     # Fill color
    'color': '#000000',          # Border color
    'weight': 2,                 # Border width
    'fillOpacity': 0.35,         # Transparency
},
```

### Educational Content

Update the `education` section for any layer:
```python
'education': {
    'title': 'Layer Title',
    'description': 'What this is...',
    'purpose': 'What it does...',
    'structure': 'How it's organized...',
    'established': 'When it was created...',
    'why_it_matters': 'Real-world impact...',
},
```

## 📊 Technical Details

**Technologies**:
- **GeoPandas** - Geospatial data processing
- **Folium** - Interactive map generation
- **Leaflet.js** (via Folium) - Client-side mapping
- **OpenStreetMap** - Base map tiles

**Data Format**: GeoJSON (EPSG:4326 / WGS84)

**Browser Support**:
- Chrome/Edge (recommended)
- Firefox
- Safari
- Mobile browsers

**Performance**:
- Initial load: ~1-3 seconds (depending on connection)
- Interaction: Instant
- Works offline: Yes (after initial load)

## 📝 License

This mini-web version uses the same license as the parent District-Maps project.
Source data comes from official US federal government agencies and is in the public domain.

## 🤝 Contributing

Since this is a subset of the larger project, contributions should generally be made to the [parent District-Maps repository](../README.md).

For mini-web specific suggestions:
- Educational content improvements
- Additional layer suggestions
- UI/UX enhancements
- Bug reports

## 🔗 Related Resources

- **Full Project**: [District-Maps](../README.md) - Complete system with all 45+ district types
- **Documentation**: [docs/](../docs/) - Comprehensive project documentation
- **Data Sources**: [data-sources.md](../docs/data/data-sources.md) - Where data comes from

## 📞 Support

Questions or issues? Open an issue on the main [District-Maps GitHub repository](https://github.com/yourusername/District-Maps).

## 🎓 Learn More

Want to understand more about federal administrative districts?

- [USA.gov - Branches of Government](https://www.usa.gov/branches-of-government)
- [Federal Register](https://www.federalregister.gov/) - Official government actions
- [Data.gov](https://data.gov/) - Federal open data portal

---

**Made with ❤️ for civics education**

*Last updated: October 2025*

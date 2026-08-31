# US Federal Districts — Interactive Educational Map

An interactive web map for civics education, showing how the US federal government
divides the country for administrative purposes across all three branches of
government — and letting you find every federal district *you* live in.

**Overlay judicial circuits, FEMA regions, Federal Reserve districts, Coast Guard
districts, and more — then search your address to see where you sit in the
federal government's geography.**

## Features

- **Address search** — geocode any US address (via OpenStreetMap/Nominatim) and see
  every federal district containing it, grouped by branch of government
- **"Use my location"** — one-tap district lookup via browser geolocation
- **10 district systems** across the Judicial, Executive, and Military branches
- **Educational popups** — click any region for its purpose, history, and why it
  matters, with links to official resources (each Federal Reserve bank and appeals
  circuit links to its own site)
- **Shareable links** — the URL tracks your enabled layers and last search, so you
  can send a classroom-ready view to anyone
- **Fast** — layers load lazily on first toggle (~100–500 KB each); no build step,
  no backend, no framework
- **Mobile-friendly** — collapsible sidebar, works on phones and tablets

## Included district systems

| Branch | System | Districts |
|---|---|---|
| ⚖️ Judicial | Courts of Appeals Circuits | 12 |
| ⚖️ Judicial | Bankruptcy Courts (grouped by circuit)¹ | 12 |
| 🏛️ Executive | FEMA Regions | 10 |
| 🏛️ Executive | EPA Regions | 10 |
| 🏛️ Executive | Federal Reserve Districts² | 12 |
| 🏛️ Executive | Census Regions | 4 |
| 🏛️ Executive | Census Divisions | 9 |
| 🏛️ Executive | Dept. of Education Regions | 10 |
| 🏛️ Executive | BLM Administrative Units | 220 |
| 🛡️ Military | Coast Guard Districts | 9 |

¹ The 90 bankruptcy courts follow the 94 federal judicial districts; this map
currently shows them grouped at the circuit level. District-level boundaries are
planned.
² The Federal Reserve is an independent central bank, grouped here with the
Executive branch for navigation.

## Running locally

The app fetches its data files, so it needs to be served over HTTP (opening
`index.html` directly from disk won't work):

```bash
python3 -m http.server 8000
# then open http://localhost:8000/
```

That's it — no dependencies, no build step.

## Project structure

```
index.html          # The map app
landing.html        # Introduction page
layers.json         # Layer registry: files, styles, educational content, links
js/app.js           # All application logic (Leaflet, search, point-in-polygon)
css/style.css       # Styles
data/*.geojson      # Optimized district boundaries (~2.8 MB total)
scripts/optimize_data.py  # Simplifies raw agency GeoJSON (needs geopandas)
```

## Adding a new district system

1. Get the boundaries as GeoJSON (WGS84 / EPSG:4326) from the agency —
   [data.gov](https://data.gov/) and agency open-data portals are good sources.
2. Optionally simplify it with `scripts/optimize_data.py` (requires Python +
   geopandas) to keep it under ~500 KB.
3. Drop the file in `data/` and add an entry to the `layers` array in
   `layers.json` — name, style colors, which property holds the district name
   (`nameField`), the educational text, and an official link.

No code changes needed for a standard polygon layer.

## Data & accuracy

- Boundaries are **simplified for web performance** (97% size reduction from
  source data) and are approximate — fine for education, not for legal use.
- Source data comes from official US federal agencies and is in the public domain.
- Address geocoding is performed client-side against OpenStreetMap's Nominatim
  service; addresses are not stored anywhere.

## Deployment

Any static host works — see [DEPLOYMENT.md](DEPLOYMENT.md). For GitHub Pages:
Settings → Pages → deploy from the `main` branch, and the map is live at
`https://<user>.github.io/Federal-Districts-Map/`.

## Roadmap

- US District Courts (the 94 judicial districts — also fixes footnote ¹)
- More agencies: US Attorney districts, HHS regions, Army Corps divisions,
  National Weather Service regions
- Printable "your federal government" report after an address search
- Per-district official links for more systems

## License

Code is open source; district boundary data is from US federal government
sources and in the public domain.

---

*Made for civics education.*

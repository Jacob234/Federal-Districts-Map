# Deployment Guide

The map is a plain static site — any static host works. Everything in the repo
root gets deployed:

```
index.html   landing.html   layers.json   js/   css/   data/
```

> **Important:** unlike earlier versions, the data is no longer embedded in
> `index.html`. The app fetches `layers.json` and the `data/*.geojson` files at
> runtime, so those files **must** be deployed alongside the HTML, and the site
> must be served over HTTP(S) — opening `index.html` from disk (`file://`)
> will not work.

## GitHub Pages (recommended)

1. In the repository, go to **Settings → Pages**.
2. Under **Build and deployment**, choose **Deploy from a branch**, select
   `main` and `/ (root)`, and save.
3. After a minute the site is live at
   `https://<username>.github.io/Federal-Districts-Map/`.

Every push to `main` redeploys automatically. No build step or GitHub Action
is needed.

- `index.html` (the map) is the default page.
- `landing.html` is the introduction page, linked from the map's About section.

## Netlify / Vercel / Cloudflare Pages

Point the platform at the repo, leave the build command empty, and set the
publish directory to the repo root. Done.

## Any web server

Copy the repo contents to the server's document root:

```bash
rsync -av --exclude='.git' --exclude='scripts' ./ user@server:/var/www/districts/
```

## Testing locally before deploying

```bash
python3 -m http.server 8000
# open http://localhost:8000/
```

## Notes

- **Geocoding**: address search calls `nominatim.openstreetmap.org` directly
  from the visitor's browser (free, no API key). Nominatim's usage policy
  allows light use like this; if the site ever gets heavy traffic, switch to a
  commercial geocoder or self-hosted Nominatim.
- **Base map tiles**: served by CARTO's free basemap CDN with OpenStreetMap
  attribution.
- **HTTPS**: required for the "Use my location" button (browsers block
  geolocation on insecure origins). GitHub Pages, Netlify, and Vercel all
  provide HTTPS by default.

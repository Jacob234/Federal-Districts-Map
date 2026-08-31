/*
 * US Federal Districts — Educational Map
 *
 * A hand-written Leaflet app. Layers are defined in layers.json and their
 * GeoJSON is fetched lazily the first time a layer is turned on, so the
 * initial page load stays small. Address search geocodes via Nominatim
 * (OpenStreetMap) and runs a client-side point-in-polygon lookup across
 * all layers.
 */

'use strict';

const state = {
  map: null,
  config: null,          // parsed layers.json
  layers: new Map(),     // id -> { config, leafletLayer, data (GeoJSON), loading }
  profiles: new Map(),   // layer id -> promise of parsed profiles file
  searchMarker: null,
  lastQuery: null,       // last successful search string, kept in the URL
  openProfile: null,     // { layerId, district } while the profile panel is open
};

// ---------------------------------------------------------------------------
// Bootstrap

document.addEventListener('DOMContentLoaded', init);

async function init() {
  const resp = await fetch('layers.json');
  state.config = await resp.json();

  state.map = L.map('map', {
    center: [39.8283, -98.5795],
    zoom: 4,
    minZoom: 3,
    maxZoom: 18,
    zoomControl: false,
  });
  L.control.zoom({ position: 'topright' }).addTo(state.map);

  L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 19,
  }).addTo(state.map);

  for (const layerConfig of state.config.layers) {
    state.layers.set(layerConfig.id, { config: layerConfig, leafletLayer: null, data: null, loading: null });
  }

  buildLayerPanel();
  wireControls();

  // Restore state from the URL (?layers=a,b&q=address)
  const params = new URLSearchParams(location.search);
  const urlLayers = params.get('layers');
  const enabled = urlLayers !== null
    ? urlLayers.split(',').filter((id) => state.layers.has(id))
    : state.config.layers.filter((l) => l.enabledByDefault).map((l) => l.id);
  enabled.forEach((id) => setLayerEnabled(id, true));

  const q = params.get('q');
  if (q) {
    document.getElementById('address-input').value = q;
    searchAddress();
  }

  // ?profile=layerId:District Name deep-links straight into a district profile
  const profileParam = params.get('profile');
  if (profileParam) {
    const sep = profileParam.indexOf(':');
    if (sep > 0) {
      const layerId = profileParam.slice(0, sep);
      const district = profileParam.slice(sep + 1);
      if (state.layers.has(layerId)) {
        setLayerEnabled(layerId, true);
        openProfile(layerId, district, { zoomTo: !q });
      }
    }
  }
}

// ---------------------------------------------------------------------------
// Layer panel (sidebar)

function buildLayerPanel() {
  const panel = document.getElementById('layer-panel');
  const byBranch = new Map();
  for (const layer of state.config.layers) {
    if (!byBranch.has(layer.branch)) byBranch.set(layer.branch, []);
    byBranch.get(layer.branch).push(layer);
  }

  for (const [branchId, layers] of byBranch) {
    const branch = state.config.branches[branchId] || { label: branchId, icon: '', color: '#666' };

    const group = document.createElement('div');
    group.className = 'branch-group';

    const heading = document.createElement('h3');
    heading.style.color = branch.color;
    heading.textContent = `${branch.icon} ${branch.label}`;
    heading.title = branch.blurb || '';
    group.appendChild(heading);

    for (const layer of layers) {
      group.appendChild(buildLayerRow(layer));
    }
    panel.appendChild(group);
  }
}

function buildLayerRow(layer) {
  const row = document.createElement('div');
  row.className = 'layer-row';

  const label = document.createElement('label');
  label.className = 'layer-label';

  const checkbox = document.createElement('input');
  checkbox.type = 'checkbox';
  checkbox.id = `toggle-${layer.id}`;
  checkbox.addEventListener('change', () => setLayerEnabled(layer.id, checkbox.checked));

  const swatch = document.createElement('span');
  swatch.className = 'swatch';
  swatch.style.background = layer.style.fillColor;
  swatch.style.borderColor = layer.style.color;

  const name = document.createElement('span');
  name.className = 'layer-name';
  name.textContent = layer.name;

  const spinner = document.createElement('span');
  spinner.className = 'spinner';
  spinner.id = `spinner-${layer.id}`;
  spinner.hidden = true;

  label.append(checkbox, swatch, name, spinner);

  const info = document.createElement('button');
  info.className = 'info-btn';
  info.type = 'button';
  info.setAttribute('aria-label', `About ${layer.name}`);
  info.textContent = 'ℹ';
  info.addEventListener('click', () => {
    const blurb = document.getElementById(`blurb-${layer.id}`);
    blurb.hidden = !blurb.hidden;
  });

  const blurb = document.createElement('div');
  blurb.className = 'layer-blurb';
  blurb.id = `blurb-${layer.id}`;
  blurb.hidden = true;
  blurb.innerHTML = educationHtml(layer, { compact: true });

  const top = document.createElement('div');
  top.className = 'layer-row-top';
  top.append(label, info);
  row.append(top, blurb);
  return row;
}

async function setLayerEnabled(id, enabled) {
  const entry = state.layers.get(id);
  if (!entry) return;
  const checkbox = document.getElementById(`toggle-${id}`);
  if (checkbox) checkbox.checked = enabled;

  if (enabled) {
    try {
      await ensureLayerData(id);
    } catch (err) {
      console.error(`Failed to load layer ${id}:`, err);
      if (checkbox) checkbox.checked = false;
      return;
    }
    if (!entry.leafletLayer) {
      entry.leafletLayer = L.geoJSON(entry.data, {
        style: () => entry.config.style,
        onEachFeature: (feature, lyr) => {
          lyr.bindPopup(() => featurePopupHtml(entry.config, feature.properties), { maxWidth: 340 });
          lyr.on('mouseover', () => lyr.setStyle({ fillOpacity: Math.min(entry.config.style.fillOpacity + 0.25, 0.75) }));
          lyr.on('mouseout', () => lyr.setStyle({ fillOpacity: entry.config.style.fillOpacity }));
        },
      });
    }
    entry.leafletLayer.addTo(state.map);
  } else if (entry.leafletLayer) {
    state.map.removeLayer(entry.leafletLayer);
  }
  syncUrl();
}

function ensureLayerData(id) {
  const entry = state.layers.get(id);
  if (entry.data) return Promise.resolve(entry.data);
  if (entry.loading) return entry.loading;

  const spinner = document.getElementById(`spinner-${id}`);
  if (spinner) spinner.hidden = false;

  entry.loading = fetch(entry.config.file)
    .then((r) => {
      if (!r.ok) throw new Error(`HTTP ${r.status} for ${entry.config.file}`);
      return r.json();
    })
    .then((data) => {
      entry.data = data;
      return data;
    })
    .finally(() => {
      entry.loading = null;
      if (spinner) spinner.hidden = true;
    });
  return entry.loading;
}

// ---------------------------------------------------------------------------
// Popups & educational content

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (c) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
  }[c]));
}

function featureName(layerConfig, props) {
  const fields = [layerConfig.nameField, ...(layerConfig.fallbackNameFields || [])];
  for (const f of fields) {
    if (f && props[f]) return String(props[f]);
  }
  return 'Unknown district';
}

function featurePopupHtml(layerConfig, props) {
  const name = featureName(layerConfig, props);
  let html = `<div class="popup">`;
  html += `<div class="popup-layer">${escapeHtml(layerConfig.name)}</div>`;
  html += `<h3 class="popup-title">${escapeHtml(name)}</h3>`;

  for (const sub of layerConfig.subtitleFields || []) {
    if (props[sub.field]) {
      html += `<div class="popup-sub"><strong>${escapeHtml(sub.label)}:</strong> ${escapeHtml(props[sub.field])}</div>`;
    }
  }
  if (layerConfig.department) {
    html += `<div class="popup-sub"><strong>Part of:</strong> ${escapeHtml(layerConfig.department)}</div>`;
  }

  html += educationHtml(layerConfig, { compact: false });

  const featureLink = (layerConfig.featureLinks || {})[name];
  const link = featureLink || layerConfig.officialLink;
  if (link) {
    const linkLabel = featureLink ? `Visit the ${escapeHtml(name)} website` : 'Official resource';
    html += `<div class="popup-link"><a href="${escapeHtml(link)}" target="_blank" rel="noopener">${linkLabel} ↗</a></div>`;
  }
  if (layerConfig.profilesFile) {
    html += `<button type="button" class="profile-btn" data-layer="${escapeHtml(layerConfig.id)}" data-district="${escapeHtml(name)}">📖 Full profile: history &amp; why it matters</button>`;
  }
  html += `</div>`;
  return html;
}

function educationHtml(layerConfig, { compact }) {
  const edu = layerConfig.education || {};
  let html = '';
  if (edu.description) html += `<p class="edu-desc">${escapeHtml(edu.description)}</p>`;
  if (!compact && edu.purpose) html += `<p class="edu-item"><strong>Purpose:</strong> ${escapeHtml(edu.purpose)}</p>`;
  if (edu.established) html += `<p class="edu-item"><strong>Established:</strong> ${escapeHtml(edu.established)}</p>`;
  if (edu.whyItMatters) html += `<div class="edu-matters"><strong>Why it matters:</strong> ${escapeHtml(edu.whyItMatters)}</div>`;
  if (compact && layerConfig.officialLink) {
    html += `<div class="popup-link"><a href="${escapeHtml(layerConfig.officialLink)}" target="_blank" rel="noopener">Official resource ↗</a></div>`;
  }
  return html;
}

// ---------------------------------------------------------------------------
// Address search & geolocation

function wireControls() {
  document.getElementById('search-btn').addEventListener('click', searchAddress);
  document.getElementById('address-input').addEventListener('keydown', (e) => {
    if (e.key === 'Enter') searchAddress();
  });
  document.getElementById('locate-btn').addEventListener('click', useMyLocation);
  document.getElementById('share-btn').addEventListener('click', shareLink);
  document.getElementById('sidebar-toggle').addEventListener('click', () => {
    document.getElementById('sidebar').classList.toggle('open');
  });
  document.getElementById('profile-close').addEventListener('click', closeProfile);
  // Profile buttons live inside popups and search results, which are inserted
  // dynamically — handle their clicks by delegation.
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('.profile-btn');
    if (btn) openProfile(btn.dataset.layer, btn.dataset.district, { zoomTo: false });
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeProfile();
  });
}

// ---------------------------------------------------------------------------
// District profiles (content/*.json)

function ensureProfiles(layerId) {
  if (state.profiles.has(layerId)) return state.profiles.get(layerId);
  const entry = state.layers.get(layerId);
  if (!entry || !entry.config.profilesFile) return Promise.resolve(null);
  const promise = fetch(entry.config.profilesFile)
    .then((r) => {
      if (!r.ok) throw new Error(`HTTP ${r.status} for ${entry.config.profilesFile}`);
      return r.json();
    })
    .catch((err) => {
      console.error('Failed to load profiles:', err);
      state.profiles.delete(layerId);
      return null;
    });
  state.profiles.set(layerId, promise);
  return promise;
}

async function openProfile(layerId, district, { zoomTo = false } = {}) {
  const entry = state.layers.get(layerId);
  if (!entry) return;

  const panel = document.getElementById('profile-panel');
  const content = document.getElementById('profile-content');
  panel.hidden = false;
  content.innerHTML = '<p class="profile-loading">Loading profile…</p>';
  state.openProfile = { layerId, district };
  syncUrl();

  const profiles = await ensureProfiles(layerId);
  const profile = profiles && profiles[district];
  if (!profile) {
    content.innerHTML = `
      <h2>${escapeHtml(district)}</h2>
      <p class="profile-loading">A full profile for this district hasn't been written yet.</p>`;
    return;
  }
  content.innerHTML = renderProfileHtml(entry.config, district, profile);
  panel.scrollTop = 0;

  if (zoomTo) zoomToDistrict(layerId, district);
}

function closeProfile() {
  document.getElementById('profile-panel').hidden = true;
  state.openProfile = null;
  syncUrl();
}

function renderProfileHtml(layerConfig, district, profile) {
  const branch = state.config.branches[layerConfig.branch] || {};
  let html = `<div class="profile-kicker" style="color:${branch.color || '#666'}">${branch.icon || ''} ${escapeHtml(layerConfig.name)}</div>`;
  html += `<h2>${escapeHtml(district)}</h2>`;
  if (profile.tagline) html += `<p class="profile-tagline">${escapeHtml(profile.tagline)}</p>`;

  if (profile.quickFacts && profile.quickFacts.length) {
    html += '<dl class="profile-facts">';
    for (const fact of profile.quickFacts) {
      html += `<div><dt>${escapeHtml(fact.label)}</dt><dd>${escapeHtml(fact.value)}</dd></div>`;
    }
    html += '</dl>';
  }

  if (profile.timeline && profile.timeline.length) {
    html += '<h3>History</h3><ol class="profile-timeline">';
    for (const item of profile.timeline) {
      html += `<li><span class="timeline-period">${escapeHtml(item.period)}</span><span class="timeline-text">${escapeHtml(item.text)}</span></li>`;
    }
    html += '</ol>';
  }

  if (profile.today) {
    html += `<h3>Today</h3><p class="profile-today">${escapeHtml(profile.today)}</p>`;
  }

  const featureLink = (layerConfig.featureLinks || {})[district];
  if (featureLink) {
    html += `<p class="popup-link"><a href="${escapeHtml(featureLink)}" target="_blank" rel="noopener">Official ${escapeHtml(district)} website ↗</a></p>`;
  }

  if (profile.sources && profile.sources.length) {
    html += '<h3>Sources &amp; further reading</h3><ul class="profile-sources">';
    for (const src of profile.sources) {
      html += `<li><a href="${escapeHtml(src.url)}" target="_blank" rel="noopener">${escapeHtml(src.title)} ↗</a></li>`;
    }
    html += '</ul>';
  }

  html += `<p class="profile-share"><button type="button" class="profile-copy" onclick="navigator.clipboard && navigator.clipboard.writeText(location.href)">🔗 Copy link to this profile</button></p>`;
  return html;
}

async function zoomToDistrict(layerId, district) {
  const entry = state.layers.get(layerId);
  try {
    await ensureLayerData(layerId);
  } catch {
    return;
  }
  const feature = (entry.data.features || []).find(
    (f) => featureName(entry.config, f.properties || {}) === district
  );
  if (feature) {
    const bounds = featureBounds(feature.geometry);
    if (bounds && bounds.isValid()) state.map.fitBounds(bounds, { padding: [40, 40], maxZoom: 7 });
  }
}

// Bounds that survive the antimeridian: districts like the Ninth Circuit
// include Guam, so naive min/max longitude spans the whole globe. If the
// longitudes span more than 180°, shift the eastern-hemisphere points by
// -360° so the bounds stay contiguous (Leaflet accepts out-of-range lngs).
function featureBounds(geometry) {
  const lons = [];
  const lats = [];
  const collect = (coords) => {
    if (typeof coords[0] === 'number') {
      lons.push(coords[0]);
      lats.push(coords[1]);
    } else {
      coords.forEach(collect);
    }
  };
  if (!geometry || !geometry.coordinates) return null;
  collect(geometry.coordinates);
  if (!lons.length) return null;

  let adjusted = lons;
  if (Math.max(...lons) - Math.min(...lons) > 180) {
    adjusted = lons.map((l) => (l > 0 ? l - 360 : l));
  }
  return L.latLngBounds(
    [Math.min(...lats), Math.min(...adjusted)],
    [Math.max(...lats), Math.max(...adjusted)]
  );
}

function setSearchStatus(message, isError = false) {
  const el = document.getElementById('search-status');
  el.textContent = message || '';
  el.hidden = !message;
  el.classList.toggle('error', isError);
}

function setSearchBusy(busy) {
  const btn = document.getElementById('search-btn');
  btn.disabled = busy;
  btn.textContent = busy ? 'Searching…' : '🔍 Find My Districts';
}

async function searchAddress() {
  const address = document.getElementById('address-input').value.trim();
  if (!address) {
    setSearchStatus('Please enter an address.', true);
    return;
  }

  setSearchBusy(true);
  setSearchStatus('Looking up address…');
  try {
    const url = 'https://nominatim.openstreetmap.org/search?format=json&limit=1&countrycodes=us&q=' + encodeURIComponent(address);
    const resp = await fetch(url);
    if (!resp.ok) throw new Error('Geocoding service unavailable');
    const results = await resp.json();
    if (!results.length) {
      setSearchStatus('Address not found. Try adding a city and state.', true);
      return;
    }
    const { lat, lon, display_name: displayName } = results[0];
    state.lastQuery = address;
    syncUrl();
    await lookupPoint(parseFloat(lat), parseFloat(lon), displayName);
  } catch (err) {
    console.error('Search error:', err);
    setSearchStatus(`Search failed: ${err.message}`, true);
  } finally {
    setSearchBusy(false);
  }
}

function useMyLocation() {
  if (!navigator.geolocation) {
    setSearchStatus('Geolocation is not supported by this browser.', true);
    return;
  }
  setSearchStatus('Getting your location…');
  navigator.geolocation.getCurrentPosition(
    async (pos) => {
      const { latitude, longitude } = pos.coords;
      state.lastQuery = null;
      syncUrl();
      await lookupPoint(latitude, longitude, `Your location (${latitude.toFixed(4)}, ${longitude.toFixed(4)})`);
    },
    (err) => setSearchStatus(`Could not get location: ${err.message}`, true),
    { enableHighAccuracy: false, timeout: 10000 }
  );
}

async function lookupPoint(lat, lon, label) {
  setSearchStatus('Finding your districts…');

  // The point-in-polygon lookup needs every layer's data, so fetch any
  // that haven't been loaded yet (files are cached after the first fetch).
  await Promise.all([...state.layers.keys()].map((id) => ensureLayerData(id).catch(() => null)));

  const matches = [];
  for (const entry of state.layers.values()) {
    if (!entry.data) continue;
    for (const feature of entry.data.features || []) {
      if (feature.geometry && pointInGeometry(lat, lon, feature.geometry)) {
        matches.push({ layer: entry.config, props: feature.properties || {} });
      }
    }
  }

  if (state.searchMarker) state.map.removeLayer(state.searchMarker);
  state.searchMarker = L.marker([lat, lon], {
    icon: L.divIcon({
      className: 'search-pin',
      html: '<div class="pin"></div>',
      iconSize: [24, 34],
      iconAnchor: [12, 34],
      popupAnchor: [0, -30],
    }),
  }).addTo(state.map);
  state.searchMarker.bindPopup(
    `<strong>${escapeHtml(label)}</strong><br>In ${matches.length} federal district${matches.length === 1 ? '' : 's'}`
  ).openPopup();
  state.map.flyTo([lat, lon], 9);

  renderResults(label, matches);
  setSearchStatus('');
}

function renderResults(label, matches) {
  const panel = document.getElementById('results-panel');
  const content = document.getElementById('results-content');
  panel.hidden = false;

  if (!matches.length) {
    content.innerHTML = '<p class="no-results">No federal districts found here. This location may be outside the US or in a data gap.</p>';
    return;
  }

  let html = `<div class="results-location">📍 ${escapeHtml(label)}</div>`;
  html += `<p class="results-count">You are within <strong>${matches.length}</strong> federal districts:</p>`;

  const branchOrder = Object.keys(state.config.branches);
  for (const branchId of branchOrder) {
    const branch = state.config.branches[branchId];
    const inBranch = matches.filter((m) => m.layer.branch === branchId);
    if (!inBranch.length) continue;

    html += `<h4 class="results-branch" style="color:${branch.color}">${branch.icon} ${escapeHtml(branch.label)}</h4>`;
    for (const { layer, props } of inBranch) {
      const name = featureName(layer, props);
      const link = (layer.featureLinks || {})[name] || layer.officialLink;
      html += `<div class="result-card" style="border-left-color:${layer.style.color}">`;
      html += `<div class="result-layer">${escapeHtml(layer.name)}</div>`;
      html += `<div class="result-name">${escapeHtml(name)}</div>`;
      if (layer.education && layer.education.purpose) {
        html += `<div class="result-purpose">${escapeHtml(layer.education.purpose)}</div>`;
      }
      if (link) {
        html += `<a class="result-link" href="${escapeHtml(link)}" target="_blank" rel="noopener">Learn more ↗</a>`;
      }
      if (layer.profilesFile) {
        html += ` <button type="button" class="profile-btn profile-btn-inline" data-layer="${escapeHtml(layer.id)}" data-district="${escapeHtml(name)}">📖 Full profile</button>`;
      }
      html += `</div>`;
    }
  }
  content.innerHTML = html;
  panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// ---------------------------------------------------------------------------
// Geometry: point-in-polygon (ray casting, hole-aware)

function pointInGeometry(lat, lon, geometry) {
  let polygons;
  if (geometry.type === 'Polygon') polygons = [geometry.coordinates];
  else if (geometry.type === 'MultiPolygon') polygons = geometry.coordinates;
  else return false;

  for (const rings of polygons) {
    if (!rings.length) continue;
    if (pointInRing(lat, lon, rings[0])) {
      // Inside the outer ring — make sure it isn't inside a hole.
      let inHole = false;
      for (let i = 1; i < rings.length; i++) {
        if (pointInRing(lat, lon, rings[i])) { inHole = true; break; }
      }
      if (!inHole) return true;
    }
  }
  return false;
}

function pointInRing(lat, lon, ring) {
  // GeoJSON positions are [lon, lat]
  let inside = false;
  for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
    const xi = ring[i][0], yi = ring[i][1];
    const xj = ring[j][0], yj = ring[j][1];
    if (((yi > lat) !== (yj > lat)) && (lon < ((xj - xi) * (lat - yi)) / (yj - yi) + xi)) {
      inside = !inside;
    }
  }
  return inside;
}

// Exposed for testing in the browser console
window.__federalDistricts = { pointInGeometry, lookupPoint, state };

// ---------------------------------------------------------------------------
// URL state & sharing

function syncUrl() {
  const params = new URLSearchParams();
  const enabled = [...state.layers.values()]
    .filter((e) => e.leafletLayer && state.map.hasLayer(e.leafletLayer))
    .map((e) => e.config.id);
  params.set('layers', enabled.join(','));
  if (state.lastQuery) params.set('q', state.lastQuery);
  if (state.openProfile) params.set('profile', `${state.openProfile.layerId}:${state.openProfile.district}`);
  history.replaceState(null, '', `${location.pathname}?${params.toString()}`);
}

async function shareLink() {
  const btn = document.getElementById('share-btn');
  try {
    await navigator.clipboard.writeText(location.href);
    btn.textContent = '✓ Link copied';
  } catch {
    window.prompt('Copy this link:', location.href);
    btn.textContent = '🔗 Share this view';
  }
  setTimeout(() => { btn.textContent = '🔗 Share this view'; }, 2000);
}

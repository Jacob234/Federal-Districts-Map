#!/usr/bin/env python3
"""
Build the agency layers added for JBK-920.
==========================================

    data/US_Attorney_Districts.geojson  93 US Attorney districts
    data/HHS_Regions.geojson            10 HHS regions
    data/NWS_Regions.geojson            6 National Weather Service regions
    data/USACE_Divisions.geojson        8 Army Corps of Engineers civil works divisions

Like scripts/build_district_courts.py, everything is drawn from us-atlas
county shapes so the new layers line up with the existing district layers:

    curl -sL https://registry.npmjs.org/us-atlas/-/us-atlas-3.0.1.tgz | tar xz
    # -> package/counties-10m.json

- US Attorney districts are the 94 judicial districts in
  data/US_District_Courts.geojson, except that one US Attorney serves both
  Guam and the Northern Mariana Islands, so those two are merged.
- HHS regions are the standard ten federal regions, by state.
- NWS regions follow the forecast office that serves each county, listed in
  scripts/nws_region_counties.json (see its _source note).
- Army Corps divisions follow watersheds rather than county lines. Their
  boundaries come from the USACE Civil Works Divisions feature service,
  generalized to about 5 km, in scripts/usace_divisions_generalized.geojson:

      https://services7.arcgis.com/n1YM8pTrFmm7L4hs/arcgis/rest/services/usace_cw_divisions/FeatureServer/0/query
          ?where=DIV_SYM<>'POD'&outFields=DIV_SYM&maxAllowableOffset=0.05
          &geometryPrecision=2&outSR=4326&f=geojson

  Only each division's mainland ring is kept. The script clips them to the
  county coastline, gives overlaps to the first division, and hands gaps and
  islands (Puerto Rico, the Keys, the Channel Islands) to the division they
  touch most, or failing that the nearest. The Pacific Ocean Division is
  Alaska, Hawaii and the Pacific territories.

Usage:
    pip install shapely topojson
    python3 scripts/build_agency_layers.py package/counties-10m.json
"""

import json
import sys
from pathlib import Path

import topojson
from shapely.geometry import mapping, shape
from shapely.ops import unary_union

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_district_courts import TOLERANCE, decode_counties, round_coords  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data'
SCRIPTS = ROOT / 'scripts'

FIPS = {
    'AL': '01', 'AK': '02', 'AZ': '04', 'AR': '05', 'CA': '06', 'CO': '08', 'CT': '09',
    'DE': '10', 'DC': '11', 'FL': '12', 'GA': '13', 'HI': '15', 'ID': '16', 'IL': '17',
    'IN': '18', 'IA': '19', 'KS': '20', 'KY': '21', 'LA': '22', 'ME': '23', 'MD': '24',
    'MA': '25', 'MI': '26', 'MN': '27', 'MS': '28', 'MO': '29', 'MT': '30', 'NE': '31',
    'NV': '32', 'NH': '33', 'NJ': '34', 'NM': '35', 'NY': '36', 'NC': '37', 'ND': '38',
    'OH': '39', 'OK': '40', 'OR': '41', 'PA': '42', 'RI': '44', 'SC': '45', 'SD': '46',
    'TN': '47', 'TX': '48', 'UT': '49', 'VT': '50', 'VA': '51', 'WA': '53', 'WV': '54',
    'WI': '55', 'WY': '56', 'AS': '60', 'GU': '66', 'MP': '69', 'PR': '72', 'VI': '78',
}

# Region number -> (regional office, states). The Pacific freely associated
# states in Region 9 are not in us-atlas.
HHS_REGIONS = {
    1: ('Boston', ['CT', 'ME', 'MA', 'NH', 'RI', 'VT']),
    2: ('New York', ['NJ', 'NY', 'PR', 'VI']),
    3: ('Philadelphia', ['DE', 'DC', 'MD', 'PA', 'VA', 'WV']),
    4: ('Atlanta', ['AL', 'FL', 'GA', 'KY', 'MS', 'NC', 'SC', 'TN']),
    5: ('Chicago', ['IL', 'IN', 'MI', 'MN', 'OH', 'WI']),
    6: ('Dallas', ['AR', 'LA', 'NM', 'OK', 'TX']),
    7: ('Kansas City', ['IA', 'KS', 'MO', 'NE']),
    8: ('Denver', ['CO', 'MT', 'ND', 'SD', 'UT', 'WY']),
    9: ('San Francisco', ['AZ', 'CA', 'HI', 'NV', 'AS', 'GU', 'MP']),
    10: ('Seattle', ['AK', 'ID', 'OR', 'WA']),
}

NWS_HQ = {
    'ER': 'Bohemia, New York', 'SR': 'Fort Worth, Texas', 'CR': 'Kansas City, Missouri',
    'WR': 'Salt Lake City, Utah', 'AR': 'Anchorage, Alaska', 'PR': 'Honolulu, Hawaii',
}

USACE_DIVISIONS = {
    'LRD': ('Great Lakes and Ohio River Division', 'Cincinnati, Ohio'),
    'MVD': ('Mississippi Valley Division', 'Vicksburg, Mississippi'),
    'NAD': ('North Atlantic Division', 'Brooklyn, New York'),
    'NWD': ('Northwestern Division', 'Portland, Oregon'),
    'POD': ('Pacific Ocean Division', 'Fort Shafter, Hawaii'),
    'SAD': ('South Atlantic Division', 'Atlanta, Georgia'),
    'SPD': ('South Pacific Division', 'San Francisco, California'),
    'SWD': ('Southwestern Division', 'Dallas, Texas'),
}


def write_layer(name, features, simplify=True):
    """Write features as a compact GeoJSON file, simplifying shared arcs once."""
    fc = {'type': 'FeatureCollection', 'features': features}
    if simplify:
        topo = topojson.Topology(fc, prequantize=False, toposimplify=TOLERANCE)
        features = json.loads(topo.to_geojson())['features']
    for f in features:
        f.pop('id', None)
        f['geometry'] = round_coords(f['geometry'])
    path = DATA / f'{name}.geojson'
    path.write_text(json.dumps({'type': 'FeatureCollection', 'name': name, 'features': features},
                               separators=(',', ':')))
    print(f'wrote {path.relative_to(ROOT)}: {len(features)} features, {path.stat().st_size / 1024:.0f} KB')


def feature(props, geom):
    return {'type': 'Feature', 'properties': props, 'geometry': mapping(geom)}


def build_us_attorneys():
    courts = json.loads((DATA / 'US_District_Courts.geojson').read_text())['features']
    features, pacific = [], []
    for f in courts:
        if f['properties']['STATE_FIPS'] in ('66', '69'):
            pacific.append(shape(f['geometry']))
            continue
        name = f['properties']['DISTRICT_NAME']
        features.append({'type': 'Feature', 'geometry': f['geometry'], 'properties': {
            'DISTRICT_NAME': name, 'OFFICE': f"U.S. Attorney's Office for the {name}"}})
    name = 'District of Guam and the Northern Mariana Islands'
    features.append(feature({'DISTRICT_NAME': name, 'OFFICE': f"U.S. Attorney's Office for the {name}"},
                            unary_union(pacific)))
    features.sort(key=lambda f: f['properties']['DISTRICT_NAME'])
    assert len(features) == 93, 'expected 93 US Attorney districts'
    # Geometry is already simplified in the district courts file.
    write_layer('US_Attorney_Districts', features, simplify=False)


def build_hhs(by_state):
    features = []
    for number, (office, states) in HHS_REGIONS.items():
        geom = unary_union([g for st in states for g in by_state[FIPS[st]]])
        features.append(feature({'REGION': f'Region {number}', 'OFFICE': office,
                                 'STATES': ', '.join(states)}, geom))
    write_layer('HHS_Regions', features)


def build_nws(counties):
    cfg = json.loads((SCRIPTS / 'nws_region_counties.json').read_text())
    state_region = {FIPS[st]: r for r, sts in cfg['states'].items() for st in sts}
    county_region = {c: r for r, v in cfg['counties'].items() for c in v['fips']}
    assert len(state_region) == len(FIPS), 'every state needs an NWS region'
    known = {fips for fips, _, _ in counties}
    missing = sorted(set(county_region) - known)
    assert not missing, f'override counties not in us-atlas: {missing}'

    groups = {}
    for fips, _, geom in counties:
        region = county_region.get(fips, state_region[fips[:2]])
        if geom is not None:
            groups.setdefault(region, []).append(geom)
    features = [feature({'REGION': cfg['regions'][r], 'HEADQUARTERS': NWS_HQ[r]}, unary_union(gs))
                for r, gs in groups.items()]
    write_layer('NWS_Regions', features)


def build_usace(by_state):
    pod_states = [FIPS[st] for st in ('AK', 'HI', 'AS', 'GU', 'MP')]
    pod = unary_union([g for st in pod_states for g in by_state[st]])
    land = unary_union([g for st, gs in by_state.items() if st not in pod_states for g in gs])

    src = json.loads((SCRIPTS / 'usace_divisions_generalized.geojson').read_text())['features']
    divisions, taken = {}, None
    for f in src:
        geom = shape(f['geometry']).buffer(0).intersection(land)
        if taken is not None:
            geom = geom.difference(taken)
        divisions[f['properties']['DIV_SYM']] = geom
        taken = geom if taken is None else taken.union(geom)

    gaps = land.difference(taken)
    pieces = list(getattr(gaps, 'geoms', [gaps]))
    for piece in pieces:
        if piece.is_empty or piece.geom_type != 'Polygon':
            continue
        touch = {d: piece.boundary.intersection(g.buffer(1e-6)).length for d, g in divisions.items()}
        best = max(touch, key=touch.get)
        if touch[best] == 0:
            best = min(divisions, key=lambda d: divisions[d].distance(piece))
        divisions[best] = divisions[best].union(piece)
    print(f'usace: {len(pieces)} gap pieces assigned')

    divisions['POD'] = pod
    features = []
    for sym, geom in sorted(divisions.items()):
        name, hq = USACE_DIVISIONS[sym]
        # Drop zero-area slivers left by the clipping.
        polys = [p for p in getattr(geom, 'geoms', [geom]) if p.geom_type == 'Polygon' and p.area > 1e-6]
        features.append(feature({'DIVISION': name, 'CODE': sym, 'HEADQUARTERS': hq}, unary_union(polys)))
    write_layer('USACE_Divisions', features)


def main(topo_path):
    counties = decode_counties(topo_path)
    by_state = {}
    for fips, _, geom in counties:
        if geom is not None:
            by_state.setdefault(fips[:2], []).append(geom)

    build_us_attorneys()
    build_hhs(by_state)
    build_nws(counties)
    build_usace(by_state)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])

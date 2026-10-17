#!/usr/bin/env python3
"""
Build data/US_District_Courts.geojson — the 94 federal judicial districts.
=========================================================================

No agency publishes a small, current, public-domain file of district court
boundaries, so this script assembles one from two public sources:

1. County shapes from the US Census Bureau's cartographic boundary files, as
   packaged by the `us-atlas` npm module (TopoJSON, already web-simplified):

       curl -sL https://registry.npmjs.org/us-atlas/-/us-atlas-3.0.1.tgz | tar xz
       # -> package/counties-10m.json

2. The county lists in 28 U.S.C. §§ 81–131, transcribed into
   scripts/district_court_counties.json. Only states with more than one
   district are listed there; every other state, DC, Puerto Rico, Guam, the
   Virgin Islands and the Northern Mariana Islands is a single district.

Every county in a split state must land in exactly one district, and every
county named in the statute must match a Census county, or the build fails.

Usage:
    pip install shapely topojson
    python3 scripts/build_district_courts.py package/counties-10m.json
"""

import json
import re
import sys
from pathlib import Path

import topojson
from shapely.geometry import MultiPolygon, Polygon, mapping
from shapely.ops import unary_union

ROOT = Path(__file__).resolve().parent.parent
COUNTY_LISTS = ROOT / 'scripts' / 'district_court_counties.json'
OUTPUT = ROOT / 'data' / 'US_District_Courts.geojson'

# Topology-preserving simplification tolerance in degrees (~0.01 = ~1 km).
# Applied to shared arcs, so neighbouring districts never gap or overlap.
TOLERANCE = 0.01

# FIPS code -> (name used in "District of X", Bluebook abbreviation, circuit)
STATES = {
    '01': ('Alabama', 'Ala.', 'Eleventh'), '02': ('Alaska', 'Alaska', 'Ninth'),
    '04': ('Arizona', 'Ariz.', 'Ninth'), '05': ('Arkansas', 'Ark.', 'Eighth'),
    '06': ('California', 'Cal.', 'Ninth'), '08': ('Colorado', 'Colo.', 'Tenth'),
    '09': ('Connecticut', 'Conn.', 'Second'), '10': ('Delaware', 'Del.', 'Third'),
    '11': ('Columbia', 'D.C.', 'DC'), '12': ('Florida', 'Fla.', 'Eleventh'),
    '13': ('Georgia', 'Ga.', 'Eleventh'), '15': ('Hawaii', 'Haw.', 'Ninth'),
    '16': ('Idaho', 'Idaho', 'Ninth'), '17': ('Illinois', 'Ill.', 'Seventh'),
    '18': ('Indiana', 'Ind.', 'Seventh'), '19': ('Iowa', 'Iowa', 'Eighth'),
    '20': ('Kansas', 'Kan.', 'Tenth'), '21': ('Kentucky', 'Ky.', 'Sixth'),
    '22': ('Louisiana', 'La.', 'Fifth'), '23': ('Maine', 'Me.', 'First'),
    '24': ('Maryland', 'Md.', 'Fourth'), '25': ('Massachusetts', 'Mass.', 'First'),
    '26': ('Michigan', 'Mich.', 'Sixth'), '27': ('Minnesota', 'Minn.', 'Eighth'),
    '28': ('Mississippi', 'Miss.', 'Fifth'), '29': ('Missouri', 'Mo.', 'Eighth'),
    '30': ('Montana', 'Mont.', 'Ninth'), '31': ('Nebraska', 'Neb.', 'Eighth'),
    '32': ('Nevada', 'Nev.', 'Ninth'), '33': ('New Hampshire', 'N.H.', 'First'),
    '34': ('New Jersey', 'N.J.', 'Third'), '35': ('New Mexico', 'N.M.', 'Tenth'),
    '36': ('New York', 'N.Y.', 'Second'), '37': ('North Carolina', 'N.C.', 'Fourth'),
    '38': ('North Dakota', 'N.D.', 'Eighth'), '39': ('Ohio', 'Ohio', 'Sixth'),
    '40': ('Oklahoma', 'Okla.', 'Tenth'), '41': ('Oregon', 'Or.', 'Ninth'),
    '42': ('Pennsylvania', 'Pa.', 'Third'), '44': ('Rhode Island', 'R.I.', 'First'),
    '45': ('South Carolina', 'S.C.', 'Fourth'), '46': ('South Dakota', 'S.D.', 'Eighth'),
    '47': ('Tennessee', 'Tenn.', 'Sixth'), '48': ('Texas', 'Tex.', 'Fifth'),
    '49': ('Utah', 'Utah', 'Tenth'), '50': ('Vermont', 'Vt.', 'Second'),
    '51': ('Virginia', 'Va.', 'Fourth'), '53': ('Washington', 'Wash.', 'Ninth'),
    '54': ('West Virginia', 'W. Va.', 'Fourth'), '55': ('Wisconsin', 'Wis.', 'Seventh'),
    '56': ('Wyoming', 'Wyo.', 'Tenth'),
    '66': ('Guam', 'Guam', 'Ninth'),
    '69': ('the Northern Mariana Islands', 'N. Mar. I.', 'Ninth'),
    '72': ('Puerto Rico', 'P.R.', 'First'),
    '78': ('the Virgin Islands', 'V.I.', 'Third'),
}
# American Samoa (60) has no federal district court and is left off the map.

POSTAL = {
    'AL': '01', 'AR': '05', 'CA': '06', 'FL': '12', 'GA': '13', 'IL': '17',
    'IN': '18', 'IA': '19', 'KY': '21', 'LA': '22', 'MI': '26', 'MS': '28',
    'MO': '29', 'NY': '36', 'NC': '37', 'OH': '39', 'OK': '40', 'PA': '42',
    'TN': '47', 'TX': '48', 'VA': '51', 'WA': '53', 'WV': '54', 'WI': '55',
}

TERRITORIAL = {'66', '69', '78'}  # Article IV courts with district-court jurisdiction


def norm(name):
    """Normalise a county name so statute and Census spellings compare equal."""
    n = name.lower().replace('saint ', 'st. ').replace('sainte ', 'ste. ')
    return re.sub(r'[^a-z.]', '', n)


def is_independent_city(fips):
    # Virginia's independent cities, Baltimore and St. Louis are coded 510-840.
    return int(fips[2:]) >= 510


def county_key(fips, name):
    return norm(name) + (' city' if is_independent_city(fips) else '')


def statute_key(name):
    if name.endswith(' (city)'):
        return norm(name[: -len(' (city)')]) + ' city'
    return norm(name)


def abbreviation(direction, state_abbr):
    prefix = f'{direction[0]}.D.' if direction else 'D.'
    # Bluebook closes up adjacent single capitals: S.D.N.Y., N.D.W. Va., but D. Mass.
    sep = '' if re.match(r'^[A-Z]\.', state_abbr) else ' '
    return f'{prefix}{sep}{state_abbr}'


def decode_counties(topo_path):
    topo = json.loads(Path(topo_path).read_text())
    # Decode the TopoJSON by hand: quantized, delta-encoded arcs.
    (sx, sy), (tx, ty) = topo['transform']['scale'], topo['transform']['translate']
    arcs = []
    for arc in topo['arcs']:
        x = y = 0
        pts = []
        for dx, dy in arc:
            x += dx
            y += dy
            pts.append((round(x * sx + tx, 6), round(y * sy + ty, 6)))
        arcs.append(pts)

    def ring(indexes):
        pts = []
        for i in indexes:
            seg = arcs[i] if i >= 0 else arcs[~i][::-1]
            pts.extend(seg if not pts else seg[1:])
        return pts

    def polygon(rings):
        # Quantization collapses some tiny islands to fewer than 4 points; drop them.
        rings = [r for r in (ring(idx) for idx in rings) if len(r) >= 4]
        return Polygon(rings[0], rings[1:]) if rings else None

    counties = []
    for g in topo['objects']['counties']['geometries']:
        parts = {'Polygon': [g.get('arcs')], 'MultiPolygon': g.get('arcs')}.get(g['type'], [])
        polys = [p for p in (polygon(rings) for rings in parts) if p is not None]
        # A few tiny independent cities (e.g. Falls Church) vanish at this scale; keep them
        # with no geometry so the county-list check still sees them.
        counties.append((g['id'], g['properties']['name'], MultiPolygon(polys).buffer(0) if polys else None))
    return counties


def main(topo_path):
    lists = {k: v for k, v in json.loads(COUNTY_LISTS.read_text()).items() if not k.startswith('_')}
    counties = decode_counties(topo_path)

    # (state fips, direction or '') -> list of county geometries
    groups = {}
    errors = []
    by_state = {}
    for fips, name, geom in counties:
        by_state.setdefault(fips[:2], []).append((fips, name, geom))

    split_states = {POSTAL[p]: p for p in lists}
    for st, members in by_state.items():
        if st not in STATES:
            continue
        if st not in split_states:
            groups[(st, '')] = [g for _, _, g in members]
            continue
        districts = lists[split_states[st]]
        lookup = {}
        for direction, names in districts.items():
            for n in names:
                k = statute_key(n)
                if k in lookup:
                    errors.append(f'{split_states[st]}: {n} listed in both {lookup[k]} and {direction}')
                lookup[k] = direction
        seen = set()
        for fips, name, geom in members:
            k = county_key(fips, name)
            if k not in lookup:
                errors.append(f'{split_states[st]}: Census county {name} ({fips}) is in no district')
                continue
            seen.add(k)
            groups.setdefault((st, lookup[k]), []).append(geom)
        for k, direction in lookup.items():
            if k not in seen:
                errors.append(f'{split_states[st]}: statute county "{k}" ({direction}) matched no Census county')

    if errors:
        print('\n'.join(errors))
        sys.exit(f'{len(errors)} errors; no file written')

    features = []
    for (st, direction), geoms in sorted(groups.items()):
        state_name, state_abbr, circuit = STATES[st]
        name = f'{direction} District of {state_name}' if direction else f'District of {state_name}'
        props = {
            'DISTRICT_NAME': name,
            'ABBREVIATION': abbreviation(direction, state_abbr),
            'CIRCUIT': 'DC Circuit' if circuit == 'DC' else f'{circuit} Circuit',
            'COURT_TYPE': 'Territorial court' if st in TERRITORIAL else 'Article III court',
            'STATE_FIPS': st,
        }
        features.append({'type': 'Feature', 'properties': props, 'geometry': mapping(unary_union([g for g in geoms if g is not None]))})

    print(f'{len(features)} districts')
    assert len(features) == 94, 'expected 94 judicial districts'

    fc = {'type': 'FeatureCollection', 'features': features}
    topo = topojson.Topology(fc, prequantize=False, toposimplify=TOLERANCE)
    out = json.loads(topo.to_geojson())
    for f in out['features']:
        f.pop('id', None)
        f['geometry'] = round_coords(f['geometry'])
    OUTPUT.write_text(json.dumps({'type': 'FeatureCollection', 'name': 'US_District_Courts',
                                  'features': out['features']}, separators=(',', ':')))
    print(f'wrote {OUTPUT.relative_to(ROOT)} ({OUTPUT.stat().st_size / 1024:.0f} KB)')


def round_coords(geom, places=4):
    def r(c):
        return [round(c[0], places), round(c[1], places)] if isinstance(c[0], (int, float)) else [r(x) for x in c]
    return {'type': geom['type'], 'coordinates': r(geom['coordinates'])}


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])

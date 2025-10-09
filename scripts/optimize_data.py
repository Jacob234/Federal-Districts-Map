#!/usr/bin/env python3
"""
Data Optimization Script for Mini-Web Version
==============================================

Simplifies GeoJSON geometries to reduce file sizes while preserving shape.
Optimizes selected datasets for web hosting.
"""

import geopandas as gpd
import json
from pathlib import Path
import sys

# Define source files and their target simplification tolerances
# tolerance in degrees (~0.01 = ~1km, higher = more simplification)
DATASETS = {
    'courts_of_appeals': {
        'source': 'district-shapefiles/gov-structure/Judicial_Branch/Court_of_Appeals/US_Courts_of_Appeals_Circuits.geojson',
        'output': 'Courts_of_Appeals_Circuits.geojson',
        'tolerance': 0.015,  # Aggressive simplification (6.7M → ~2M)
        'category': 'Judicial'
    },
    'bankruptcy_courts': {
        'source': 'district-shapefiles/gov-structure/Judicial_Branch/Bankruptcy_Courts/US_Bankruptcy_Courts.geojson',
        'output': 'Bankruptcy_Courts.geojson',
        'tolerance': 0.015,  # Aggressive simplification (6.7M → ~2M)
        'category': 'Judicial'
    },
    'epa_regions': {
        'source': 'district-shapefiles/gov-structure/Executive_Branch/Independent_Agencies/Environmental_Protection_Agency/EPA_Regions.geojson',
        'output': 'EPA_Regions.geojson',
        'tolerance': 0.005,  # Light simplification (already small at 325K)
        'category': 'Executive'
    },
    'fema_regions': {
        'source': 'district-shapefiles/gov-structure/Executive_Branch/Cabinet_Departments/Department_of_Homeland_Security/FEMA/FEMA_Regions.geojson',
        'output': 'FEMA_Regions.geojson',
        'tolerance': 0.01,  # Light simplification (727K → ~300K)
        'category': 'Executive'
    },
    'federal_reserve': {
        'source': 'district-shapefiles/gov-structure/Executive_Branch/Cabinet_Departments/Department_of_the_Treasury/Federal_Reserve_System/Federal_Reserve_Districts.geojson',
        'output': 'Federal_Reserve_Districts.geojson',
        'tolerance': 0.015,  # Aggressive simplification (6.8M → ~2M)
        'category': 'Executive'
    },
    'census_regions': {
        'source': 'district-shapefiles/gov-structure/Executive_Branch/Cabinet_Departments/Department_of_Commerce/Census_Bureau/Census_Regions.geojson',
        'output': 'Census_Regions.geojson',
        'tolerance': 0.02,  # Very aggressive (21M → ~500K)
        'category': 'Executive'
    },
    'census_divisions': {
        'source': 'district-shapefiles/gov-structure/Executive_Branch/Cabinet_Departments/Department_of_Commerce/Census_Bureau/Census_Divisions.geojson',
        'output': 'Census_Divisions.geojson',
        'tolerance': 0.02,  # Very aggressive (39M → ~1M)
        'category': 'Executive'
    },
    'blm_districts': {
        'source': 'district-shapefiles/gov-structure/Executive_Branch/Cabinet_Departments/Department_of_the_Interior/Bureau_of_Land_Management/BLM_Districts.geojson',
        'output': 'BLM_Districts.geojson',
        'tolerance': 0.005,  # Light (already small at 111K)
        'category': 'Executive'
    },
    'education_regions': {
        'source': 'district-shapefiles/gov-structure/Executive_Branch/Cabinet_Departments/Department_of_Education/Education_Regions.geojson',
        'output': 'Education_Regions.geojson',
        'tolerance': 0.005,  # Light (already small at 325K)
        'category': 'Executive'
    },
    'coast_guard': {
        'source': 'district-shapefiles/gov-structure/Executive_Branch/Cabinet_Departments/Department_of_Homeland_Security/US_Coast_Guard/Coast_Guard_Districts.geojson',
        'output': 'Coast_Guard_Districts.geojson',
        'tolerance': 0.02,  # Aggressive (16M → ~3M)
        'category': 'Military'
    },
}


def get_file_size_mb(filepath):
    """Get file size in megabytes"""
    return filepath.stat().st_size / (1024 * 1024)


def optimize_geojson(source_path, output_path, tolerance, dataset_name):
    """
    Load, simplify, and save a GeoJSON file

    Parameters:
    -----------
    source_path : Path
        Source GeoJSON file
    output_path : Path
        Output path for simplified file
    tolerance : float
        Simplification tolerance in degrees
    dataset_name : str
        Name for logging
    """
    print(f"\n{'='*60}")
    print(f"Processing: {dataset_name}")
    print(f"{'='*60}")

    # Check if source exists
    if not source_path.exists():
        print(f"❌ ERROR: Source file not found: {source_path}")
        return False

    original_size = get_file_size_mb(source_path)
    print(f"Original size: {original_size:.2f} MB")

    try:
        # Load GeoJSON
        print(f"Loading GeoDataFrame...")
        gdf = gpd.read_file(source_path)
        print(f"  Features: {len(gdf)}")
        print(f"  CRS: {gdf.crs}")

        # Ensure WGS84 (EPSG:4326) for web mapping
        if gdf.crs and gdf.crs.to_epsg() != 4326:
            print(f"  Reprojecting to EPSG:4326...")
            gdf = gdf.to_crs(epsg=4326)

        # Simplify geometries
        print(f"Simplifying geometries (tolerance={tolerance})...")
        gdf['geometry'] = gdf['geometry'].simplify(
            tolerance=tolerance,
            preserve_topology=True
        )

        # Clean up data - remove NaN values that cause JSON issues
        print(f"Cleaning data...")
        for col in gdf.columns:
            if col != 'geometry':
                gdf[col] = gdf[col].fillna('')

        # Save optimized version
        print(f"Saving to {output_path}...")
        gdf.to_file(output_path, driver='GeoJSON')

        # Report results
        optimized_size = get_file_size_mb(output_path)
        reduction = ((original_size - optimized_size) / original_size) * 100

        print(f"\n✅ SUCCESS!")
        print(f"  Original:  {original_size:.2f} MB")
        print(f"  Optimized: {optimized_size:.2f} MB")
        print(f"  Reduction: {reduction:.1f}%")

        return True

    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Process all datasets"""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    output_dir = script_dir.parent / 'data'

    print("=" * 60)
    print("Mini-Web Data Optimization")
    print("=" * 60)
    print(f"Project root: {project_root}")
    print(f"Output directory: {output_dir}")

    # Ensure output directory exists
    output_dir.mkdir(exist_ok=True, parents=True)

    # Process each dataset
    results = {}
    total_original = 0
    total_optimized = 0

    for dataset_id, config in DATASETS.items():
        source_path = project_root / config['source']
        output_path = output_dir / config['output']

        success = optimize_geojson(
            source_path,
            output_path,
            config['tolerance'],
            dataset_id
        )

        results[dataset_id] = success

        if success and output_path.exists():
            total_optimized += get_file_size_mb(output_path)

    # Summary
    print("\n" + "=" * 60)
    print("OPTIMIZATION SUMMARY")
    print("=" * 60)

    successful = sum(1 for v in results.values() if v)
    failed = sum(1 for v in results.values() if not v)

    print(f"Successful: {successful}/{len(DATASETS)}")
    print(f"Failed: {failed}/{len(DATASETS)}")
    print(f"Total optimized data size: {total_optimized:.2f} MB")

    if failed > 0:
        print("\nFailed datasets:")
        for dataset_id, success in results.items():
            if not success:
                print(f"  - {dataset_id}")

    print("\n✅ Optimization complete!")
    print(f"Optimized files saved to: {output_dir}")


if __name__ == '__main__':
    main()

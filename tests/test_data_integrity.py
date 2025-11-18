#!/usr/bin/env python3
"""
Data Integrity Tests
====================

Tests for GeoJSON data files.
"""

import unittest
import json
from pathlib import Path


class TestGeoJSONData(unittest.TestCase):
    """Test GeoJSON data files"""

    def setUp(self):
        """Set up test fixtures"""
        self.data_dir = Path(__file__).parent.parent / 'data'
        self.expected_files = [
            'Courts_of_Appeals_Circuits.geojson',
            'Bankruptcy_Courts.geojson',
            'FEMA_Regions.geojson',
            'EPA_Regions.geojson',
            'Federal_Reserve_Districts.geojson',
            'Census_Regions.geojson',
            'Census_Divisions.geojson',
            'Education_Regions.geojson',
            'BLM_Districts.geojson',
            'Coast_Guard_Districts.geojson',
        ]

    def test_data_directory_exists(self):
        """Test data directory exists"""
        self.assertTrue(self.data_dir.exists())
        self.assertTrue(self.data_dir.is_dir())

    def test_all_required_files_exist(self):
        """Test all required GeoJSON files exist"""
        for filename in self.expected_files:
            filepath = self.data_dir / filename
            self.assertTrue(
                filepath.exists(),
                f"Missing required file: {filename}"
            )

    def test_geojson_valid_structure(self):
        """Test each GeoJSON file has valid structure"""
        for filename in self.expected_files:
            filepath = self.data_dir / filename

            if not filepath.exists():
                continue

            with open(filepath, 'r') as f:
                data = json.load(f)

            # Test basic GeoJSON structure
            self.assertEqual(
                data.get('type'),
                'FeatureCollection',
                f"{filename}: Not a FeatureCollection"
            )

            features = data.get('features', [])
            self.assertGreater(
                len(features),
                0,
                f"{filename}: No features found"
            )

    def test_features_have_geometry(self):
        """Test features have valid geometry"""
        for filename in self.expected_files:
            filepath = self.data_dir / filename

            if not filepath.exists():
                continue

            with open(filepath, 'r') as f:
                data = json.load(f)

            features = data.get('features', [])

            for i, feature in enumerate(features[:5]):  # Test first 5
                self.assertIn(
                    'geometry',
                    feature,
                    f"{filename}: Feature {i} missing geometry"
                )

                geometry = feature['geometry']
                self.assertIn(
                    'type',
                    geometry,
                    f"{filename}: Feature {i} geometry missing type"
                )

                self.assertIn(
                    'coordinates',
                    geometry,
                    f"{filename}: Feature {i} geometry missing coordinates"
                )

    def test_features_have_properties(self):
        """Test features have properties"""
        for filename in self.expected_files:
            filepath = self.data_dir / filename

            if not filepath.exists():
                continue

            with open(filepath, 'r') as f:
                data = json.load(f)

            features = data.get('features', [])

            for i, feature in enumerate(features[:5]):  # Test first 5
                self.assertIn(
                    'properties',
                    feature,
                    f"{filename}: Feature {i} missing properties"
                )

    def test_total_feature_count(self):
        """Test total features across all files"""
        total_features = 0

        for filename in self.expected_files:
            filepath = self.data_dir / filename

            if not filepath.exists():
                continue

            with open(filepath, 'r') as f:
                data = json.load(f)

            features = data.get('features', [])
            total_features += len(features)

        # Should have 308 total features as documented
        self.assertEqual(
            total_features,
            308,
            f"Expected 308 total features, found {total_features}"
        )


class TestDataOptimization(unittest.TestCase):
    """Test data is properly optimized"""

    def setUp(self):
        """Set up test fixtures"""
        self.data_dir = Path(__file__).parent.parent / 'data'

    def test_file_sizes_reasonable(self):
        """Test optimized files are not too large"""
        max_size_mb = 2.0  # 2MB per file max

        for geojson_file in self.data_dir.glob('*.geojson'):
            size_mb = geojson_file.stat().st_size / (1024 * 1024)

            self.assertLess(
                size_mb,
                max_size_mb,
                f"{geojson_file.name} is too large: {size_mb:.2f}MB"
            )

    def test_total_data_size(self):
        """Test total data directory size"""
        total_size = sum(
            f.stat().st_size
            for f in self.data_dir.glob('*.geojson')
        )

        total_size_mb = total_size / (1024 * 1024)

        # Total should be under 5MB
        self.assertLess(
            total_size_mb,
            5.0,
            f"Total data size too large: {total_size_mb:.2f}MB"
        )


if __name__ == '__main__':
    unittest.main()

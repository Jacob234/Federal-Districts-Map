#!/usr/bin/env python3
"""
Unit Tests for Map Generation
==============================

Tests for generate_map.py functionality.
"""

import unittest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from generate_map import EducationalMapGenerator
from map_config import LAYERS, MAP_CONFIG


class TestMapGenerator(unittest.TestCase):
    """Test EducationalMapGenerator class"""

    def setUp(self):
        """Set up test fixtures"""
        self.generator = EducationalMapGenerator('test_output.html')

    def test_initialization(self):
        """Test generator initialization"""
        self.assertEqual(self.generator.output_file, 'test_output.html')
        self.assertIsNone(self.generator.map)
        self.assertIsNotNone(self.generator.script_dir)

    def test_create_base_map(self):
        """Test base map creation"""
        self.generator.create_base_map()

        self.assertIsNotNone(self.generator.map)
        # Check map center is correct
        self.assertEqual(
            self.generator.map.location,
            MAP_CONFIG['center']
        )

    def test_create_educational_popup(self):
        """Test popup HTML generation"""
        layer_config = {
            'name': 'Test Layer',
            'education': {
                'title': 'Test Title',
                'purpose': 'Test purpose',
                'structure': '10 regions',
                'established': '2020',
                'why_it_matters': 'Test importance'
            }
        }

        properties = {
            'NAME': 'Test District',
            'ID': '123'
        }

        html = self.generator.create_educational_popup(properties, layer_config)

        self.assertIn('Test Title', html)
        self.assertIn('Test purpose', html)
        self.assertIn('Test District', html)
        self.assertIn('123', html)

    def test_popup_handles_missing_education(self):
        """Test popup generation with minimal data"""
        layer_config = {'name': 'Minimal Layer'}
        properties = {'NAME': 'District'}

        html = self.generator.create_educational_popup(properties, layer_config)

        self.assertIn('District', html)
        self.assertIsInstance(html, str)


class TestMapConfiguration(unittest.TestCase):
    """Test map configuration"""

    def test_map_config_structure(self):
        """Test MAP_CONFIG has required keys"""
        required_keys = ['center', 'zoom_start', 'tiles']

        for key in required_keys:
            self.assertIn(key, MAP_CONFIG)

    def test_map_config_values(self):
        """Test MAP_CONFIG has valid values"""
        self.assertIsInstance(MAP_CONFIG['center'], list)
        self.assertEqual(len(MAP_CONFIG['center']), 2)
        self.assertIsInstance(MAP_CONFIG['zoom_start'], int)
        self.assertIsInstance(MAP_CONFIG['tiles'], str)

    def test_layers_configuration(self):
        """Test LAYERS dictionary structure"""
        self.assertIsInstance(LAYERS, dict)
        self.assertGreater(len(LAYERS), 0)

        # Check each layer has required keys
        for layer_id, config in LAYERS.items():
            self.assertIn('name', config)
            self.assertIn('file', config)
            self.assertIn('branch', config)
            self.assertIn('style', config)
            self.assertIn('education', config)

    def test_all_layers_have_education_content(self):
        """Test all layers have educational content"""
        for layer_id, config in LAYERS.items():
            education = config.get('education', {})

            # Check for key educational fields
            self.assertIn('title', education, f"Layer {layer_id} missing education.title")
            self.assertIn('purpose', education, f"Layer {layer_id} missing education.purpose")
            self.assertIn('structure', education, f"Layer {layer_id} missing education.structure")

    def test_layer_branches(self):
        """Test layers are properly categorized by branch"""
        valid_branches = ['Judicial', 'Executive', 'Military']

        for layer_id, config in LAYERS.items():
            branch = config.get('branch')
            self.assertIn(
                branch,
                valid_branches,
                f"Layer {layer_id} has invalid branch: {branch}"
            )


class TestEducationalContent(unittest.TestCase):
    """Test educational content quality"""

    def test_education_descriptions_not_empty(self):
        """Test educational descriptions are not empty"""
        for layer_id, config in LAYERS.items():
            education = config.get('education', {})

            description = education.get('description', '')
            self.assertGreater(
                len(description),
                10,
                f"Layer {layer_id} has too short description"
            )

    def test_why_it_matters_exists(self):
        """Test all layers explain why they matter"""
        for layer_id, config in LAYERS.items():
            education = config.get('education', {})

            why_it_matters = education.get('why_it_matters', '')
            self.assertGreater(
                len(why_it_matters),
                10,
                f"Layer {layer_id} missing 'why_it_matters'"
            )


if __name__ == '__main__':
    unittest.main()

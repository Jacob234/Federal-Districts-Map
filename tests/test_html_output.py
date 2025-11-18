#!/usr/bin/env python3
"""
HTML Output Tests
=================

Tests for generated HTML files.
"""

import unittest
from pathlib import Path


class TestHTMLFiles(unittest.TestCase):
    """Test HTML file structure and content"""

    def setUp(self):
        """Set up test fixtures"""
        self.project_root = Path(__file__).parent.parent
        self.index_html = self.project_root / 'index.html'
        self.landing_html = self.project_root / 'landing.html'

    def test_html_files_exist(self):
        """Test required HTML files exist"""
        self.assertTrue(
            self.index_html.exists(),
            "index.html not found"
        )
        self.assertTrue(
            self.landing_html.exists(),
            "landing.html not found"
        )

    def test_index_html_structure(self):
        """Test index.html has required structure"""
        with open(self.index_html, 'r', encoding='utf-8') as f:
            content = f.read()

        # Basic HTML structure
        self.assertTrue(content.strip().startswith('<!DOCTYPE html>'))
        self.assertIn('<html', content)
        self.assertIn('</html>', content)
        self.assertIn('<head>', content or '<head ', content)
        self.assertIn('<body>', content or '<body ', content)

    def test_index_html_has_leaflet(self):
        """Test index.html includes Leaflet library"""
        with open(self.index_html, 'r', encoding='utf-8') as f:
            content = f.read().lower()

        self.assertIn('leaflet', content)

    def test_index_html_has_search_function(self):
        """Test index.html includes address search"""
        with open(self.index_html, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('searchAddress', content)
        self.assertIn('address-input', content)

    def test_landing_html_structure(self):
        """Test landing.html has required structure"""
        with open(self.landing_html, 'r', encoding='utf-8') as f:
            content = f.read()

        # Basic HTML structure
        self.assertTrue(content.strip().startswith('<!DOCTYPE html>'))
        self.assertIn('<html', content)
        self.assertIn('</html>', content)

    def test_landing_html_has_link_to_map(self):
        """Test landing.html links to interactive map"""
        with open(self.landing_html, 'r', encoding='utf-8') as f:
            content = f.read()

        self.assertIn('index.html', content)

    def test_index_html_size(self):
        """Test index.html size is reasonable"""
        size_mb = self.index_html.stat().st_size / (1024 * 1024)

        # Should be between 3MB and 15MB
        self.assertGreater(size_mb, 3.0, "index.html too small, data may be missing")
        self.assertLess(size_mb, 15.0, "index.html too large")

    def test_landing_html_size(self):
        """Test landing.html size is reasonable"""
        size_kb = self.landing_html.stat().st_size / 1024

        # Should be less than 50KB
        self.assertLess(size_kb, 50.0, "landing.html too large")


if __name__ == '__main__':
    unittest.main()

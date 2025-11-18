#!/usr/bin/env python3
"""
Validation Script for Federal Districts Map
============================================

Validates that all required files exist and are properly formatted.
Run this before deploying or committing changes.

Usage:
    python validate.py
"""

import json
import sys
from pathlib import Path
from typing import List, Tuple

# ANSI color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


class Validator:
    """Validates project files and structure"""

    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.errors = []
        self.warnings = []
        self.checks_passed = 0
        self.checks_total = 0

    def check(self, condition: bool, success_msg: str, error_msg: str, is_warning: bool = False):
        """
        Perform a validation check

        Parameters:
        -----------
        condition : bool
            True if check passed
        success_msg : str
            Message to display on success
        error_msg : str
            Message to display on failure
        is_warning : bool
            If True, failure is a warning not an error
        """
        self.checks_total += 1
        if condition:
            self.checks_passed += 1
            print(f"{GREEN}✓{RESET} {success_msg}")
        else:
            if is_warning:
                self.warnings.append(error_msg)
                print(f"{YELLOW}⚠{RESET}  {error_msg}")
            else:
                self.errors.append(error_msg)
                print(f"{RED}✗{RESET} {error_msg}")

    def validate_file_exists(self, filepath: Path, description: str) -> bool:
        """Check if a file exists"""
        exists = filepath.exists()
        self.check(
            exists,
            f"{description} exists: {filepath.name}",
            f"{description} not found: {filepath}"
        )
        return exists

    def validate_geojson(self, filepath: Path) -> Tuple[bool, int]:
        """
        Validate a GeoJSON file

        Returns:
        --------
        tuple : (is_valid, feature_count)
        """
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)

            # Check basic GeoJSON structure
            if not isinstance(data, dict):
                self.check(False, "", f"Invalid GeoJSON structure in {filepath.name}")
                return False, 0

            if data.get('type') != 'FeatureCollection':
                self.check(False, "", f"Not a FeatureCollection: {filepath.name}")
                return False, 0

            features = data.get('features', [])
            feature_count = len(features)

            if feature_count == 0:
                self.check(False, "", f"No features in {filepath.name}")
                return False, 0

            # Check that features have geometry
            has_geometry = all(
                isinstance(f, dict) and 'geometry' in f
                for f in features[:5]  # Check first 5
            )

            self.check(
                has_geometry,
                f"Valid GeoJSON: {filepath.name} ({feature_count} features)",
                f"Features missing geometry in {filepath.name}"
            )

            return has_geometry, feature_count

        except json.JSONDecodeError as e:
            self.check(False, "", f"Invalid JSON in {filepath.name}: {e}")
            return False, 0
        except Exception as e:
            self.check(False, "", f"Error reading {filepath.name}: {e}")
            return False, 0

    def validate_html(self, filepath: Path) -> bool:
        """Basic HTML validation"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Basic checks
            has_doctype = content.strip().startswith('<!DOCTYPE html>')
            has_html_tags = '<html' in content and '</html>' in content
            has_head = '<head>' in content or '<head ' in content
            has_body = '<body>' in content or '<body ' in content

            is_valid = has_doctype and has_html_tags and has_head and has_body

            self.check(
                is_valid,
                f"Valid HTML structure: {filepath.name}",
                f"Invalid HTML structure in {filepath.name}"
            )

            # Check for Leaflet (for index.html)
            if filepath.name == 'index.html':
                has_leaflet = 'leaflet' in content.lower()
                self.check(
                    has_leaflet,
                    "Leaflet library found in index.html",
                    "Leaflet library not found in index.html"
                )

            return is_valid

        except Exception as e:
            self.check(False, "", f"Error reading {filepath.name}: {e}")
            return False

    def validate_data_directory(self):
        """Validate all GeoJSON files in data directory"""
        print(f"\n{BLUE}=== Validating Data Directory ==={RESET}")

        data_dir = self.script_dir / 'data'

        if not self.validate_file_exists(data_dir, "Data directory"):
            return

        # Expected files from map_config.py
        expected_files = [
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

        total_features = 0
        for filename in expected_files:
            filepath = data_dir / filename
            if filepath.exists():
                is_valid, count = self.validate_geojson(filepath)
                total_features += count
            else:
                self.check(False, "", f"Missing required file: {filename}")

        print(f"\n  {BLUE}Total features across all datasets: {total_features}{RESET}")

    def validate_html_files(self):
        """Validate HTML files"""
        print(f"\n{BLUE}=== Validating HTML Files ==={RESET}")

        index_html = self.script_dir / 'index.html'
        landing_html = self.script_dir / 'landing.html'

        self.validate_file_exists(index_html, "Interactive map")
        self.validate_html(index_html)

        self.validate_file_exists(landing_html, "Landing page")
        self.validate_html(landing_html)

        # Check file sizes
        if index_html.exists():
            size_mb = index_html.stat().st_size / (1024 * 1024)
            is_reasonable = 3 < size_mb < 15
            self.check(
                is_reasonable,
                f"index.html size is reasonable: {size_mb:.2f} MB",
                f"index.html size is unusual: {size_mb:.2f} MB (expected 3-15 MB)",
                is_warning=True
            )

    def validate_python_files(self):
        """Validate Python scripts"""
        print(f"\n{BLUE}=== Validating Python Files ==={RESET}")

        generate_map = self.script_dir / 'generate_map.py'
        map_config = self.script_dir / 'map_config.py'
        optimize_data = self.script_dir / 'scripts' / 'optimize_data.py'

        self.validate_file_exists(generate_map, "Map generator script")
        self.validate_file_exists(map_config, "Map configuration")
        self.validate_file_exists(optimize_data, "Data optimization script")

        # Check for shebang in main scripts
        for script in [generate_map, optimize_data]:
            if script.exists():
                with open(script, 'r') as f:
                    first_line = f.readline()
                has_shebang = first_line.startswith('#!/usr/bin/env python')
                self.check(
                    has_shebang,
                    f"{script.name} has proper shebang",
                    f"{script.name} missing shebang",
                    is_warning=True
                )

    def validate_documentation(self):
        """Validate documentation files"""
        print(f"\n{BLUE}=== Validating Documentation ==={RESET}")

        readme = self.script_dir / 'README.md'
        deployment = self.script_dir / 'DEPLOYMENT.md'
        requirements = self.script_dir / 'requirements.txt'

        self.validate_file_exists(readme, "README.md")
        self.validate_file_exists(deployment, "DEPLOYMENT.md")
        self.validate_file_exists(requirements, "requirements.txt")

        # Check README has key sections
        if readme.exists():
            with open(readme, 'r') as f:
                content = f.read()

            has_purpose = '## 🎯 Purpose' in content or '## Purpose' in content
            has_quick_start = 'Quick Start' in content
            has_features = 'Features' in content or 'FEATURES' in content

            self.check(
                has_purpose and has_quick_start and has_features,
                "README has key sections",
                "README missing important sections",
                is_warning=True
            )

    def validate_configuration(self):
        """Validate configuration files"""
        print(f"\n{BLUE}=== Validating Configuration ==={RESET}")

        gitignore = self.script_dir / '.gitignore'
        self.validate_file_exists(gitignore, ".gitignore")

        if gitignore.exists():
            with open(gitignore, 'r') as f:
                content = f.read()

            has_python = '__pycache__' in content or '*.pyc' in content
            has_venv = 'venv/' in content or 'ENV/' in content

            self.check(
                has_python and has_venv,
                ".gitignore has Python patterns",
                ".gitignore missing Python patterns",
                is_warning=True
            )

    def print_summary(self):
        """Print validation summary"""
        print(f"\n{BLUE}{'=' * 60}{RESET}")
        print(f"{BLUE}VALIDATION SUMMARY{RESET}")
        print(f"{BLUE}{'=' * 60}{RESET}")

        print(f"\nChecks passed: {self.checks_passed}/{self.checks_total}")

        if self.errors:
            print(f"\n{RED}Errors ({len(self.errors)}):{RESET}")
            for error in self.errors:
                print(f"  {RED}•{RESET} {error}")

        if self.warnings:
            print(f"\n{YELLOW}Warnings ({len(self.warnings)}):{RESET}")
            for warning in self.warnings:
                print(f"  {YELLOW}•{RESET} {warning}")

        if not self.errors and not self.warnings:
            print(f"\n{GREEN}✓ All validation checks passed!{RESET}")
            return 0
        elif not self.errors:
            print(f"\n{YELLOW}⚠ Validation passed with warnings{RESET}")
            return 0
        else:
            print(f"\n{RED}✗ Validation failed with {len(self.errors)} error(s){RESET}")
            return 1

    def run_all(self):
        """Run all validation checks"""
        print(f"{BLUE}{'=' * 60}{RESET}")
        print(f"{BLUE}Federal Districts Map - Validation{RESET}")
        print(f"{BLUE}{'=' * 60}{RESET}")

        self.validate_data_directory()
        self.validate_html_files()
        self.validate_python_files()
        self.validate_documentation()
        self.validate_configuration()

        return self.print_summary()


def main():
    """Main execution"""
    validator = Validator()
    exit_code = validator.run_all()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()

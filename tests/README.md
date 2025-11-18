# Test Suite for Federal Districts Map

Automated tests for map generation, data integrity, and HTML output.

## Running Tests

### Using unittest (built-in)

```bash
# Run all tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests.test_generate_map

# Run with verbose output
python -m unittest discover tests -v
```

### Using pytest (recommended)

```bash
# Install pytest
pip install pytest

# Run all tests
pytest tests/

# Run with coverage
pip install pytest-cov
pytest tests/ --cov=. --cov-report=html
```

## Test Structure

- `test_generate_map.py` - Unit tests for map generation logic
- `test_data_integrity.py` - Tests for GeoJSON data files
- `test_html_output.py` - Tests for generated HTML files

## Test Coverage

Current test coverage:
- ✅ Map configuration validation
- ✅ Educational content completeness
- ✅ GeoJSON structure and validity
- ✅ Feature count verification (308 total)
- ✅ HTML file structure
- ✅ File size optimization
- ✅ Search functionality presence

## Continuous Integration

Tests run automatically on GitHub Actions for:
- Every push to main branch
- Every pull request
- Manual workflow dispatch

See `.github/workflows/validate.yml` for CI configuration.

## Adding New Tests

1. Create test file in `tests/` directory
2. Use naming convention: `test_*.py`
3. Inherit from `unittest.TestCase`
4. Use descriptive test method names starting with `test_`
5. Add docstrings explaining what each test validates

Example:

```python
import unittest

class TestNewFeature(unittest.TestCase):
    """Test description"""

    def test_something(self):
        """Test what this validates"""
        self.assertTrue(True)
```

## Expected Results

All tests should pass:

```
.............................
----------------------------------------------------------------------
Ran 29 tests in 2.456s

OK
```

## Troubleshooting

**Import errors:**
- Ensure you're in the project root
- Check virtual environment is activated

**Missing dependencies:**
```bash
pip install -r requirements.txt
```

**Test failures:**
- Check data files exist in `data/` directory
- Verify `index.html` and `landing.html` are generated
- Run `python validate.py` first

# Contributing to Federal Districts Map

Thank you for your interest in contributing to the Federal Districts Map project! This document provides guidelines and instructions for contributing.

## 🎯 Ways to Contribute

### 1. Report Bugs
Found a bug? Please [open an issue](https://github.com/Jacob234/Federal-Districts-Map/issues/new?template=bug_report.md) with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable
- Browser/device information

### 2. Suggest Features
Have an idea? [Request a feature](https://github.com/Jacob234/Federal-Districts-Map/issues/new?template=feature_request.md) with:
- Description of the feature
- Use case and benefits
- Potential implementation approach

### 3. Improve Documentation
- Fix typos or clarify explanations
- Add examples or tutorials
- Improve code comments
- Enhance educational content

### 4. Add District Systems
Suggest new federal district systems to include:
- Provide official data source (must be public domain)
- Explain educational value
- Include historical context

### 5. Enhance Code
- Fix bugs
- Improve performance
- Add new features
- Write tests

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- Text editor or IDE
- Web browser for testing

### Setup Development Environment

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/YOUR-USERNAME/Federal-Districts-Map.git
   cd Federal-Districts-Map
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov  # For testing
   ```

4. **Install pre-commit hooks (optional but recommended):**
   ```bash
   pip install pre-commit
   pre-commit install
   ```

5. **Verify setup:**
   ```bash
   python validate.py
   python -m unittest discover tests
   ```

---

## 📝 Development Workflow

### 1. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

**Branch naming conventions:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `test/` - Test additions or improvements
- `refactor/` - Code refactoring

### 2. Make Your Changes

Follow these guidelines:

#### Code Style
- **Python:** Follow PEP 8
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Add docstrings to all functions
- Use type hints where helpful

Example:
```python
def create_district_layer(layer_id: str, config: dict) -> bool:
    """
    Create a district layer on the map.

    Parameters:
    -----------
    layer_id : str
        Unique identifier for the layer
    config : dict
        Layer configuration dictionary

    Returns:
    --------
    bool
        True if successful, False otherwise
    """
    pass
```

#### Educational Content
When adding or modifying educational content:
- Use clear, accessible language
- Cite official sources
- Include historical context
- Explain real-world impact
- Keep descriptions concise (2-3 paragraphs)

#### GeoJSON Data
- Ensure CRS is EPSG:4326 (WGS84)
- Simplify geometries for web performance
- Include proper attributions
- Verify data is public domain

### 3. Test Your Changes

```bash
# Run validation script
python validate.py

# Run unit tests
python -m unittest discover tests -v

# Test locally in browser
python -m http.server 8000
# Open http://localhost:8000/landing.html
```

### 4. Commit Your Changes

```bash
git add .
git commit -m "Add: brief description of changes"
```

**Commit message format:**
```
Type: Brief description (50 chars max)

Detailed explanation if needed (wrap at 72 chars)

- Bullet points for multiple changes
- Reference issues: Fixes #123
```

**Types:**
- `Add:` - New features
- `Fix:` - Bug fixes
- `Update:` - Changes to existing features
- `Docs:` - Documentation only
- `Test:` - Test additions
- `Refactor:` - Code refactoring
- `Style:` - Formatting, no code change

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then:
1. Go to GitHub repository
2. Click "New Pull Request"
3. Fill out the PR template
4. Wait for review

---

## 🧪 Testing Requirements

All contributions must include appropriate tests:

### For New Features
- Add unit tests for new functions
- Add integration tests if applicable
- Update `tests/README.md` if needed
- Ensure all tests pass

### For Bug Fixes
- Add test that reproduces the bug
- Verify fix resolves the issue
- Ensure no regression

### Running Tests
```bash
# All tests
python -m unittest discover tests

# Specific test file
python -m unittest tests.test_generate_map

# With coverage
pip install pytest pytest-cov
pytest tests/ --cov=. --cov-report=html
```

---

## 📋 Pull Request Guidelines

### Before Submitting
- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] Validation script passes (`python validate.py`)
- [ ] Documentation updated if needed
- [ ] CHANGELOG.md updated (if applicable)
- [ ] Commits are clear and descriptive
- [ ] Branch is up to date with main

### PR Description Should Include
- **What:** What changes does this PR make?
- **Why:** Why are these changes needed?
- **How:** How were these changes implemented?
- **Testing:** How were the changes tested?
- **Screenshots:** If UI changes (before/after)

### Review Process
1. Automated tests run on GitHub Actions
2. Maintainer reviews code and provides feedback
3. Make requested changes if needed
4. Maintainer merges when approved

---

## 🎨 Adding New District Systems

Want to add a new federal district system? Follow these steps:

### 1. Find Data Source
- Must be from official US federal government source
- Must be public domain
- Must be available as shapefile or GeoJSON
- Verify accuracy and currency

### 2. Prepare Data
```bash
# Place source file in appropriate location
# Then optimize
python scripts/optimize_data.py
```

### 3. Add Configuration
Edit `map_config.py`:
```python
'new_system': {
    'name': 'Display Name',
    'file': 'data/New_System.geojson',
    'branch': 'Executive',  # or Judicial, Military
    'style': {
        'fillColor': '#COLOR',
        'color': '#BORDER',
        'weight': 2,
        'fillOpacity': 0.35,
    },
    'education': {
        'title': 'System Title',
        'description': '...',
        'purpose': '...',
        'structure': '...',
        'established': 'Year',
        'why_it_matters': '...',
    },
}
```

### 4. Update Documentation
- Add to README.md list of systems
- Update total feature count
- Add to CHANGELOG.md

### 5. Regenerate Map
```bash
python generate_map.py
```

### 6. Test
- Verify layer appears in control
- Check popups display correctly
- Test address search includes new system
- Run validation script

---

## 🐛 Reporting Security Issues

**Do not open public issues for security vulnerabilities.**

Instead, email: [security contact - TBD]

Include:
- Description of vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

---

## 🙏 Recognition

Contributors will be recognized in:
- GitHub contributors page
- CHANGELOG.md for significant contributions
- Project documentation

Thank you for making Federal Districts Map better for everyone!

---

## 📞 Questions?

- **General questions:** [Open a discussion](https://github.com/Jacob234/Federal-Districts-Map/discussions)
- **Bug reports:** [Create an issue](https://github.com/Jacob234/Federal-Districts-Map/issues)
- **Feature requests:** [Create an issue](https://github.com/Jacob234/Federal-Districts-Map/issues)

---

*Happy contributing! 🗺️*

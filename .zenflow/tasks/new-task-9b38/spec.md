# Technical Specification: Make Repository Structure Compliant

## Task Assessment

**Complexity Level**: Easy

This is a straightforward repository structure setup task. The main branch is currently empty and needs to be populated with the minimum required files and directory structure to comply with Home Assistant Custom Integration (HACS) standards.

## Technical Context

- **Project Type**: Home Assistant Custom Integration
- **Integration Domain**: oblamatik
- **Target Platform**: HACS (Home Assistant Community Store)
- **Repository State**: Main branch is empty
- **Language**: Python (Home Assistant integrations are Python-based)

## Problem Statement

The repository structure for the "bobsilesia/oblamatik" integration on the main branch does not meet HACS requirements. An empty repository cannot be:
- Discovered by HACS
- Installed by users
- Validated against Home Assistant standards

## Requirements for HACS Compliance

According to HACS documentation, a valid integration repository must have:

### 1. Directory Structure
- **Required**: `custom_components/INTEGRATION_NAME/` directory
- All integration files must be inside this directory
- Only one integration per repository

### 2. Minimum Required Files

Inside `custom_components/oblamatik/`:
- **`manifest.json`**: Integration metadata with required keys:
  - `domain` (must match directory name: "oblamatik")
  - `name` (human-readable name)
  - `version` (semantic version)
  - `documentation` (URL to documentation)
  - `issue_tracker` (URL to issue tracker)
  - `codeowners` (list of maintainers)
  - `requirements` (Python dependencies)
  - `dependencies` (HA integration dependencies)
  
- **`__init__.py`**: Component entry point
  - Minimum: docstring describing the integration
  - Should handle async setup

### 3. Recommended Root Files
- **`README.md`**: Project documentation
- **`info.md`**: Brief description for HACS UI (optional)
- **`.gitignore`**: To exclude Python cache and other build artifacts

## Implementation Approach

### Phase 1: Create Directory Structure
1. Create `custom_components/oblamatik/` directory
2. Create `.gitignore` at repository root

### Phase 2: Create Minimum Required Files
1. Create `manifest.json` with all required fields
   - Use placeholder URLs for documentation and issue_tracker
   - Set initial version as "0.1.0"
   - Add appropriate codeowners
2. Create `__init__.py` with basic setup structure
   - Add docstring
   - Add async_setup stub function
   - Add proper logging

### Phase 3: Add Documentation
1. Create `README.md` with:
   - Integration description
   - Installation instructions
   - Basic usage information
   - Development/contribution guidelines

## Files to be Created

```
/
├── .gitignore                              # NEW: Python/HA specific ignores
├── README.md                               # NEW: Project documentation
├── custom_components/                      # NEW: HACS required directory
│   └── oblamatik/                         # NEW: Integration directory
│       ├── __init__.py                    # NEW: Component entry point
│       └── manifest.json                  # NEW: Integration metadata
```

## Data Model / API Changes

No API or data model changes required. This task only establishes the repository structure.

## Implementation Details

### manifest.json Structure
```json
{
  "domain": "oblamatik",
  "name": "Oblamatik",
  "version": "0.1.0",
  "documentation": "https://github.com/bobsilesia/oblamatik",
  "issue_tracker": "https://github.com/bobsilesia/oblamatik/issues",
  "codeowners": ["@bobsilesia"],
  "requirements": [],
  "dependencies": [],
  "iot_class": "local_polling"
}
```

### __init__.py Structure
```python
"""The Oblamatik integration."""
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
    """Set up the Oblamatik component."""
    _LOGGER.info("Setting up Oblamatik integration")
    return True
```

### .gitignore Contents
Standard Python/Home Assistant ignores:
- `__pycache__/`
- `*.py[cod]`
- `.pytest_cache/`
- `.vscode/`
- `.DS_Store`

## Verification Approach

### Manual Verification
1. Check directory structure matches HACS requirements:
   - `custom_components/oblamatik/` exists
   - Required files present: `manifest.json`, `__init__.py`

2. Validate `manifest.json`:
   - Contains all required fields
   - Valid JSON syntax
   - Version follows semantic versioning

3. Validate `__init__.py`:
   - Valid Python syntax
   - Contains async_setup function

### Automated Verification
- Run Python syntax check: `python -m py_compile custom_components/oblamatik/__init__.py`
- Validate JSON: `python -m json.tool custom_components/oblamatik/manifest.json`

## Assumptions

1. Integration name is "oblamatik" (derived from task description)
2. Repository will be hosted at `github.com/bobsilesia/oblamatik`
3. Maintainer username is "bobsilesia"
4. Integration is in initial development stage (version 0.1.0)
5. Integration uses local polling for IoT class
6. No external Python dependencies required yet
7. No Home Assistant integration dependencies required yet

## Risks and Constraints

**Low Risk**: This is purely structural setup with no business logic. The main constraint is ensuring all HACS-required fields are present and properly formatted.

## Future Considerations

After establishing the compliant structure, future work may include:
- Adding platform files (e.g., `sensor.py`, `switch.py`)
- Implementing actual integration logic
- Adding configuration flow (`config_flow.py`)
- Adding translations
- Adding tests
- Registering with Home Assistant Brands
- Publishing to HACS default repository list

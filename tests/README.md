# CompPy Tests

This directory contains functional tests for the CompPy compressor design application.

## Test Coverage

### test_blade_calc.py
- Tests stage blade angle calculations (velocity triangles)
- Tests full stage property calculations with consistent axial velocity
- Tests NACA 4-series airfoil blade generation
- Tests bounding box calculations for meshes

### test_stl_utils.py
- Tests cylinder mesh generation
- Tests duct (hollow cylinder) mesh generation
- Tests blade mesh generation with twist and taper
- Tests rotation matrix generation

### test_file_ops.py
- Tests saving compressor configurations to JSON
- Tests loading compressor configurations from JSON
- Tests multi-stage configurations
- Tests file extension handling

## Running Tests

### With virtual environment (recommended):
```bash
source venv/bin/activate
python -m unittest discover -s tests -v
```

### Run specific test file:
```bash
source venv/bin/activate
python -m unittest tests.test_blade_calc -v
```

### Run specific test:
```bash
source venv/bin/activate
python -m unittest tests.test_blade_calc.TestBladeCalc.test_stage_calc -v
```

## Requirements

Tests require the same dependencies as the main application:
- PyQt5
- matplotlib
- numpy
- numpy-stl

Install with: `pip install -r requirements.txt`

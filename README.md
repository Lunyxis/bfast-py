# bfast-py

Python implementation of the BFAST and BFAST0n structural change detection algorithms  
by Jan Verbeselt et al. The implementation is based on the original  
[R implementation](https://github.com/bfast2/bfast).  

## Installation

This package uses [UV](https://github.com/astral-sh/uv) for package management, which is a fast, reliable Python package installer and resolver.

### Install UV

If you don't have UV installed yet, you can install it with:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or using pip:

```bash
pip install uv
```

### Install the package

#### For development

Clone the repository and install the package in development mode:

```bash
# Clone the repository
git clone git@github.com:Lunyxis/bfast-py.git
cd bfast-py

# Create and activate a virtual environment using UV
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package in development mode
uv pip install -e .
```

#### For usage

```bash
uv pip install git+https://github.com/Lunyxis/bfast-py.git
```

## Usage

TODO : update example usage, test, etc.

```python
import bfast_py

# Update with examples
```

## Development

### Creating a virtual environment

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Installing dependencies

```bash
# Development dependencies
uv pip install -e .[dev]

# Classic dependencies
uv pip install -e .
```

### Adding new dependencies

Edit the `pyproject.toml` file to add new dependencies, then run:

```bash
uv pip install -e .
```

### Running tests

```bash
uv pip install pytest
pytest
```

<!-- ## How to run the tests
Tests for each file in the `src` directory are contained withing that
source file. In order to run the test, run:

`python file.py`

In order to get the more verbose output, run:

`python file.py --log=INFO`

In order to see the debug information, run:

`python file.py --log=DEBUG`

In order to reproduce the plots, run:

`python plots.py` -->

<!-- ## Building and publishing

Build the package:

```bash
uv pip install build
python -m build
```

Publish to PyPI:

```bash
uv pip install twine
twine upload dist/*
``` -->

## License

Proprietary. For internal use only.
@ 2025 Airbus Defence and Space. All rights reserved.


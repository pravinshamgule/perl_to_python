# Perl to Python Module - Quick Start Guide

## How to Install

### Prerequisites
- Python 3.6 or higher
- Git (for cloning the repository)

### Installation Steps
```bash
# Clone the repository
git clone https://github.com/yourusername/perl2python.git
cd perl2python

# Standard installation
pip install .

# OR Development installation (if you plan to modify the code)
pip install -e .
```

## How to Use

### Command-line Usage
```bash
# Basic conversion
perl2python path/to/your/script.pl

# Specify output file
perl2python path/to/your/script.pl -o path/to/output/script.py

# Convert directory (recursively)
perl2python path/to/perl/dir -o path/to/python/dir -r

# Use custom configuration
perl2python path/to/your/script.pl -c path/to/config.json

# Get help
perl2python --help
```

### Python Module Usage
```python
# Simple usage
from perl2python.converter import convert_perl_to_python
convert_perl_to_python("path/to/your/script.pl", "path/to/output.py")

# Advanced usage
from perl2python.converter import PerlToPythonConverter
converter = PerlToPythonConverter()
converter.convert_file("path/to/your/script.pl", "path/to/output.py")
```

For detailed instructions and examples, see the comprehensive guide in `INSTALL_AND_USAGE.md`.
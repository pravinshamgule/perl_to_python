# Perl to Python Conversion Agent - Installation and Usage Guide

This guide provides detailed instructions on how to install and use the Perl to Python Conversion Agent.

## Table of Contents

- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Installation from Source](#installation-from-source)
  - [Development Installation](#development-installation)
- [Usage](#usage)
  - [Command-line Interface](#command-line-interface)
  - [Python Module Usage](#python-module-usage)
  - [Configuration Options](#configuration-options)
- [Examples](#examples)
  - [Basic Conversion](#basic-conversion)
  - [Directory Conversion](#directory-conversion)
  - [Using Custom Configuration](#using-custom-configuration)
  - [Programmatic Usage](#programmatic-usage)

## Installation

### Prerequisites

- Python 3.6 or higher
- Git (for cloning the repository)

### Installation from Source

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/perl2python.git
   cd perl2python
   ```

2. Install the package:
   ```bash
   pip install .
   ```

   This will install the package and create a `perl2python` command-line tool that you can use from anywhere.

### Development Installation

If you plan to modify the code or contribute to the project, install in development mode:

```bash
pip install -e .
```

This creates an "editable" installation where changes to the source code are immediately reflected without needing to reinstall.

## Usage

The Perl to Python Conversion Agent can be used in two ways:
1. As a command-line tool
2. As a Python module in your own code

### Command-line Interface

After installation, you can use the `perl2python` command from your terminal:

#### Basic Usage

Convert a single Perl file to Python:

```bash
perl2python path/to/your/script.pl
```

This will create a new Python file with the same name but with a `.py` extension in the same directory.

#### Specifying Output

You can specify the output file or directory:

```bash
perl2python path/to/your/script.pl -o path/to/output/script.py
```

#### Converting Directories

Convert all Perl files in a directory:

```bash
perl2python path/to/perl/dir -o path/to/python/dir
```

Use the `-r` flag to recursively process subdirectories:

```bash
perl2python path/to/perl/dir -o path/to/python/dir -r
```

#### Using Configuration Files

You can customize the conversion process using a configuration file:

```bash
perl2python path/to/your/script.pl -c path/to/config.json
```

#### Other Options

- `--verbose` or `-v`: Enable verbose output
- `--debug` or `-d`: Enable debug mode with more detailed logging
- `--dry-run`: Show what would be done without making changes
- `--version`: Show version information and exit

For a complete list of options:

```bash
perl2python --help
```

### Python Module Usage

You can also use the converter programmatically in your Python code:

#### Basic Import

```python
from perl2python.converter import convert_perl_to_python

# Convert a file
python_code = convert_perl_to_python("path/to/your/script.pl", "path/to/output.py")
```

#### Using the Converter Class

For more control, use the `PerlToPythonConverter` class directly:

```python
from perl2python.converter import PerlToPythonConverter

# Create a converter instance
converter = PerlToPythonConverter()

# Convert a file
python_code = converter.convert_file("path/to/your/script.pl", "path/to/output.py")

# Or convert code from a string
perl_code = """
#!/usr/bin/perl
print "Hello, World!\n";
"""
python_code = converter.convert_code(perl_code)
```

### Configuration Options

The conversion process can be customized using a JSON configuration file. Here's an example configuration:

```json
{
  "conversion_options": {
    "preserve_comments": true,
    "add_type_hints": true,
    "convert_pod_to_docstrings": true
  },
  "module_mappings": {
    "Data::Dumper": "pprint",
    "Getopt::Long": "argparse"
  },
  "syntax_mappings": {
    "variable_prefixes": {
      "$": "",
      "@": "",
      "%": ""
    },
    "operators": {
      "eq": "==",
      "ne": "!="
    }
  }
}
```

A complete template with all available options can be found in the `src/perl2python/config_template.json` file.

## Examples

### Basic Conversion

Convert a single Perl file to Python:

```bash
# Command-line
perl2python input/add_numbers.pl -o output/add_numbers.py

# Python code
from perl2python.converter import convert_perl_to_python
convert_perl_to_python("input/add_numbers.pl", "output/add_numbers.py")
```

### Directory Conversion

Convert all Perl files in a directory:

```bash
# Command-line
perl2python input -o output -r

# Python code
import os
from pathlib import Path
from perl2python.converter import PerlToPythonConverter

converter = PerlToPythonConverter()
perl_dir = Path("input")
output_dir = Path("output")

for perl_file in perl_dir.glob("*.pl"):
    output_file = output_dir / f"{perl_file.stem}.py"
    converter.convert_file(str(perl_file), str(output_file))
```

### Using Custom Configuration

```bash
# Command-line
perl2python input/test_script.pl -o output/test_script.py -c my_config.json

# Python code
from perl2python.converter import PerlToPythonConverter

config = {
    "conversion_options": {
        "preserve_comments": True,
        "add_type_hints": True
    }
}

converter = PerlToPythonConverter(config)
converter.convert_file("input/test_script.pl", "output/test_script.py")
```

### Programmatic Usage

For more advanced programmatic usage examples, see the `examples/programmatic_usage.py` file in the repository. It includes examples of:

1. Basic usage with the convenience function
2. Using custom configuration
3. Batch conversion of multiple files
4. Converting Perl code from a string

You can run the examples with:

```bash
python examples/programmatic_usage.py
```

## Additional Resources

- For detailed documentation, see the [docs/README.md](docs/README.md) file.
- For more examples, check out the [examples](examples/) directory.
- To run tests, use: `python -m unittest discover tests`

## Troubleshooting

If you encounter any issues:

1. Make sure you have Python 3.6 or higher installed
2. Try running with the `--debug` flag for more detailed output
3. Check that your Perl files are valid and can be parsed
4. For complex Perl code, you may need to adjust the configuration or manually edit the converted Python code

### Installation Issues

If you encounter errors during installation, try the following:

1. **File lock errors** (e.g., "The process cannot access the file because it is being used by another process"):
   - Close any applications that might be accessing the package files (editors, file explorers, etc.)
   - Try installing with the `--use-pep517` flag: `pip install --use-pep517 .`
   - If using development mode, try a regular installation: `pip install .` instead of `pip install -e .`
   - As a last resort, restart your computer to release all file locks

2. **Permission errors**:
   - On Unix-like systems, try using `sudo pip install .` or install in user mode with `pip install --user .`
   - On Windows, run your command prompt or terminal as Administrator

3. **Dependency issues**:
   - Ensure you have the latest version of pip: `python -m pip install --upgrade pip`
   - If you're using a virtual environment, make sure it's activated

4. **Other issues**:
   - Try installing with verbose output for more details: `pip install -v .`
   - Check the [pip documentation](https://pip.pypa.io/) for more troubleshooting tips
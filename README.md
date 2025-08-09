# Perl to Python Conversion Agent

An AI-powered tool for converting Perl code to Python.

## Quick Start

```bash
# Install the package
pip install -e .

# Convert a Perl file to Python
perl2python path/to/your/script.pl

# Convert a directory of Perl files
perl2python path/to/perl/dir -o path/to/python/dir -r

# Get help
perl2python --help
```

An AI-powered Perl to Python conversion agent has been successfully implemented, including a well-defined directory structure, essential modules, and comprehensive documentation. The implementation is complete and ready for use, with the repository said to be structured appropriately for future enhancements. No errors or significant issues were noted during the process.

## Project Structure

- `src/perl2python/`: Main package source code
  - `__init__.py`: Package initialization
  - `converter.py`: Core conversion logic
  - `cli.py`: Command-line interface
  - `__main__.py`: Entry point for running as a module
- `tests/`: Test files
  - `sample_perl/`: Sample Perl files for testing
  - `test_converter.py`: Unit tests for the converter
- `docs/`: Documentation
  - `README.md`: Detailed documentation
- `examples/`: Example scripts
  - `programmatic_usage.py`: Examples of using the converter in Python code

## Features

- Convert individual Perl files or entire directories to Python
- Preserve code structure and comments
- Map Perl modules to their Python equivalents
- Convert Perl's special variables to Python equivalents
- Handle Perl-specific syntax like variable prefixes (`$`, `@`, `%`)
- Support for Perl's loop constructs (for, foreach, while, until)
- Support for Perl's regex operations (match, substitution, translation)
- Support for Perl's hash and array operations
- Automatic post-processing to fix common conversion issues
- Customizable conversion through configuration files
- Command-line interface for easy integration into workflows

## Documentation

For detailed documentation, see the [docs/README.md](docs/README.md) file.

## Examples

Check out the [examples](examples/) directory for examples of how to use the converter programmatically.

## Testing

Run the tests with:

```bash
python -m unittest discover tests
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
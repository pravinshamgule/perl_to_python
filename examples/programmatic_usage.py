#!/usr/bin/env python3
"""
Example script demonstrating how to use the Perl to Python converter programmatically.

This script shows how to integrate the converter into your own Python code.
"""

import os
import sys
import json
from pathlib import Path

# Add the src directory to the Python path if not installed
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from perl2python.converter import PerlToPythonConverter, convert_perl_to_python


def example_1_basic_usage():
    """Basic usage example using the convenience function."""
    print("\n=== Example 1: Basic Usage ===")
    
    # Define paths
    perl_file = Path(__file__).parent.parent / 'tests' / 'sample_perl' / 'hello_world.pl'
    output_file = Path(__file__).parent / 'output' / 'hello_world.py'
    
    # Create output directory if it doesn't exist
    os.makedirs(output_file.parent, exist_ok=True)
    
    print(f"Converting {perl_file} to {output_file}")
    
    # Use the convenience function
    python_code = convert_perl_to_python(str(perl_file), str(output_file))
    
    print(f"Conversion complete. Output saved to {output_file}")
    print(f"First 10 lines of the converted code:")
    print("\n".join(python_code.split("\n")[:10]))


def example_2_custom_configuration():
    """Example with custom configuration."""
    print("\n=== Example 2: Custom Configuration ===")
    
    # Define paths
    perl_file = Path(__file__).parent.parent / 'tests' / 'sample_perl' / 'hello_world.pl'
    output_file = Path(__file__).parent / 'output' / 'hello_world_custom.py'
    
    # Create output directory if it doesn't exist
    os.makedirs(output_file.parent, exist_ok=True)
    
    # Define custom configuration
    config = {
        "conversion_options": {
            "preserve_comments": True,
            "add_type_hints": True,
            "convert_pod_to_docstrings": True
        },
        "module_mappings": {
            "Data::Dumper": "pprint",
            "Getopt::Long": "argparse"
        }
    }
    
    print(f"Converting {perl_file} to {output_file} with custom configuration")
    
    # Create converter with custom configuration
    converter = PerlToPythonConverter(config)
    
    # Convert the file
    python_code = converter.convert_file(str(perl_file), str(output_file))
    
    print(f"Conversion complete. Output saved to {output_file}")
    print(f"First 10 lines of the converted code:")
    print("\n".join(python_code.split("\n")[:10]))


def example_3_batch_conversion():
    """Example of batch conversion of multiple files."""
    print("\n=== Example 3: Batch Conversion ===")
    
    # Define paths
    perl_dir = Path(__file__).parent.parent / 'tests' / 'sample_perl'
    output_dir = Path(__file__).parent / 'output' / 'batch'
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create converter
    converter = PerlToPythonConverter()
    
    # Process all Perl files in the directory
    perl_files = list(perl_dir.glob('*.pl'))
    print(f"Found {len(perl_files)} Perl files in {perl_dir}")
    
    for perl_file in perl_files:
        output_file = output_dir / f"{perl_file.stem}.py"
        print(f"Converting {perl_file} to {output_file}")
        
        # Convert the file
        converter.convert_file(str(perl_file), str(output_file))
    
    print(f"Batch conversion complete. Output saved to {output_dir}")


def example_4_string_conversion():
    """Example of converting Perl code from a string."""
    print("\n=== Example 4: String Conversion ===")
    
    # Define Perl code as a string
    perl_code = """
#!/usr/bin/perl
use strict;
use warnings;

# A simple subroutine
sub greet {
    my ($name) = @_;
    print "Hello, $name!\\n";
}

# Call the subroutine
greet("World");
"""
    
    print("Converting Perl code from string:")
    print("-" * 40)
    print(perl_code)
    print("-" * 40)
    
    # Create converter
    converter = PerlToPythonConverter()
    
    # Convert the code
    python_code = converter.convert_code(perl_code)
    
    print("Converted Python code:")
    print("-" * 40)
    print(python_code)
    print("-" * 40)


def main():
    """Run all examples."""
    print("Perl to Python Converter - Programmatic Usage Examples")
    print("=" * 60)
    
    # Run examples
    example_1_basic_usage()
    example_2_custom_configuration()
    example_3_batch_conversion()
    example_4_string_conversion()
    
    print("\nAll examples completed successfully!")


if __name__ == '__main__':
    main()
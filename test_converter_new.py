#!/usr/bin/env python3
"""
New test script for the Perl to Python converter.
This script ensures that the latest version of the converter is used.
"""

import os
import sys
import importlib
from datetime import datetime

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Force reload of the converter module to ensure latest changes are used
if 'perl2python.converter' in sys.modules:
    importlib.reload(sys.modules['perl2python.converter'])

# Import the converter
from perl2python.converter import PerlToPythonConverter

def main():
    """Main function."""
    # Set conversion date environment variable for the header
    os.environ['CONVERSION_DATE'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Create converter with default configuration
    config = {'options': {'add_exception_handling': True}}
    converter = PerlToPythonConverter(config)
    
    # Convert add_numbers.pl
    perl_file = 'input/add_numbers.pl'
    output_file = 'output/add_numbers_fixed.py'
    
    print(f"Converting {perl_file} to {output_file}...")
    converter.convert_file(perl_file, output_file)
    print(f"Conversion complete. Output file: {output_file}")
    
    # Convert test_script.pl
    perl_file = 'input/test_script.pl'
    output_file = 'output/test_script_fixed.py'
    
    print(f"Converting {perl_file} to {output_file}...")
    converter.convert_file(perl_file, output_file)
    print(f"Conversion complete. Output file: {output_file}")
    
    # Convert StringUtils.pm
    perl_file = 'input/StringUtils.pm'
    output_file = 'output/StringUtils_fixed.py'
    
    print(f"Converting {perl_file} to {output_file}...")
    converter.convert_file(perl_file, output_file)
    print(f"Conversion complete. Output file: {output_file}")
    
    print("\nAll conversions completed. Please check the output files for proper handling of special variables.")

if __name__ == '__main__':
    main()
#!/usr/bin/env python3
"""
Test script for the Perl to Python converter.

This script tests the conversion of sample Perl files to Python
and validates that the output is as expected.
"""

import os
import sys
import unittest
import tempfile
import shutil
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from perl2python.converter import PerlToPythonConverter


class TestPerlToPythonConverter(unittest.TestCase):
    """Test cases for the Perl to Python converter."""

    def setUp(self):
        """Set up the test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.sample_dir = Path(__file__).parent / 'sample_perl'
        self.converter = PerlToPythonConverter()
        
        # Set the conversion date to a fixed value for testing
        os.environ['CONVERSION_DATE'] = '2025-08-03 21:34'

    def tearDown(self):
        """Clean up the test environment."""
        shutil.rmtree(self.temp_dir)

    def test_hello_world_conversion(self):
        """Test the conversion of the hello_world.pl sample file."""
        perl_file = self.sample_dir / 'hello_world.pl'
        python_file = Path(self.temp_dir) / 'hello_world.py'
        
        # Convert the file
        self.converter.convert_file(str(perl_file), str(python_file))
        
        # Check that the output file exists
        self.assertTrue(python_file.exists())
        
        # Read the converted Python code
        with open(python_file, 'r', encoding='utf-8') as f:
            python_code = f.read()
        
        # Validate the conversion
        self.assertIn('#!/usr/bin/env python3', python_code)
        self.assertIn('import argparse', python_code)
        self.assertIn('import pprint', python_code)
        self.assertIn('def main():', python_code)
        self.assertIn('def say_hello', python_code)
        self.assertIn('def print_help', python_code)
        self.assertIn('if __name__ == \'__main__\':', python_code)
        
        # Print the converted code for inspection
        print("\nConverted Python code:")
        print("-" * 40)
        print(python_code)
        print("-" * 40)

    def test_directory_conversion(self):
        """Test the conversion of a directory of Perl files."""
        # Create a temporary directory structure
        perl_dir = Path(self.temp_dir) / 'perl'
        python_dir = Path(self.temp_dir) / 'python'
        perl_dir.mkdir()
        
        # Copy the sample Perl file to the temporary directory
        shutil.copy(self.sample_dir / 'hello_world.pl', perl_dir / 'hello_world.pl')
        
        # Create a simple test script to convert the directory
        test_script = """
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
from perl2python.cli import main
sys.argv = ['perl2python', '{perl_dir}', '-o', '{python_dir}']
main()
        """.format(perl_dir=str(perl_dir), python_dir=str(python_dir))
        
        test_script_path = Path(self.temp_dir) / 'test_script.py'
        with open(test_script_path, 'w', encoding='utf-8') as f:
            f.write(test_script)
        
        # Run the test script
        os.system(f'python {test_script_path}')
        
        # Check that the output directory and file exist
        self.assertTrue(python_dir.exists())
        self.assertTrue((python_dir / 'hello_world.py').exists())


def validate_conversion_output(python_file):
    """
    Validate that the converted Python file meets our expectations.
    
    Args:
        python_file: Path to the converted Python file
        
    Returns:
        True if the conversion is valid, False otherwise
    """
    # Read the converted Python code
    with open(python_file, 'r', encoding='utf-8') as f:
        python_code = f.read()
    
    # Check for expected Python constructs
    expected_constructs = [
        '#!/usr/bin/env python3',
        'import argparse',
        'def main():',
        'if __name__ == \'__main__\':',
    ]
    
    for construct in expected_constructs:
        if construct not in python_code:
            print(f"Missing expected construct: {construct}")
            return False
    
    # Check for Perl constructs that should have been converted
    perl_constructs = [
        'use strict',
        'my $',
        'sub ',
        'print "',
    ]
    
    for construct in perl_constructs:
        if construct in python_code:
            print(f"Found unconverted Perl construct: {construct}")
            return False
    
    return True


def main():
    """Run the tests."""
    unittest.main()


if __name__ == '__main__':
    main()
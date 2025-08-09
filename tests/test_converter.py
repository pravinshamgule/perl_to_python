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
        
    def test_loop_constructs_conversion(self):
        """Test the conversion of Perl loop constructs."""
        # Create a temporary Perl file with loop constructs
        perl_code = """#!/usr/bin/perl
use strict;
use warnings;

# For loop with range
for my $i (1..5) {
    print "i = $i\\n";
}

# Foreach loop with array
my @fruits = ('apple', 'banana', 'orange');
foreach my $fruit (@fruits) {
    print "fruit = $fruit\\n";
}

# While loop
my $count = 0;
while ($count < 3) {
    print "count = $count\\n";
    $count++;
}

# Until loop
my $value = 10;
until ($value <= 0) {
    print "value = $value\\n";
    $value -= 2;
}
"""
        perl_file = Path(self.temp_dir) / 'loops.pl'
        with open(perl_file, 'w', encoding='utf-8') as f:
            f.write(perl_code)
            
        python_file = Path(self.temp_dir) / 'loops.py'
        
        # Convert the file
        self.converter.convert_file(str(perl_file), str(python_file))
        
        # Check that the output file exists
        self.assertTrue(python_file.exists())
        
        # Read the converted Python code
        with open(python_file, 'r', encoding='utf-8') as f:
            python_code = f.read()
        
        # Validate the conversion
        self.assertIn('for i in range(1, 6):', python_code)
        self.assertIn('for fruit in fruits:', python_code)
        self.assertIn('while count < 3:', python_code)
        self.assertIn('while not (value <= 0):', python_code)
        
        # Print the converted code for inspection
        print("\nConverted loop constructs code:")
        print("-" * 40)
        print(python_code)
        print("-" * 40)
        
    def test_regex_operations_conversion(self):
        """Test the conversion of Perl regex operations."""
        # Create a temporary Perl file with regex operations
        perl_code = """#!/usr/bin/perl
use strict;
use warnings;

my $text = "Hello, World!";

# Match operation
if ($text =~ m/Hello/) {
    print "Text contains 'Hello'\\n";
}

# Case-insensitive match
if ($text =~ m/world/i) {
    print "Text contains 'world' (case-insensitive)\\n";
}

# Substitution
$text =~ s/Hello/Hi/;
print "After substitution: $text\\n";

# Global substitution
my $sentence = "apple orange apple banana apple";
$sentence =~ s/apple/fruit/g;
print "After global substitution: $sentence\\n";

# Translation
my $uppercase = "abcdef";
$uppercase =~ tr/a-z/A-Z/;
print "After translation: $uppercase\\n";
"""
        perl_file = Path(self.temp_dir) / 'regex.pl'
        with open(perl_file, 'w', encoding='utf-8') as f:
            f.write(perl_code)
            
        python_file = Path(self.temp_dir) / 'regex.py'
        
        # Convert the file
        self.converter.convert_file(str(perl_file), str(python_file))
        
        # Check that the output file exists
        self.assertTrue(python_file.exists())
        
        # Read the converted Python code
        with open(python_file, 'r', encoding='utf-8') as f:
            python_code = f.read()
        
        # Validate the conversion
        self.assertIn('import re', python_code)
        self.assertIn("re.search(r'Hello'", python_code)
        self.assertIn("re.search(r'world'", python_code)
        self.assertIn("re.IGNORECASE", python_code)
        self.assertIn("re.sub(r'Hello'", python_code)
        self.assertIn("re.sub(r'apple'", python_code)
        self.assertIn("str.maketrans", python_code)
        
        # Print the converted code for inspection
        print("\nConverted regex operations code:")
        print("-" * 40)
        print(python_code)
        print("-" * 40)
        
    def test_hash_array_operations_conversion(self):
        """Test the conversion of Perl hash and array operations."""
        # Create a temporary Perl file with hash and array operations
        perl_code = """#!/usr/bin/perl
use strict;
use warnings;

# Array operations
my @numbers = (1, 2, 3, 4, 5);
print "First element: $numbers[0]\\n";
print "Last index: $#numbers\\n";
push @numbers, 6;
my $popped = pop @numbers;
unshift @numbers, 0;
my $shifted = shift @numbers;

# Hash operations
my %person = (
    'name' => 'John',
    'age' => 30,
    'city' => 'New York'
);
print "Name: $person{'name'}\\n";
print "Age: $person{age}\\n";
$person{'job'} = 'Developer';
delete $person{'city'};

# Hash iteration
foreach my $key (keys %person) {
    print "$key: $person{$key}\\n";
}
"""
        perl_file = Path(self.temp_dir) / 'hash_array.pl'
        with open(perl_file, 'w', encoding='utf-8') as f:
            f.write(perl_code)
            
        python_file = Path(self.temp_dir) / 'hash_array.py'
        
        # Convert the file
        self.converter.convert_file(str(perl_file), str(python_file))
        
        # Check that the output file exists
        self.assertTrue(python_file.exists())
        
        # Read the converted Python code
        with open(python_file, 'r', encoding='utf-8') as f:
            python_code = f.read()
        
        # Validate the conversion
        self.assertIn("numbers = [1, 2, 3, 4, 5]", python_code)
        self.assertIn("numbers[0]", python_code)
        self.assertIn("len(numbers) - 1", python_code)
        self.assertIn("numbers.append", python_code)
        self.assertIn("numbers.pop", python_code)
        self.assertIn("numbers.insert(0", python_code)
        self.assertIn("numbers.pop(0)", python_code)
        self.assertIn("person = {", python_code)
        self.assertIn("'name': 'John'", python_code)
        self.assertIn("person['name']", python_code)
        self.assertIn("person['job'] = 'Developer'", python_code)
        self.assertIn("del person['city']", python_code)
        self.assertIn("for key in person.keys():", python_code)
        
        # Print the converted code for inspection
        print("\nConverted hash and array operations code:")
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
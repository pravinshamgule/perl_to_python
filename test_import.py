#!/usr/bin/env python3
"""
Test script to verify that the perl2python package can be imported and used.
"""

try:
    # Try importing the package
    import perl2python
    print(f"Successfully imported perl2python version {perl2python.__version__}")
    
    # Try importing specific modules
    from perl2python import converter
    print("Successfully imported perl2python.converter module")
    
    from perl2python import cli
    print("Successfully imported perl2python.cli module")
    
    # Try creating a converter instance
    converter_instance = converter.PerlToPythonConverter()
    print("Successfully created a PerlToPythonConverter instance")
    
    print("All imports and basic functionality tests passed!")
except Exception as e:
    print(f"Error: {e}")
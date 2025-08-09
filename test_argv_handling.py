#!/usr/bin/env python3
"""
Test script to verify that the generated Python code correctly handles command-line arguments.
"""

import sys
import subprocess

def test_with_args():
    """Test with command-line arguments."""
    print("Testing with command-line arguments...")
    result = subprocess.run(
        ["python", "output/add_numbers_argv_test.py", "10", "20"],
        capture_output=True,
        text=True
    )
    print(f"Output: {result.stdout}")
    print(f"Error: {result.stderr}")
    print(f"Return code: {result.returncode}")
    print()

def test_without_args():
    """Test without command-line arguments (interactive mode)."""
    print("Testing without command-line arguments (interactive mode)...")
    print("This will prompt for input, so we'll simulate it with a subprocess.")
    # Create a process with input for the prompts
    result = subprocess.run(
        ["python", "output/add_numbers_argv_test.py"],
        input="30\n40\n",
        capture_output=True,
        text=True
    )
    print(f"Output: {result.stdout}")
    print(f"Error: {result.stderr}")
    print(f"Return code: {result.returncode}")
    print()

def main():
    """Main function."""
    # First, fix the looks_like_number function in the generated code
    print("Fixing the looks_like_number function in the generated code...")
    with open("output/add_numbers_argv_test.py", "r") as f:
        code = f.read()
    
    # Add a simple implementation of looks_like_number
    code = code.replace(
        "# TODO: Import equivalent for Perl module 'Scalar::Util'",
        "# Implementation of Perl's looks_like_number function\n"
        "def looks_like_number(s):\n"
        "    try:\n"
        "        float(s)\n"
        "        return True\n"
        "    except (ValueError, TypeError):\n"
        "        return False"
    )
    
    with open("output/add_numbers_argv_test.py", "w") as f:
        f.write(code)
    
    print("Fixed the looks_like_number function.")
    print()
    
    # Run the tests
    test_with_args()
    test_without_args()

if __name__ == "__main__":
    main()
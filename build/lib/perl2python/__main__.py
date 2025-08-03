#!/usr/bin/env python3
"""
Main entry point for the Perl to Python Conversion Agent.

This module allows running the converter as a module:
    python -m perl2python [arguments]
"""

import sys
from perl2python.cli import main

if __name__ == '__main__':
    sys.exit(main())
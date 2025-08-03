#!/usr/bin/env python3
"""
Setup script for the Perl to Python Conversion Agent.
"""

from setuptools import setup, find_packages
import os
import re

# Read the version from __init__.py
with open(os.path.join('src', 'perl2python', '__init__.py'), 'r', encoding='utf-8') as f:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string in __init__.py")

# Read the long description from README.md
with open('docs/README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='perl2python',
    version=version,
    description='An AI-powered tool for converting Perl code to Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Perl to Python Conversion Agent',
    author_email='example@example.com',
    url='https://github.com/yourusername/perl2python',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6',
    install_requires=[
        'typing;python_version<"3.7"',
    ],
    entry_points={
        'console_scripts': [
            'perl2python=perl2python.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='perl, python, conversion, migration, code generation',
    project_urls={
        'Documentation': 'https://github.com/yourusername/perl2python/tree/main/docs',
        'Source': 'https://github.com/yourusername/perl2python',
        'Tracker': 'https://github.com/yourusername/perl2python/issues',
    },
)
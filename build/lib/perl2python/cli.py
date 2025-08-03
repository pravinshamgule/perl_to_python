#!/usr/bin/env python3
"""
Perl to Python Converter CLI
============================

Command-line interface for the Perl to Python conversion agent.
"""

import os
import sys
import argparse
import logging
import json
from typing import Dict, List, Optional
from datetime import datetime

from perl2python.converter import PerlToPythonConverter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Convert Perl code to Python',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        'input',
        help='Input Perl file or directory containing Perl files'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output Python file or directory (default: derived from input)'
    )
    
    parser.add_argument(
        '-r', '--recursive',
        action='store_true',
        help='Process directories recursively'
    )
    
    parser.add_argument(
        '-c', '--config',
        help='Path to configuration file (JSON format)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '-d', '--debug',
        action='store_true',
        help='Enable debug mode'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without making changes'
    )
    
    parser.add_argument(
        '--version',
        action='store_true',
        help='Show version information and exit'
    )
    
    return parser.parse_args()


def load_config(config_path: Optional[str]) -> Dict:
    """
    Load configuration from a JSON file.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Configuration dictionary
    """
    config = {}
    
    if config_path:
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            logger.info(f"Loaded configuration from {config_path}")
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            sys.exit(1)
    
    return config


def process_file(perl_file: str, output_file: Optional[str], config: Dict, dry_run: bool) -> bool:
    """
    Process a single Perl file.
    
    Args:
        perl_file: Path to the Perl file
        output_file: Path to the output Python file
        config: Configuration dictionary
        dry_run: If True, don't actually write the output file
        
    Returns:
        True if successful, False otherwise
    """
    if not output_file:
        # Derive output file name from input file
        base_name = os.path.splitext(perl_file)[0]
        output_file = f"{base_name}.py"
    
    try:
        logger.info(f"Converting {perl_file} to {output_file}")
        
        if dry_run:
            logger.info(f"[DRY RUN] Would convert {perl_file} to {output_file}")
            return True
        
        # Set conversion date environment variable for the header
        os.environ['CONVERSION_DATE'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Create converter and convert the file
        converter = PerlToPythonConverter(config)
        converter.convert_file(perl_file, output_file)
        
        logger.info(f"Successfully converted {perl_file} to {output_file}")
        return True
    
    except Exception as e:
        logger.error(f"Error converting {perl_file}: {e}")
        return False


def process_directory(perl_dir: str, output_dir: Optional[str], config: Dict, 
                     recursive: bool, dry_run: bool) -> Dict:
    """
    Process a directory containing Perl files.
    
    Args:
        perl_dir: Path to the directory containing Perl files
        output_dir: Path to the output directory
        config: Configuration dictionary
        recursive: If True, process subdirectories recursively
        dry_run: If True, don't actually write the output files
        
    Returns:
        Dictionary with success and failure counts
    """
    if not output_dir:
        # Use the same directory structure for output
        output_dir = perl_dir
    
    # Create output directory if it doesn't exist
    if not dry_run and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    results = {'success': 0, 'failure': 0}
    
    for item in os.listdir(perl_dir):
        item_path = os.path.join(perl_dir, item)
        
        # Process subdirectories if recursive flag is set
        if os.path.isdir(item_path) and recursive:
            output_subdir = os.path.join(output_dir, item)
            subdir_results = process_directory(item_path, output_subdir, config, recursive, dry_run)
            results['success'] += subdir_results['success']
            results['failure'] += subdir_results['failure']
        
        # Process Perl files
        elif os.path.isfile(item_path) and item.endswith('.pl'):
            output_file = os.path.join(output_dir, f"{os.path.splitext(item)[0]}.py")
            
            if process_file(item_path, output_file, config, dry_run):
                results['success'] += 1
            else:
                results['failure'] += 1
    
    return results


def main():
    """Main entry point for the CLI."""
    args = parse_arguments()
    
    # Set logging level
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    elif args.verbose:
        logging.getLogger().setLevel(logging.INFO)
    else:
        logging.getLogger().setLevel(logging.WARNING)
    
    # Show version and exit
    if args.version:
        from perl2python import __version__
        print(f"Perl to Python Converter v{__version__}")
        return 0
    
    # Load configuration
    config = load_config(args.config)
    
    # Process input
    input_path = args.input
    output_path = args.output
    
    if os.path.isfile(input_path):
        # Process a single file
        success = process_file(input_path, output_path, config, args.dry_run)
        return 0 if success else 1
    
    elif os.path.isdir(input_path):
        # Process a directory
        results = process_directory(input_path, output_path, config, args.recursive, args.dry_run)
        
        logger.info(f"Conversion complete: {results['success']} successful, {results['failure']} failed")
        
        return 0 if results['failure'] == 0 else 1
    
    else:
        logger.error(f"Input path does not exist: {input_path}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
"""
Perl to Python Converter
========================

This module provides the core functionality for converting Perl code to Python.
"""

import re
import os
import sys
import logging
from typing import Dict, List, Optional, Tuple, Union

# Add the project root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
try:
    from post_process import post_process_python_code
    POST_PROCESS_AVAILABLE = True
except ImportError:
    POST_PROCESS_AVAILABLE = False
    logging.warning("post_process module not found. Post-processing will be skipped.")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PerlToPythonConverter:
    """
    Main class for converting Perl code to Python.
    
    This class handles the parsing of Perl code and generation of equivalent Python code.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the converter with optional configuration.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.perl_builtins_map = self._initialize_perl_builtins_map()
        logger.info("PerlToPythonConverter initialized")
    
    def _initialize_perl_builtins_map(self) -> Dict[str, str]:
        """
        Initialize the mapping of Perl built-in functions to Python equivalents.
        
        Returns:
            Dictionary mapping Perl functions to Python equivalents
        """
        return {
            # Basic I/O
            'print': 'print',
            'say': 'print',
            'printf': 'print(f-string)',
            'sprintf': 'f-string',
            'readline': 'input',
            'getc': 'sys.stdin.read(1)',
            'eof': 'not sys.stdin.readable()',
            
            # String manipulation
            'chomp': 'str.rstrip',
            'chop': 'str[:-1]',
            'length': 'len',
            'substr': 'str[start:end]',
            'index': 'str.find',
            'rindex': 'str.rfind',
            'split': 'str.split',
            'join': 'str.join',
            'uc': 'str.upper',
            'lc': 'str.lower',
            'ucfirst': 'str.capitalize',
            'lcfirst': 'lambda s: s[0].lower() + s[1:] if s else s',
            'quotemeta': 're.escape',
            'reverse': 'reversed',
            'pack': 'struct.pack',
            'unpack': 'struct.unpack',
            
            # Array/list operations
            'push': 'list.append or list.extend',
            'pop': 'list.pop',
            'shift': 'list.pop(0)',
            'unshift': 'list.insert(0, item)',
            'splice': 'list[start:end] = new_items',
            'sort': 'sorted',
            'map': 'map or list comprehension',
            'grep': 'filter or list comprehension',
            'foreach': 'for item in iterable',
            'for': 'for item in iterable',
            'while': 'while condition',
            'until': 'while not condition',
            
            # Hash/dictionary operations
            'keys': 'dict.keys',
            'values': 'dict.values',
            'each': 'dict.items',
            'exists': 'key in dict',
            'delete': 'del dict[key]',
            
            # File operations
            'open': 'open',
            'close': 'file.close',
            'read': 'file.read',
            'write': 'file.write',
            'seek': 'file.seek',
            'tell': 'file.tell',
            'binmode': '# Python handles binary mode with "b" flag in open',
            'chmod': 'os.chmod',
            'chown': 'os.chown',
            'mkdir': 'os.mkdir',
            'rmdir': 'os.rmdir',
            'unlink': 'os.unlink or os.remove',
            'rename': 'os.rename',
            
            # Type checking and conversion
            'defined': 'is not None',
            'undef': 'None',
            'scalar': 'len',
            'ref': 'type',
            'bless': '# Use Python classes instead',
            'int': 'int',
            'hex': 'hex',
            'oct': 'oct',
            'chr': 'chr',
            'ord': 'ord',
            'looks_like_number': 'looks_like_number',  # Custom implementation
            
            # Error handling
            'die': 'raise Exception',
            'warn': 'warnings.warn',
            'eval': 'try/except block',
            'try': 'try',
            'catch': 'except',
            
            # Module handling
            'require': 'import',
            'use': 'import',
            'package': 'class',
            'sub': 'def',
            
            # System operations
            'system': 'os.system or subprocess.run',
            'exec': 'os.execv',
            'fork': 'os.fork',
            'wait': 'os.wait',
            'exit': 'sys.exit',
            'getpid': 'os.getpid',
            'getppid': 'os.getppid',
            'getpgrp': 'os.getpgrp',
            'setpgrp': 'os.setpgrp',
            
            # Time operations
            'time': 'time.time',
            'localtime': 'time.localtime',
            'gmtime': 'time.gmtime',
            'sleep': 'time.sleep',
            'alarm': 'signal.alarm',
            
            # Math operations
            'rand': 'random.random',
            'srand': 'random.seed',
            'sin': 'math.sin',
            'cos': 'math.cos',
            'tan': 'math.tan',
            'exp': 'math.exp',
            'log': 'math.log',
            'sqrt': 'math.sqrt',
            'abs': 'abs',
            
            # Regular expressions
            'm/': 're.search',
            's/': 're.sub',
            'tr/': 'str.translate',
            'qr/': 're.compile',
        }
    
    def convert_file(self, perl_file_path: str, output_file_path: Optional[str] = None) -> str:
        """
        Convert a Perl file to Python.
        
        Args:
            perl_file_path: Path to the Perl file to convert
            output_file_path: Optional path to save the converted Python code
            
        Returns:
            The converted Python code as a string
        """
        if not os.path.exists(perl_file_path):
            raise FileNotFoundError(f"Perl file not found: {perl_file_path}")
        
        logger.info(f"Converting Perl file: {perl_file_path}")
        
        with open(perl_file_path, 'r', encoding='utf-8') as f:
            perl_code = f.read()
        
        python_code = self.convert_code(perl_code)
        
        if output_file_path:
            os.makedirs(os.path.dirname(os.path.abspath(output_file_path)), exist_ok=True)
            with open(output_file_path, 'w', encoding='utf-8') as f:
                f.write(python_code)
            logger.info(f"Converted Python code saved to: {output_file_path}")
        
        return python_code
    
    def convert_code(self, perl_code: str) -> str:
        """
        Convert Perl code string to Python code.
        
        Args:
            perl_code: Perl code as a string
            
        Returns:
            Converted Python code as a string
        """
        logger.info("Starting code conversion")
        
        # Preprocessing
        preprocessed_code = self._preprocess_perl_code(perl_code)
        
        # Parse the Perl code
        parsed_elements = self._parse_perl_code(preprocessed_code)
        
        # Generate Python code
        python_code = self._generate_python_code(parsed_elements)
        
        # Postprocessing
        final_code = self._postprocess_python_code(python_code)
        
        logger.info("Code conversion completed")
        return final_code
    
    def _preprocess_perl_code(self, perl_code: str) -> str:
        """
        Preprocess Perl code before parsing.
        
        Args:
            perl_code: Raw Perl code
            
        Returns:
            Preprocessed Perl code
        """
        # Remove Perl POD documentation
        perl_code = re.sub(r'=pod.*?=cut', '', perl_code, flags=re.DOTALL)
        
        # Handle line continuations
        perl_code = re.sub(r'\\\n\s*', ' ', perl_code)
        
        return perl_code
    
    def _parse_perl_code(self, perl_code: str) -> List[Dict]:
        """
        Parse Perl code into a structured representation.
        
        Args:
            perl_code: Preprocessed Perl code
            
        Returns:
            List of parsed elements with their types and content
        """
        # This is a placeholder for actual parsing logic
        # In a real implementation, this would use a proper Perl parser
        
        # For now, we'll just do some basic parsing
        elements = []
        
        # Extract package declarations
        package_matches = re.finditer(r'package\s+([A-Za-z0-9:]+)\s*;', perl_code)
        for match in package_matches:
            elements.append({
                'type': 'package',
                'name': match.group(1),
                'start': match.start(),
                'end': match.end()
            })
        
        # Extract use/require statements
        import_matches = re.finditer(r'(use|require)\s+([A-Za-z0-9:]+)(\s+.*?)?;', perl_code)
        for match in import_matches:
            elements.append({
                'type': 'import',
                'import_type': match.group(1),
                'module': match.group(2),
                'args': match.group(3).strip() if match.group(3) else '',
                'start': match.start(),
                'end': match.end()
            })
        
        # Extract subroutine definitions
        sub_matches = re.finditer(r'sub\s+([A-Za-z0-9_]+)\s*(\{)', perl_code)
        for match in sub_matches:
            # Find the matching closing brace (this is a simplification)
            sub_name = match.group(1)
            start_pos = match.end()
            brace_count = 1
            end_pos = start_pos
            
            for i in range(start_pos, len(perl_code)):
                if perl_code[i] == '{':
                    brace_count += 1
                elif perl_code[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end_pos = i + 1
                        break
            
            elements.append({
                'type': 'subroutine',
                'name': sub_name,
                'body': perl_code[start_pos:end_pos-1],
                'start': match.start(),
                'end': end_pos
            })
        
        # Extract the main script body (code that's not in a subroutine)
        # First, mark all the regions that are part of subroutines, packages, or imports
        used_regions = []
        for element in elements:
            used_regions.append((element['start'], element['end']))
        
        # Sort the used regions by start position
        used_regions.sort()
        
        # Find the unused regions (main script body)
        main_script_parts = []
        last_end = 0
        
        for start, end in used_regions:
            if start > last_end:
                # There's a gap between the last element and this one
                main_script_parts.append(perl_code[last_end:start])
            last_end = end
        
        # Add any code after the last element
        if last_end < len(perl_code):
            main_script_parts.append(perl_code[last_end:])
        
        # Join the main script parts and add as a main_script element
        main_script = ''.join(main_script_parts).strip()
        if main_script:
            elements.append({
                'type': 'main_script',
                'body': main_script,
                'start': -1,  # Use -1 to indicate it's not a specific position
                'end': -1
            })
        
        # Sort elements by their position in the code
        elements.sort(key=lambda x: x['start'])
        
        return elements
    
    def _generate_python_code(self, parsed_elements: List[Dict]) -> str:
        """
        Generate Python code from parsed Perl elements.
        
        Args:
            parsed_elements: List of parsed Perl code elements
            
        Returns:
            Generated Python code
        """
        python_code = [
            "#!/usr/bin/env python3",
            "# -*- coding: utf-8 -*-",
            "# Generated by Perl to Python Converter",
            ""
        ]
        
        # Process imports
        imports = set()
        for element in parsed_elements:
            if element['type'] == 'import':
                module = element['module']
                if module in ['strict', 'warnings']:
                    continue  # These are Perl-specific and don't need Python equivalents
                
                # Convert common Perl modules to Python equivalents
                if module == 'Data::Dumper':
                    imports.add('import pprint')
                elif module == 'Getopt::Long':
                    imports.add('import argparse')
                elif module == 'File::Basename':
                    imports.add('import os.path')
                elif module == 'Time::Local':
                    imports.add('import time')
                elif module == 'JSON':
                    imports.add('import json')
                else:
                    # For other modules, just add a comment
                    imports.add(f"# TODO: Import equivalent for Perl module '{module}'")
        
        # Add imports to the code
        python_code.extend(sorted(imports))
        python_code.append("")
        
        # Process package declarations
        for element in parsed_elements:
            if element['type'] == 'package':
                python_code.append(f"# Perl package: {element['name']}")
                python_code.append(f"# In Python, we use modules instead of packages")
                python_code.append("")
        
        # Process subroutines
        for element in parsed_elements:
            if element['type'] == 'subroutine':
                # Check if the subroutine uses @_ for parameters
                has_params = re.search(r'\@_|\$_\[\d+\]', element['body']) is not None
                
                # Extract parameter names if possible
                param_names = []
                
                # Look for common parameter extraction patterns
                # Pattern 1: my ($param1, $param2) = @_;
                tuple_assign = re.search(r'my\s*\(\s*\$([\w,\s$]+)\s*\)\s*=\s*\@_;', element['body'])
                if tuple_assign:
                    # Extract parameter names from the tuple assignment
                    param_str = tuple_assign.group(1)
                    param_names = [p.strip().lstrip('$') for p in param_str.split(',')]
                    # Remove the tuple assignment from the body
                    element['body'] = re.sub(r'my\s*\(\s*\$([\w,\s$]+)\s*\)\s*=\s*\@_\s*;?\n?', '', element['body'])
                else:
                    # Pattern 2: my $param1 = $_[0]; my $param2 = $_[1]; etc.
                    param_assignments = re.findall(r'my\s+\$(\w+)\s*=\s*\$_\[(\d+)\]', element['body'])
                    if param_assignments:
                        # Sort by index to maintain order
                        param_assignments.sort(key=lambda x: int(x[1]))
                        param_names = [name for name, _ in param_assignments]
                        # Remove the parameter assignments from the body
                        body = element['body']
                        for name, idx in param_assignments:
                            body = re.sub(r'my\s+\$' + name + r'\s*=\s*\$_\[' + idx + r'\]\s*;?\n?', '', body)
                        element['body'] = body
                
                # If we found explicit parameter assignments, use those names
                if param_names:
                    python_code.append(f"def {element['name']}({', '.join(param_names)}):")
                    # Replace @_ with args in the body if it's still used
                    element['body'] = re.sub(r'\@_', r'args', element['body'])
                    element['body'] = re.sub(r'\$_\[(\d+)\]', r'args[\1]', element['body'])
                # Otherwise, if it uses @_ but we couldn't determine names, use *args
                elif has_params:
                    python_code.append(f"def {element['name']}(*args):")
                else:
                    python_code.append(f"def {element['name']}():")
                
                # Convert the subroutine body
                body_lines = self._convert_perl_body_to_python(element['body'])
                
                # If the body is empty, add a pass statement
                if not body_lines:
                    python_code.append("    pass")
                else:
                    python_code.extend([f"    {line}" for line in body_lines])
                
                python_code.append("")
        
        # Find main script element
        main_script_element = None
        for element in parsed_elements:
            if element['type'] == 'main_script':
                main_script_element = element
                break
        
        # Add main guard with the main script body
        python_code.append("if __name__ == '__main__':")
        
        if main_script_element:
            # Convert the main script body
            main_script_lines = self._convert_perl_body_to_python(main_script_element['body'])
            
            # If the body is empty, add a pass statement
            if not main_script_lines:
                python_code.append("    pass")
            else:
                python_code.extend([f"    {line}" for line in main_script_lines])
        else:
            # No main script body found
            python_code.append("    # No main script code found in the Perl file")
            python_code.append("    pass")
        
        return "\n".join(python_code)
    
    def _convert_perl_body_to_python(self, perl_body: str) -> List[str]:
        """
        Convert Perl subroutine body to Python code.
        
        Args:
            perl_body: Perl subroutine body
            
        Returns:
            List of Python code lines
        """
        # Parse and convert the Perl code
        lines = []
        
        # Check if the Perl code has error handling
        has_error_handling = self._has_perl_error_handling(perl_body)
        
        # Convert the Perl code to Python
        python_lines = self._basic_perl_to_python_conversion(perl_body)
        
        # Check if we should add exception handling
        add_exception_handling = self.config.get('options', {}).get('add_exception_handling', True)
        
        # Add exception handling if not present in the original code and not disabled in config
        if not has_error_handling and add_exception_handling:
            lines.append("try:")
            # Indent the converted code
            for line in python_lines:
                lines.append(f"    {line}")
            
            # Add except blocks
            lines.append("except ValueError as e:")
            lines.append("    print(f\"Value Error: {e}\")")
            lines.append("    raise")
            lines.append("except FileNotFoundError as e:")
            lines.append("    print(f\"File Error: {e}\")")
            lines.append("    raise")
            lines.append("except Exception as e:")
            lines.append("    print(f\"Error: {e}\")")
            lines.append("    raise")
        else:
            # If error handling is already present or disabled, just use the converted code
            lines.extend(python_lines)
        
        return lines
        
    def _has_perl_error_handling(self, perl_body: str) -> bool:
        """
        Check if the Perl code has error handling.
        
        Args:
            perl_body: Perl subroutine body
            
        Returns:
            True if the code has error handling, False otherwise
        """
        # Check for common Perl error handling patterns
        error_patterns = [
            r'\bdie\b',           # die statements
            r'\bcroak\b',         # croak statements
            r'\bconfess\b',       # confess statements
            r'\beval\s*\{',       # eval blocks
            r'\btry\s*\{',        # try blocks (from Try::Tiny)
            r'\bwarn\b',          # warn statements
            r'\bor\s+die\b',      # or die pattern
            r'\bunless.*?die\b',  # unless with die
            r'\bif.*?die\b',      # if with die
            r'die\s+"[^"]+"',     # die with string literal
            r'die\s+\'[^\']+\'',  # die with string literal (single quotes)
            r'die\s+\$\w+',       # die with variable
            r'die\s+\w+\(',       # die with function call
            r'or\s+die',          # or die pattern (without whitespace)
            r'\|\|\s+die'         # || die pattern
        ]
        
        for pattern in error_patterns:
            if re.search(pattern, perl_body, re.DOTALL):
                logger.debug(f"Found error handling pattern: {pattern}")
                return True
                
        return False
        
    def _basic_perl_to_python_conversion(self, perl_body: str) -> List[str]:
        """
        Perform basic conversion of Perl code to Python.
        
        Args:
            perl_body: Perl subroutine body
            
        Returns:
            List of Python code lines
        """
        lines = []
        
        # Remove shebang line and use/require statements (already handled elsewhere)
        perl_body = re.sub(r'^#!.*?\n', '', perl_body)
        perl_body = re.sub(r'use\s+[^;]+;', '', perl_body)
        perl_body = re.sub(r'require\s+[^;]+;', '', perl_body)
        
        # Add necessary imports based on functions and variables used
        imports = []
        
        # Add import for sys if @ARGV, $0, or other sys-related variables are used
        if '@ARGV' in perl_body or '$0' in perl_body or 'getc' in perl_body or 'eof' in perl_body or 'exit' in perl_body:
            imports.append('import sys')
            
        # Add import for os and errno if $!, $?, or other OS-related variables are used
        if '$!' in perl_body or '$?' in perl_body or re.search(r'(?:chmod|chown|mkdir|rmdir|unlink|rename|system|exec|fork|wait|getpid|getppid|getpgrp|setpgrp)\b', perl_body):
            imports.append('import os')
            imports.append('import errno')
            
        # Add import for random if rand or srand is used
        if re.search(r'(?:rand|srand)\b', perl_body):
            imports.append('import random')
            
        # Add import for time if time functions are used
        if re.search(r'(?:time|localtime|gmtime|sleep)\b', perl_body):
            imports.append('import time')
            
        # Add import for re if regex operations are used
        if re.search(r'(?:m\/|s\/|tr\/|qr\/|quotemeta)\b', perl_body) or '=~' in perl_body or '!~' in perl_body:
            imports.append('import re')
            
        # Add import for math if math functions are used
        if re.search(r'(?:sin|cos|tan|exp|log|sqrt)\b', perl_body):
            imports.append('import math')
            
        # Add import for struct if pack/unpack is used
        if re.search(r'(?:pack|unpack)\b', perl_body):
            imports.append('import struct')
            
        # Add import for signal if alarm is used
        if 'alarm' in perl_body:
            imports.append('import signal')
            
        # Add import for warnings if warn is used
        if 'warn' in perl_body:
            imports.append('import warnings')
            
        # Add the imports to the beginning of the code
        if imports:
            lines.extend(sorted(imports))
            lines.append('')
        
        # Process the Perl code line by line
        current_indent = 0
        indent_stack = []
        
        for line in perl_body.strip().split('\n'):
            # Skip comments and empty lines
            if not line.strip():
                lines.append('')
                continue
                
            if line.strip().startswith('#'):
                lines.append(' ' * current_indent + line.strip())
                continue
                
            # Check for closing braces that decrease indentation
            if line.strip() == '}':
                if indent_stack:
                    current_indent = indent_stack.pop()
                continue
                
            # Convert die statements to raise Exception
            if 'die' in line:
                # Extract the error message
                match = re.search(r'die\s+"([^"]+)"', line)
                if match:
                    error_msg = match.group(1)
                    # Replace Perl variable references with Python format
                    error_msg = re.sub(r'\$(\w+)', r'{\1}', error_msg)
                    lines.append(' ' * current_indent + f'raise Exception(f"{error_msg}")')
                    continue
                    
            # Convert unless statements to if not
            match = re.search(r'unless\s*\((.*?)\)\s*\{', line)
            if match:
                condition = match.group(1)
                
                # Convert variable references first
                condition = re.sub(r'\$(\w+)', r'\1', condition)
                
                # Special handling for defined function in conditions
                condition = re.sub(r'defined\s+(\w+)', r'\1 is not None', condition, count=0)
                condition = re.sub(r'defined\s*\(\s*(\w+)\s*\)', r'\1 is not None', condition, count=0)
                
                # Convert logical operators
                condition = condition.replace('&&', ' and ')
                condition = condition.replace('||', ' or ')
                condition = condition.replace('!', ' not ')
                lines.append(' ' * current_indent + f'if not ({condition}):')
                indent_stack.append(current_indent)
                current_indent += 4
                continue
                
            # Convert if statements
            match = re.search(r'if\s*\((.*?)\)\s*\{', line)
            if match:
                condition = match.group(1)
                # Convert Perl condition to Python
                condition = self._convert_perl_condition(condition)
                lines.append(' ' * current_indent + f'if {condition}:')
                indent_stack.append(current_indent)
                current_indent += 4
                continue
                
            # Convert foreach/for statements
            match = re.search(r'(?:foreach|for)\s+(?:my\s+)?\$(\w+)\s+\((.*?)\)\s*\{', line)
            if match:
                var_name = match.group(1)
                iterable = match.group(2)
                
                # Convert the iterable
                if iterable.startswith('@'):
                    # Array variable
                    iterable = iterable[1:]  # Remove the @ prefix
                elif iterable.startswith('%'):
                    # Hash variable
                    iterable = f"{iterable[1:]}.keys()"  # Remove the % prefix and add .keys()
                elif iterable.strip() == '1..10' or re.match(r'\d+\.\.\d+', iterable.strip()):
                    # Range like 1..10
                    range_match = re.match(r'(\d+)\.\.(\d+)', iterable.strip())
                    if range_match:
                        start = range_match.group(1)
                        end = range_match.group(2)
                        iterable = f"range({start}, {int(end) + 1})"
                
                lines.append(' ' * current_indent + f'for {var_name} in {iterable}:')
                indent_stack.append(current_indent)
                current_indent += 4
                continue
                
            # Convert while statements
            match = re.search(r'while\s*\((.*?)\)\s*\{', line)
            if match:
                condition = match.group(1)
                # Convert Perl condition to Python
                condition = self._convert_perl_condition(condition)
                lines.append(' ' * current_indent + f'while {condition}:')
                indent_stack.append(current_indent)
                current_indent += 4
                continue
                
            # Convert until statements (while not)
            match = re.search(r'until\s*\((.*?)\)\s*\{', line)
            if match:
                condition = match.group(1)
                # Convert Perl condition to Python
                condition = self._convert_perl_condition(condition)
                lines.append(' ' * current_indent + f'while not ({condition}):')
                indent_stack.append(current_indent)
                current_indent += 4
                continue
                
            # Convert variable declarations with tuple assignment
            match = re.search(r'my\s+\(([^)]+)\)\s*=\s*(.+)', line)
            if match:
                variables = match.group(1)
                value = match.group(2).strip()
                # Convert variable references
                variables = re.sub(r'\$(\w+)', r'\1', variables)
                value = re.sub(r'\$(\w+)', r'\1', value)
                # Remove semicolons
                value = value.rstrip(';')
                
                # Special handling for @ARGV assignments
                if value == '@ARGV':
                    # Add a check for enough command-line arguments
                    # This handles the common Perl pattern: my ($var1, $var2) = @ARGV;
                    # It converts to: var1, var2 = sys.argv[1:] if len(sys.argv) > 2 else (None, None)
                    # This ensures that if not enough command-line arguments are provided,
                    # the variables are set to None, which matches Perl's undefined behavior
                    var_count = len(re.findall(r'\w+', variables))
                    # Construct the tuple with None values directly
                    none_tuple = '(' + ', '.join(['None'] * var_count) + ')'
                    lines.append(' ' * current_indent + f'{variables} = sys.argv[1:] if len(sys.argv) > {var_count} else {none_tuple}')
                else:
                    # Handle other assignments normally
                    lines.append(' ' * current_indent + f'{variables} = {value}')
                continue
                
            # Convert variable declarations
            line = re.sub(r'my\s+\$(\w+)\s*=\s*', r'\1 = ', line)
            line = re.sub(r'my\s+\@(\w+)\s*=\s*', r'\1 = []  # Initialize as empty list\n            ', line)
            line = re.sub(r'my\s+\%(\w+)\s*=\s*', r'\1 = {}  # Initialize as empty dictionary\n            ', line)
            
            # Convert array and hash element access
            line = re.sub(r'\$(\w+)\[(\d+|"\w+"|\'[^\']+\'|\$\w+)\]', r'\1[\2]', line)
            line = re.sub(r'\$(\w+)\{(\w+|"\w+"|\'[^\']+\'|\$\w+)\}', r'\1[\2]', line)
            
            # Handle special cases for variable assignments
            if '=' in line and '@ARGV' in line:
                # Handle assignment from @ARGV
                match = re.search(r'(\w+(?:\s*,\s*\w+)*)\s*=\s*\@ARGV', line)
                if match:
                    vars = match.group(1)
                    line = re.sub(r'(\w+(?:\s*,\s*\w+)*)\s*=\s*\@ARGV', r'\1 = sys.argv[1:]', line)
            
            # Convert Perl special variables first (before general variable references)
            line = re.sub(r'\@ARGV', r'sys.argv[1:]', line)
            line = re.sub(r'\@_', r'args', line)  # Function arguments
            line = re.sub(r'\$_', r'item', line)  # Default variable
            line = re.sub(r'\$!', r'os.strerror(errno.errno)', line)  # Error message
            line = re.sub(r'\$\?', r'os.system_exit_code', line)  # Exit code
            line = re.sub(r'\$0', r'sys.argv[0]', line)  # Script name
            
            # Convert defined and ref functions
            line = re.sub(r'defined\s+(\$?\w+)', r'\1 is not None', line)
            line = re.sub(r'defined\s*\(\s*(\$?\w+)\s*\)', r'\1 is not None', line)
            line = re.sub(r'!\s*defined\s+(\$?\w+)', r'\1 is None', line)
            line = re.sub(r'!\s*defined\s*\(\s*(\$?\w+)\s*\)', r'\1 is None', line)
            
            # Convert ref function
            line = re.sub(r'ref\s*\(\s*(\$?\w+)\s*\)', r'isinstance(\1, (list, dict, object))', line)
            line = re.sub(r'!\s*ref\s*\(\s*(\$?\w+)\s*\)', r'not isinstance(\1, (list, dict, object))', line)
            
            # Convert our and qw syntax
            line = re.sub(r'our\s+(\$?\@?\%?\w+)', r'\1', line)
            line = re.sub(r'qw\s*\(\s*(.*?)\s*\)', r'[\1]', line)
            
            # Convert regex operations
            # Match operator: $var =~ m/pattern/
            match = re.search(r'(\$\w+)\s*=~\s*m\/([^\/]+)\/([a-z]*)', line)
            if match:
                var = match.group(1).lstrip('$')
                pattern = match.group(2)
                flags = match.group(3)
                
                # Convert flags
                re_flags = []
                if 'i' in flags:
                    re_flags.append('re.IGNORECASE')
                if 'm' in flags:
                    re_flags.append('re.MULTILINE')
                if 's' in flags:
                    re_flags.append('re.DOTALL')
                
                flags_str = ', '.join(re_flags) if re_flags else ''
                
                if flags_str:
                    line = f"re.search(r'{pattern}', {var}, {flags_str})"
                else:
                    line = f"re.search(r'{pattern}', {var})"
                
            # Substitution operator: $var =~ s/pattern/replacement/
            match = re.search(r'(\$\w+)\s*=~\s*s\/([^\/]+)\/([^\/]*)\/([a-z]*)', line)
            if match:
                var = match.group(1).lstrip('$')
                pattern = match.group(2)
                replacement = match.group(3)
                flags = match.group(4)
                
                # Convert flags
                re_flags = []
                if 'i' in flags:
                    re_flags.append('re.IGNORECASE')
                if 'm' in flags:
                    re_flags.append('re.MULTILINE')
                if 's' in flags:
                    re_flags.append('re.DOTALL')
                if 'g' in flags:
                    # Global replacement
                    count = 0
                else:
                    # Single replacement
                    count = 1
                
                flags_str = ', '.join(re_flags) if re_flags else ''
                
                if flags_str:
                    if count == 0:
                        line = f"{var} = re.sub(r'{pattern}', r'{replacement}', {var}, flags={flags_str})"
                    else:
                        line = f"{var} = re.sub(r'{pattern}', r'{replacement}', {var}, count={count}, flags={flags_str})"
                else:
                    if count == 0:
                        line = f"{var} = re.sub(r'{pattern}', r'{replacement}', {var})"
                    else:
                        line = f"{var} = re.sub(r'{pattern}', r'{replacement}', {var}, count={count})"
            
            # Translation operator: $var =~ tr/pattern/replacement/
            match = re.search(r'(\$\w+)\s*=~\s*tr\/([^\/]+)\/([^\/]*)\/([a-z]*)', line)
            if match:
                var = match.group(1).lstrip('$')
                pattern = match.group(2)
                replacement = match.group(3)
                
                # Create a translation table
                line = f"{var} = {var}.translate(str.maketrans('{pattern}', '{replacement}'))"
            
            # Convert variable references
            line = re.sub(r'\$(\w+)', r'\1', line)
            line = re.sub(r'\@(\w+)', r'\1', line)  # Full array reference
            line = re.sub(r'\%(\w+)', r'\1', line)  # Full hash reference
            
            # Convert Perl string concatenation
            line = re.sub(r'\s+\.\s+', r' + ', line)
            
            # Convert Perl hash and array operations
            # $hash{key} -> hash[key]
            line = re.sub(r'(\w+)\{([\'"]?\w+[\'"]?)\}', r'\1[\2]', line)
            
            # @array[index] -> array[index]
            line = re.sub(r'@(\w+)\[(\d+)\]', r'\1[\2]', line)
            
            # $#array (array length - 1) -> len(array) - 1
            line = re.sub(r'\$#(\w+)', r'len(\1) - 1', line)
            
            # Convert Perl print statements
            match = re.search(r'print\s+"([^"]+)"', line)
            if match:
                text = match.group(1)
                # Replace Perl variable references with Python format
                text = re.sub(r'\$(\w+)', r'{\1}', text)
                # Handle newlines properly
                text = text.replace('\\n', '\\n')
                
                # Fix variable names that aren't prefixed with $ in the original
                # Look for words that match variable names in the current scope
                for var_name in re.findall(r'\b(\w+)\b', text):
                    if var_name in ['and', 'or', 'not', 'is', 'in', 'for', 'while', 'if', 'else', 'elif', 'try', 'except', 'finally', 'with', 'as', 'def', 'class', 'return', 'yield', 'from', 'import', 'True', 'False', 'None', 'sum']:
                        continue  # Skip Python keywords and built-in functions
                    if re.search(r'\b' + var_name + r'\s*=', perl_body):  # Check if it's a variable
                        text = re.sub(r'\b' + var_name + r'\b', '{' + var_name + '}', text)
                
                # Special handling for 'sum' which is both a variable and a built-in function
                if 'sum' in text and re.search(r'\bsum\s*=', perl_body):
                    text = text.replace('sum', '{sum}')
                
                lines.append(' ' * current_indent + f'print(f"{text}")')
                continue
                
            # Convert Perl stdin reading with chomp
            match = re.search(r'chomp\s*\(\s*\$?(\w+)\s*=\s*<STDIN>\s*\)', line)
            if match:
                var_name = match.group(1)
                lines.append(' ' * current_indent + f'{var_name} = input().rstrip()')
                continue
                
            # Convert Perl stdin reading
            if '<STDIN>' in line:
                line = line.replace('<STDIN>', 'input()')
                
            # Handle Perl-specific return values
            if line.strip() == '1':
                line = '# Return value from Perl module (not needed in Python)'
                
            # Remove semicolons
            line = line.rstrip(';')
            
            # Convert Perl functions to Python equivalents
            for perl_func, python_func in self.perl_builtins_map.items():
                if perl_func in line:
                    line = line.replace(perl_func, python_func)
            
            # Add the converted line with proper indentation
            lines.append(' ' * current_indent + line)
        
        return lines
        
    def _convert_perl_condition(self, condition: str) -> str:
        """
        Convert a Perl condition to Python.
        
        Args:
            condition: Perl condition
            
        Returns:
            Python condition
        """
        # Convert Perl logical operators
        condition = condition.replace('&&', ' and ')
        condition = condition.replace('||', ' or ')
        condition = condition.replace('!', ' not ')
        
        # Convert Perl equality operators
        condition = condition.replace('eq', '==')
        condition = condition.replace('ne', '!=')
        condition = condition.replace('lt', '<')
        condition = condition.replace('gt', '>')
        condition = condition.replace('le', '<=')
        condition = condition.replace('ge', '>=')
        
        # Convert Perl defined check - handle all occurrences
        condition = re.sub(r'defined\s+\$?(\w+)', r'\1 is not None', condition, count=0)
        # Also handle defined with parentheses
        condition = re.sub(r'defined\s*\(\s*\$?(\w+)\s*\)', r'\1 is not None', condition, count=0)
        
        # Convert variable references
        condition = re.sub(r'\$(\w+)', r'\1', condition)
        
        return condition
    
    def _postprocess_python_code(self, python_code: str) -> str:
        """
        Postprocess the generated Python code.
        
        Args:
            python_code: Generated Python code
            
        Returns:
            Postprocessed Python code
        """
        # Add a header comment
        header = (
            "# This file was automatically converted from Perl to Python\n"
            "# by the Perl to Python Conversion Agent\n"
            f"# Conversion date: {os.environ.get('CONVERSION_DATE', 'unknown')}\n"
            "# Note: This is an automated conversion and may require manual review\n\n"
        )
        
        # Apply the header
        python_code_with_header = header + python_code
        
        # Apply additional post-processing if available
        if POST_PROCESS_AVAILABLE:
            logger.info("Applying post-processing to the generated Python code")
            try:
                return post_process_python_code(python_code_with_header)
            except Exception as e:
                logger.error(f"Error during post-processing: {e}")
                logger.info("Falling back to basic post-processing")
                return python_code_with_header
        else:
            return python_code_with_header


def convert_perl_to_python(perl_file: str, output_file: Optional[str] = None, 
                          config: Optional[Dict] = None) -> str:
    """
    Convenience function to convert a Perl file to Python.
    
    Args:
        perl_file: Path to the Perl file to convert
        output_file: Optional path to save the converted Python code
        config: Optional configuration dictionary
        
    Returns:
        The converted Python code as a string
    """
    converter = PerlToPythonConverter(config)
    return converter.convert_file(perl_file, output_file)
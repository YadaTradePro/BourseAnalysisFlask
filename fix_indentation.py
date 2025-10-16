#!/usr/bin/env python3
import os
import textwrap
from pathlib import Path

def fix_file_indentation(filepath):
    """Remove uniform leading indentation from a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Use textwrap.dedent to remove common leading whitespace
        dedented = textwrap.dedent(content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(dedented)
        
        return True
    except Exception as e:
        print(f"Error fixing {filepath}: {e}")
        return False

def main():
    # Find all Python files except in .pythonlibs and migrations/versions
    python_files = []
    
    for root, dirs, files in os.walk('.'):
        # Skip these directories
        if '.pythonlibs' in root or 'migrations/versions' in root:
            continue
        
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                python_files.append(filepath)
    
    print(f"Found {len(python_files)} Python files to fix")
    
    fixed_count = 0
    for filepath in python_files:
        if fix_file_indentation(filepath):
            fixed_count += 1
            print(f"Fixed: {filepath}")
    
    print(f"\nFixed {fixed_count} files successfully")

if __name__ == "__main__":
    main()

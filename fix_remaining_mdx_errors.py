#!/usr/bin/env python3

import os
import re
import glob

def fix_mdx_errors(file_path):
    """Fix common MDX compilation errors in a file"""
    print(f"Checking: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Fix 1: Remove invalid {{...}} expressions
    content = re.sub(r'\{\{[^}]*\}\}', '', content)
    
    # Fix 2: Fix malformed JSON strings
    content = re.sub(r'\d+\{\d+"[^"]*":[^}]*\d+\}', '', content)
    
    # Fix 3: Clean up extra backslashes in docid references  
    content = re.sub(r'docid\\[^\\]*\\[^\\]*', '', content)
    
    # Fix 4: Remove problematic special characters in table cells
    content = re.sub(r'\|([^|]*)\{[^}]*\}([^|]*)\|', r'|\1\2|', content)
    
    # Fix 5: Fix unclosed code blocks or expressions
    content = re.sub(r'\{[^}]*$', '', content, flags=re.MULTILINE)
    
    # Fix 6: Clean up broken links with special characters
    content = re.sub(r'\]\([^)]*\{[^}]*\}[^)]*\)', ']', content)
    
    # Fix 7: Remove standalone problematic characters
    content = re.sub(r'[{}](?![^`]*`)', '', content)
    
    # Fix 8: Clean up malformed HTML-like tags
    content = re.sub(r'<[^>]*\{[^}]*\}[^>]*>', '', content)
    
    # Fix 9: Fix broken table formatting with long content
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        # If line is extremely long (>1000 chars) and contains table markers, break it
        if len(line) > 1000 and '|' in line:
            # Split long table cells
            parts = line.split('|')
            new_parts = []
            for part in parts:
                if len(part) > 500:
                    # Truncate overly long table cells
                    part = part[:500] + '...'
                new_parts.append(part)
            line = '|'.join(new_parts)
        
        fixed_lines.append(line)
    
    content = '\n'.join(fixed_lines)
    
    # Fix 10: Remove any remaining problematic patterns
    content = re.sub(r'\\{2,}', r'\\', content)  # Fix multiple backslashes
    content = re.sub(r'\n{3,}', '\n\n', content)  # Fix excessive line breaks
    
    # Write back if changed
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed: {file_path}")
        return True
    else:
        print(f"No changes needed: {file_path}")
        return False

def main():
    """Fix MDX errors in all documentation files"""
    print("Fixing MDX compilation errors...")
    
    # Find all .md files in docs directory
    md_files = glob.glob('docs/**/*.md', recursive=True)
    
    fixed_count = 0
    for file_path in md_files:
        if fix_mdx_errors(file_path):
            fixed_count += 1
    
    print(f"\nFixed {fixed_count} files")
    print("MDX error fixing completed!")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3

import os
import re
import glob

def clean_title(title):
    """Clean up the title format"""
    # Remove "Title: " prefix and " - Help Center" suffix
    title = re.sub(r'^Title:\s*', '', title)
    title = re.sub(r'\s*-\s*Help Center$', '', title)
    title = title.strip('"').strip()
    return title

def clean_content(content):
    """Clean up the content by removing website elements"""
    lines = content.split('\n')
    cleaned_lines = []
    skip_section = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Skip certain sections entirely
        if any(marker in line for marker in [
            '[![Image', 'Website logo', 'Make Help Center', 'Apps Documentation',
            'Navigate through spaces', '⌘K', 'Docs powered by Archbee',
            'Get started', 'Key concepts', 'Explore more', 'Developers',
            'Error handling', 'Your organization', 'Your profile', 'Release notes',
            'TABLE OF CONTENTS', 'With cookies we can ensure', 'Privacy Preference Center',
            'Manage Consent Preferences', 'Cookie List', 'Powered by Onetrust',
            'Updated', 'Did this page help you?', 'Yes', 'No'
        ]):
            i += 1
            continue
            
        # Skip image lines
        if line.strip().startswith('![Image') or 'format=webp' in line:
            i += 1
            continue
            
        # Skip empty navigation sections
        if line.strip() in ['×', '---', '===============']:
            i += 1
            continue
            
        # Skip URL source line
        if line.startswith('URL Source:'):
            i += 1
            continue
            
        # Skip "Markdown Content:" line
        if line.strip() == 'Markdown Content:':
            i += 1
            continue
            
        # Skip certain patterns
        if any(pattern in line for pattern in [
            'checkbox label label', 'Apply Cancel', 'Consent Leg.Interest',
            'Reject All Confirm My Choices', 'Always Active', 'Clear',
            'More information', 'Allow All'
        ]):
            i += 1
            continue
            
        # Clean up duplicate title sections
        if line.strip() and '=====' in lines[i+1:i+3] if i+1 < len(lines) else False:
            # This might be a duplicate title with underline, skip both
            if any(title_word in line.lower() for title_word in ['learn the basics', 'create your first scenario', 'expand your scenario']):
                i += 2  # Skip title and underline
                continue
        
        # Remove PREVIOUS/NEXT navigation
        if line.startswith('[PREVIOUS') or line.startswith('[NEXT'):
            i += 1
            continue
            
        # Clean up the line
        line = re.sub(r'\[.*?\]\(https://help\.make\.com/[^)]*\)', '', line)  # Remove internal links
        line = re.sub(r'\s+', ' ', line)  # Normalize whitespace
        line = line.strip()
        
        # Only add non-empty lines
        if line:
            cleaned_lines.append(line)
        
        i += 1
    
    return '\n\n'.join(cleaned_lines)

def fix_frontmatter(content):
    """Fix the frontmatter of a markdown file"""
    if not content.startswith('---'):
        return content
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        return content
    
    frontmatter = parts[1].strip()
    body = parts[2].strip()
    
    # Extract and clean title
    title_match = re.search(r'title:\s*["\']?([^"\'\n]+)["\']?', frontmatter)
    if title_match:
        old_title = title_match.group(1)
        new_title = clean_title(old_title)
        frontmatter = re.sub(r'title:\s*["\']?[^"\'\n]+["\']?', f'title: "{new_title}"', frontmatter)
    
    # Clean the body content
    clean_body = clean_content(body)
    
    # Extract the main title from the cleaned content for the markdown
    first_line = clean_body.split('\n')[0] if clean_body else ""
    if first_line.startswith('#'):
        # If first line is already a header, use it
        main_title = first_line[1:].strip()
    else:
        # Use the title from frontmatter
        main_title = new_title if title_match else "Documentation"
    
    # Remove duplicate title from body if it exists
    if clean_body.startswith(f"# {main_title}"):
        clean_body = '\n'.join(clean_body.split('\n')[1:]).strip()
    
    # Construct the final content
    final_content = f"""---
{frontmatter}
---

# {main_title}

{clean_body}"""
    
    return final_content

def fix_file(file_path):
    """Fix a single markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        fixed_content = fix_frontmatter(content)
        
        if fixed_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print(f"Fixed: {file_path}")
            return True
        else:
            print(f"No changes needed: {file_path}")
            return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Fix display issues in all get-started markdown files"""
    print("Fixing content display issues in get-started directory...")
    print("=" * 60)
    
    # Find all markdown files in get-started directory
    md_files = glob.glob('docs/get-started/**/*.md', recursive=True)
    
    fixed_count = 0
    for file_path in md_files:
        if fix_file(file_path):
            fixed_count += 1
    
    print(f"\nFixed {fixed_count} files")
    print("Content display fixes completed!")
    print("\nChanges made:")
    print("- Cleaned up titles (removed 'Title:' and '- Help Center')")
    print("- Removed website navigation elements")
    print("- Removed images and HTML elements")
    print("- Removed cookie consent and footer content")
    print("- Cleaned up duplicate titles")
    print("- Improved overall formatting")

if __name__ == "__main__":
    main() 
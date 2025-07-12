#!/usr/bin/env python3

import os
import re

def clean_content(content):
    """Clean up extracted content by removing navigation and extra elements"""
    lines = content.split('\n')
    cleaned_lines = []
    
    # Skip patterns for navigation and extra content
    skip_patterns = [
        'Help Center', 'Get started', 'Create your first scenario', 'Expand your scenario',
        'Learn the basics', '-------------------------', '=============',
        'Press space bar to start a drag', 'When dragging you can use',
        'Some screen readers may require', 'focus mode or to use your pass through key',
        'Step 1.', 'Step 2.', 'Step 3.', 'Step 4.', 'Step 5.', 'Step 6.', 'Step 7.', 'Step 8.', 'Step 9.', 'Step 10.'
    ]
    
    in_frontmatter = False
    frontmatter_end_count = 0
    main_content_started = False
    
    for line in lines:
        line_stripped = line.strip()
        
        # Handle frontmatter
        if line_stripped == '---':
            if not in_frontmatter:
                in_frontmatter = True
                cleaned_lines.append(line)
                continue
            else:
                frontmatter_end_count += 1
                cleaned_lines.append(line)
                if frontmatter_end_count >= 2:
                    in_frontmatter = False
                continue
        
        if in_frontmatter:
            cleaned_lines.append(line)
            continue
        
        # Skip empty lines before main content starts
        if not main_content_started and not line_stripped:
            continue
            
        # Skip navigation breadcrumbs and headers
        if any(skip in line_stripped for skip in skip_patterns):
            continue
            
        # Start main content when we see the main title (starts with #)
        if line_stripped.startswith('# ') and not main_content_started:
            main_content_started = True
            cleaned_lines.append(line)
            continue
            
        # If main content has started, include everything except skip patterns
        if main_content_started:
            # Skip repeated section headers that are just navigation
            if line_stripped and not line_stripped.startswith('#') and len(line_stripped.split()) <= 5:
                # Check if this line is repeated content
                if any(existing_line.strip().lower() == line_stripped.lower() for existing_line in cleaned_lines[-10:]):
                    continue
            
            cleaned_lines.append(line)
    
    # Join and clean up
    result = '\n'.join(cleaned_lines)
    
    # Remove excessive blank lines
    result = re.sub(r'\n\s*\n\s*\n', '\n\n', result)
    
    return result.strip()

def process_file(file_path):
    """Process a single file to clean its content"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        cleaned_content = clean_content(content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        
        filename = os.path.basename(file_path)
        print(f"✅ Cleaned: {filename}")
        
    except Exception as e:
        print(f"❌ Error cleaning {file_path}: {e}")

def main():
    """Clean all files in both scenario directories"""
    print("🧹 Cleaning scenario directory files...")
    print("=" * 50)
    
    directories = [
        'docs/get-started/create-your-first-scenario',
        'docs/get-started/expand-your-scenario'
    ]
    
    for directory in directories:
        print(f"\n📁 Cleaning directory: {directory}")
        print("-" * 30)
        
        if os.path.exists(directory):
            for filename in os.listdir(directory):
                if filename.endswith('.md') and filename != 'index.md':  # Skip index files
                    file_path = os.path.join(directory, filename)
                    process_file(file_path)
        else:
            print(f"❌ Directory not found: {directory}")
    
    print(f"\n🎉 Cleaning completed!")
    print("✨ All files have been cleaned of:")
    print("   • Navigation breadcrumbs")
    print("   • Repeated headers")
    print("   • Extra spacing")
    print("   • Accessibility text")

if __name__ == "__main__":
    main() 
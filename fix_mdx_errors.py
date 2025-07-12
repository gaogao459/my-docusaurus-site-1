#!/usr/bin/env python3
"""
Fix MDX compilation errors in crawled Make.com documentation
"""

import os
import re
import json
from pathlib import Path

def fix_mdx_content(content):
    """Fix common MDX issues that cause compilation errors"""
    
    # Fix JavaScript-like expressions that aren't valid
    # Remove {{...}} expressions that are not valid JavaScript
    content = re.sub(r'\{\{[^}]*\}\}', '', content)
    
    # Fix HTML-like tags that aren't properly closed
    # Replace unclosed angle brackets with escaped versions
    content = re.sub(r'<([^/>]+)>', r'`<\1>`', content)
    
    # Remove time estimates and other noise
    content = re.sub(r'\b\d+\s*min\b', '', content)
    
    # Remove common problematic patterns
    problematic_patterns = [
        r'Did this page help you\?',
        r'Press space bar to start.*?',
        r'When dragging you can use.*?',
        r'Always Active Clear.*?',
        r'checkbox label label.*?',
        r'Navigate through spaces.*?',
        r'⌘K',
        r'Docs powered by.*?',
        r'Updated \d+.*?\d+',
        r'PREVIOUS.*?NEXT',
        r'×'
    ]
    
    for pattern in problematic_patterns:
        content = re.sub(pattern, '', content, flags=re.IGNORECASE | re.DOTALL)
    
    # Clean up excessive whitespace
    content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
    content = re.sub(r'[ \t]+', ' ', content)
    
    # Remove lines that are too short or just punctuation
    lines = content.split('\n')
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if len(line) > 5 and not re.match(r'^[^\w]*$', line):
            cleaned_lines.append(line)
    
    content = '\n'.join(cleaned_lines)
    
    return content

def fix_category_json_files():
    """Fix empty or malformed JSON category files"""
    docs_dir = Path("docs")
    
    # Find all _category_.json files
    for json_file in docs_dir.glob("**/_category_.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            if not content:
                # Create default category content based on directory name
                dir_name = json_file.parent.name
                category_name = dir_name.replace('-', ' ').title()
                
                default_config = {
                    "label": category_name,
                    "position": 1,
                    "link": {
                        "type": "generated-index",
                        "description": f"Documentation for {category_name.lower()}"
                    }
                }
                
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(default_config, f, indent=2)
                
                print(f"  ✅ Fixed empty JSON: {json_file}")
                
        except Exception as e:
            print(f"  ❌ Error fixing {json_file}: {e}")

def fix_problematic_files():
    """Fix the specific files mentioned in the error log"""
    
    problematic_files = [
        "docs/get-started/step-3-create-a-scenario-to-send-tasks-to-the-ai-agent.md",
        "docs/misc/certificates-and-keys.md", 
        "docs/misc/data-structures.md",
        "docs/misc/incomplete-executions-retry.md",
        "docs/misc/keys.md",
        "docs/misc/math-variables.md",
        "docs/release-notes/january-16-2024.md",
        "docs/tools/tools.md",
        "docs/your-organization/access-management/google-saml.md"
    ]
    
    for file_path in problematic_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract frontmatter
                parts = content.split('---')
                if len(parts) >= 3:
                    frontmatter = parts[1]
                    body = '---'.join(parts[2:])
                else:
                    frontmatter = ""
                    body = content
                
                # Fix the body content
                fixed_body = fix_mdx_content(body)
                
                # Reconstruct the file
                if frontmatter:
                    fixed_content = f"---{frontmatter}---{fixed_body}"
                else:
                    fixed_content = fixed_body
                
                # Only write if content changed significantly
                if len(fixed_content) > 200:  # Ensure we have substantial content
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(fixed_content)
                    print(f"  ✅ Fixed: {file_path}")
                else:
                    # Content too short, create a simple placeholder
                    filename = os.path.basename(file_path)
                    title = filename.replace('.md', '').replace('-', ' ').title()
                    
                    simple_content = f"""---
sidebar_position: 1
title: {title}
description: {title} documentation
---

# {title}

This page is currently being updated. Please check back later for more information.

For the latest documentation, visit [Make.com Help Center](https://help.make.com/).
"""
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(simple_content)
                    print(f"  ✅ Created placeholder: {file_path}")
                    
            except Exception as e:
                print(f"  ❌ Error fixing {file_path}: {e}")

def remove_duplicate_files():
    """Remove duplicate files that might cause conflicts"""
    docs_dir = Path("docs")
    
    # Remove files with obvious duplicates or conflicts
    for md_file in docs_dir.glob("**/*.md"):
        content_size = md_file.stat().st_size
        
        # Remove very small files (likely incomplete)
        if content_size < 100:
            try:
                md_file.unlink()
                print(f"  🗑️ Removed tiny file: {md_file}")
            except Exception as e:
                print(f"  ❌ Error removing {md_file}: {e}")

def main():
    print("🔧 Fixing MDX compilation errors...")
    print("=" * 60)
    
    # Fix empty JSON files
    print("\n📁 Fixing category JSON files...")
    fix_category_json_files()
    
    # Fix problematic markdown files
    print("\n📝 Fixing problematic markdown files...")
    fix_problematic_files()
    
    # Remove duplicate/tiny files
    print("\n🗑️ Cleaning up duplicate files...")
    remove_duplicate_files()
    
    print("\n✅ MDX error fixing completed!")
    print("🌐 Try restarting Docusaurus now")

if __name__ == "__main__":
    main() 
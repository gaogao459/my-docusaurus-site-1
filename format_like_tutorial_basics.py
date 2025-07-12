#!/usr/bin/env python3

import os
import re
import glob
import json

def extract_meaningful_content(content):
    """Extract only the meaningful content, following tutorial-basics style"""
    lines = content.split('\n')
    meaningful_lines = []
    
    # Skip to actual content
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Skip common website junk
        if any(skip in line for skip in [
            'Help Center', 'Website logo', 'Make Help Center', 'Navigate through spaces',
            'Docs powered by', 'Get started', 'Key concepts', 'Explore more',
            'Error handling', 'Your organization', 'Your profile', 'Release notes',
            'Updated', 'Did this page help you?', 'cookies', 'Privacy Preference',
            'checkbox label', '===============', '---', '×', 'TABLE OF CONTENTS',
            '[](https:', '[![Image', '![Image', 'format=webp'
        ]):
            continue
            
        # Look for actual content starting points
        if any(starter in line.lower() for starter in [
            'welcome to make', 'the best way to understand', 'automation is about',
            'successful automation begins', 'create your first', 'you\'ll create',
            'what you\'ll build', 'what you\'ll need'
        ]):
            # Start collecting from here
            meaningful_lines = lines[i:]
            break
    
    if not meaningful_lines:
        # If no clear starting point, look for the main content
        for i, line in enumerate(lines):
            if line.strip() and not any(skip in line for skip in [
                'Help Center', 'Website logo', 'Navigate', 'Docs powered'
            ]):
                meaningful_lines = lines[i:]
                break
    
    # Clean up the collected lines
    cleaned_lines = []
    for line in meaningful_lines:
        line = line.strip()
        
        # Skip unwanted content
        if any(skip in line for skip in [
            'Help Center', 'Website logo', 'Navigate through spaces', 'Docs powered',
            'Updated', 'Did this page help you?', 'cookies', 'Privacy Preference',
            'checkbox', '===============', 'TABLE OF CONTENTS', '[](https:',
            '[![Image', '![Image', 'format=webp', 'Always Active', 'Apply Cancel'
        ]):
            continue
            
        # Stop at navigation or footer
        if line.startswith('[PREVIOUS') or line.startswith('[NEXT'):
            break
            
        # Clean internal links but keep external ones
        line = re.sub(r'\[([^\]]+)\]\(https://help\.make\.com/[^)]*\)', r'\1', line)
        
        if line:
            cleaned_lines.append(line)
    
    # Join with proper spacing
    content = '\n'.join(cleaned_lines)
    
    # Clean up excessive whitespace
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = content.strip()
    
    return content

def create_tutorial_style_file(file_path):
    """Reformat file in tutorial-basics style"""
    with open(file_path, 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    # Extract current frontmatter
    frontmatter = {}
    body = original_content
    
    if original_content.startswith('---'):
        parts = original_content.split('---', 2)
        if len(parts) >= 3:
            fm_lines = parts[1].strip().split('\n')
            body = parts[2].strip()
            
            for line in fm_lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter[key.strip()] = value.strip().strip('"\'')
    
    # Get clean content
    clean_content = extract_meaningful_content(body)
    
    # Extract title from content or existing frontmatter
    title = "Documentation"
    first_line = clean_content.split('\n')[0] if clean_content else ""
    
    if first_line.startswith('# '):
        title = first_line[2:].strip()
        # Remove title from content since it will be the markdown header
        clean_content = '\n'.join(clean_content.split('\n')[1:]).strip()
    elif 'title' in frontmatter:
        old_title = frontmatter['title']
        if old_title.startswith('Title: '):
            title = old_title[7:]
        elif old_title.endswith(' - Help Center'):
            title = old_title[:-13]
        else:
            title = old_title
    
    # Clean up title
    title = title.strip('"\'').strip()
    if ' - Help Center' in title:
        title = title.split(' - Help Center')[0]
    
    # Create frontmatter preserving title and description
    simple_frontmatter = {}
    
    # Add title (cleaned up)
    simple_frontmatter['title'] = f'"{title}"'
    
    # Add description if exists
    if 'description' in frontmatter:
        simple_frontmatter['description'] = f'"{frontmatter["description"]}"'
    
    # Add sidebar_position
    if 'sidebar_position' in frontmatter:
        simple_frontmatter['sidebar_position'] = frontmatter['sidebar_position']
    else:
        simple_frontmatter['sidebar_position'] = '1'
    
    # Build final content
    fm_lines = []
    for key, value in simple_frontmatter.items():
        fm_lines.append(f'{key}: {value}')
    
    final_content = f"""---
{chr(10).join(fm_lines)}
---

# {title}

{clean_content}"""
    
    return final_content

def update_category_files():
    """Update _category_.json files to match tutorial-basics style"""
    categories = {
        'docs/get-started/_category_.json': {
            "label": "Get Started",
            "position": 1,
            "link": {
                "type": "generated-index",
                "description": "Start your automation journey with Make.com"
            }
        },
        'docs/get-started/learn-the-basics/_category_.json': {
            "label": "Learn the Basics",
            "position": 1,
            "link": {
                "type": "generated-index", 
                "description": "Understand automation fundamentals"
            }
        },
        'docs/get-started/create-your-first-scenario/_category_.json': {
            "label": "Create Your First Scenario",
            "position": 2,
            "link": {
                "type": "generated-index",
                "description": "Step-by-step tutorial for your first automation"
            }
        },
        'docs/get-started/expand-your-scenario/_category_.json': {
            "label": "Expand Your Scenario", 
            "position": 3,
            "link": {
                "type": "generated-index",
                "description": "Advanced techniques for complex automations"
            }
        }
    }
    
    for file_path, config in categories.items():
        if os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            print(f"✅ Updated: {file_path}")

def main():
    """Format all get-started files like tutorial-basics"""
    print("🎯 Formatting get-started files like tutorial-basics...")
    print("=" * 70)
    
    # Update category files first
    print("📁 Updating category files...")
    update_category_files()
    print()
    
    # Process all markdown files
    print("📝 Processing markdown files...")
    md_files = glob.glob('docs/get-started/**/*.md', recursive=True)
    
    fixed_count = 0
    for file_path in md_files:
        try:
            print(f"Processing: {file_path}")
            
            original_content = ""
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            new_content = create_tutorial_style_file(file_path)
            
            if new_content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"✅ Reformatted: {file_path}")
                fixed_count += 1
            else:
                print(f"✅ Already clean: {file_path}")
        except Exception as e:
            print(f"❌ Error: {file_path} - {e}")
    
    print(f"\n🎉 Formatting completed!")
    print(f"📊 Reformatted {fixed_count} out of {len(md_files)} files")
    print("\n✨ Now following tutorial-basics style:")
    print("   • Simple frontmatter (only sidebar_position)")
    print("   • Clean, meaningful content only")
    print("   • Standard markdown formatting")
    print("   • Enhanced category configurations")
    print("   • No website navigation or cookie content")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3

import os
import re
import glob

def extract_clean_title(content):
    """Extract a clean title from the content"""
    lines = content.split('\n')
    
    # Look for meaningful titles in the content
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Skip common website elements
        if any(skip in line.lower() for skip in [
            'help center', 'website logo', 'make help center', 'docs powered',
            'url source', 'markdown content', 'navigate through spaces'
        ]):
            continue
            
        # Look for actual titles
        if line.startswith('# '):
            title = line[2:].strip()
            if title and len(title) < 100:  # Reasonable title length
                return title
        elif line and len(line) < 100 and not line.startswith('['):
            # Might be a title
            if any(keyword in line.lower() for keyword in [
                'learn the basics', 'create your first scenario', 'expand your scenario',
                'step', 'plan', 'get your app', 'set up', 'add', 'test', 'map', 'schedule'
            ]):
                return line
    
    return "Documentation"

def get_clean_content(content):
    """Extract only the meaningful content"""
    lines = content.split('\n')
    content_lines = []
    found_main_content = False
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Skip empty lines at the start
        if not found_main_content and not line:
            continue
            
        # Skip website headers and navigation
        if any(skip in line for skip in [
            '[![Image', 'Website logo', 'Make Help Center', 'Apps Documentation',
            'Navigate through spaces', '⌘K', 'Docs powered by Archbee',
            'URL Source:', 'Markdown Content:', '===============',
            '[](https://archbee-doc-uploads', 'TABLE OF CONTENTS',
            'With cookies we can ensure', 'Privacy Preference Center',
            'Manage Consent Preferences', 'Necessary Cookies', 'Functional Cookies',
            'Marketing Cookies', 'Performance Cookies', 'Cookie List',
            'Always Active', 'Select Cookies Settings', 'Understood',
            'checkbox label', 'Apply Cancel', 'Consent Leg.Interest',
            'Reject All Confirm My Choices', 'Powered by Onetrust'
        ]):
            continue
            
        # Skip images
        if line.startswith('![Image') or 'format=webp' in line:
            continue
            
        # Skip navigation
        if line in ['×', '---'] or line.startswith('[PREVIOUS') or line.startswith('[NEXT'):
            continue
            
        # Skip duplicate titles with underlines
        if line and i+1 < len(lines) and '=====' in lines[i+1]:
            continue
            
        # Skip certain single words that are navigation
        if line in ['Get started', 'Key concepts', 'Explore more', 'Developers', 
                   'Error handling', 'Your organization', 'Your profile', 'Release notes',
                   'Learn the basics', 'Create your first scenario', 'Expand your scenario',
                   'Scenarios & connections', 'Apps & modules', 'Data & mapping', 'Tools',
                   'Resources', 'Scenarios', 'Connections', 'Functions', 'Data stores',
                   'Make AI Agents', 'Introduction to AI agents', 'AI agent best practices',
                   'Manage AI agents', 'Make AI agent reference', 'AI agent use case',
                   'Introduction to errors and warnings', 'How to handle errors',
                   'Error handlers', 'Types of errors', 'Types of warnings',
                   'Exponential backoff', 'Throw', 'Organizations & teams',
                   'Subscription', 'Administration', 'Access management',
                   'Make Managed Services (MMS)', 'Profile settings', 'Make programs',
                   '2025', '2024', '4 min', '2 min']:
            continue
            
        # Skip "Updated" lines
        if line.startswith('Updated ') and ('2024' in line or '2025' in line):
            continue
            
        # Skip feedback lines
        if line in ['Did this page help you?', 'Yes', 'No']:
            continue
            
        # Clean internal links
        line = re.sub(r'\[([^\]]+)\]\(https://help\.make\.com/[^)]*\)', r'\1', line)
        
        # If we have meaningful content, start collecting
        if line and (found_main_content or any(keyword in line.lower() for keyword in [
            'welcome to make', 'the best way to understand', 'automation is about',
            'successful automation', 'you\'ll create', 'what you\'ll build',
            'what you\'ll need', 'step', 'scenario'
        ])):
            found_main_content = True
            content_lines.append(line)
        elif found_main_content and line:
            content_lines.append(line)
    
    return '\n\n'.join(content_lines)

def create_clean_markdown(file_path):
    """Create a completely clean markdown file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract frontmatter
    frontmatter = {}
    body = content
    
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            fm_content = parts[1].strip()
            body = parts[2].strip()
            
            # Parse frontmatter
            for line in fm_content.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter[key.strip()] = value.strip().strip('"\'')
    
    # Get clean title and content
    clean_title = extract_clean_title(body)
    clean_content = get_clean_content(body)
    
    # Clean the title in frontmatter
    if 'title' in frontmatter:
        old_title = frontmatter['title']
        if old_title.startswith('Title: '):
            old_title = old_title[7:]
        if old_title.endswith(' - Help Center'):
            old_title = old_title[:-13]
        frontmatter['title'] = f'"{old_title.strip()}"'
    else:
        frontmatter['title'] = f'"{clean_title}"'
    
    # Ensure sidebar_position exists
    if 'sidebar_position' not in frontmatter:
        frontmatter['sidebar_position'] = '1'
    
    # Build final content
    fm_lines = []
    for key, value in frontmatter.items():
        fm_lines.append(f'{key}: {value}')
    
    final_content = f"""---
{chr(10).join(fm_lines)}
---

# {clean_title}

{clean_content}"""
    
    return final_content

def fix_file_comprehensive(file_path):
    """Comprehensively fix a markdown file"""
    try:
        print(f"Processing: {file_path}")
        
        # Read original content
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Create clean content
        clean_content = create_clean_markdown(file_path)
        
        # Write back if different
        if clean_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(clean_content)
            print(f"✅ Fixed: {file_path}")
            return True
        else:
            print(f"✅ Already clean: {file_path}")
            return False
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False

def main():
    """Comprehensively clean all get-started markdown files"""
    print("🧹 Comprehensive content cleaning for get-started directory...")
    print("=" * 70)
    
    # Find all markdown files in get-started directory
    md_files = glob.glob('docs/get-started/**/*.md', recursive=True)
    
    fixed_count = 0
    for file_path in md_files:
        if fix_file_comprehensive(file_path):
            fixed_count += 1
    
    print(f"\n🎉 Cleaning completed!")
    print(f"📊 Fixed {fixed_count} out of {len(md_files)} files")
    print("\n✨ Improvements made:")
    print("   • Completely removed website navigation elements")
    print("   • Cleaned up all titles and removed 'Help Center' suffixes")
    print("   • Extracted only meaningful content")
    print("   • Removed all cookie consent and footer content")
    print("   • Fixed frontmatter formatting")
    print("   • Ensured proper markdown structure")

if __name__ == "__main__":
    main() 
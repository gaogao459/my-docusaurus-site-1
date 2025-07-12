#!/usr/bin/env python3

import requests
import re

def get_jina_content(url):
    """Get content using Jina.ai"""
    jina_url = f"https://r.jina.ai/{url}"
    try:
        response = requests.get(jina_url, timeout=30)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to get content from {url}: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error getting content from {url}: {e}")
        return None

def clean_extracted_content(raw_content):
    """Clean and format the extracted content"""
    if not raw_content:
        return None
    
    lines = raw_content.split('\n')
    content_lines = []
    skip_patterns = [
        'Website logo', 'Developers Hub', 'Community', 'Academy', 'Customer Care',
        'Make Help Center', 'Apps Documentation', 'Navigate through spaces', '⌘K',
        'Docs powered by Archbee', 'TABLE OF CONTENTS', 'Updated', 'PREVIOUS', 'NEXT',
        'Did this page help you?', 'Yes', 'No', 'Docs powered by', '×',
        'Title:', 'URL Source:', 'Markdown Content:', '===============',
        'Get started', 'Learn the basics', 'Create your first scenario'
    ]
    
    collecting = False
    
    for line in lines:
        line = line.strip()
        
        # Skip navigation and metadata
        if any(skip in line for skip in skip_patterns):
            continue
            
        # Skip single character lines
        if len(line) <= 2:
            continue
            
        # Skip time indicators like "3 min"
        if re.match(r'^\d+\s+min$', line):
            continue
            
        # Start collecting after we see the main title or content
        if not collecting and (
            'Make is a powerful' in line or 
            'API, or Application Programming Interface' in line or
            line.startswith('#') or
            len(line) > 20
        ):
            collecting = True
            
        if collecting:
            # Clean up markdown links and formatting
            line = re.sub(r'\[\]\([^)]*\)', '', line)  # Remove empty links
            line = re.sub(r'\[([^\]]*)\]\([^)]*#[^)]*\)', r'\1', line)  # Remove anchor links
            line = line.strip()
            
            if line:
                content_lines.append(line)
    
    if content_lines:
        content = '\n\n'.join(content_lines)
        
        # Clean up excessive spacing
        content = re.sub(r'\n\n+', '\n\n', content)
        
        return content.strip()
    
    return None

def extract_what_is_make():
    """Extract original What is Make content"""
    print("🌐 Extracting original content from: https://help.make.com/what-is-make")
    
    raw_content = get_jina_content("https://help.make.com/what-is-make")
    content = clean_extracted_content(raw_content)
    
    if content:
        frontmatter = """---
title: "What is Make?"
sidebar_position: 2
---

# What is Make?

"""
        
        full_content = frontmatter + content
        
        with open("docs/get-started/learn-the-basics/what-is-make.md", 'w', encoding='utf-8') as f:
            f.write(full_content)
        print("✅ Extracted original content for: what-is-make.md")
    else:
        print("❌ Failed to extract content for what-is-make.md")

def extract_whats_an_api():
    """Extract original What's an API content"""
    print("🌐 Extracting original content from: https://help.make.com/whats-an-api")
    
    raw_content = get_jina_content("https://help.make.com/whats-an-api")
    content = clean_extracted_content(raw_content)
    
    if content:
        frontmatter = """---
title: "What's an API?"
sidebar_position: 3
---

# What's an API?

"""
        
        full_content = frontmatter + content
        
        with open("docs/get-started/learn-the-basics/whats-an-api.md", 'w', encoding='utf-8') as f:
            f.write(full_content)
        print("✅ Extracted original content for: whats-an-api.md")
    else:
        print("❌ Failed to extract content for whats-an-api.md")

def main():
    """Extract original content from Make.com pages"""
    print("📄 Extracting original content from Make.com...")
    print("=" * 60)
    
    extract_what_is_make()
    print()
    extract_whats_an_api()
    
    print(f"\n🎉 Original content extraction completed!")
    print("✨ Files now contain original Make.com content")

if __name__ == "__main__":
    main() 
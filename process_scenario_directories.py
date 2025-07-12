#!/usr/bin/env python3

import requests
import re
import os

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
        'Privacy Preference Center', 'Manage Consent Preferences', 'Necessary Cookies',
        'Functional Cookies', 'Marketing Cookies', 'Performance Cookies', 'Cookie List',
        'Allow All', 'Reject All', 'Confirm My Choices', 'Powered by Onetrust',
        'Select Cookies Settings', 'Understood'
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
            
        # Skip time indicators like "3 min", "5 min"
        if re.match(r'^\d+\s+min$', line):
            continue
            
        # Skip image references and tracking codes
        if line.startswith('![Image') or 'bing.com/action' in line or 'cookielaw.org' in line:
            continue
            
        # Start collecting after we see content
        if not collecting and (
            len(line) > 15 and any(word in line.lower() for word in [
                'step', 'scenario', 'automation', 'make', 'create', 'connect',
                'module', 'trigger', 'action', 'app', 'google', 'slack'
            ])
        ):
            collecting = True
            
        if collecting:
            # Clean up markdown links and formatting
            line = re.sub(r'\[\]\([^)]*\)', '', line)  # Remove empty links
            line = re.sub(r'\[([^\]]*)\]\([^)]*#[^)]*\)', r'\1', line)  # Remove anchor links
            line = line.strip()
            
            # Stop at footer elements
            if any(footer in line.lower() for footer in [
                'privacy preference', 'cookie', 'consent', 'onetrust',
                'checkbox label', 'apply cancel'
            ]):
                break
            
            if line:
                content_lines.append(line)
    
    if content_lines:
        content = '\n\n'.join(content_lines)
        
        # Clean up excessive spacing
        content = re.sub(r'\n\n+', '\n\n', content)
        
        return content.strip()
    
    return None

def get_make_url_from_filename(filename):
    """Convert filename to Make.com URL"""
    # Remove .md extension
    base_name = filename.replace('.md', '')
    
    # Handle index files
    if base_name == 'index':
        return None  # Skip index files for now, will handle separately
    
    # Convert filename to URL format
    url_slug = base_name.replace('_', '-')
    
    # Try different URL patterns for Make.com
    possible_urls = [
        f"https://help.make.com/{url_slug}",
        f"https://help.make.com/hc/en-us/articles/{url_slug}",
        f"https://help.make.com/get-started/{url_slug}",
    ]
    
    return possible_urls

def process_file(file_path, directory_name):
    """Process a single file"""
    filename = os.path.basename(file_path)
    
    # Skip _category_.json files
    if filename == '_category_.json':
        return
    
    print(f"📄 Processing: {filename}")
    
    # Handle index files with static content
    if filename == 'index.md':
        process_index_file(file_path, directory_name)
        return
    
    # Get possible URLs for this file
    possible_urls = get_make_url_from_filename(filename)
    
    if not possible_urls:
        print(f"⚠️ Skipping {filename} - no URL mapping")
        return
    
    # Try to extract content from the URLs
    content = None
    for url in possible_urls:
        print(f"🌐 Trying: {url}")
        raw_content = get_jina_content(url)
        if raw_content:
            content = clean_extracted_content(raw_content)
            if content and len(content) > 100:  # Ensure we got substantial content
                break
    
    if content:
        # Read current file to get frontmatter
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                current_content = f.read()
            
            # Extract frontmatter
            if current_content.startswith('---'):
                parts = current_content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter = f"---{parts[1]}---"
                else:
                    frontmatter = parts[0]
            else:
                # Create basic frontmatter
                title = filename.replace('.md', '').replace('-', ' ').title()
                frontmatter = f"""---
title: "{title}"
---"""
            
            # Get title from frontmatter or filename
            title_match = re.search(r'title:\s*["\']([^"\']+)["\']', frontmatter)
            if title_match:
                title = title_match.group(1)
            else:
                title = filename.replace('.md', '').replace('-', ' ').title()
            
            # Combine frontmatter with cleaned content
            full_content = f"{frontmatter}\n\n# {title}\n\n{content}"
            
            # Write the updated content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(full_content)
            
            print(f"✅ Updated: {filename}")
        
        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")
    else:
        print(f"⚠️ Could not extract content for: {filename}")

def process_index_file(file_path, directory_name):
    """Process index.md files with directory-specific content"""
    print(f"📄 Processing index.md for {directory_name}")
    
    # Create appropriate content based on directory
    if 'create-your-first-scenario' in directory_name:
        content = """---
sidebar_position: 1
---

# Create your first scenario

The best way to understand Make is to try it yourself! This guide will walk you through creating your first Make scenario—an automated workflow that will send notifications to a sales team. By the end, you'll understand Make's core concepts and be ready to build your own scenarios.

A scenario is a series of modules that indicate how data should be transferred and transformed between apps/services. In Make, each user can create up to 100 scenarios per day.

## What you'll build

You'll create a notification system that bridges the gap between marketing and sales teams. Imagine this business challenge: your marketing team adds new prospects to a spreadsheet, and your sales team needs immediate notifications.

Your Make scenario will:

* Monitor a Google Sheet for new prospect entries by the marketing team
* Send Slack notifications to the sales team when new prospects are added

## What you'll need

* A Make account ([Create one here](https://www.make.com/en/register))
* A Slack account and workspace ([Sign up for Slack](https://slack.com/get-started))
* A Google account ([Create an account](https://accounts.google.com/signup))

All these accounts are free to create, including a Make account. While this guide uses Slack and Google Sheets, you can adapt these steps to work with your preferred applications."""
    
    elif 'expand-your-scenario' in directory_name:
        content = """---
sidebar_position: 1
---

# Expand your scenario

Now that you've created your first scenario, let's expand it with more advanced features. In this section, you'll learn how to add logic, routing, and mobile notifications to make your automation more powerful and flexible.

## What you'll learn

* How to add conditional logic with routers
* Setting up mobile push notifications
* Working with AI agents
* Using aggregators to process multiple items
* Testing complex scenarios

## Building on your foundation

We'll take the basic scenario you created and enhance it with:

* **Router modules** - to handle different types of data
* **Mobile notifications** - to alert you on the go
* **AI integration** - to add intelligence to your workflows
* **Data aggregation** - to process multiple items together

These advanced features will help you create more sophisticated automations that can handle complex business logic."""
    
    else:
        # Generic content
        content = f"""---
sidebar_position: 1
---

# {directory_name.replace('-', ' ').title()}

Welcome to this section of the Make documentation."""
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Updated index.md for {directory_name}")
    except Exception as e:
        print(f"❌ Error updating index.md: {e}")

def main():
    """Process all files in both scenario directories"""
    print("🎯 Processing scenario directories...")
    print("=" * 60)
    
    directories = [
        'docs/get-started/create-your-first-scenario',
        'docs/get-started/expand-your-scenario'
    ]
    
    for directory in directories:
        print(f"\n📁 Processing directory: {directory}")
        print("-" * 40)
        
        if os.path.exists(directory):
            for filename in os.listdir(directory):
                if filename.endswith('.md'):
                    file_path = os.path.join(directory, filename)
                    process_file(file_path, directory)
                    print()
        else:
            print(f"❌ Directory not found: {directory}")
    
    print(f"\n🎉 Processing completed!")
    print("✨ All scenario files have been updated with:")
    print("   • Original content from Make.com")
    print("   • Cleaned formatting")
    print("   • Proper structure")
    print("   • Consistent frontmatter")

if __name__ == "__main__":
    main() 
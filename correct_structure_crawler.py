#!/usr/bin/env python3

import requests
import json
import re
import os
import time
from urllib.parse import urljoin, urlparse
from pathlib import Path

class MakeCorrectStructureCrawler:
    def __init__(self):
        self.base_url = "https://help.make.com"
        self.visited_urls = set()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Exact structure from Make.com website
        self.target_structure = {
            "get-started": [
                "learn-the-basics",
                "create-your-first-scenario", 
                "expand-your-scenario"
            ],
            "key-concepts": [
                "scenarios-connections",
                "apps-modules", 
                "data-mapping",
                "tools",
                "resources"
            ],
            "explore-more": [
                "scenarios",
                "connections", 
                "tools",
                "functions",
                "data-stores"
            ],
            "developers": [
                "make-ai-agents"
            ],
            "error-handling": [
                "introduction-to-errors-and-warnings",
                "how-to-handle-errors",
                "error-handlers", 
                "types-of-errors",
                "types-of-warnings",
                "exponential-backoff",
                "throw"
            ],
            "your-organization": [
                "organizations-teams",
                "subscription",
                "administration", 
                "access-management",
                "make-managed-services-mms"
            ],
            "your-profile": [
                "profile-settings",
                "make-programs"
            ],
            "release-notes": [
                "2025",
                "2024"
            ]
        }

    def get_jina_content(self, url):
        """Get content using Jina.ai"""
        jina_url = f"https://r.jina.ai/{url}"
        try:
            response = self.session.get(jina_url, timeout=30)
            if response.status_code == 200:
                return response.text
            else:
                print(f"Jina failed for {url}: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error getting content for {url}: {e}")
            return None

    def clean_filename(self, text):
        """Clean text for use as filename"""
        # Remove special characters and replace with hyphens
        text = re.sub(r'[^\w\s-]', '', text.lower())
        text = re.sub(r'[\s_]+', '-', text)
        text = text.strip('-')
        return text

    def save_content(self, content, filepath):
        """Save content to file"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Saved: {filepath}")

    def create_category_file(self, category_path, category_name):
        """Create _category_.json file"""
        category_config = {
            "label": category_name.replace('-', ' ').title(),
            "position": 1
        }
        
        category_file = os.path.join(category_path, "_category_.json")
        with open(category_file, 'w', encoding='utf-8') as f:
            json.dump(category_config, f, indent=2)
        print(f"Created category file: {category_file}")

    def extract_title_and_content(self, raw_content):
        """Extract title and clean content"""
        lines = raw_content.strip().split('\n')
        
        # Find the main title (usually the largest heading)
        title = "Documentation"
        content_start = 0
        
        for i, line in enumerate(lines):
            line = line.strip()
            if line.startswith('# ') and len(line) > 2:
                title = line[2:].strip()
                content_start = i + 1
                break
            elif line and not line.startswith('Website') and not line.startswith('http'):
                # If no # title found, use first meaningful line
                title = line
                content_start = i + 1
                break
        
        # Get content after title
        content_lines = lines[content_start:]
        content = '\n'.join(content_lines).strip()
        
        # Clean up the content
        content = re.sub(r'\n{3,}', '\n\n', content)  # Remove excessive line breaks
        content = re.sub(r'^\s*Website.*?\n', '', content, flags=re.MULTILINE)  # Remove website headers
        
        return title, content

    def create_mdx_file(self, title, content, filepath):
        """Create MDX file with proper frontmatter"""
        # Clean title for frontmatter
        clean_title = title.replace('"', '\\"')
        
        mdx_content = f"""---
title: "{clean_title}"
---

# {title}

{content}
"""
        self.save_content(mdx_content, filepath)

    def crawl_section(self, section_name, subsections):
        """Crawl a specific section with its subsections"""
        section_path = f"docs/{section_name}"
        os.makedirs(section_path, exist_ok=True)
        
        # Create category file
        self.create_category_file(section_path, section_name)
        
        # Crawl each subsection
        for subsection in subsections:
            self.crawl_subsection(section_name, subsection)
            time.sleep(2)  # Rate limiting

    def crawl_subsection(self, section_name, subsection_name):
        """Crawl a specific subsection"""
        # Try different URL patterns for the subsection
        possible_urls = [
            f"{self.base_url}/{subsection_name}",
            f"{self.base_url}/{section_name}/{subsection_name}",
            f"{self.base_url}/{subsection_name.replace('-', ' ')}",
        ]
        
        for url in possible_urls:
            if url in self.visited_urls:
                continue
                
            print(f"Trying: {url}")
            content = self.get_jina_content(url)
            
            if content and len(content.strip()) > 200:  # Valid content
                self.visited_urls.add(url)
                
                title, clean_content = self.extract_title_and_content(content)
                
                # Save to appropriate path
                filepath = f"docs/{section_name}/{subsection_name}.md"
                self.create_mdx_file(title, clean_content, filepath)
                
                return True
        
        print(f"Could not find content for {section_name}/{subsection_name}")
        return False

    def run(self):
        """Run the crawler with correct structure"""
        print("Starting Make.com Help Center crawler with correct structure...")
        
        # Remove old structure first
        print("Cleaning up old structure...")
        dirs_to_remove = ["docs/misc", "docs/main", "docs/resources"]
        for dir_path in dirs_to_remove:
            if os.path.exists(dir_path):
                import shutil
                shutil.rmtree(dir_path)
                print(f"Removed: {dir_path}")
        
        # Crawl each section according to actual structure
        for section_name, subsections in self.target_structure.items():
            print(f"\n=== Crawling {section_name.upper()} ===")
            self.crawl_section(section_name, subsections)
            time.sleep(3)  # Rate limiting between sections
        
        print(f"\nCrawling completed!")
        print(f"Total URLs processed: {len(self.visited_urls)}")
        print(f"Structure matches Make.com help center")

if __name__ == "__main__":
    crawler = MakeCorrectStructureCrawler()
    crawler.run() 
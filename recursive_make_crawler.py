#!/usr/bin/env python3
"""
Recursive Make.com Documentation Crawler
Crawls all help.make.com pages starting from get-started and maintains hierarchical structure
"""

import requests
import yaml
import os
import re
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from collections import defaultdict, deque
import json

class MakeDocsCrawler:
    def __init__(self, base_url="https://help.make.com", start_path="/get-started"):
        self.base_url = base_url
        self.start_url = urljoin(base_url, start_path)
        self.visited_urls = set()
        self.url_hierarchy = {}
        self.page_content = {}
        self.docs_structure = defaultdict(list)
        
        # Jina.ai settings
        self.jina_base = "https://r.jina.ai/"
        
        print(f"🚀 Initializing Make.com Documentation Crawler")
        print(f"📍 Base URL: {self.base_url}")
        print(f"🎯 Starting from: {self.start_url}")
    
    def is_valid_make_url(self, url):
        """Check if URL is a valid Make.com help page"""
        parsed = urlparse(url)
        return (
            parsed.netloc == "help.make.com" and
            not url.endswith(('.pdf', '.png', '.jpg', '.gif', '.svg')) and
            not url.startswith('mailto:') and
            not url.startswith('tel:') and
            '/en/' not in url and  # Skip language variants
            '#' not in url  # Skip anchor links
        )
    
    def extract_page_with_jina(self, url):
        """Extract page content using Jina.ai"""
        jina_url = f"{self.jina_base}{url}"
        
        try:
            print(f"  📖 Extracting with Jina.ai: {url}")
            response = requests.get(jina_url, timeout=30)
            
            if response.status_code == 200:
                return response.text
            else:
                print(f"  ❌ Jina.ai failed for {url}: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"  ❌ Error extracting {url}: {e}")
            return None
    
    def extract_links_from_content(self, content, base_url):
        """Extract internal links from Jina.ai content"""
        links = set()
        
        # Look for markdown links [text](url)
        markdown_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        
        for text, url in markdown_links:
            # Convert relative URLs to absolute
            if url.startswith('/'):
                full_url = urljoin(base_url, url)
            elif url.startswith('http'):
                full_url = url
            else:
                continue
                
            if self.is_valid_make_url(full_url):
                links.add(full_url)
        
        return links
    
    def clean_content_for_docs(self, raw_content, url):
        """Clean and structure content for documentation"""
        if not raw_content:
            return None
        
        lines = raw_content.split('\n')
        
        # Find main content (after separator)
        main_content_start = False
        content_lines = []
        
        for line in lines:
            line = line.strip()
            
            if line == "===============":
                main_content_start = True
                continue
            
            if not main_content_start:
                continue
            
            # Skip navigation and metadata
            if (line and 
                not line.startswith(('[', 'Updated', 'PREVIOUS', 'NEXT', 'Docs powered')) and
                not line.endswith(('Hub', 'Community', 'Academy', 'Care', 'Center', 'Documentation')) and
                'Navigate through spaces' not in line and
                '⌘K' not in line and
                len(line) > 3):
                content_lines.append(line)
        
        if not content_lines:
            return None
        
        # Process content to create structured markdown
        processed_content = self.structure_markdown_content(content_lines, url)
        
        return processed_content
    
    def structure_markdown_content(self, content_lines, url):
        """Structure content lines into proper markdown"""
        
        # Extract page title from URL
        path_parts = urlparse(url).path.strip('/').split('/')
        page_title = path_parts[-1].replace('-', ' ').title() if path_parts else "Documentation"
        
        structured_lines = []
        current_paragraph = []
        
        for line in content_lines:
            line = line.strip()
            
            # Look for content that should be headings
            if (len(line) < 100 and 
                any(keyword in line.lower() for keyword in ['what is', 'how to', 'benefits', 'introduction', 'create', 'manage']) and
                not line.startswith('[')):
                
                # Save current paragraph
                if current_paragraph:
                    structured_lines.append(' '.join(current_paragraph))
                    current_paragraph = []
                
                # Add as heading
                if line.lower().startswith(('what is', 'how to', 'benefits')):
                    structured_lines.append(f"## {line}")
                else:
                    structured_lines.append(line)
            else:
                current_paragraph.append(line)
                
                # Create paragraph breaks
                if len(current_paragraph) >= 3:
                    structured_lines.append(' '.join(current_paragraph))
                    current_paragraph = []
        
        # Add remaining content
        if current_paragraph:
            structured_lines.append(' '.join(current_paragraph))
        
        # Join with proper spacing
        final_content = '\n\n'.join([line for line in structured_lines if line.strip()])
        
        return final_content
    
    def determine_page_hierarchy(self, url):
        """Determine the hierarchical position of a page"""
        path = urlparse(url).path.strip('/')
        
        if not path:
            return [], "index"
        
        parts = path.split('/')
        
        # Map URL paths to category structure
        category_mapping = {
            'get-started': 'get-started',
            'learn-the-basics': 'get-started',
            'create-your-first-scenario': 'get-started',
            'expand-your-scenario': 'get-started',
            'key-concepts': 'key-concepts',
            'scenarios-and-connections': 'key-concepts',
            'apps-and-modules': 'key-concepts',
            'data-and-mapping': 'key-concepts',
            'error-handling': 'error-handling',
            'your-organization': 'organization',
            'your-profile': 'profile',
            'developers': 'developers',
            'make-ai-agents': 'developers'
        }
        
        # Determine category and subcategory
        page_name = parts[-1] if parts else 'index'
        
        for key, category in category_mapping.items():
            if key in path:
                if key == page_name:  # This is a main category page
                    return [category], page_name
                else:  # This is a subcategory page
                    return [category], page_name
        
        # Default categorization
        return ['misc'], page_name
    
    def create_docusaurus_file(self, url, content, category_path, filename):
        """Create a Docusaurus-compatible markdown file"""
        
        if not content:
            return False
        
        # Extract title from URL
        page_title = filename.replace('-', ' ').title()
        
        # Create directory structure
        if category_path:
            docs_dir = Path("docs") / "/".join(category_path)
        else:
            docs_dir = Path("docs")
        
        docs_dir.mkdir(parents=True, exist_ok=True)
        
        # Determine sidebar position
        position = len(self.docs_structure["/".join(category_path)]) + 1
        
        # Create frontmatter
        frontmatter = {
            'sidebar_position': position,
            'title': page_title,
            'description': f'Documentation for {page_title}'
        }
        
        # Build file content
        file_content = "---\n"
        file_content += yaml.dump(frontmatter, default_flow_style=False)
        file_content += "---\n\n"
        file_content += f"# {page_title}\n\n"
        file_content += content
        
        # Write file
        file_path = docs_dir / f"{filename}.md"
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(file_content)
            
            print(f"  ✅ Created: {file_path}")
            
            # Track in structure
            self.docs_structure["/".join(category_path)].append(filename)
            
            return True
            
        except Exception as e:
            print(f"  ❌ Error creating {file_path}: {e}")
            return False
    
    def crawl_recursively(self, max_pages=50):
        """Recursively crawl all Make.com documentation pages"""
        
        print(f"\n🕷️ Starting recursive crawl (max {max_pages} pages)")
        print("=" * 60)
        
        to_visit = deque([self.start_url])
        pages_processed = 0
        
        while to_visit and pages_processed < max_pages:
            current_url = to_visit.popleft()
            
            if current_url in self.visited_urls:
                continue
            
            print(f"\n📄 Processing ({pages_processed + 1}/{max_pages}): {current_url}")
            
            # Extract content
            raw_content = self.extract_page_with_jina(current_url)
            
            if not raw_content:
                continue
            
            # Mark as visited
            self.visited_urls.add(current_url)
            pages_processed += 1
            
            # Clean content
            clean_content = self.clean_content_for_docs(raw_content, current_url)
            
            if clean_content:
                # Determine hierarchy
                category_path, filename = self.determine_page_hierarchy(current_url)
                
                # Create documentation file
                self.create_docusaurus_file(current_url, clean_content, category_path, filename)
                
                # Store content
                self.page_content[current_url] = clean_content
            
            # Extract links for further crawling
            links = self.extract_links_from_content(raw_content, current_url)
            
            # Add new links to visit queue
            for link in links:
                if link not in self.visited_urls and link not in to_visit:
                    to_visit.append(link)
                    print(f"  🔗 Found link: {link}")
            
            # Be respectful to the server
            time.sleep(1)
        
        print(f"\n✅ Crawling completed!")
        print(f"📊 Processed {pages_processed} pages")
        print(f"📊 Created {sum(len(files) for files in self.docs_structure.values())} documentation files")
        
        return pages_processed
    
    def generate_summary_report(self):
        """Generate a summary report of the crawled documentation"""
        
        print(f"\n📋 CRAWLING SUMMARY REPORT")
        print("=" * 60)
        
        for category, files in self.docs_structure.items():
            if files:
                print(f"\n📁 {category}/")
                for i, filename in enumerate(files, 1):
                    print(f"  {i}. {filename.replace('-', ' ').title()}")
        
        print(f"\n📈 Statistics:")
        print(f"  📄 Total pages: {len(self.visited_urls)}")
        print(f"  📁 Categories: {len(self.docs_structure)}")
        print(f"  📝 Files created: {sum(len(files) for files in self.docs_structure.values())}")
        
        # Save structure to JSON for reference
        structure_file = Path("docs") / "_crawl_structure.json"
        with open(structure_file, 'w', encoding='utf-8') as f:
            json.dump({
                'visited_urls': list(self.visited_urls),
                'docs_structure': dict(self.docs_structure),
                'total_pages': len(self.visited_urls)
            }, f, indent=2)
        
        print(f"  💾 Structure saved to: {structure_file}")

def main():
    """Main function to run the recursive crawler"""
    
    print("🚀 Make.com Documentation Recursive Crawler")
    print("=" * 70)
    print("This will crawl all Make.com help pages and create a Docusaurus site")
    print("=" * 70)
    
    # Initialize crawler
    crawler = MakeDocsCrawler()
    
    # Start crawling
    pages_crawled = crawler.crawl_recursively(max_pages=30)  # Start with 30 pages
    
    # Generate report
    crawler.generate_summary_report()
    
    print(f"\n🎉 SUCCESS!")
    print(f"📁 Documentation created in: {os.path.abspath('docs')}")
    print(f"🌐 Ready for Docusaurus!")
    
    print(f"\n💡 Next steps:")
    print(f"  1. Review the generated files in docs/")
    print(f"  2. Restart Docusaurus: npm run start")
    print(f"  3. Check the new documentation structure")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Advanced Make.com Documentation Crawler - Improved version
Better content filtering, more categories, enhanced link discovery
"""

import requests
import yaml
import os
import re
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote
from bs4 import BeautifulSoup
from collections import defaultdict, deque
import json

class AdvancedMakeDocsCrawler:
    def __init__(self, base_url="https://help.make.com"):
        self.base_url = base_url
        self.visited_urls = set()
        self.page_content = {}
        self.docs_structure = defaultdict(list)
        
        # Jina.ai settings
        self.jina_base = "https://r.jina.ai/"
        
        # Starting URLs for different categories
        self.seed_urls = [
            "https://help.make.com/get-started",
            "https://help.make.com/key-concepts", 
            "https://help.make.com/scenarios-and-connections",
            "https://help.make.com/apps-and-modules",
            "https://help.make.com/data-and-mapping",
            "https://help.make.com/error-handling",
            "https://help.make.com/developers",
            "https://help.make.com/your-organization"
        ]
        
        print(f"🚀 Advanced Make.com Documentation Crawler")
        print(f"📍 Base URL: {self.base_url}")
        print(f"🌐 Seed URLs: {len(self.seed_urls)} categories")
    
    def is_valid_make_url(self, url):
        """Check if URL is a valid Make.com help page"""
        if not url or not isinstance(url, str):
            return False
            
        # Clean the URL
        url = url.strip().strip('"\'')
        
        parsed = urlparse(url)
        return (
            parsed.netloc == "help.make.com" and
            not url.endswith(('.pdf', '.png', '.jpg', '.gif', '.svg', '.ico')) and
            not url.startswith(('mailto:', 'tel:', 'javascript:')) and
            '/en/' not in url and
            '?' not in url and  # Skip query parameters
            '#' not in url and  # Skip anchors
            len(parsed.path) > 1  # Must have actual path
        )
    
    def extract_page_with_jina(self, url):
        """Extract page content using Jina.ai"""
        jina_url = f"{self.jina_base}{url}"
        
        try:
            print(f"  📖 Extracting: {url}")
            response = requests.get(jina_url, timeout=30)
            
            if response.status_code == 200:
                return response.text
            else:
                print(f"  ❌ Failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
            return None
    
    def extract_links_from_content(self, content, base_url):
        """Extract internal links from content more aggressively"""
        links = set()
        
        if not content:
            return links
        
        # Method 1: Extract markdown links
        markdown_links = re.findall(r'\[([^\]]*)\]\(([^)]+)\)', content)
        
        for text, url in markdown_links:
            if url.startswith('/'):
                full_url = urljoin(base_url, url)
            elif url.startswith('http'):
                full_url = url
            else:
                continue
                
            if self.is_valid_make_url(full_url):
                links.add(full_url)
        
        # Method 2: Extract URLs from text content
        url_pattern = r'https://help\.make\.com/[a-zA-Z0-9\-/]+'
        found_urls = re.findall(url_pattern, content)
        
        for url in found_urls:
            if self.is_valid_make_url(url):
                links.add(url)
        
        return links
    
    def clean_content_advanced(self, raw_content, url):
        """Advanced content cleaning with better filtering"""
        if not raw_content:
            return None
        
        lines = raw_content.split('\n')
        
        # Find main content section
        main_content_start = False
        content_lines = []
        
        for line in lines:
            line = line.strip()
            
            # Start collecting after the separator
            if line == "===============":
                main_content_start = True
                continue
            
            if not main_content_start:
                continue
            
            # Advanced filtering - skip unwanted content
            skip_line = (
                not line or
                len(line) < 4 or
                line.startswith(('[', 'Updated', 'PREVIOUS', 'NEXT', 'Docs powered', 'TABLE OF CONTENTS')) or
                line.endswith(('Hub', 'Community', 'Academy', 'Care', 'Center', 'Documentation')) or
                'Navigate through spaces' in line or
                '⌘K' in line or
                'Apps Documentation' in line or
                'cookie' in line.lower() or
                'privacy' in line.lower() or
                'advertisement' in line.lower() or
                'bing.com' in line.lower() or
                'cookielaw' in line.lower() or
                'consent' in line.lower() or
                line.startswith('![Image') or
                re.match(r'^-+$', line) or  # Skip separator lines
                line in ['Get started', 'Key concepts', 'Tools', 'Resources', 'Explore more',
                        'Scenarios', 'Connections', 'Functions', 'Data stores', 'Developers',
                        'Error handling', 'Your organization', 'Your profile', 'Release notes',
                        '2025', '2024', '×', 'Allow All', 'Reject All', 'Apply Cancel']
            )
            
            if not skip_line:
                content_lines.append(line)
        
        if not content_lines:
            return None
        
        # Advanced content structuring
        structured_content = self.structure_content_advanced(content_lines, url)
        
        return structured_content
    
    def structure_content_advanced(self, content_lines, url):
        """Advanced content structuring with better paragraph formation"""
        
        # Extract clean lines and group into meaningful sections
        clean_lines = []
        
        for line in content_lines:
            # Skip very short lines unless they look like headings
            if len(line) < 8 and not any(word in line.lower() for word in ['step', 'what', 'how', 'why']):
                continue
            
            # Skip lines that are mostly special characters
            if len(re.sub(r'[a-zA-Z0-9\s]', '', line)) > len(line) * 0.5:
                continue
                
            clean_lines.append(line)
        
        if not clean_lines:
            return None
        
        # Structure into paragraphs and headings
        structured_parts = []
        current_paragraph = []
        
        for line in clean_lines:
            # Identify potential headings
            is_heading = (
                len(line) < 80 and
                (line.lower().startswith(('what is', 'how to', 'why', 'when', 'step', '## ')) or
                 any(keyword in line.lower() for keyword in ['introduction', 'overview', 'benefits', 'features']))
            )
            
            if is_heading and current_paragraph:
                # Save current paragraph
                paragraph_text = ' '.join(current_paragraph)
                if len(paragraph_text) > 20:  # Only keep substantial paragraphs
                    structured_parts.append(paragraph_text)
                current_paragraph = []
                
                # Add heading
                if not line.startswith('#'):
                    structured_parts.append(f"## {line}")
                else:
                    structured_parts.append(line)
            else:
                current_paragraph.append(line)
                
                # Create paragraph break when we have enough content
                if len(' '.join(current_paragraph)) > 300:
                    paragraph_text = ' '.join(current_paragraph)
                    structured_parts.append(paragraph_text)
                    current_paragraph = []
        
        # Add remaining content
        if current_paragraph:
            paragraph_text = ' '.join(current_paragraph)
            if len(paragraph_text) > 20:
                structured_parts.append(paragraph_text)
        
        # Join with proper spacing
        final_content = '\n\n'.join([part for part in structured_parts if part.strip()])
        
        return final_content if len(final_content) > 50 else None
    
    def determine_page_hierarchy_advanced(self, url):
        """Advanced hierarchy determination with better categorization"""
        path = urlparse(url).path.strip('/')
        
        if not path:
            return [], "index"
        
        # Enhanced category mapping
        category_mapping = {
            # Get Started category
            'get-started': ('get-started', 'get-started'),
            'learn-the-basics': ('get-started', 'learn-the-basics'),
            'create-your-first-scenario': ('get-started', 'create-your-first-scenario'),
            'expand-your-scenario': ('get-started', 'expand-your-scenario'),
            
            # Key Concepts category  
            'key-concepts': ('key-concepts', 'key-concepts'),
            'scenarios-and-connections': ('key-concepts', 'scenarios-and-connections'),
            'apps-and-modules': ('key-concepts', 'apps-and-modules'), 
            'data-and-mapping': ('key-concepts', 'data-and-mapping'),
            
            # Error Handling category
            'error-handling': ('error-handling', 'error-handling'),
            'introduction-to-errors': ('error-handling', 'introduction-to-errors'),
            'how-to-handle-errors': ('error-handling', 'how-to-handle-errors'),
            
            # Developers category
            'developers': ('developers', 'developers'),
            'make-ai-agents': ('developers', 'make-ai-agents'),
            
            # Organization category
            'your-organization': ('organization', 'your-organization'),
            'organizations-teams': ('organization', 'organizations-teams'),
        }
        
        # Find the best match
        for key, (category, filename) in category_mapping.items():
            if key in path:
                return [category], filename
        
        # Extract filename from path
        filename = path.split('/')[-1] if '/' in path else path
        
        # Default categorization based on path structure
        if 'step-' in path:
            return ['tutorials'], filename
        elif 'what' in path or 'api' in path:
            return ['concepts'], filename
        else:
            return ['misc'], filename
    
    def create_docusaurus_file_advanced(self, url, content, category_path, filename):
        """Create advanced Docusaurus file with better metadata"""
        
        if not content or len(content) < 50:
            print(f"  ⚠️ Skipping {filename}: content too short")
            return False
        
        # Generate title from filename
        page_title = filename.replace('-', ' ').title()
        
        # Create directory structure
        if category_path:
            docs_dir = Path("docs") / "/".join(category_path)
        else:
            docs_dir = Path("docs")
        
        docs_dir.mkdir(parents=True, exist_ok=True)
        
        # Determine sidebar position
        category_key = "/".join(category_path)
        position = len(self.docs_structure[category_key]) + 1
        
        # Create enhanced frontmatter
        frontmatter = {
            'sidebar_position': position,
            'title': page_title,
            'description': f'Learn about {page_title.lower()} in Make.com automation platform'
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
            self.docs_structure[category_key].append(filename)
            
            return True
            
        except Exception as e:
            print(f"  ❌ Error creating {file_path}: {e}")
            return False
    
    def crawl_comprehensively(self, max_pages=40):
        """Comprehensive crawl with multiple seed URLs"""
        
        print(f"\n🕷️ Starting comprehensive crawl (max {max_pages} pages)")
        print("=" * 70)
        
        to_visit = deque(self.seed_urls)
        pages_processed = 0
        successful_files = 0
        
        while to_visit and pages_processed < max_pages:
            current_url = to_visit.popleft()
            
            if current_url in self.visited_urls:
                continue
            
            print(f"\n📄 Processing ({pages_processed + 1}/{max_pages}): {current_url}")
            
            # Extract content
            raw_content = self.extract_page_with_jina(current_url)
            
            self.visited_urls.add(current_url)
            pages_processed += 1
            
            if not raw_content:
                continue
            
            # Clean content with advanced filtering
            clean_content = self.clean_content_advanced(raw_content, current_url)
            
            if clean_content:
                # Determine hierarchy
                category_path, filename = self.determine_page_hierarchy_advanced(current_url)
                
                # Create documentation file
                if self.create_docusaurus_file_advanced(current_url, clean_content, category_path, filename):
                    successful_files += 1
                
                # Store content
                self.page_content[current_url] = clean_content
            
            # Extract links for further crawling
            links = self.extract_links_from_content(raw_content, current_url)
            
            # Add new links to visit queue
            new_links = 0
            for link in links:
                if link not in self.visited_urls and link not in to_visit:
                    to_visit.append(link)
                    new_links += 1
            
            if new_links > 0:
                print(f"  🔗 Found {new_links} new links")
            
            # Be respectful to the server
            time.sleep(1)
        
        print(f"\n✅ Comprehensive crawling completed!")
        print(f"📊 Processed {pages_processed} pages")
        print(f"📊 Created {successful_files} documentation files")
        
        return pages_processed, successful_files
    
    def generate_comprehensive_report(self):
        """Generate comprehensive crawling report"""
        
        print(f"\n📋 COMPREHENSIVE CRAWLING REPORT")
        print("=" * 70)
        
        total_files = 0
        for category, files in self.docs_structure.items():
            if files:
                print(f"\n📁 {category}/")
                for i, filename in enumerate(files, 1):
                    print(f"  {i}. {filename.replace('-', ' ').title()}")
                total_files += len(files)
        
        print(f"\n📈 Final Statistics:")
        print(f"  📄 Total pages processed: {len(self.visited_urls)}")
        print(f"  📁 Categories created: {len([k for k, v in self.docs_structure.items() if v])}")
        print(f"  📝 Documentation files: {total_files}")
        
        # Save comprehensive structure
        structure_file = Path("docs") / "_comprehensive_structure.json"
        with open(structure_file, 'w', encoding='utf-8') as f:
            json.dump({
                'visited_urls': list(self.visited_urls),
                'docs_structure': dict(self.docs_structure),
                'total_pages': len(self.visited_urls),
                'total_files': total_files,
                'seed_urls': self.seed_urls
            }, f, indent=2)
        
        print(f"  💾 Complete structure saved to: {structure_file}")

def main():
    """Main function for comprehensive crawling"""
    
    print("🚀 Advanced Make.com Documentation Crawler")
    print("=" * 80)
    print("Comprehensive crawling with multiple categories and improved filtering")
    print("=" * 80)
    
    # Initialize advanced crawler
    crawler = AdvancedMakeDocsCrawler()
    
    # Start comprehensive crawling
    total_pages, successful_files = crawler.crawl_comprehensively(max_pages=40)
    
    # Generate comprehensive report
    crawler.generate_comprehensive_report()
    
    print(f"\n🎉 COMPREHENSIVE SUCCESS!")
    print(f"📁 Documentation created in: {os.path.abspath('docs')}")
    print(f"📊 {successful_files} high-quality files created from {total_pages} pages")
    print(f"🌐 Ready for Docusaurus!")
    
    print(f"\n💡 Next steps:")
    print(f"  1. Review generated files in docs/ directories")
    print(f"  2. Restart Docusaurus: npm run start")
    print(f"  3. Explore the comprehensive documentation structure")

if __name__ == "__main__":
    main() 
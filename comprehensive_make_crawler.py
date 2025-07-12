#!/usr/bin/env python3
"""
Comprehensive Make.com Documentation Crawler
Starts from main page and discovers ALL help content systematically
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

class ComprehensiveMakeCrawler:
    def __init__(self, base_url="https://help.make.com"):
        self.base_url = base_url
        self.visited_urls = set()
        self.page_content = {}
        self.docs_structure = defaultdict(list)
        self.failed_urls = set()
        
        # Jina.ai settings
        self.jina_base = "https://r.jina.ai/"
        
        # Comprehensive seed URLs - start from main pages and major categories
        self.seed_urls = [
            "https://help.make.com/",  # Main help page
            "https://help.make.com/get-started",
            "https://help.make.com/learn-the-basics",
            "https://help.make.com/create-your-first-scenario", 
            "https://help.make.com/expand-your-scenario",
            "https://help.make.com/key-concepts",
            "https://help.make.com/scenarios-and-connections",
            "https://help.make.com/apps-and-modules",
            "https://help.make.com/data-and-mapping",
            "https://help.make.com/error-handling",
            "https://help.make.com/developers",
            "https://help.make.com/your-organization",
            "https://help.make.com/resources",
            "https://help.make.com/tools",
            
            # Add specific step tutorials that we know exist
            "https://help.make.com/step-1-plan-your-scenario",
            "https://help.make.com/step-2-get-your-apps-ready", 
            "https://help.make.com/step-3-add-your-first-app",
            "https://help.make.com/step-4-create-a-connection",
            "https://help.make.com/step-5-set-up-the-trigger",
            "https://help.make.com/step-6-test-the-module",
            "https://help.make.com/step-7-add-another-module",
            "https://help.make.com/step-8-map-data",
            "https://help.make.com/step-9-test-your-scenario",
            "https://help.make.com/step-10-schedule-your-scenario",
        ]
        
        print(f"🚀 Comprehensive Make.com Documentation Crawler")
        print(f"📍 Base URL: {self.base_url}")
        print(f"🌐 Starting with {len(self.seed_urls)} seed URLs")
    
    def is_valid_make_url(self, url):
        """Enhanced URL validation"""
        if not url or not isinstance(url, str):
            return False
            
        # Clean the URL
        url = url.strip().strip('"\'')
        
        # Skip obviously invalid URLs
        if any(skip in url.lower() for skip in ['javascript:', 'mailto:', 'tel:', 'www.make.com', 'academy.make.com', 'community.make.com']):
            return False
            
        parsed = urlparse(url)
        return (
            parsed.netloc == "help.make.com" and
            not url.endswith(('.pdf', '.png', '.jpg', '.gif', '.svg', '.ico', '.jpeg')) and
            '/en/' not in url and
            len(parsed.path) > 1  # Must have actual path
        )
    
    def extract_page_with_jina(self, url):
        """Extract page content using Jina.ai with retries"""
        jina_url = f"{self.jina_base}{url}"
        
        for attempt in range(2):  # 2 attempts
            try:
                print(f"  📖 Extracting ({attempt+1}/2): {url}")
                response = requests.get(jina_url, timeout=45)
                
                if response.status_code == 200:
                    return response.text
                else:
                    print(f"  ❌ HTTP {response.status_code}")
                    if attempt == 0:
                        time.sleep(2)  # Wait before retry
                    
            except Exception as e:
                print(f"  ❌ Error: {e}")
                if attempt == 0:
                    time.sleep(2)
        
        self.failed_urls.add(url)
        return None
    
    def extract_links_aggressively(self, content, base_url):
        """Aggressively extract all possible internal links"""
        links = set()
        
        if not content:
            return links
        
        # Method 1: Extract markdown links [text](url)
        markdown_links = re.findall(r'\[([^\]]*)\]\(([^)]+)\)', content)
        
        for text, url in markdown_links:
            # Clean up the URL
            url = url.strip().strip('"\'')
            
            if url.startswith('/'):
                full_url = urljoin(base_url, url)
            elif url.startswith('http'):
                full_url = url
            else:
                continue
                
            if self.is_valid_make_url(full_url):
                links.add(full_url)
        
        # Method 2: Extract direct URLs from text
        url_patterns = [
            r'https://help\.make\.com/[a-zA-Z0-9\-/_]+',
            r'help\.make\.com/([a-zA-Z0-9\-/_]+)',
        ]
        
        for pattern in url_patterns:
            found_urls = re.findall(pattern, content)
            for url in found_urls:
                if not url.startswith('http'):
                    url = f"https://help.make.com/{url}"
                if self.is_valid_make_url(url):
                    links.add(url)
        
        # Method 3: Look for step patterns and common page names
        content_lower = content.lower()
        
        # Find step references
        step_matches = re.findall(r'step[\s\-]?(\d+)', content_lower)
        for step_num in step_matches:
            potential_urls = [
                f"https://help.make.com/step-{step_num}",
                f"https://help.make.com/step-{step_num}-plan-your-scenario",
                f"https://help.make.com/step-{step_num}-get-your-apps-ready",
                f"https://help.make.com/step-{step_num}-add-your-first-app",
                f"https://help.make.com/step-{step_num}-create-a-connection",
                f"https://help.make.com/step-{step_num}-set-up-the-trigger",
                f"https://help.make.com/step-{step_num}-test-the-module",
                f"https://help.make.com/step-{step_num}-add-another-module",
                f"https://help.make.com/step-{step_num}-map-data",
                f"https://help.make.com/step-{step_num}-test-your-scenario",
                f"https://help.make.com/step-{step_num}-schedule-your-scenario",
            ]
            for url in potential_urls:
                links.add(url)
        
        # Method 4: Common page patterns
        common_topics = [
            'what-is-make', 'whats-an-api', 'operations', 'filtering', 'mapping',
            'types-of-modules', 'module-settings', 'webhooks', 'connections',
            'functions', 'data-stores', 'organizations-teams', 'subscription',
            'administration', 'access-management', 'profile-settings',
            'introduction-to-errors', 'error-handlers', 'types-of-errors',
            'types-of-warnings', 'exponential-backoff', 'throw'
        ]
        
        for topic in common_topics:
            if topic.replace('-', ' ') in content_lower:
                url = f"https://help.make.com/{topic}"
                links.add(url)
        
        return links
    
    def clean_content_comprehensively(self, raw_content, url):
        """Comprehensive content cleaning"""
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
            
            # Enhanced filtering
            skip_line = (
                not line or
                len(line) < 4 or
                line.startswith(('[', 'Updated ', 'PREVIOUS', 'NEXT', 'Docs powered', 'TABLE OF CONTENTS')) or
                line.endswith(('Hub', 'Community', 'Academy', 'Care', 'Center', 'Documentation')) or
                any(term in line.lower() for term in [
                    'navigate through spaces', '⌘k', 'apps documentation',
                    'cookie', 'privacy', 'advertisement', 'bing.com', 'cookielaw',
                    'consent', 'allow all', 'reject all', 'apply cancel'
                ]) or
                line.startswith('![Image') or
                re.match(r'^-{3,}$', line) or  # Skip long separator lines
                line in ['Get started', 'Key concepts', 'Tools', 'Resources', 'Explore more',
                        'Scenarios', 'Connections', 'Functions', 'Data stores', 'Developers',
                        'Error handling', 'Your organization', 'Your profile', 'Release notes',
                        '2025', '2024', '×']
            )
            
            if not skip_line:
                content_lines.append(line)
        
        if not content_lines:
            return None
        
        # Structure the content
        structured_content = self.structure_content_intelligently(content_lines, url)
        
        return structured_content
    
    def structure_content_intelligently(self, content_lines, url):
        """Intelligently structure content into markdown"""
        
        # Join content and split into meaningful chunks
        full_text = ' '.join(content_lines)
        
        # Basic sentence splitting
        sentences = re.split(r'(?<=[.!?])\s+', full_text)
        
        structured_parts = []
        current_paragraph = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence or len(sentence) < 10:
                continue
            
            # Check if this should be a heading
            is_heading = (
                len(sentence) < 100 and
                any(starter in sentence.lower() for starter in [
                    'what is', 'how to', 'why', 'when to', 'step ', 'introduction to',
                    'types of', 'benefits of', 'overview of'
                ]) and
                not sentence.startswith('http')
            )
            
            if is_heading and current_paragraph:
                # Save current paragraph
                paragraph_text = ' '.join(current_paragraph)
                if len(paragraph_text) > 30:
                    structured_parts.append(paragraph_text)
                current_paragraph = []
                
                # Add heading
                if not sentence.startswith('#'):
                    structured_parts.append(f"## {sentence}")
                else:
                    structured_parts.append(sentence)
            else:
                current_paragraph.append(sentence)
                
                # Create paragraph breaks for readability
                if len(' '.join(current_paragraph)) > 400:
                    paragraph_text = ' '.join(current_paragraph)
                    structured_parts.append(paragraph_text)
                    current_paragraph = []
        
        # Add remaining content
        if current_paragraph:
            paragraph_text = ' '.join(current_paragraph)
            if len(paragraph_text) > 30:
                structured_parts.append(paragraph_text)
        
        # Join with proper spacing
        final_content = '\n\n'.join([part for part in structured_parts if part.strip()])
        
        return final_content if len(final_content) > 80 else None
    
    def determine_category_intelligently(self, url):
        """Intelligently determine category from URL and content"""
        path = urlparse(url).path.strip('/')
        
        if not path or path == '/':
            return ['main'], "index"
        
        # Enhanced category mapping
        category_rules = [
            # Get Started and basic tutorials
            (['get-started'], ['get-started', 'learn-the-basics', 'create-your-first-scenario', 'expand-your-scenario']),
            
            # Step-by-step tutorials  
            (['tutorials'], [r'step-\d+', r'step-\d+-.*']),
            
            # Key concepts
            (['key-concepts'], ['key-concepts', 'scenarios-and-connections', 'apps-and-modules', 'data-and-mapping', 'operations', 'filtering', 'mapping']),
            
            # Error handling
            (['error-handling'], ['error-handling', 'introduction-to-errors', 'how-to-handle-errors', 'error-handlers', 'types-of-errors', 'types-of-warnings', 'exponential-backoff', 'throw']),
            
            # Apps and integrations
            (['apps'], ['introduction-to-make-apps', 'types-of-modules', 'module-settings', 'webhooks', 'connect-an-application']),
            
            # Organization and management
            (['organization'], ['your-organization', 'organizations-teams', 'subscription', 'administration', 'access-management', 'profile-settings']),
            
            # Developers
            (['developers'], ['developers', 'make-ai-agents', 'api']),
            
            # Tools and resources
            (['tools'], ['tools', 'resources', 'functions', 'data-stores']),
        ]
        
        filename = path.split('/')[-1] if '/' in path else path
        
        # Apply category rules
        for category_path, patterns in category_rules:
            for pattern in patterns:
                if re.search(pattern, path) or pattern == filename:
                    return category_path, filename
        
        # Default categorization
        if 'what' in path or 'api' in path:
            return ['concepts'], filename
        elif any(term in path for term in ['step', 'tutorial', 'guide']):
            return ['tutorials'], filename
        else:
            return ['misc'], filename
    
    def create_comprehensive_file(self, url, content, category_path, filename):
        """Create comprehensive documentation file"""
        
        if not content or len(content) < 80:
            print(f"  ⚠️ Skipping {filename}: content too short ({len(content) if content else 0} chars)")
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
        
        # Create frontmatter
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
            
            print(f"  ✅ Created: {file_path} ({len(content)} chars)")
            
            # Track in structure
            self.docs_structure[category_key].append(filename)
            
            return True
            
        except Exception as e:
            print(f"  ❌ Error creating {file_path}: {e}")
            return False
    
    def crawl_comprehensively(self, max_pages=200):
        """Comprehensive crawl with aggressive link discovery"""
        
        print(f"\n🕷️ Starting comprehensive crawl (max {max_pages} pages)")
        print("=" * 80)
        
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
            
            # Clean content
            clean_content = self.clean_content_comprehensively(raw_content, current_url)
            
            if clean_content:
                # Determine hierarchy
                category_path, filename = self.determine_category_intelligently(current_url)
                
                # Create documentation file
                if self.create_comprehensive_file(current_url, clean_content, category_path, filename):
                    successful_files += 1
                
                # Store content
                self.page_content[current_url] = clean_content
            
            # Extract links aggressively
            links = self.extract_links_aggressively(raw_content, current_url)
            
            # Add new links to visit queue
            new_links = 0
            for link in links:
                if link not in self.visited_urls and link not in to_visit and link not in self.failed_urls:
                    to_visit.append(link)
                    new_links += 1
            
            if new_links > 0:
                print(f"  🔗 Found {new_links} new links (queue: {len(to_visit)})")
            
            # Be respectful to the server
            time.sleep(1.5)
        
        print(f"\n✅ Comprehensive crawling completed!")
        print(f"📊 Processed {pages_processed} pages")
        print(f"📊 Created {successful_files} documentation files")
        print(f"📊 Failed URLs: {len(self.failed_urls)}")
        
        return pages_processed, successful_files
    
    def create_category_files(self):
        """Create _category_.json files for all discovered categories"""
        
        category_configs = {
            "get-started": {
                "label": "Get Started",
                "position": 1,
                "link": {
                    "type": "generated-index",
                    "description": "Step-by-step guide to building your first Make.com automation"
                }
            },
            "tutorials": {
                "label": "Tutorials",
                "position": 2,
                "link": {
                    "type": "generated-index",
                    "description": "Step-by-step tutorials and detailed walkthroughs"
                }
            },
            "key-concepts": {
                "label": "Key Concepts",
                "position": 3,
                "link": {
                    "type": "generated-index",
                    "description": "Learn the fundamental concepts of Make.com automation"
                }
            },
            "apps": {
                "label": "Apps & Integrations",
                "position": 4,
                "link": {
                    "type": "generated-index",
                    "description": "Learn about apps, modules, and integrations"
                }
            },
            "error-handling": {
                "label": "Error Handling",
                "position": 5,
                "link": {
                    "type": "generated-index",
                    "description": "Handle errors and keep your scenarios running smoothly"
                }
            },
            "organization": {
                "label": "Organization",
                "position": 6,
                "link": {
                    "type": "generated-index",
                    "description": "Manage your organization, teams, and settings"
                }
            },
            "developers": {
                "label": "Developers",
                "position": 7,
                "link": {
                    "type": "generated-index",
                    "description": "Developer resources and advanced features"
                }
            },
            "tools": {
                "label": "Tools & Resources",
                "position": 8,
                "link": {
                    "type": "generated-index",
                    "description": "Tools, functions, and additional resources"
                }
            },
            "concepts": {
                "label": "Concepts",
                "position": 9,
                "link": {
                    "type": "generated-index",
                    "description": "Additional concepts and explanations"
                }
            },
            "misc": {
                "label": "Additional Resources",
                "position": 10,
                "link": {
                    "type": "generated-index",
                    "description": "Additional documentation and resources"
                }
            }
        }
        
        print(f"\n📁 Creating category configuration files...")
        
        created_count = 0
        for category_name, config in category_configs.items():
            category_dir = Path("docs") / category_name
            
            if category_dir.exists() and any(category_dir.iterdir()):
                category_file = category_dir / "_category_.json"
                
                try:
                    with open(category_file, 'w', encoding='utf-8') as f:
                        json.dump(config, f, indent=2)
                    print(f"  ✅ Created: {category_file}")
                    created_count += 1
                except Exception as e:
                    print(f"  ❌ Error creating {category_file}: {e}")
        
        return created_count
    
    def generate_final_report(self):
        """Generate comprehensive final report"""
        
        print(f"\n📋 COMPREHENSIVE CRAWLING REPORT")
        print("=" * 80)
        
        total_files = 0
        for category, files in self.docs_structure.items():
            if files:
                print(f"\n📁 {category}/")
                for i, filename in enumerate(sorted(files), 1):
                    print(f"  {i}. {filename.replace('-', ' ').title()}")
                total_files += len(files)
        
        print(f"\n📈 Final Statistics:")
        print(f"  📄 Total pages processed: {len(self.visited_urls)}")
        print(f"  📁 Categories created: {len([k for k, v in self.docs_structure.items() if v])}")
        print(f"  📝 Documentation files: {total_files}")
        print(f"  ❌ Failed URLs: {len(self.failed_urls)}")
        
        if self.failed_urls:
            print(f"\n⚠️ Failed URLs:")
            for url in sorted(self.failed_urls):
                print(f"    - {url}")
        
        # Save comprehensive structure
        structure_file = Path("docs") / "_comprehensive_crawl_report.json"
        with open(structure_file, 'w', encoding='utf-8') as f:
            json.dump({
                'visited_urls': list(self.visited_urls),
                'failed_urls': list(self.failed_urls),
                'docs_structure': dict(self.docs_structure),
                'total_pages': len(self.visited_urls),
                'total_files': total_files,
                'seed_urls': self.seed_urls
            }, f, indent=2)
        
        print(f"  💾 Complete report saved to: {structure_file}")

def main():
    """Main function for comprehensive crawling"""
    
    print("🚀 Comprehensive Make.com Documentation Crawler")
    print("=" * 90)
    print("Discovering and crawling ALL Make.com help content systematically")
    print("=" * 90)
    
    # Initialize comprehensive crawler
    crawler = ComprehensiveMakeCrawler()
    
    # Start comprehensive crawling
    total_pages, successful_files = crawler.crawl_comprehensively(max_pages=400)
    
    # Create category files
    category_count = crawler.create_category_files()
    
    # Generate final report
    crawler.generate_final_report()
    
    print(f"\n🎉 COMPREHENSIVE CRAWLING SUCCESS!")
    print(f"📁 Documentation created in: {os.path.abspath('docs')}")
    print(f"📊 {successful_files} high-quality files from {total_pages} pages")
    print(f"📁 {category_count} categories configured")
    print(f"🌐 Ready for Docusaurus!")
    
    print(f"\n💡 Next steps:")
    print(f"  1. Review the comprehensive structure in docs/")
    print(f"  2. Restart Docusaurus to see all new content")
    print(f"  3. Explore the much more complete documentation!")

if __name__ == "__main__":
    main() 
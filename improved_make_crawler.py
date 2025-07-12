#!/usr/bin/env python3
"""
Improved Make.com Documentation Crawler
Based on actual website structure with proper multi-level directories
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

class ImprovedMakeCrawler:
    def __init__(self, base_url="https://help.make.com"):
        self.base_url = base_url
        self.visited_urls = set()
        self.page_content = {}
        self.docs_structure = defaultdict(list)
        self.failed_urls = set()
        
        # Jina.ai settings
        self.jina_base = "https://r.jina.ai/"
        
        # Comprehensive seed URLs based on actual Make.com structure
        self.seed_urls = [
            "https://help.make.com/",  # Main help page
            
            # Get started section
            "https://help.make.com/get-started",
            "https://help.make.com/learn-the-basics",
            "https://help.make.com/create-your-first-scenario", 
            "https://help.make.com/expand-your-scenario",
            
            # Key concepts
            "https://help.make.com/key-concepts",
            "https://help.make.com/scenarios-and-connections",
            "https://help.make.com/apps-and-modules",
            "https://help.make.com/data-and-mapping",
            
            # Tools & Resources
            "https://help.make.com/tools",
            "https://help.make.com/resources",
            "https://help.make.com/functions",
            "https://help.make.com/data-stores",
            
            # Error handling
            "https://help.make.com/error-handling",
            "https://help.make.com/introduction-to-errors",
            "https://help.make.com/how-to-handle-errors",
            "https://help.make.com/error-handlers",
            "https://help.make.com/types-of-errors",
            "https://help.make.com/types-of-warnings",
            "https://help.make.com/exponential-backoff",
            "https://help.make.com/throw",
            
            # Your organization (proper name!)
            "https://help.make.com/organizations",
            "https://help.make.com/teams",
            "https://help.make.com/subscription",
            "https://help.make.com/administration",
            "https://help.make.com/access-management",
            "https://help.make.com/single-sign-on",
            
            # Your profile (missing section!)
            "https://help.make.com/profile-settings",
            "https://help.make.com/manage-time-zones",
            "https://help.make.com/api-key",
            "https://help.make.com/delete-your-profile",
            
            # Developers
            "https://help.make.com/developers",
            "https://help.make.com/make-ai-agents",
            
            # Make AI Agents subsection
            "https://help.make.com/introduction-to-ai-agents",
            "https://help.make.com/ai-agent-best-practices",
            "https://help.make.com/manage-ai-agents",
            
            # Release notes
            "https://help.make.com/release-notes",
            "https://help.make.com/2025",
            "https://help.make.com/2024",
        ]
        
        print(f"🚀 Improved Make.com Documentation Crawler")
        print(f"📍 Base URL: {self.base_url}")
        print(f"🌐 Starting with {len(self.seed_urls)} seed URLs")
    
    def is_valid_make_url(self, url):
        """Enhanced URL validation"""
        if not url or not isinstance(url, str):
            return False
            
        # Clean the URL
        url = url.strip().strip('"\'')
        
        # Skip obviously invalid URLs
        if any(skip in url.lower() for skip in ['javascript:', 'mailto:', 'tel:', 'www.make.com', 'academy.make.com', 'community.make.com', 'developers.make.com']):
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
        """Enhanced link extraction with better filtering"""
        links = set()
        
        if not content:
            return links
        
        # Method 1: Extract markdown links [text](url)
        markdown_links = re.findall(r'\[([^\]]*)\]\(([^)]+)\)', content)
        
        for text, url in markdown_links:
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
        ]
        
        for pattern in url_patterns:
            found_urls = re.findall(pattern, content)
            for url in found_urls:
                if self.is_valid_make_url(url):
                    links.add(url)
        
        return links
    
    def clean_content_properly(self, raw_content, url):
        """Improved content cleaning with better structure"""
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
            
            # Enhanced filtering - remove more noise
            skip_line = (
                not line or
                len(line) < 5 or
                line.startswith(('[', 'Updated ', 'PREVIOUS', 'NEXT', 'Docs powered', 'TABLE OF CONTENTS', '×')) or
                line.endswith(('Hub', 'Community', 'Academy', 'Care', 'Center', 'Documentation')) or
                any(term in line.lower() for term in [
                    'navigate through spaces', '⌘k', 'apps documentation',
                    'cookie', 'privacy', 'advertisement', 'bing.com', 'cookielaw',
                    'consent', 'allow all', 'reject all', 'apply cancel',
                    'did this page help you', 'press space bar to start',
                    'when dragging you can use', 'always active clear',
                    'checkbox label label'
                ]) or
                line.startswith('![Image') or
                re.match(r'^-{3,}$', line) or  # Skip long separator lines
                re.match(r'^={3,}$', line) or  # Skip separator lines
                line in ['Get started', 'Key concepts', 'Tools', 'Resources', 'Explore more',
                        'Scenarios', 'Connections', 'Functions', 'Data stores', 'Developers',
                        'Error handling', 'Your organization', 'Your profile', 'Release notes',
                        '2025', '2024', '×', 'Make Help Center', 'Website logo']
            )
            
            if not skip_line:
                content_lines.append(line)
        
        if not content_lines:
            return None
        
        # Structure the content
        structured_content = self.structure_content_properly(content_lines, url)
        
        return structured_content
    
    def structure_content_properly(self, content_lines, url):
        """Better content structuring"""
        
        # Join content and clean it
        full_text = ' '.join(content_lines)
        
        # Remove time estimates and other noise
        full_text = re.sub(r'\b\d+\s*min\b', '', full_text)
        full_text = re.sub(r'\s+', ' ', full_text)  # Normalize whitespace
        
        # Split into sentences
        sentences = re.split(r'(?<=[.!?])\s+', full_text)
        
        structured_parts = []
        current_paragraph = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence or len(sentence) < 15:
                continue
            
            # Better heading detection
            is_heading = (
                len(sentence) < 150 and
                (sentence.endswith(':') or
                 any(starter in sentence.lower() for starter in [
                    'what is', 'how to', 'why', 'when to', 'step ', 'introduction to',
                    'types of', 'benefits of', 'overview of', 'getting started',
                    'create ', 'manage ', 'configure ', 'setup '
                ]) or
                 sentence.isupper()) and
                not sentence.startswith('http')
            )
            
            if is_heading and current_paragraph:
                # Save current paragraph
                paragraph_text = ' '.join(current_paragraph)
                if len(paragraph_text) > 50:
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
                if len(' '.join(current_paragraph)) > 500:
                    paragraph_text = ' '.join(current_paragraph)
                    structured_parts.append(paragraph_text)
                    current_paragraph = []
        
        # Add remaining content
        if current_paragraph:
            paragraph_text = ' '.join(current_paragraph)
            if len(paragraph_text) > 50:
                structured_parts.append(paragraph_text)
        
        # Join with proper spacing
        final_content = '\n\n'.join([part for part in structured_parts if part.strip()])
        
        return final_content if len(final_content) > 100 else None
    
    def determine_proper_category(self, url):
        """Properly categorize based on actual Make.com structure"""
        path = urlparse(url).path.strip('/')
        
        if not path or path == '/':
            return ['main'], "index"
        
        # Enhanced category mapping based on actual website structure
        category_rules = [
            # Get Started
            (['get-started'], [
                'get-started', 'learn-the-basics', 'create-your-first-scenario', 
                'expand-your-scenario', r'step-\d+.*'
            ]),
            
            # Key Concepts  
            (['key-concepts'], [
                'key-concepts', 'scenarios-and-connections', 'apps-and-modules', 
                'data-and-mapping', 'operations', 'filtering', 'mapping',
                'types-of-modules', 'module-settings', 'webhooks'
            ]),
            
            # Tools & Resources
            (['tools'], ['tools']),
            (['resources'], ['resources', 'functions', 'data-stores', 'keyboard-shortcuts']),
            
            # Error handling
            (['error-handling'], [
                'error-handling', 'introduction-to-errors', 'how-to-handle-errors',
                'error-handlers', 'types-of-errors', 'types-of-warnings', 
                'exponential-backoff', 'throw'
            ]),
            
            # Your organization (proper multi-level structure)
            (['your-organization'], ['organizations', 'teams']),
            (['your-organization', 'access-management'], [
                'access-management', 'single-sign-on', 'okta-saml', 'google-saml',
                'ms-azure-ad-saml', 'ms-azure-ad-oidc'
            ]),
            (['your-organization', 'administration'], ['administration', 'subscription']),
            
            # Your profile (missing section!)
            (['your-profile'], [
                'profile-settings', 'manage-time-zones', 'api-key', 
                'delete-your-profile', 'make-programs'
            ]),
            
            # Developers
            (['developers'], ['developers']),
            (['developers', 'make-ai-agents'], [
                'make-ai-agents', 'introduction-to-ai-agents', 'ai-agent-best-practices',
                'manage-ai-agents', 'make-ai-agent-reference', 'ai-agent-use-case'
            ]),
            
            # Release notes
            (['release-notes'], ['release-notes', '2025', '2024']),
            (['release-notes', '2024'], [r'.*2024.*']),
            (['release-notes', '2025'], [r'.*2025.*']),
        ]
        
        filename = path.split('/')[-1] if '/' in path else path
        
        # Apply category rules
        for category_path, patterns in category_rules:
            for pattern in patterns:
                if re.search(pattern, path) or pattern == filename:
                    return category_path, filename
        
        # Default categorization with better logic
        if any(term in path for term in ['profile', 'user', 'account']):
            return ['your-profile'], filename
        elif any(term in path for term in ['organization', 'team', 'admin']):
            return ['your-organization'], filename
        elif any(term in path for term in ['ai', 'agent']):
            return ['developers', 'make-ai-agents'], filename
        elif any(term in path for term in ['error', 'warning', 'handle']):
            return ['error-handling'], filename
        else:
            return ['misc'], filename
    
    def create_improved_file(self, url, content, category_path, filename):
        """Create properly structured documentation file"""
        
        if not content or len(content) < 100:
            print(f"  ⚠️ Skipping {filename}: content too short ({len(content) if content else 0} chars)")
            return False
        
        # Generate title from filename
        page_title = filename.replace('-', ' ').title()
        
        # Create directory structure (support multi-level)
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
    
    def crawl_improved(self, max_pages=400):
        """Improved crawl with proper structure"""
        
        print(f"\n🕷️ Starting improved crawl (max {max_pages} pages)")
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
            clean_content = self.clean_content_properly(raw_content, current_url)
            
            if clean_content:
                # Determine hierarchy (proper multi-level)
                category_path, filename = self.determine_proper_category(current_url)
                
                # Create documentation file
                if self.create_improved_file(current_url, clean_content, category_path, filename):
                    successful_files += 1
                
                # Store content
                self.page_content[current_url] = clean_content
            
            # Extract links
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
        
        print(f"\n✅ Improved crawling completed!")
        print(f"📊 Processed {pages_processed} pages")
        print(f"📊 Created {successful_files} documentation files")
        print(f"📊 Failed URLs: {len(self.failed_urls)}")
        
        return pages_processed, successful_files
    
    def create_proper_category_files(self):
        """Create _category_.json files with proper Make.com structure"""
        
        category_configs = {
            "get-started": {
                "label": "Get Started",
                "position": 1,
                "link": {
                    "type": "generated-index",
                    "description": "Get started with Make.com automation platform"
                }
            },
            "key-concepts": {
                "label": "Key Concepts",
                "position": 2,
                "link": {
                    "type": "generated-index",
                    "description": "Learn the fundamental concepts of Make.com"
                }
            },
            "tools": {
                "label": "Tools",
                "position": 3,
                "link": {
                    "type": "generated-index",
                    "description": "Advanced tools for complex automations"
                }
            },
            "resources": {
                "label": "Resources",
                "position": 4,
                "link": {
                    "type": "generated-index",
                    "description": "Functions, data stores, and additional resources"
                }
            },
            "error-handling": {
                "label": "Error Handling",
                "position": 5,
                "link": {
                    "type": "generated-index",
                    "description": "Handle errors and keep scenarios running smoothly"
                }
            },
            "your-organization": {
                "label": "Your Organization",
                "position": 6,
                "link": {
                    "type": "generated-index",
                    "description": "Manage your organization, teams, and settings"
                }
            },
            "your-organization/access-management": {
                "label": "Access Management",
                "position": 1,
                "link": {
                    "type": "generated-index",
                    "description": "Single sign-on and access control"
                }
            },
            "your-organization/administration": {
                "label": "Administration",
                "position": 2,
                "link": {
                    "type": "generated-index",
                    "description": "Subscription and administrative settings"
                }
            },
            "your-profile": {
                "label": "Your Profile",
                "position": 7,
                "link": {
                    "type": "generated-index",
                    "description": "Manage your profile and account settings"
                }
            },
            "developers": {
                "label": "Developers",
                "position": 8,
                "link": {
                    "type": "generated-index",
                    "description": "Developer resources and advanced features"
                }
            },
            "developers/make-ai-agents": {
                "label": "Make AI Agents",
                "position": 1,
                "link": {
                    "type": "generated-index",
                    "description": "AI agents and artificial intelligence features"
                }
            },
            "release-notes": {
                "label": "Release Notes",
                "position": 9,
                "link": {
                    "type": "generated-index",
                    "description": "Latest updates and release information"
                }
            },
            "release-notes/2024": {
                "label": "2024",
                "position": 2,
                "link": {
                    "type": "generated-index",
                    "description": "2024 release notes"
                }
            },
            "release-notes/2025": {
                "label": "2025",
                "position": 1,
                "link": {
                    "type": "generated-index",
                    "description": "2025 release notes"
                }
            }
        }
        
        print(f"\n📁 Creating proper category configuration files...")
        
        created_count = 0
        for category_path, config in category_configs.items():
            category_dir = Path("docs") / category_path
            
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
    
    def generate_improved_report(self):
        """Generate improved final report"""
        
        print(f"\n📋 IMPROVED CRAWLING REPORT")
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

def main():
    """Main function for improved crawling"""
    
    print("🚀 Improved Make.com Documentation Crawler")
    print("=" * 90)
    print("Properly structured crawling with correct directory hierarchy")
    print("=" * 90)
    
    # Initialize improved crawler
    crawler = ImprovedMakeCrawler()
    
    # Start improved crawling
    total_pages, successful_files = crawler.crawl_improved(max_pages=400)
    
    # Create proper category files
    category_count = crawler.create_proper_category_files()
    
    # Generate improved report
    crawler.generate_improved_report()
    
    print(f"\n🎉 IMPROVED CRAWLING SUCCESS!")
    print(f"📁 Documentation created in: {os.path.abspath('docs')}")
    print(f"📊 {successful_files} properly structured files from {total_pages} pages")
    print(f"📁 {category_count} categories configured with proper hierarchy")
    print(f"🌐 Ready for Docusaurus with correct structure!")
    
    print(f"\n💡 Next steps:")
    print(f"  1. Review the properly structured docs/ directory")
    print(f"  2. Notice the correct naming: 'Your Organization', 'Your Profile'")
    print(f"  3. Check multi-level directories like 'your-organization/access-management'")
    print(f"  4. Restart Docusaurus to see the improved structure!")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Script to scrape Make.com learn-the-basics page using crawl4ai and convert to markdown using Jina.ai
"""

import asyncio
import re
import os
import requests
from pathlib import Path
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from bs4 import BeautifulSoup
import yaml


async def scrape_with_crawl4ai(url):
    """Use crawl4ai to scrape the webpage"""
    
    print(f"🚀 Using crawl4ai to scrape: {url}")
    
    # Configure browser settings
    browser_config = BrowserConfig(
        headless=True,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    )
    
    # Configure crawler settings
    crawler_config = CrawlerRunConfig(
        word_count_threshold=10,
        page_timeout=30000,
        delay_before_return_html=3000,
        wait_for_content=True
    )
    
    async with AsyncWebCrawler(config=browser_config) as crawler:
        try:
            result = await crawler.arun(url=url, config=crawler_config)
            
            if result.success:
                print("✅ Successfully scraped with crawl4ai")
                return result.html
            else:
                print(f"❌ crawl4ai failed: {result.error_message}")
                return None
                
        except Exception as e:
            print(f"❌ Error with crawl4ai: {e}")
            return None


def convert_with_jina(url):
    """Use Jina.ai Reader API to convert webpage to markdown"""
    
    print(f"🤖 Using Jina.ai to convert: {url}")
    
    try:
        # Jina.ai Reader API endpoint
        jina_url = f"https://r.jina.ai/{url}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/plain, application/json'
        }
        
        # Make request to Jina.ai
        response = requests.get(jina_url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            print("✅ Successfully converted with Jina.ai")
            return response.text
        else:
            print(f"❌ Jina.ai API returned status: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error with Jina.ai: {e}")
        return None


def extract_content_from_html(html_content):
    """Extract main content from HTML as fallback"""
    
    if not html_content:
        return None
    
    print("🔧 Extracting content from HTML as fallback")
    
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "header", "footer"]):
            script.decompose()
        
        # Try different selectors for main content
        main_content = None
        selectors = [
            'main',
            'article', 
            '[role="main"]',
            '.content',
            '#content',
            '.main-content',
            '.page-content'
        ]
        
        for selector in selectors:
            main_content = soup.select_one(selector)
            if main_content:
                break
        
        if not main_content:
            main_content = soup.find('body') or soup
        
        # Extract text content
        text_content = main_content.get_text()
        
        # Clean up the text
        lines = text_content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if (line and 
                len(line) > 3 and 
                not line.startswith(('Skip to', 'Cookie', 'Privacy', 'Terms')) and
                line not in ['Home', 'About', 'Contact', 'Login', 'Sign up']):
                cleaned_lines.append(line)
        
        # Join lines and remove excessive whitespace
        content = '\n\n'.join(cleaned_lines)
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        print("✅ Successfully extracted content from HTML")
        return content
        
    except Exception as e:
        print(f"❌ Error extracting from HTML: {e}")
        return None


def create_docusaurus_file(content, filename="learn-the-basics.md"):
    """Create a Docusaurus-compatible markdown file"""
    
    if not content:
        print("❌ No content to write")
        return False
    
    print(f"📝 Creating Docusaurus file: {filename}")
    
    # Create frontmatter to match existing docs format
    frontmatter = {
        'sidebar_position': 1,
        'title': 'Learn the Basics',
        'description': 'Learn the basic concepts and fundamentals of Make.com automation platform'
    }
    
    # Create the complete file content
    file_content = "---\n"
    file_content += yaml.dump(frontmatter, default_flow_style=False)
    file_content += "---\n\n"
    
    # Add main heading if not present
    if not content.strip().startswith('#'):
        file_content += "# Learn the Basics\n\n"
    
    # Add the content
    file_content += content
    
    # Ensure docs directory exists
    docs_path = Path("docs")
    docs_path.mkdir(exist_ok=True)
    
    file_path = docs_path / filename
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(file_content)
        
        print(f"✅ Successfully created: {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return False


async def main():
    """Main function to run the scraping and conversion process"""
    
    url = "https://help.make.com/learn-the-basics"
    
    print("🚀 Starting Make.com content extraction...")
    print("=" * 60)
    print(f"Target URL: {url}")
    print("=" * 60)
    
    content = None
    
    # Method 1: Try Jina.ai first (fastest and cleanest)
    print("\n📖 Method 1: Using Jina.ai Reader API")
    content = convert_with_jina(url)
    
    # Method 2: If Jina.ai fails, use crawl4ai + manual extraction
    if not content:
        print("\n🕷️ Method 2: Using crawl4ai + manual extraction")
        html_content = await scrape_with_crawl4ai(url)
        
        if html_content:
            content = extract_content_from_html(html_content)
    
    # Create the documentation file
    if content:
        print(f"\n📊 Content length: {len(content)} characters")
        
        success = create_docusaurus_file(content)
        
        if success:
            print("\n🎉 SUCCESS! Created learn-the-basics.md")
            print(f"📁 File location: {os.path.abspath('docs/learn-the-basics.md')}")
            print("\n✨ File features:")
            print("  ✅ English language")
            print("  ✅ Docusaurus frontmatter") 
            print("  ✅ Markdown format")
            print("  ✅ Proper sidebar position")
            print("\n💡 The file is ready to be used in your Docusaurus site!")
        else:
            print("\n❌ Failed to create documentation file")
    else:
        print("\n❌ Failed to extract content from the website")
        print("💡 Please check your internet connection and try again")
    
    print("\n" + "=" * 60)
    print("🏁 Process completed")


if __name__ == "__main__":
    asyncio.run(main()) 
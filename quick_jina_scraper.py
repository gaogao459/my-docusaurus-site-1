#!/usr/bin/env python3
"""
Quick scraper using only Jina.ai to extract Make.com content
"""

import requests
import yaml
from pathlib import Path


def scrape_with_jina(url):
    """Use Jina.ai Reader API to convert webpage to markdown"""
    
    print(f"🤖 Using Jina.ai to extract content from: {url}")
    
    try:
        # Jina.ai Reader API endpoint
        jina_url = f"https://r.jina.ai/{url}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/plain'
        }
        
        print("📡 Making request to Jina.ai...")
        response = requests.get(jina_url, headers=headers, timeout=45)
        
        if response.status_code == 200:
            print("✅ Successfully extracted content with Jina.ai")
            return response.text
        else:
            print(f"❌ Jina.ai API returned status: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
            return None
            
    except Exception as e:
        print(f"❌ Error with Jina.ai: {e}")
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
    
    # Add the content (Jina.ai usually includes proper headings)
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


def main():
    """Main function"""
    
    url = "https://help.make.com/learn-the-basics"
    
    print("🚀 Quick Make.com content extraction with Jina.ai")
    print("=" * 55)
    print(f"Target: {url}")
    print("=" * 55)
    
    # Extract content with Jina.ai
    content = scrape_with_jina(url)
    
    if content:
        print(f"\n📊 Content length: {len(content)} characters")
        print(f"📊 Content preview: {content[:100]}...")
        
        # Create the documentation file
        success = create_docusaurus_file(content)
        
        if success:
            print("\n🎉 SUCCESS! Created learn-the-basics.md")
            print(f"📁 File location: {Path('docs/learn-the-basics.md').absolute()}")
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
    
    print("\n" + "=" * 55)
    print("🏁 Process completed")


if __name__ == "__main__":
    main() 
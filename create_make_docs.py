#!/usr/bin/env python3
"""
Complete script to extract Make.com content using Jina.ai and create Docusaurus documentation
"""

import requests
import yaml
import os
import re
from pathlib import Path

def extract_with_jina(url):
    """Extract content using Jina.ai Reader API"""
    
    jina_url = f"https://r.jina.ai/{url}"
    
    print(f"🤖 Extracting content with Jina.ai...")
    print(f"📍 Target: {url}")
    
    try:
        response = requests.get(jina_url, timeout=30)
        
        if response.status_code == 200:
            content = response.text
            print(f"✅ Success! Extracted {len(content)} characters")
            return content
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def clean_and_filter_content(content):
    """Clean and filter content to extract only title and main content"""
    
    if not content:
        return None
    
    print("🔧 Cleaning and filtering content...")
    
    # Split content into lines
    lines = content.split('\n')
    
    # Find the main content start (after the separator)
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
            
        # Skip navigation and metadata lines
        if (line and 
            not line.startswith(('[', 'Updated', 'PREVIOUS', 'NEXT', 'Docs powered')) and
            not line.endswith(('Hub', 'Community', 'Academy', 'Care', 'Center', 'Documentation')) and
            'Navigate through spaces' not in line and
            '⌘K' not in line and
            'Apps Documentation' not in line and
            line not in ['Get started', 'Key concepts', 'Tools', 'Resources', 'Explore more', 
                        'Scenarios', 'Connections', 'Functions', 'Data stores', 'Developers',
                        'Error handling', 'Your organization', 'Your profile', 'Release notes',
                        '2025', '2024', '×'] and
            not line.startswith('Make ') and
            len(line) > 3):
            content_lines.append(line)
    
    if not content_lines:
        return None
    
    # Process the content to create proper markdown structure
    processed_lines = []
    current_section = []
    
    for line in content_lines:
        # Check if this looks like a section title
        if (len(line) < 100 and 
            any(keyword in line.lower() for keyword in ['learn', 'basic', 'automation', 'what is', 'benefits']) and
            not line.startswith('[')):
            
            # If we have accumulated content, process it
            if current_section:
                processed_lines.extend(process_section(current_section))
                current_section = []
            
            # Add this as a heading
            if line.lower().startswith('learn the basics'):
                processed_lines.append(f"# {line}")
            elif any(keyword in line.lower() for keyword in ['what is', 'benefits']):
                processed_lines.append(f"## {line}")
            else:
                processed_lines.append(line)
        else:
            current_section.append(line)
    
    # Process any remaining content
    if current_section:
        processed_lines.extend(process_section(current_section))
    
    # Join and clean up
    final_content = '\n\n'.join([line for line in processed_lines if line.strip()])
    
    # Clean up excessive whitespace and normalize
    final_content = re.sub(r'\n{3,}', '\n\n', final_content)
    
    print(f"✅ Cleaned content: {len(final_content)} characters")
    return final_content

def process_section(section_lines):
    """Process a section of content lines"""
    if not section_lines:
        return []
    
    # Join lines and split into sentences for better formatting
    text = ' '.join(section_lines)
    
    # Split into sentences and reformat
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    # Group sentences into paragraphs (every 2-3 sentences)
    paragraphs = []
    current_paragraph = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence:
            current_paragraph.append(sentence)
            
            # Start new paragraph after 2-3 sentences or if sentence is long
            if len(current_paragraph) >= 2 or len(sentence) > 150:
                paragraphs.append(' '.join(current_paragraph))
                current_paragraph = []
    
    # Add any remaining content
    if current_paragraph:
        paragraphs.append(' '.join(current_paragraph))
    
    return paragraphs

def create_docusaurus_file(content, filename="learn-the-basics.md"):
    """Create Docusaurus-compatible markdown file"""
    
    if not content:
        print("❌ No content to write")
        return False
    
    print(f"📝 Creating Docusaurus file: {filename}")
    
    # Create frontmatter matching tutorial-extras format (only sidebar_position)
    frontmatter = {
        'sidebar_position': 1
    }
    
    # Build the complete file content
    file_content = "---\n"
    file_content += yaml.dump(frontmatter, default_flow_style=False)
    file_content += "---\n\n"
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
    
    print("🚀 Make.com Documentation Creator (Improved)")
    print("=" * 55)
    print("Using Jina.ai to extract clean title and content only")
    print("=" * 55)
    
    # Extract content
    raw_content = extract_with_jina(url)
    
    if not raw_content:
        print("\n❌ Failed to extract content")
        return
    
    # Clean and filter the content
    cleaned_content = clean_and_filter_content(raw_content)
    
    if not cleaned_content:
        print("\n❌ Failed to clean content")
        return
    
    # Preview the content
    print(f"\n📖 Content preview (first 500 chars):")
    print("-" * 50)
    print(cleaned_content[:500] + "...")
    print("-" * 50)
    
    # Create the Docusaurus file
    success = create_docusaurus_file(cleaned_content)
    
    if success:
        abs_path = os.path.abspath("docs/learn-the-basics.md")
        print(f"\n🎉 SUCCESS!")
        print(f"📁 File created: {abs_path}")
        
        print(f"\n✨ File specifications:")
        print(f"  ✅ Language: English")
        print(f"  ✅ Format: Markdown (.md)")
        print(f"  ✅ Simple frontmatter (sidebar_position only)")
        print(f"  ✅ Clean title and content only")
        print(f"  ✅ Matches tutorial-extras format")
        
        print(f"\n💡 The file is ready to use in your Docusaurus website!")
        print(f"💡 Content extracted from: {url}")
    else:
        print(f"\n❌ Failed to create the documentation file")
    
    print("\n" + "=" * 55)
    print("🏁 Process completed")

if __name__ == "__main__":
    main() 
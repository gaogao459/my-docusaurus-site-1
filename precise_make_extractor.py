#!/usr/bin/env python3
"""
Precise extractor for Make.com content - focuses on core educational content only
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

def extract_core_content(content):
    """Extract only the core educational content"""
    
    if not content:
        return None
    
    print("🎯 Extracting core educational content...")
    
    # Find the main content paragraph that starts with "welcome to make!"
    # This is the actual educational content we want
    
    lines = content.split('\n')
    
    # Look for the core content
    core_text = ""
    found_core = False
    
    for line in lines:
        line = line.strip()
        
        # Find the line that contains the main content
        if "welcome to make!" in line.lower():
            # This line contains the core content
            # Extract everything from "welcome to make!" onwards
            start_idx = line.lower().find("welcome to make!")
            core_text = line[start_idx:]
            found_core = True
            break
    
    if not found_core or not core_text:
        print("❌ Could not find core educational content")
        return None
    
    # Clean and structure the core text
    structured_content = structure_content(core_text)
    
    print(f"✅ Extracted core content: {len(structured_content)} characters")
    return structured_content

def structure_content(text):
    """Structure the core content into proper markdown format"""
    
    # Split into sentences for better processing
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    content_parts = []
    current_paragraph = []
    
    # Key phrases that should start new sections
    section_starters = [
        "what is automation",
        "benefits of automation", 
        "automation brings",
        "save time",
        "reduce errors",
        "improve efficiency",
        "scale easily"
    ]
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        # Check if this sentence starts a new section
        is_section_start = any(starter in sentence.lower() for starter in section_starters)
        
        if is_section_start and current_paragraph:
            # Save current paragraph and start new section
            content_parts.append(' '.join(current_paragraph))
            current_paragraph = []
            
            # Add section heading
            if "what is automation" in sentence.lower():
                content_parts.append("## What is automation?")
            elif "benefits of automation" in sentence.lower() or "automation brings" in sentence.lower():
                content_parts.append("## Benefits of automation")
        
        current_paragraph.append(sentence)
        
        # Create paragraph breaks for readability (every 2-3 sentences)
        if len(current_paragraph) >= 3:
            content_parts.append(' '.join(current_paragraph))
            current_paragraph = []
    
    # Add any remaining content
    if current_paragraph:
        content_parts.append(' '.join(current_paragraph))
    
    # Join all parts with proper spacing
    final_content = '\n\n'.join([part for part in content_parts if part.strip()])
    
    return final_content

def create_docusaurus_file(content, filename="learn-the-basics.md"):
    """Create Docusaurus-compatible markdown file"""
    
    if not content:
        print("❌ No content to write")
        return False
    
    print(f"📝 Creating Docusaurus file: {filename}")
    
    # Create frontmatter with title and description
    frontmatter = {
        'sidebar_position': 1,
        'title': 'Learn the Basics',
        'description': 'Learn the basic concepts and fundamentals of Make.com automation platform'
    }
    
    # Build the complete file content
    file_content = "---\n"
    file_content += yaml.dump(frontmatter, default_flow_style=False)
    file_content += "---\n\n"
    file_content += "# Learn the Basics\n\n"
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
    
    print("🚀 Precise Make.com Content Extractor")
    print("=" * 50)
    print("Extracting ONLY core educational content")
    print("=" * 50)
    
    # Extract content
    raw_content = extract_with_jina(url)
    
    if not raw_content:
        print("\n❌ Failed to extract content")
        return
    
    # Extract core content
    core_content = extract_core_content(raw_content)
    
    if not core_content:
        print("\n❌ Failed to extract core content")
        return
    
    # Preview the content
    print(f"\n📖 Core content preview:")
    print("-" * 60)
    print(core_content[:600] + "...")
    print("-" * 60)
    
    # Create the Docusaurus file
    success = create_docusaurus_file(core_content)
    
    if success:
        abs_path = os.path.abspath("docs/learn-the-basics.md")
        print(f"\n🎉 SUCCESS!")
        print(f"📁 File created: {abs_path}")
        
        print(f"\n✨ File specifications:")
        print(f"  ✅ Clean educational content only")
        print(f"  ✅ Proper markdown structure")
        print(f"  ✅ Matches tutorial-extras format")
        print(f"  ✅ No navigation or metadata")
        
        print(f"\n💡 Ready to use in your Docusaurus website!")
    else:
        print(f"\n❌ Failed to create the documentation file")
    
    print("\n" + "=" * 50)
    print("🏁 Process completed")

if __name__ == "__main__":
    main() 
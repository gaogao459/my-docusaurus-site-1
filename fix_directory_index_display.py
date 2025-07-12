#!/usr/bin/env python3

import os
import json

def fix_learn_basics_index():
    """Fix the learn-the-basics directory to properly display index.md as the category page"""
    print("🔧 Fixing learn-the-basics directory index display...")
    
    # Fix 1: Update _category_.json to not generate an index automatically
    category_file = "docs/get-started/learn-the-basics/_category_.json"
    if os.path.exists(category_file):
        category_config = {
            "label": "Learn the Basics",
            "position": 1
        }
        # Remove the "link" configuration so it uses index.md instead
        
        with open(category_file, 'w', encoding='utf-8') as f:
            json.dump(category_config, f, indent=2)
        print(f"✅ Updated: {category_file}")
    
    # Fix 2: Update index.md to have a different title or no title in frontmatter
    index_file = "docs/get-started/learn-the-basics/index.md"
    if os.path.exists(index_file):
        with open(index_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Method 1: Remove title from frontmatter, let it use the category label
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter_lines = parts[1].strip().split('\n')
                body = parts[2]
                
                # Keep only sidebar_position, remove title
                new_frontmatter_lines = []
                for line in frontmatter_lines:
                    if line.strip() and not line.strip().startswith('title:'):
                        new_frontmatter_lines.append(line)
                
                # Add custom slug if needed
                new_frontmatter_lines.append('slug: /get-started/learn-the-basics')
                
                new_content = f"""---
{chr(10).join(new_frontmatter_lines)}
---{body}"""
                
                with open(index_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"✅ Updated: {index_file} (removed title from frontmatter)")
    
    print("\n🎉 Learn the basics index display fixed!")
    print("Now the index.md content will display when clicking 'Learn the Basics'")

def fix_all_category_indexes():
    """Fix all category directories to properly display their index pages"""
    print("\n🔧 Fixing all category index displays...")
    
    categories = [
        {
            "dir": "docs/get-started/create-your-first-scenario",
            "label": "Create Your First Scenario",
            "position": 2
        },
        {
            "dir": "docs/get-started/expand-your-scenario", 
            "label": "Expand Your Scenario",
            "position": 3
        }
    ]
    
    for cat in categories:
        cat_file = f"{cat['dir']}/_category_.json"
        index_file = f"{cat['dir']}/index.md"
        
        # Update category file
        if os.path.exists(cat_file):
            category_config = {
                "label": cat['label'],
                "position": cat['position']
            }
            with open(cat_file, 'w', encoding='utf-8') as f:
                json.dump(category_config, f, indent=2)
            print(f"✅ Updated: {cat_file}")
        
        # Update index file
        if os.path.exists(index_file):
            with open(index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter_lines = parts[1].strip().split('\n')
                    body = parts[2]
                    
                    # Keep only sidebar_position, remove title
                    new_frontmatter_lines = []
                    for line in frontmatter_lines:
                        if line.strip() and not line.strip().startswith('title:'):
                            new_frontmatter_lines.append(line)
                    
                    new_content = f"""---
{chr(10).join(new_frontmatter_lines)}
---{body}"""
                    
                    with open(index_file, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"✅ Updated: {index_file}")

def main():
    """Fix directory index display issues"""
    print("🎯 Fixing directory index display issues...")
    print("=" * 60)
    
    fix_learn_basics_index()
    fix_all_category_indexes()
    
    print(f"\n✨ All index displays fixed!")
    print("Now each directory will show its index.md content instead of auto-generated indexes")

if __name__ == "__main__":
    main() 
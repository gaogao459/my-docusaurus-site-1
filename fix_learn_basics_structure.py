#!/usr/bin/env python3

import os
import shutil
import json

def fix_learn_basics_structure():
    """Fix the learn-the-basics structure to match Make.com's actual layout"""
    print("🔧 Fixing learn-the-basics structure...")
    
    # Current structure problem:
    # get-started/
    #   learn-the-basics/
    #     index.md (title: "Learn the basics")
    #     what-is-make.md
    #     whats-an-api.md
    
    # Should be:
    # get-started/
    #   learn-the-basics.md (single page)
    #   what-is-make.md (separate page)
    #   whats-an-api.md (separate page)
    
    # Step 1: Move index.md to become learn-the-basics.md
    src_index = "docs/get-started/learn-the-basics/index.md"
    dst_learn_basics = "docs/get-started/learn-the-basics.md"
    
    if os.path.exists(src_index):
        # Read the content and update the sidebar_position
        with open(src_index, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update frontmatter to have position 1
        content = content.replace('sidebar_position: 1', 'sidebar_position: 1')
        
        # Write to new location
        with open(dst_learn_basics, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Moved: {src_index} -> {dst_learn_basics}")
    
    # Step 2: Move other files to get-started root
    files_to_move = [
        ("docs/get-started/learn-the-basics/what-is-make.md", "docs/get-started/what-is-make.md", 2),
        ("docs/get-started/learn-the-basics/whats-an-api.md", "docs/get-started/whats-an-api.md", 3)
    ]
    
    for src, dst, position in files_to_move:
        if os.path.exists(src):
            # Read content and update position
            with open(src, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Update sidebar_position
            if 'sidebar_position:' in content:
                content = re.sub(r'sidebar_position:\s*\d+', f'sidebar_position: {position}', content)
            else:
                # Add sidebar_position if not present
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        frontmatter = parts[1].strip()
                        body = parts[2]
                        frontmatter += f'\nsidebar_position: {position}'
                        content = f"---\n{frontmatter}\n---{body}"
            
            # Write to new location
            with open(dst, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Moved: {src} -> {dst}")
    
    # Step 3: Remove the empty learn-the-basics directory
    learn_basics_dir = "docs/get-started/learn-the-basics"
    if os.path.exists(learn_basics_dir):
        shutil.rmtree(learn_basics_dir)
        print(f"✅ Removed directory: {learn_basics_dir}")
    
    # Step 4: Update positions of other subdirectories
    subdirs = [
        ("docs/get-started/create-your-first-scenario/_category_.json", 4),
        ("docs/get-started/expand-your-scenario/_category_.json", 5)
    ]
    
    for cat_file, position in subdirs:
        if os.path.exists(cat_file):
            with open(cat_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            config['position'] = position
            with open(cat_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            print(f"✅ Updated position {position}: {cat_file}")
    
    print("\n🎉 Structure fixed!")
    print("New structure:")
    print("get-started/")
    print("├── _category_.json")
    print("├── get-started.md")
    print("├── learn-the-basics.md (position: 1)")
    print("├── what-is-make.md (position: 2)")  
    print("├── whats-an-api.md (position: 3)")
    print("├── create-your-first-scenario/ (position: 4)")
    print("└── expand-your-scenario/ (position: 5)")

if __name__ == "__main__":
    import re
    fix_learn_basics_structure() 
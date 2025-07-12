#!/usr/bin/env python3

import os
import shutil
import json
import re

def create_category_json(path, label, position=1):
    """Create a _category_.json file"""
    category_config = {
        "label": label,
        "position": position
    }
    
    os.makedirs(path, exist_ok=True)
    category_file = os.path.join(path, "_category_.json")
    with open(category_file, 'w', encoding='utf-8') as f:
        json.dump(category_config, f, indent=2)
    print(f"Created: {category_file}")

def add_frontmatter_position(file_path, position):
    """Add position to frontmatter of a markdown file"""
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if frontmatter exists
    if content.startswith('---'):
        # Split frontmatter and content
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1].strip()
            body = parts[2]
            
            # Add position if not already present
            if 'sidebar_position:' not in frontmatter:
                frontmatter += f'\nsidebar_position: {position}'
            else:
                # Update existing position
                frontmatter = re.sub(r'sidebar_position:\s*\d+', f'sidebar_position: {position}', frontmatter)
            
            new_content = f"---\n{frontmatter}\n---{body}"
        else:
            new_content = content
    else:
        # Add frontmatter if it doesn't exist
        new_content = f"""---
sidebar_position: {position}
---

{content}"""
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated position {position}: {file_path}")

def fix_learn_the_basics():
    """Convert learn-the-basics.md to a directory structure"""
    print("Converting learn-the-basics to directory structure...")
    
    # Create the learn-the-basics directory
    learn_basics_dir = "docs/get-started/learn-the-basics"
    create_category_json(learn_basics_dir, "Learn the Basics", 1)
    
    # Move the current file to index.md
    src_file = "docs/get-started/learn-the-basics.md"
    if os.path.exists(src_file):
        dst_file = f"{learn_basics_dir}/index.md"
        shutil.move(src_file, dst_file)
        print(f"Moved: {src_file} -> {dst_file}")
        
        # Add position to the index file
        add_frontmatter_position(dst_file, 1)
    
    # Create additional pages that typically exist in "Learn the basics"
    additional_pages = [
        ("what-is-make.md", "What is Make?", 2),
        ("whats-an-api.md", "What's an API?", 3)
    ]
    
    for filename, title, position in additional_pages:
        page_path = f"{learn_basics_dir}/{filename}"
        if not os.path.exists(page_path):
            # Create a placeholder page
            content = f"""---
title: "{title}"
sidebar_position: {position}
---

# {title}

This page covers {title.lower()} concepts in Make.com automation.

(Content to be added from Make.com help center)
"""
            with open(page_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Created: {page_path}")

def order_create_scenario_steps():
    """Add proper ordering to create-your-first-scenario step files"""
    print("Adding proper ordering to create-your-first-scenario steps...")
    
    scenario_dir = "docs/get-started/create-your-first-scenario"
    
    # Define the correct order for step files
    step_files = [
        ("index.md", 1),
        ("step-1-plan-your-scenario.md", 2),
        ("step-2-get-your-apps-ready.md", 3),
        ("step-3-add-your-first-app.md", 4),
        ("step-4-create-a-connection.md", 5),
        ("step-6-test-the-module.md", 6),  # Note: step-5 might be missing
        ("step-7-add-another-module.md", 7),
        ("step-8-map-data.md", 8),
        ("step-9-test-your-scenario.md", 9),
        ("step-10-schedule-your-scenario.md", 10)
    ]
    
    for filename, position in step_files:
        file_path = f"{scenario_dir}/{filename}"
        add_frontmatter_position(file_path, position)

def order_expand_scenario_steps():
    """Add proper ordering to expand-your-scenario step files"""
    print("Adding proper ordering to expand-your-scenario steps...")
    
    scenario_dir = "docs/get-started/expand-your-scenario"
    
    # Define the correct order for step files
    step_files = [
        ("index.md", 1),
        ("step-1-get-your-app-ready.md", 2),
        ("step-1-set-up-the-ai-agent.md", 3),
        ("step-2-add-a-router.md", 4),
        ("step-3-create-a-scenario-to-send-tasks-to-the-ai-agent.md", 5),
        ("step-3-set-up-another-module.md", 6),
        ("step-6-add-an-aggregator.md", 7),
        ("step-7-test-the-final-scenario.md", 8)
    ]
    
    for filename, position in step_files:
        file_path = f"{scenario_dir}/{filename}"
        add_frontmatter_position(file_path, position)

def update_subdirectory_positions():
    """Update the positions of subdirectories in get-started"""
    print("Updating subdirectory positions...")
    
    # Update learn-the-basics position
    learn_basics_cat = "docs/get-started/learn-the-basics/_category_.json"
    if os.path.exists(learn_basics_cat):
        with open(learn_basics_cat, 'r', encoding='utf-8') as f:
            config = json.load(f)
        config['position'] = 1
        with open(learn_basics_cat, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        print(f"Updated position for learn-the-basics: 1")
    
    # Update create-your-first-scenario position
    create_cat = "docs/get-started/create-your-first-scenario/_category_.json"
    if os.path.exists(create_cat):
        with open(create_cat, 'r', encoding='utf-8') as f:
            config = json.load(f)
        config['position'] = 2
        with open(create_cat, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        print(f"Updated position for create-your-first-scenario: 2")
    
    # Update expand-your-scenario position
    expand_cat = "docs/get-started/expand-your-scenario/_category_.json"
    if os.path.exists(expand_cat):
        with open(expand_cat, 'r', encoding='utf-8') as f:
            config = json.load(f)
        config['position'] = 3
        with open(expand_cat, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        print(f"Updated position for expand-your-scenario: 3")

def main():
    """Main function to fix structure and ordering"""
    print("Fixing get-started directory structure and ordering...")
    print("=" * 60)
    
    # 1. Fix learn-the-basics structure
    fix_learn_the_basics()
    print()
    
    # 2. Add ordering to step files
    order_create_scenario_steps()
    print()
    order_expand_scenario_steps()
    print()
    
    # 3. Update subdirectory positions
    update_subdirectory_positions()
    
    print("\n" + "=" * 60)
    print("Structure and ordering fixes completed!")
    print("\nNew structure:")
    print("get-started/")
    print("├── _category_.json")
    print("├── get-started.md")
    print("├── learn-the-basics/ (position: 1)")
    print("│   ├── _category_.json")
    print("│   ├── index.md (position: 1)")
    print("│   ├── what-is-make.md (position: 2)")
    print("│   └── whats-an-api.md (position: 3)")
    print("├── create-your-first-scenario/ (position: 2)")
    print("│   ├── _category_.json")
    print("│   ├── index.md (position: 1)")
    print("│   ├── step-1-plan-your-scenario.md (position: 2)")
    print("│   ├── step-2-get-your-apps-ready.md (position: 3)")
    print("│   └── ... (ordered steps)")
    print("└── expand-your-scenario/ (position: 3)")
    print("    ├── _category_.json")
    print("    ├── index.md (position: 1)")
    print("    └── ... (ordered steps)")

if __name__ == "__main__":
    main() 
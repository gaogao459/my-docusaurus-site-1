#!/usr/bin/env python3

import os
import shutil
import glob
import json

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

def move_file(src, dst):
    """Move a file from src to dst"""
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.move(src, dst)
    print(f"Moved: {src} -> {dst}")

def reorganize_get_started():
    """Reorganize the get-started directory structure"""
    print("Reorganizing get-started directory structure...")
    
    # Create subdirectories
    create_first_scenario_dir = "docs/get-started/create-your-first-scenario"
    expand_scenario_dir = "docs/get-started/expand-your-scenario"
    
    # Create category files for subdirectories
    create_category_json(create_first_scenario_dir, "Create Your First Scenario", 2)
    create_category_json(expand_scenario_dir, "Expand Your Scenario", 3)
    
    # Files that belong to "Create your first scenario" tutorial
    create_scenario_files = [
        "create-your-first-scenario.md",  # This becomes index.md
        "step-1-plan-your-scenario.md",
        "step-2-get-your-apps-ready.md", 
        "step-3-add-your-first-app.md",
        "step-4-create-a-connection.md",
        "step-6-test-the-module.md",
        "step-7-add-another-module.md",
        "step-8-map-data.md",
        "step-9-test-your-scenario.md",
        "step-10-schedule-your-scenario.md"
    ]
    
    # Files that belong to "Expand your scenario" tutorial  
    expand_scenario_files = [
        "expand-your-scenario.md",  # This becomes index.md
        "step-1-get-your-app-ready.md",
        "step-1-set-up-the-ai-agent.md", 
        "step-2-add-a-router.md",
        "step-3-create-a-scenario-to-send-tasks-to-the-ai-agent.md",
        "step-3-set-up-another-module.md",
        "step-6-add-an-aggregator.md",
        "step-7-test-the-final-scenario.md"
    ]
    
    # Move "Create your first scenario" files
    for filename in create_scenario_files:
        src = f"docs/get-started/{filename}"
        if os.path.exists(src):
            if filename == "create-your-first-scenario.md":
                # Main tutorial file becomes index.md
                dst = f"{create_first_scenario_dir}/index.md"
            else:
                dst = f"{create_first_scenario_dir}/{filename}"
            move_file(src, dst)
        else:
            print(f"File not found: {src}")
    
    # Move "Expand your scenario" files  
    for filename in expand_scenario_files:
        src = f"docs/get-started/{filename}"
        if os.path.exists(src):
            if filename == "expand-your-scenario.md":
                # Main tutorial file becomes index.md
                dst = f"{expand_scenario_dir}/index.md"
            else:
                dst = f"{expand_scenario_dir}/{filename}"
            move_file(src, dst)
        else:
            print(f"File not found: {src}")
    
    # Update the main get-started _category_.json to adjust positions
    remaining_files = ["learn-the-basics.md", "get-started.md"]
    
    print("\nReorganization completed!")
    print("\nNew structure:")
    print("get-started/")
    print("├── _category_.json")
    print("├── learn-the-basics.md (position 1)")
    print("├── create-your-first-scenario/ (position 2)")
    print("│   ├── _category_.json") 
    print("│   ├── index.md")
    print("│   ├── step-1-plan-your-scenario.md")
    print("│   ├── step-2-get-your-apps-ready.md")
    print("│   └── ... (other step files)")
    print("└── expand-your-scenario/ (position 3)")
    print("    ├── _category_.json")
    print("    ├── index.md") 
    print("    └── ... (other step files)")

def check_remaining_files():
    """Check what files are left in get-started root"""
    remaining = glob.glob("docs/get-started/*.md")
    if remaining:
        print(f"\nRemaining files in get-started root:")
        for f in remaining:
            print(f"  - {os.path.basename(f)}")
    else:
        print("\nAll files have been organized into subdirectories!")

if __name__ == "__main__":
    reorganize_get_started()
    check_remaining_files() 
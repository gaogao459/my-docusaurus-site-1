#!/usr/bin/env python3
"""
Fix category display by adding _category_.json files to all documentation categories
"""

import json
import os
from pathlib import Path

def create_category_configs():
    """Create _category_.json files for all documentation categories"""
    
    # Define category configurations
    category_configs = {
        "get-started": {
            "label": "Get Started",
            "position": 1,
            "link": {
                "type": "generated-index",
                "description": "Step-by-step guide to building your first Make.com automation"
            }
        },
        "key-concepts": {
            "label": "Key Concepts", 
            "position": 2,
            "link": {
                "type": "generated-index",
                "description": "Learn the fundamental concepts of Make.com automation platform"
            }
        },
        "error-handling": {
            "label": "Error Handling",
            "position": 3,
            "link": {
                "type": "generated-index", 
                "description": "Learn how to handle errors and keep your scenarios running smoothly"
            }
        },
        "developers": {
            "label": "Developers",
            "position": 4,
            "link": {
                "type": "generated-index",
                "description": "Developer resources and advanced features for Make.com"
            }
        },
        "organization": {
            "label": "Organization",
            "position": 5,
            "link": {
                "type": "generated-index",
                "description": "Manage your organization, teams, and settings"
            }
        },
        "tutorials": {
            "label": "Tutorials",
            "position": 6,
            "link": {
                "type": "generated-index",
                "description": "Step-by-step tutorials and walkthroughs"
            }
        },
        "misc": {
            "label": "Additional Resources",
            "position": 7,
            "link": {
                "type": "generated-index",
                "description": "Additional documentation and resources"
            }
        }
    }
    
    print("🔧 Fixing category display by adding _category_.json files")
    print("=" * 60)
    
    docs_dir = Path("docs")
    created_count = 0
    
    # Check each category directory
    for category_name, config in category_configs.items():
        category_dir = docs_dir / category_name
        
        if category_dir.exists() and category_dir.is_dir():
            # Create _category_.json file
            category_file = category_dir / "_category_.json"
            
            try:
                with open(category_file, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2)
                
                print(f"✅ Created: {category_file}")
                created_count += 1
                
            except Exception as e:
                print(f"❌ Error creating {category_file}: {e}")
        else:
            print(f"⚠️ Directory not found: {category_dir}")
    
    print(f"\n📊 Summary:")
    print(f"  ✅ Created {created_count} category configuration files")
    print(f"  🌐 Categories now properly configured for Docusaurus")
    
    return created_count

def list_current_structure():
    """List the current documentation structure"""
    
    print(f"\n📁 Current documentation structure:")
    print("=" * 50)
    
    docs_dir = Path("docs")
    
    for item in sorted(docs_dir.iterdir()):
        if item.is_dir() and not item.name.startswith(('.', '_')):
            print(f"\n📂 {item.name}/")
            
            # Check for _category_.json
            category_file = item / "_category_.json"
            if category_file.exists():
                try:
                    with open(category_file, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    print(f"  📋 Label: {config.get('label', 'N/A')}")
                    print(f"  📍 Position: {config.get('position', 'N/A')}")
                except:
                    print(f"  ❌ Invalid _category_.json")
            else:
                print(f"  ❌ Missing _category_.json")
            
            # List markdown files
            md_files = sorted([f for f in item.iterdir() if f.suffix == '.md'])
            for i, md_file in enumerate(md_files, 1):
                print(f"    {i}. {md_file.stem.replace('-', ' ').title()}")

def main():
    """Main function to fix category display"""
    
    print("🚀 Make.com Documentation Category Display Fixer")
    print("=" * 65)
    print("Adding _category_.json files for proper Docusaurus display")
    print("=" * 65)
    
    # Show current structure
    list_current_structure()
    
    # Create category configurations
    created_count = create_category_configs()
    
    # Show updated structure
    print(f"\n🔄 Updated structure:")
    list_current_structure()
    
    if created_count > 0:
        print(f"\n🎉 SUCCESS!")
        print(f"📁 Added {created_count} category configuration files")
        print(f"🌐 Documentation categories now properly configured")
        
        print(f"\n💡 Next steps:")
        print(f"  1. Restart your Docusaurus server")
        print(f"  2. Check the sidebar - categories should now display correctly")
        print(f"  3. Each category will have its own index page")
    else:
        print(f"\n⚠️ No category files were created")
        print(f"💡 Make sure you have the correct documentation directories")

if __name__ == "__main__":
    main() 
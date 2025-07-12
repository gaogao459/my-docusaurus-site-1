#!/usr/bin/env python3
"""
Remove duplicate category files that conflict with _category_.json generated-index
"""

import os
from pathlib import Path

def remove_duplicate_category_files():
    """Remove category files that are duplicated by _category_.json"""
    
    print("🧹 Removing duplicate category files")
    print("=" * 50)
    
    docs_dir = Path("docs")
    
    # List of category directories that should use generated-index only
    categories_to_clean = [
        "get-started",
        "key-concepts", 
        "error-handling",
        "developers",
        "organization",
        "tutorials",
        "misc"
    ]
    
    removed_files = []
    
    for category in categories_to_clean:
        category_dir = docs_dir / category
        
        if not category_dir.exists():
            print(f"⚠️ Directory not found: {category_dir}")
            continue
            
        # Check if there's a _category_.json file
        category_json = category_dir / "_category_.json"
        if not category_json.exists():
            print(f"⚠️ No _category_.json found in: {category_dir}")
            continue
        
        # Look for the duplicate markdown file with the same name as the category
        duplicate_file = category_dir / f"{category}.md"
        
        if duplicate_file.exists():
            try:
                # Show what we're about to remove
                print(f"🗑️ Removing duplicate: {duplicate_file}")
                
                # Read the content to show what we're removing
                with open(duplicate_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = len(content.split('\n'))
                    chars = len(content)
                
                print(f"   📄 File size: {lines} lines, {chars} characters")
                
                # Remove the file
                duplicate_file.unlink()
                removed_files.append(str(duplicate_file))
                
                print(f"   ✅ Successfully removed")
                
            except Exception as e:
                print(f"   ❌ Error removing {duplicate_file}: {e}")
        else:
            print(f"✅ No duplicate found in: {category_dir}")
    
    print(f"\n📊 Summary:")
    print(f"  🗑️ Removed {len(removed_files)} duplicate files")
    
    if removed_files:
        print(f"  📝 Removed files:")
        for file in removed_files:
            print(f"    - {file}")
    
    return len(removed_files)

def show_clean_structure():
    """Show the cleaned structure"""
    
    print(f"\n📁 Cleaned documentation structure:")
    print("=" * 50)
    
    docs_dir = Path("docs")
    
    for item in sorted(docs_dir.iterdir()):
        if item.is_dir() and not item.name.startswith(('.', '_')):
            print(f"\n📂 {item.name}/")
            
            # Check for _category_.json
            category_file = item / "_category_.json"
            if category_file.exists():
                print(f"  📋 Has _category_.json (will generate index page)")
            else:
                print(f"  ❌ Missing _category_.json")
            
            # List markdown files (excluding category duplicates)
            md_files = sorted([f for f in item.iterdir() 
                             if f.suffix == '.md' and f.stem != item.name])
            
            if md_files:
                print(f"  📄 Documents:")
                for i, md_file in enumerate(md_files, 1):
                    print(f"    {i}. {md_file.stem.replace('-', ' ').title()}")
            else:
                print(f"  📄 No documents yet")

def main():
    """Main function to clean duplicate category files"""
    
    print("🧹 Documentation Duplicate File Cleaner")
    print("=" * 55)
    print("Removing category files that conflict with generated-index")
    print("=" * 55)
    
    # Remove duplicates
    removed_count = remove_duplicate_category_files()
    
    # Show clean structure
    show_clean_structure()
    
    if removed_count > 0:
        print(f"\n🎉 SUCCESS!")
        print(f"🗑️ Removed {removed_count} duplicate category files")
        print(f"📁 Categories now use generated-index only")
        
        print(f"\n💡 What this means:")
        print(f"  ✅ Each category will show an auto-generated index page")
        print(f"  ✅ Index pages list all documents in that category")
        print(f"  ✅ No more duplicate 'Get Started' pages")
        print(f"  ✅ Structure matches the original Make.com layout")
        
        print(f"\n🔄 Next steps:")
        print(f"  1. Refresh your browser at http://localhost:3001/")
        print(f"  2. Click on 'Get Started' - it should show the index page")
        print(f"  3. Each category will list its sub-documents properly")
    else:
        print(f"\n✨ All clean! No duplicate files found")

if __name__ == "__main__":
    main() 
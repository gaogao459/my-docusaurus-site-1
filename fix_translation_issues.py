#!/usr/bin/env python3
"""
修复翻译问题的脚本：
1. 翻译失败的文件
2. 翻译 front-matter 中的标题
3. 翻译 _category_.json 文件
"""

import os
import asyncio
import json
import re
import yaml
from pathlib import Path
from Reflection_Workflow_XAI import translate_text

# 标题翻译词典
TITLE_TRANSLATIONS = {
    "Get Started": "开始使用",
    "Learn the basics": "学习基础知识", 
    "What is Make?": "什么是 Make？",
    "What's an API?": "什么是 API？",
    "Create your first scenario": "创建你的第一个场景",
    "Expand your scenario": "扩展你的场景",
    "Step 1. Plan your scenario": "步骤 1. 规划你的场景",
    "Step 2. Get your apps ready": "步骤 2. 准备你的应用",
    "Step 3. Add your first app": "步骤 3. 添加你的第一个应用",
    "Step 4. Create a connection": "步骤 4. 创建连接",
    "Step 6. Test the module": "步骤 6. 测试模块",
    "Step 7. Add another module": "步骤 7. 添加另一个模块",
    "Step 8. Map data": "步骤 8. 映射数据",
    "Step 9. Test your scenario": "步骤 9. 测试你的场景",
    "Step 10. Schedule your scenario": "步骤 10. 安排你的场景",
    "Step 1. Get your app ready": "步骤 1. 准备你的应用",
    "Step 2. Add a router": "步骤 2. 添加路由器",
    "Step 3. Set up another module": "步骤 3. 设置另一个模块",
    "Step 4. Add a filter": "步骤 4. 添加过滤器",
    "Step 5. Test your scenario": "步骤 5. 测试你的场景",
    "Step 6. Add an aggregator": "步骤 6. 添加聚合器",
    "Step 7. Test the final scenario": "步骤 7. 测试最终场景",
}

async def translate_failed_file():
    """翻译失败的文件"""
    file_path = Path("docs/get-started/expand-your-scenario/step-1-get-your-app-ready.md")
    
    if not file_path.exists():
        print(f"❌ 文件不存在: {file_path}")
        return False
    
    print(f"🔄 翻译失败的文件: {file_path}")
    
    try:
        # 读取文件
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 分离 front-matter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = f"---{parts[1]}---"
                body = parts[2].strip()
            else:
                frontmatter = ""
                body = content
        else:
            frontmatter = ""
            body = content
        
        # 翻译正文
        result = await translate_text(
            source_text=body,
            source_lang="English",
            target_lang="Chinese",
            model="grok-3-mini"
        )
        
        translated_body = result["final_translation"]
        
        # 清理翻译结果
        cleaned_translation = clean_translation_artifacts(translated_body)
        
        # 重新组合
        final_content = frontmatter + "\n\n" + cleaned_translation if frontmatter else cleaned_translation
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(final_content)
        
        print(f"✅ 翻译完成: {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ 翻译失败: {e}")
        return False

def clean_translation_artifacts(text: str) -> str:
    """清理翻译说明文字"""
    patterns = [
        r'(?i)below is my.*?translation.*?(?=\n\n|\n#|\n\*|\Z)',
        r'(?i)here is.*?translation.*?(?=\n\n|\n#|\n\*|\Z)',
        r'(?i)sure,? here.*?(?=\n\n|\n#|\n\*|\Z)',
        r'以下是.*?翻译.*?(?=\n\n|\n#|\n\*|\Z)',
        r'### Improvement Suggestions.*?(?=\n#|\Z)',
        r'### 优化说明.*?(?=\n#|\Z)',
    ]
    
    cleaned = text
    for pattern in patterns:
        cleaned = re.sub(pattern, '', cleaned, flags=re.DOTALL | re.MULTILINE)
    
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
    return cleaned.strip()

def translate_frontmatter_titles():
    """翻译所有 markdown 文件的 front-matter 标题"""
    print("🔄 翻译 front-matter 标题...")
    
    docs_dir = Path("docs/get-started")
    count = 0
    
    for md_file in docs_dir.rglob("*.md"):
        if md_file.name.startswith('_'):
            continue
            
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not content.startswith('---'):
                continue
            
            parts = content.split('---', 2)
            if len(parts) < 3:
                continue
            
            # 解析 front-matter
            fm_content = parts[1].strip()
            body = parts[2]
            
            # 使用 yaml 解析
            try:
                fm_data = yaml.safe_load(fm_content)
                if not isinstance(fm_data, dict):
                    continue
                
                # 翻译标题
                if 'title' in fm_data:
                    original_title = fm_data['title'].strip('"\'')
                    if original_title in TITLE_TRANSLATIONS:
                        fm_data['title'] = TITLE_TRANSLATIONS[original_title]
                        
                        # 重新生成 front-matter
                        new_fm = yaml.dump(fm_data, default_flow_style=False, allow_unicode=True)
                        new_content = f"---\n{new_fm}---{body}"
                        
                        # 写回文件
                        with open(md_file, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        
                        print(f"✅ 翻译标题: {md_file.name} - {original_title} -> {TITLE_TRANSLATIONS[original_title]}")
                        count += 1
                    else:
                        print(f"⚠️  未找到翻译: {md_file.name} - {original_title}")
                        
            except yaml.YAMLError as e:
                print(f"❌ YAML 解析错误: {md_file} - {e}")
                continue
                
        except Exception as e:
            print(f"❌ 处理文件错误: {md_file} - {e}")
            continue
    
    print(f"📊 共翻译了 {count} 个标题")

def translate_category_files():
    """翻译 _category_.json 文件"""
    print("🔄 翻译分类文件...")
    
    category_translations = {
        "Get Started": "开始使用",
        "Start your automation journey with Make.com": "开始您的 Make.com 自动化之旅",
        "Learn the basics": "学习基础知识",
        "Create your first scenario": "创建你的第一个场景",
        "Expand your scenario": "扩展你的场景"
    }
    
    docs_dir = Path("docs/get-started")
    count = 0
    
    for category_file in docs_dir.rglob("_category_.json"):
        try:
            with open(category_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            modified = False
            
            # 翻译 label
            if 'label' in data and data['label'] in category_translations:
                data['label'] = category_translations[data['label']]
                modified = True
            
            # 翻译 description
            if 'link' in data and 'description' in data['link']:
                desc = data['link']['description']
                if desc in category_translations:
                    data['link']['description'] = category_translations[desc]
                    modified = True
            
            if modified:
                # 写回文件
                with open(category_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                print(f"✅ 翻译分类: {category_file}")
                count += 1
                
        except Exception as e:
            print(f"❌ 处理分类文件错误: {category_file} - {e}")
            continue
    
    print(f"📊 共翻译了 {count} 个分类文件")

async def main():
    """主函数"""
    print("🚀 开始修复翻译问题...")
    
    # 1. 翻译失败的文件
    print("\n" + "="*50)
    print("1. 翻译失败的文件")
    print("="*50)
    await translate_failed_file()
    
    # 2. 翻译 front-matter 标题
    print("\n" + "="*50)
    print("2. 翻译页面标题")
    print("="*50)
    translate_frontmatter_titles()
    
    # 3. 翻译分类文件
    print("\n" + "="*50)
    print("3. 翻译分类文件")
    print("="*50)
    translate_category_files()
    
    print("\n🎉 修复完成！")

if __name__ == "__main__":
    asyncio.run(main()) 
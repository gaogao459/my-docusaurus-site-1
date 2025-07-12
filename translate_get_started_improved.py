#!/usr/bin/env python3
"""
改进版的docs/get-started翻译脚本
- 使用增强的清洗机制
- 添加排版统一化
- 更好的错误处理
"""

import os
import asyncio
import time
import json
import re
from pathlib import Path
import subprocess

# 导入修改后的翻译模块
from Reflection_Workflow_XAI import translate_text

def preserve_frontmatter(content: str) -> tuple[str, str, str]:
    """
    分离frontmatter、正文内容
    
    Returns:
        (frontmatter, body, full_content)
    """
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = f"---{parts[1]}---"
            body = parts[2].strip()
            return frontmatter, body, content
    
    return "", content.strip(), content

def clean_translation_artifacts(text: str) -> str:
    """增强版清理翻译过程中的说明文字"""
    # 移除翻译说明段落 - 扩展更多模式
    patterns = [
        # 中文说明模式
        r'以下是您提供的英文文本的中文翻译.*?(?=\n\n|\n#|\n\*|\Z)',
        r'这个翻译.*?(?=\n\n|\n#|\n\*|\Z)',
        r'以下是.*?翻译.*?(?=\n\n|\n#|\n\*|\Z)',
        r'根据.*?建议.*?翻译.*?(?=\n\n|\n#|\n\*|\Z)',
        r'作为.*?译者.*?(?=\n\n|\n#|\n\*|\Z)',
        
        # 英文说明模式
        r'(?i)below is my.*?translation.*?(?=\n\n|\n#|\n\*|\Z)',
        r'(?i)here is.*?translation.*?(?=\n\n|\n#|\n\*|\Z)',
        r'(?i)i first analyzed.*?(?=\n\n|\n#|\n\*|\Z)',
        r'(?i)based on.*?reflection.*?(?=\n\n|\n#|\n\*|\Z)',
        r'(?i)as a professional translator.*?(?=\n\n|\n#|\n\*|\Z)',
        r'(?i)improvement suggestions.*?(?=\n\n|\n#|\n\*|\Z)',
        r'(?i)for each suggestion.*?(?=\n\n|\n#|\n\*|\Z)',
        r'(?i)sure,? here.*?(?=\n\n|\n#|\n\*|\Z)',
        
        # 改进建议相关
        r'### Improvement Suggestions.*?(?=\n#|\Z)',
        r'### 优化说明.*?(?=\n#|\Z)',
        r'此版本的翻译.*?(?=\n\n|\n#|\Z)',
        
        # 多余的分隔符
        r'---\n\n(?=# )',
        r'\n\n---\n\n(?=这个翻译)',
    ]
    
    cleaned = text
    for pattern in patterns:
        cleaned = re.sub(pattern, '', cleaned, flags=re.DOTALL | re.MULTILINE)
    
    # 清理多余的空行
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
    cleaned = cleaned.strip()
    
    return cleaned

def format_markdown(file_path: Path):
    """使用prettier格式化markdown文件"""
    try:
        result = subprocess.run(
            ["npx", "prettier", "--write", str(file_path), "--parser", "markdown"],
            capture_output=True,
            text=True,
            cwd=file_path.parent.parent.parent  # 项目根目录
        )
        if result.returncode == 0:
            print(f"✅ 格式化完成: {file_path}")
        else:
            print(f"⚠️  格式化警告: {file_path} - {result.stderr}")
    except Exception as e:
        print(f"❌ 格式化失败: {file_path} - {e}")

async def translate_markdown_file(file_path: Path, source_lang="English", target_lang="Chinese"):
    """翻译单个markdown文件"""
    try:
        print(f"\n{'='*60}")
        print(f"翻译文件: {file_path}")
        print(f"{'='*60}")
        
        # 读取原文件
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # 分离frontmatter和正文
        frontmatter, body, _ = preserve_frontmatter(original_content)
        
        if not body.strip():
            print(f"跳过空文件: {file_path}")
            return True
        
        print(f"原文内容预览: {body[:200]}...")
        
        # 使用Reflection Workflow翻译正文
        start_time = time.time()
        result = await translate_text(
            source_text=body,
            source_lang=source_lang,
            target_lang=target_lang,
            model="grok-3-mini"
        )
        translation_time = time.time() - start_time
        
        # 获取翻译结果并清理
        translated_body = result["final_translation"]
        cleaned_translation = clean_translation_artifacts(translated_body)
        
        # 检查清理效果
        if any(keyword in cleaned_translation.lower() for keyword in 
               ['below is', 'here is', 'improvement suggestions', '改进建议']):
            print(f"⚠️  警告: 清理后仍可能包含说明文字")
        
        # 重新组合内容
        final_content = frontmatter + "\n\n" + cleaned_translation if frontmatter else cleaned_translation
        
        # 写入翻译结果，覆盖原文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(final_content)
        
        # 格式化文件
        format_markdown(file_path)
        
        print(f"✅ 翻译完成: {file_path}")
        print(f"⏱️  用时: {translation_time:.2f}秒")
        print(f"📊 统计: {result['stats']}")
        
        return True
        
    except Exception as e:
        print(f"❌ 翻译失败: {file_path}")
        print(f"错误: {str(e)}")
        return False

async def translate_directory(base_dir: Path, source_lang="English", target_lang="Chinese"):
    """递归翻译目录下的所有markdown文件"""
    
    print(f"\n🚀 开始翻译 {base_dir} 目录")
    print(f"源语言: {source_lang} -> 目标语言: {target_lang}")
    
    # 收集所有需要翻译的markdown文件
    md_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.md') and not file.startswith('_'):
                file_path = Path(root) / file
                md_files.append(file_path)
    
    if not md_files:
        print(f"❌ 在 {base_dir} 中未找到markdown文件")
        return
    
    print(f"📁 找到 {len(md_files)} 个markdown文件")
    for f in md_files:
        print(f"  - {f}")
    
    # 翻译所有文件
    total_start = time.time()
    success_count = 0
    
    for i, file_path in enumerate(md_files, 1):
        print(f"\n[{i}/{len(md_files)}] 处理文件...")
        
        try:
            success = await translate_markdown_file(file_path, source_lang, target_lang)
            if success:
                success_count += 1
            
            # 在文件之间添加小延迟
            if i < len(md_files):
                await asyncio.sleep(1)
                
        except Exception as e:
            print(f"❌ 处理文件时出错: {e}")
            continue
    
    total_time = time.time() - total_start
    
    # 输出最终统计
    print(f"\n{'='*60}")
    print(f"🎉 翻译任务完成!")
    print(f"{'='*60}")
    print(f"📊 总文件数: {len(md_files)}")
    print(f"✅ 成功翻译: {success_count}")
    print(f"❌ 失败: {len(md_files) - success_count}")
    print(f"📈 成功率: {success_count/len(md_files)*100:.1f}%")
    print(f"⏱️  总用时: {total_time:.2f}秒")
    print(f"⚡ 平均速度: {total_time/len(md_files):.1f}秒/文件")

async def main():
    """主函数"""
    try:
        # 设置目标目录
        docs_dir = Path("docs/get-started")
        
        if not docs_dir.exists():
            print(f"❌ 目录不存在: {docs_dir}")
            return
        
        # 确认操作
        print(f"🔄 即将使用改进版翻译 {docs_dir} 目录下的所有文件")
        print("⚠️  警告: 这将直接覆盖原文件!")
        print("✨ 新特性: 增强清洗 + 自动格式化")
        
        # 开始翻译
        await translate_directory(docs_dir)
        
    except Exception as e:
        print(f"❌ 程序执行出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main()) 
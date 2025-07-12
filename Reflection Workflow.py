"""
翻译Agent模块，实现了吴恩达的三阶段翻译工作流
参考: https://github.com/andrewyng/translation-agent

翻译工作流包含三个步骤：
1. 初步翻译：调用大语言模型(LLM)完成基础翻译
2. 反思评估：LLM对翻译结果提出改进建议
3. 优化翻译：根据反思建议生成最终优化译文

使用示例：

1. 使用修改后的爬虫启动脚本 

# 仅爬取内容
python run_make_crawler.py https://help.make.com/step-1-get-your-app-ready

# 爬取并翻译为中文
python run_make_crawler.py https://help.make.com/step-1-get-your-app-ready --translate

# 爬取并翻译为其他语言（如西班牙语）
python run_make_crawler.py https://help.make.com/step-1-get-your-app-ready --translate --lang Spanish --country Mexico

2. 使用专门的翻译爬虫

# 爬取并翻译为中文
python sites/make_com/crawl_translate.py https://help.make.com/step-1-get-your-app-ready

# 爬取并翻译为其他语言
python sites/make_com/crawl_translate.py https://help.make.com/step-1-get-your-app-ready --lang Japanese

3. 在其他爬虫中使用翻译Agent

from utils.translation_agent import translate_text

# 在你的爬虫代码中

async def crawl_with_translation():
    # ... 爬取代码 ...
    
    # 获取内容后翻译
    translation_result = await translate_text(
        source_text=content,
        source_lang="English",
        target_lang="Chinese"
    )
    
    # 使用翻译结果
    final_translation = translation_result["final_translation"]

"""
import os
import json
from typing import Dict, Any, Optional, List, Tuple
import openai
import time
import random
import httpx
import asyncio
import logging
import math

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 检查环境变量中是否有API密钥
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

# 如果没有设置环境变量，尝试从config/credentials.py导入
if not OPENAI_API_KEY:
    try:
        from config.credentials import OPENAI_API_KEY
    except ImportError:
        pass

# 使用环境变量或配置文件中的密钥
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

# 创建OpenAI客户端
# 尝试设置代理解决连接问题

# 从环境变量获取代理设置
# 可以通过以下方式设置：
# Windows PowerShell: $env:HTTP_PROXY="http://your-proxy-server:port"
# Windows CMD: set HTTP_PROXY=http://your-proxy-server:port
# Linux/Mac: export HTTP_PROXY=http://your-proxy-server:port
# 或直接在此处修改：
http_proxy = os.environ.get("HTTP_PROXY", "http://127.0.0.1:7897")  # 固定使用指定代理
https_proxy = os.environ.get("HTTPS_PROXY", "http://127.0.0.1:7897")  # 固定使用指定代理

# 配置超时和重试参数
timeout_seconds = 60.0  # 设置为60秒的超时
max_retries = 5

# 创建HTTPX客户端，添加超时和代理设置
try:
    # 使用固定代理
    fixed_proxy = "http://127.0.0.1:7897"
    print(f"使用固定代理: {fixed_proxy}")
    
    # 创建带代理的httpx客户端
    http_client = httpx.Client(
        proxy=fixed_proxy,  # 使用固定代理
        timeout=timeout_seconds,
        transport=httpx.HTTPTransport(retries=max_retries)
    )
    
    # 创建OpenAI客户端，使用配置好的httpx客户端
    client = openai.OpenAI(
        api_key=OPENAI_API_KEY,
        http_client=http_client,
        max_retries=max_retries,
        timeout=timeout_seconds
    )
    print("OpenAI客户端创建成功，使用代理和自定义超时")

except Exception as e:
    print(f"创建代理客户端时出错: {str(e)}")
    print("尝试使用默认配置创建客户端...")
    client = openai.OpenAI(api_key=OPENAI_API_KEY)

class TranslationAgent:
    """
    实现吴恩达的三阶段翻译工作流的翻译Agent
    GPT-4是目前OpenAI最先进的大语言模型之一，它在多语言翻译、语境理解和文化细微差别处理方面表现出色。特别是它的"turbo"版本（如果有的话）通常优化了速度和准确性，适合需要高质翻译的场景，比如专业文档、技术术语或文学作品。
    """
    
    def __init__(self, model: str = "gpt-4-turbo", api_key: Optional[str] = None):
        """
        初始化翻译Agent
        
        Args:
            model: 使用的模型名称
            api_key: OpenAI API密钥，如果未提供则使用环境变量或配置文件中的密钥
        """
        self.model = model
        logger.info(f"初始化翻译Agent: 使用模型 {model}")
        if api_key:
            openai.api_key = api_key
        elif not openai.api_key:
            raise ValueError("未提供OpenAI API密钥，请设置OPENAI_API_KEY环境变量或在初始化时提供")
        
        # 设置模型的价格（每1000个token的美元价格）
        self.model_prices = {
            "gpt-4-turbo": {"input": 0.01, "output": 0.03},  # $0.01/1K输入tokens, $0.03/1K输出tokens
            "gpt-4": {"input": 0.03, "output": 0.06},        # $0.03/1K输入tokens, $0.06/1K输出tokens
            "gpt-3.5-turbo": {"input": 0.001, "output": 0.002}  # $0.001/1K输入tokens, $0.002/1K输出tokens
        }
        
        # 美元转人民币的汇率（需要定期更新）
        self.usd_to_cny = 7.22  # 1美元 = 7.22人民币（此汇率会变动）
        
        # 初始化token统计
        self.token_counts = {
            "initial_translation": {"input": 0, "output": 0},
            "reflection": {"input": 0, "output": 0},
            "refined_translation": {"input": 0, "output": 0},
            "total": {"input": 0, "output": 0}
        }
        
        # 初始化费用统计（美元）
        self.costs = {
            "initial_translation": 0.0,
            "reflection": 0.0,
            "refined_translation": 0.0,
            "total": 0.0
        }
    
    async def translate(self, source_text: str, source_lang: str = "English", 
                      target_lang: str = "Chinese", country: Optional[str] = None, 
                      glossary: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        将文本从源语言翻译到目标语言
        
        Args:
            source_text: 要翻译的文本
            source_lang: 源语言
            target_lang: 目标语言
            country: 可选的国家/地区参数，影响语言变体（如拉美西班牙语vs西班牙西班牙语）
            glossary: 可选的术语表，确保特定术语的翻译一致性
            
        Returns:
            包含翻译结果和中间步骤的字典
        """
        logger.info(f"开始翻译工作流: {source_lang} => {target_lang}")
        print(f"\n===== 开始吴恩达三阶段翻译工作流 =====")
        print(f"源语言: {source_lang} | 目标语言: {target_lang}" + (f" ({country})" if country else ""))
        print(f"文本长度: {len(source_text)} 字符")
        text_preview = source_text[:100] + "..." if len(source_text) > 100 else source_text
        print(f"文本预览: {text_preview}")
        
        # 重置token统计和费用
        self._reset_stats()
        
        # 步骤1: 初步翻译
        print(f"\n[阶段 1/3] 初步翻译...")
        logger.info("阶段1: 开始初步翻译")
        start_time = time.time()
        initial_translation, tokens_phase1 = await self._initial_translation(
            source_text, source_lang, target_lang, country, glossary
        )
        phase1_time = time.time() - start_time
        
        # 更新阶段1的token统计和费用
        self._update_stats("initial_translation", tokens_phase1)
        phase1_cost = self._calculate_cost(tokens_phase1)
        
        print(f"初步翻译完成: {len(initial_translation)} 字符")
        print(f"阶段1用时: {phase1_time:.2f}秒")
        print(f"阶段1 Token使用: 输入 {tokens_phase1['input']} / 输出 {tokens_phase1['output']} = 总计 {tokens_phase1['input'] + tokens_phase1['output']} tokens")
        print(f"阶段1费用: ${phase1_cost:.4f} (约 ¥{phase1_cost * self.usd_to_cny:.2f})")
        logger.info(f"阶段1: 初步翻译完成 ({len(initial_translation)} 字符), Token: {tokens_phase1['input']}/{tokens_phase1['output']}, 费用: ${phase1_cost:.4f}")
        
        # 步骤2: 反思评估
        print(f"\n[阶段 2/3] 反思评估...")
        logger.info("阶段2: 开始反思评估")
        start_time = time.time()
        reflection_result, tokens_phase2 = await self._reflection(
            source_text, initial_translation, source_lang, target_lang, country, glossary
        )
        phase2_time = time.time() - start_time
        
        # 更新阶段2的token统计和费用
        self._update_stats("reflection", tokens_phase2)
        phase2_cost = self._calculate_cost(tokens_phase2)
        
        print(f"反思评估完成: {len(reflection_result)} 条建议")
        for i, suggestion in enumerate(reflection_result, 1):
            print(f"  建议 {i}: {suggestion[:100]}..." if len(suggestion) > 100 else f"  建议 {i}: {suggestion}")
        print(f"阶段2用时: {phase2_time:.2f}秒")
        print(f"阶段2 Token使用: 输入 {tokens_phase2['input']} / 输出 {tokens_phase2['output']} = 总计 {tokens_phase2['input'] + tokens_phase2['output']} tokens")
        print(f"阶段2费用: ${phase2_cost:.4f} (约 ¥{phase2_cost * self.usd_to_cny:.2f})")
        logger.info(f"阶段2: 反思评估完成 ({len(reflection_result)} 条建议), Token: {tokens_phase2['input']}/{tokens_phase2['output']}, 费用: ${phase2_cost:.4f}")
        
        # 步骤3: 优化翻译
        print(f"\n[阶段 3/3] 优化翻译...")
        logger.info("阶段3: 开始优化翻译")
        start_time = time.time()
        final_translation, tokens_phase3 = await self._refined_translation(
            source_text, initial_translation, reflection_result, 
            source_lang, target_lang, country, glossary
        )
        phase3_time = time.time() - start_time
        
        # 更新阶段3的token统计和费用
        self._update_stats("refined_translation", tokens_phase3)
        phase3_cost = self._calculate_cost(tokens_phase3)
        
        print(f"优化翻译完成: {len(final_translation)} 字符")
        print(f"阶段3用时: {phase3_time:.2f}秒")
        print(f"阶段3 Token使用: 输入 {tokens_phase3['input']} / 输出 {tokens_phase3['output']} = 总计 {tokens_phase3['input'] + tokens_phase3['output']} tokens")
        print(f"阶段3费用: ${phase3_cost:.4f} (约 ¥{phase3_cost * self.usd_to_cny:.2f})")
        logger.info(f"阶段3: 优化翻译完成 ({len(final_translation)} 字符), Token: {tokens_phase3['input']}/{tokens_phase3['output']}, 费用: ${phase3_cost:.4f}")
        
        # 计算总体统计
        total_tokens = self.token_counts["total"]["input"] + self.token_counts["total"]["output"]
        total_cost = self.costs["total"]
        total_time = phase1_time + phase2_time + phase3_time
        
        print(f"\n===== 翻译工作流完成 =====")
        print(f"总用时: {total_time:.2f}秒")
        print(f"总Token使用: 输入 {self.token_counts['total']['input']} / 输出 {self.token_counts['total']['output']} = 总计 {total_tokens} tokens")
        print(f"总费用: ${total_cost:.4f} (约 ¥{total_cost * self.usd_to_cny:.2f})")
        print(f"使用模型: {self.model}")
        logger.info(f"翻译工作流完成: {source_lang} => {target_lang}, 总Token: {total_tokens}, 总费用: ${total_cost:.4f} (¥{total_cost * self.usd_to_cny:.2f})")
        
        # 返回完整结果
        return {
            "source_text": source_text,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "country": country,
            "initial_translation": initial_translation,
            "reflection": reflection_result,
            "final_translation": final_translation,
            "stats": {
                "token_counts": self.token_counts,
                "costs": self.costs,
                "time": total_time,
                "model": self.model
            }
        }
    
    def _reset_stats(self):
        """重置token统计和费用"""
        self.token_counts = {
            "initial_translation": {"input": 0, "output": 0},
            "reflection": {"input": 0, "output": 0},
            "refined_translation": {"input": 0, "output": 0},
            "total": {"input": 0, "output": 0}
        }
        
        self.costs = {
            "initial_translation": 0.0,
            "reflection": 0.0,
            "refined_translation": 0.0,
            "total": 0.0
        }
    
    def _update_stats(self, phase: str, tokens: Dict[str, int]):
        """更新统计数据"""
        self.token_counts[phase]["input"] = tokens["input"]
        self.token_counts[phase]["output"] = tokens["output"]
        self.token_counts["total"]["input"] += tokens["input"]
        self.token_counts["total"]["output"] += tokens["output"]
        
        # 计算并更新费用
        cost = self._calculate_cost(tokens)
        self.costs[phase] = cost
        self.costs["total"] += cost
    
    def _calculate_cost(self, tokens: Dict[str, int]) -> float:
        """计算给定token数量的费用（美元）"""
        model_price = self.model_prices.get(
            self.model, 
            {"input": 0.01, "output": 0.03}  # 默认使用gpt-4-turbo的价格
        )
        
        input_cost = (tokens["input"] / 1000) * model_price["input"]
        output_cost = (tokens["output"] / 1000) * model_price["output"]
        
        return input_cost + output_cost
    
    def _estimate_tokens(self, text: str) -> int:
        """估算文本中的token数量（粗略估计）"""
        # 英文大约每4个字符一个token
        # 中文大约每1.5个字符一个token
        chars = len(text)
        return math.ceil(chars / 3)  # 使用3作为平均值
    
    async def _make_openai_request(self, func, *args, **kwargs):
        """
        包装OpenAI API请求，添加重试逻辑
        
        Args:
            func: 要调用的API函数
            *args, **kwargs: 传递给函数的参数
            
        Returns:
            API响应和token使用统计
        """
        max_retries = 5
        initial_retry_delay = 3
        max_retry_delay = 60
        
        for attempt in range(max_retries):
            try:
                print(f"发送请求到OpenAI API (尝试 {attempt+1}/{max_retries})...")
                logger.info(f"向OpenAI发送请求 (尝试 {attempt+1}/{max_retries})")
                start_time = time.time()
                
                # 修复：不使用await直接调用函数，因为client.chat.completions.create不是一个协程
                response = func(*args, **kwargs)
                
                elapsed_time = time.time() - start_time
                print(f"请求成功, 用时: {elapsed_time:.2f}秒")
                
                # 提取token使用情况
                token_usage = {
                    "input": response.usage.prompt_tokens,
                    "output": response.usage.completion_tokens
                }
                
                logger.info(f"OpenAI请求成功, 用时: {elapsed_time:.2f}秒, Token使用: {token_usage}")
                return response, token_usage
            except (openai.APIConnectionError, openai.APITimeoutError) as e:
                if attempt + 1 == max_retries:
                    print(f"达到最大重试次数，错误: {str(e)}")
                    logger.error(f"达到最大重试次数: {str(e)}")
                    raise
                
                # 计算延迟时间，使用指数退避和随机抖动
                delay = min(initial_retry_delay * (2 ** attempt) + random.uniform(0, 1), max_retry_delay)
                print(f"API连接错误: {str(e)}")
                print(f"{delay:.1f}秒后重试 ({attempt+1}/{max_retries})...")
                logger.warning(f"API连接错误: {str(e)}, {delay:.1f}秒后重试")
                await asyncio.sleep(delay)
            except openai.RateLimitError as e:
                if attempt + 1 == max_retries:
                    logger.error(f"达到最大重试次数(速率限制): {str(e)}")
                    raise
                
                # 对于速率限制错误，等待更长时间
                delay = min(initial_retry_delay * (3 ** attempt) + random.uniform(0, 3), 120)
                print(f"API速率限制错误，{delay:.1f}秒后重试 ({attempt+1}/{max_retries})...")
                logger.warning(f"API速率限制错误: {str(e)}, {delay:.1f}秒后重试")
                await asyncio.sleep(delay)
            except Exception as e:
                print(f"API请求出现意外错误: {str(e)}")
                logger.error(f"API请求意外错误: {str(e)}")
                raise
    
    async def _initial_translation(self, source_text: str, source_lang: str, target_lang: str,
                                 country: Optional[str], glossary: Optional[Dict[str, str]]) -> Tuple[str, Dict[str, int]]:
        """
        第一阶段：完成初步翻译
        
        Returns:
            元组: (翻译结果, token使用统计)
        """
        # 构建指定区域的语言描述
        language_spec = f"{target_lang}"
        if country:
            language_spec += f" as colloquially spoken in {country}"
        
        # 构建包含术语表的提示（如果提供）
        glossary_prompt = ""
        if glossary:
            glossary_prompt = "Please use the following glossary for consistency:\n"
            for term, translation in glossary.items():
                glossary_prompt += f"- {term}: {translation}\n"
            logger.info(f"使用术语表: {len(glossary)} 个术语")
        
        prompt = f"""Translate the following {source_lang} text into {language_spec}. 

{glossary_prompt}

Be accurate but also natural and fluent. Maintain the same level of formality, tone, and style as the original.

{source_lang} TEXT:
{source_text}

{target_lang} TRANSLATION:"""
        
        logger.info(f"阶段1: 发送初步翻译请求, 提示长度: {len(prompt)} 字符")
        print(f"发送初步翻译请求: {len(prompt)} 字符的提示")
        response, token_usage = await self._make_openai_request(
            client.chat.completions.create,
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a professional translator."},
                {"role": "user", "content": prompt}
            ]
        )
        
        translation = response.choices[0].message.content.strip()
        logger.info(f"阶段1: 初步翻译响应长度: {len(translation)} 字符, Token使用: {token_usage}")
        return translation, token_usage
    
    async def _reflection(self, source_text: str, initial_translation: str, source_lang: str,
                        target_lang: str, country: Optional[str], glossary: Optional[Dict[str, str]]) -> Tuple[List[str], Dict[str, int]]:
        """
        第二阶段：反思评估，对初步翻译提出改进建议
        
        Returns:
            元组: (建议列表, token使用统计)
        """
        # 构建指定区域的语言描述
        language_spec = f"{target_lang}"
        if country:
            language_spec += f" as spoken in {country}"
        
        # 构建包含术语表的提示（如果提供）
        glossary_prompt = ""
        if glossary:
            glossary_prompt = "Consider the following glossary for your reflection:\n"
            for term, translation in glossary.items():
                glossary_prompt += f"- {term}: {translation}\n"
        
        prompt = f"""You are given a source text in {source_lang} and its initial translation into {language_spec}.

{glossary_prompt}

Please identify 3-5 concrete ways in which the translation could be improved. Focus on:
1. Accuracy: Does the translation correctly convey all the information?
2. Natural flow: Does it sound natural and fluent?
3. Terminology: Are specialized terms translated consistently and correctly?
4. Cultural context: Is the translation appropriate for the target audience?
5. Style and tone: Does it maintain the style and tone of the original?

For each suggestion, provide a specific example from the text and explain how it could be improved.

{source_lang} SOURCE:
{source_text}

{target_lang} INITIAL TRANSLATION:
{initial_translation}

IMPROVEMENT SUGGESTIONS:"""
        
        logger.info(f"阶段2: 发送反思评估请求, 提示长度: {len(prompt)} 字符")
        print(f"发送反思评估请求: {len(prompt)} 字符的提示")
        response, token_usage = await self._make_openai_request(
            client.chat.completions.create,
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a translation quality evaluator with expertise in multiple languages."},
                {"role": "user", "content": prompt}
            ]
        )
        
        reflection_text = response.choices[0].message.content.strip()
        logger.info(f"阶段2: 反思评估响应长度: {len(reflection_text)} 字符, Token使用: {token_usage}")
        
        # 将反思文本拆分为具体建议列表
        suggestions = []
        for line in reflection_text.split("\n"):
            if line.strip() and any(line.startswith(prefix) for prefix in ["- ", "* ", "1. ", "2. ", "3. ", "4. ", "5. ", "6. ", "7. ", "8. ", "9. ", "Suggestion "]):
                suggestions.append(line.strip())
        
        # 如果没有成功解析出建议，则返回整个反思文本作为一个建议
        if not suggestions:
            suggestions = [reflection_text]
        
        return suggestions, token_usage
    
    async def _refined_translation(self, source_text: str, initial_translation: str, 
                                 reflection: List[str], source_lang: str,
                                 target_lang: str, country: Optional[str], 
                                 glossary: Optional[Dict[str, str]]) -> Tuple[str, Dict[str, int]]:
        """
        第三阶段：根据反思建议生成优化的最终翻译
        
        Returns:
            元组: (优化后的翻译, token使用统计)
        """
        # 构建指定区域的语言描述
        language_spec = f"{target_lang}"
        if country:
            language_spec += f" as spoken in {country}"
        
        # 构建包含术语表的提示（如果提供）
        glossary_prompt = ""
        if glossary:
            glossary_prompt = "Please use the following glossary for consistency:\n"
            for term, translation in glossary.items():
                glossary_prompt += f"- {term}: {translation}\n"
        
        # 将反思建议组织为一个字符串
        reflection_text = "\n".join(reflection)
        
        prompt = f"""You are tasked with creating an improved translation from {source_lang} to {language_spec}.

{glossary_prompt}

Here is the original source text:
{source_text}

Here is the initial translation:
{initial_translation}

Based on the following suggestions for improvement:
{reflection_text}

Please provide an improved translation that addresses all these suggestions. The translation should be accurate, natural-sounding, and maintain the style and tone of the original text.

IMPROVED {target_lang} TRANSLATION:"""
        
        logger.info(f"阶段3: 发送优化翻译请求, 提示长度: {len(prompt)} 字符")
        print(f"发送优化翻译请求: {len(prompt)} 字符的提示")
        response, token_usage = await self._make_openai_request(
            client.chat.completions.create,
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a professional translator with expertise in multiple languages."},
                {"role": "user", "content": prompt}
            ]
        )
        
        translation = response.choices[0].message.content.strip()
        logger.info(f"阶段3: 优化翻译响应长度: {len(translation)} 字符, Token使用: {token_usage}")
        return translation, token_usage


async def translate_text(source_text: str, source_lang: str = "English", 
                       target_lang: str = "Chinese", country: Optional[str] = None,
                       glossary: Optional[Dict[str, str]] = None, 
                       model: str = "gpt-4-turbo",
                       api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    便捷函数：使用翻译Agent将文本从源语言翻译到目标语言
    
    Args:
        source_text: 要翻译的文本
        source_lang: 源语言
        target_lang: 目标语言
        country: 可选的国家/地区参数，影响语言变体
        glossary: 可选的术语表
        model: 使用的模型名称
        api_key: OpenAI API密钥
        
    Returns:
        包含翻译结果和中间步骤的字典
    """
    logger.info(f"开始翻译文本: {source_lang} => {target_lang}, 使用模型: {model}")
    agent = TranslationAgent(model=model, api_key=api_key)
    result = await agent.translate(source_text, source_lang, target_lang, country, glossary)
    logger.info(f"文本翻译完成: {len(source_text)} => {len(result['final_translation'])} 字符")
    return result


async def translate_file(input_file: str, output_file: str, source_lang: str = "English",
                       target_lang: str = "Chinese", country: Optional[str] = None,
                       glossary: Optional[Dict[str, str]] = None,
                       model: str = "gpt-4-turbo",
                       api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    便捷函数：翻译文件内容
    
    Args:
        input_file: 输入文件路径
        output_file: 输出文件路径
        source_lang: 源语言
        target_lang: 目标语言
        country: 可选的国家/地区参数
        glossary: 可选的术语表
        model: 使用的模型名称
        api_key: OpenAI API密钥
        
    Returns:
        包含翻译结果和中间步骤的字典
    """
    logger.info(f"开始翻译文件: {input_file} => {output_file}")
    
    # 读取输入文件
    with open(input_file, 'r', encoding='utf-8') as f:
        source_text = f.read()
    
    logger.info(f"读取输入文件: {input_file}, {len(source_text)} 字符")
    
    # 翻译文本
    result = await translate_text(
        source_text, source_lang, target_lang, country, glossary, model, api_key
    )
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result["final_translation"])
    
    logger.info(f"翻译结果已写入: {output_file}, {len(result['final_translation'])} 字符")
    return result 

def sync_translate_file(input_file: str, output_file: str, source_lang: str = "English",
                       target_lang: str = "Chinese", country: Optional[str] = None,
                       glossary: Optional[Dict[str, str]] = None,
                       model: str = "gpt-3.5-turbo",
                       api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    同步版本的文件翻译函数，不需要异步环境
    
    Args:
        input_file: 输入文件路径
        output_file: 输出文件路径
        source_lang: 源语言
        target_lang: 目标语言
        country: 可选的国家/地区参数
        glossary: 可选的术语表
        model: 使用的模型名称
        api_key: OpenAI API密钥
        
    Returns:
        包含翻译结果的字典
    """
    logger.info(f"开始同步翻译文件: {input_file} => {output_file}, 使用模型: {model}")
    print(f"\n===== 开始同步翻译文件 =====")
    print(f"输入文件: {input_file}")
    print(f"输出文件: {output_file}")
    print(f"翻译方向: {source_lang} => {target_lang}" + (f" ({country})" if country else ""))
    print(f"使用模型: {model}")
    
    # 读取输入文件
    with open(input_file, 'r', encoding='utf-8') as f:
        source_text = f.read()
    
    print(f"读取输入文件: {len(source_text)} 字符")
    logger.info(f"读取输入文件: {input_file}, {len(source_text)} 字符")
    
    # 直接使用OpenAI客户端进行翻译 - 不使用异步版本
    # 初步翻译
    language_spec = f"{target_lang}"
    if country:
        language_spec += f" as colloquially spoken in {country}"
    
    glossary_prompt = ""
    if glossary:
        glossary_prompt = "Please use the following glossary for consistency:\n"
        for term, translation in glossary.items():
            glossary_prompt += f"- {term}: {translation}\n"
        print(f"使用术语表: {len(glossary)} 个术语")
    
    # 使用多次尝试机制
    max_attempts = 5
    initial_delay = 3
    
    # 初步翻译
    prompt = f"""Translate the following {source_lang} text into {language_spec}. 
{glossary_prompt}
Be accurate but also natural and fluent. Maintain the same level of formality, tone, and style as the original.

{source_lang} TEXT:
{source_text}

{target_lang} TRANSLATION:"""
    
    print(f"\n[同步翻译] 正在翻译...")
    logger.info(f"准备同步翻译, 提示长度: {len(prompt)} 字符")
    
    for attempt in range(max_attempts):
        try:
            start_time = time.time()
            print(f"发送同步翻译请求到OpenAI API (尝试 {attempt+1}/{max_attempts})...")
            logger.info(f"发送同步翻译请求 (尝试 {attempt+1}/{max_attempts})")
            
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a professional translator."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            initial_translation = response.choices[0].message.content.strip()
            elapsed_time = time.time() - start_time
            
            print(f"翻译请求成功，用时: {elapsed_time:.2f}秒")
            print(f"接收到{len(initial_translation)}个字符的翻译结果")
            logger.info(f"同步翻译成功, 用时: {elapsed_time:.2f}秒, 结果长度: {len(initial_translation)} 字符")
            break
        except Exception as e:
            print(f"翻译出错 (尝试 {attempt+1}/{max_attempts}): {str(e)}")
            logger.error(f"同步翻译出错 (尝试 {attempt+1}/{max_attempts}): {str(e)}")
            
            if attempt < max_attempts - 1:
                delay = initial_delay * (2 ** attempt)
                print(f"等待 {delay} 秒后重试...")
                logger.warning(f"等待 {delay} 秒后重试...")
                time.sleep(delay)
            else:
                print("翻译失败，使用空翻译结果。")
                logger.error("达到最大重试次数，翻译失败")
                initial_translation = ""
    
    # 直接写入结果，忽略反思和优化步骤
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(initial_translation)
    
    print(f"\n===== 同步翻译完成 =====")
    print(f"结果已写入: {output_file}")
    logger.info(f"同步翻译结果已写入: {output_file}, {len(initial_translation)} 字符")
    
    return {
        "source_text": source_text,
        "source_lang": source_lang,
        "target_lang": target_lang,
        "country": country,
        "initial_translation": initial_translation,
        "reflection": [],
        "final_translation": initial_translation
    } 
"""
翻译Agent模块，实现了吴恩达的三阶段翻译工作流
修改版本：使用x.ai API而不是OpenAI API
参考: https://github.com/andrewyng/translation-agent

翻译工作流包含三个步骤：
1. 初步翻译：调用大语言模型(LLM)完成基础翻译
2. 反思评估：LLM对翻译结果提出改进建议
3. 优化翻译：根据反思建议生成最终优化译文
"""

import os
import json
from typing import Dict, Any, Optional, List, Tuple
import httpx
import time
import random
import asyncio
import logging
import math
import re  # Added for extracting translation markers

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# x.ai API配置
XAI_API_KEY = "xai-Sz5FgWY3HhIgL0EkGUJ9leKJq35aXRjeOSrOlDMnZiofBXEwAhxVZXfuTAXXc0vJB04IMr6yBNyWCKn7"
XAI_BASE_URL = "https://api.x.ai/v1"

class TranslationAgent:
    """
    实现吴恩达的三阶段翻译工作流的翻译Agent
    修改版本：使用x.ai的grok模型
    """
    
    def __init__(self, model: str = "grok-3-mini", api_key: Optional[str] = None):
        """
        初始化翻译Agent
        
        Args:
            model: 使用的模型名称（grok-3-mini或grok-3-latest）
            api_key: x.ai API密钥
        """
        self.model = model
        self.api_key = api_key or XAI_API_KEY
        self.base_url = XAI_BASE_URL
        
        logger.info(f"初始化翻译Agent: 使用x.ai模型 {model}")
        
        if not self.api_key:
            raise ValueError("未提供x.ai API密钥")
        
        # 设置模型的价格（每1000个token的美元价格）
        self.model_prices = {
            "grok-3-mini": {"input": 0.005, "output": 0.015},     # x.ai grok-3-mini价格
            "grok-3-latest": {"input": 0.01, "output": 0.03},    # x.ai grok-3-latest价格
        }
        
        # 美元转人民币的汇率
        self.usd_to_cny = 7.22
        
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
            country: 可选的国家/地区参数
            glossary: 可选的术语表
            
        Returns:
            包含翻译结果和中间步骤的字典
        """
        logger.info(f"开始翻译工作流: {source_lang} => {target_lang}")
        print(f"\n===== 开始吴恩达三阶段翻译工作流 (x.ai版本) =====")
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
        print(f"使用模型: {self.model} (x.ai)")
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
            {"input": 0.005, "output": 0.015}  # 默认使用grok-3-mini的价格
        )
        
        input_cost = (tokens["input"] / 1000) * model_price["input"]
        output_cost = (tokens["output"] / 1000) * model_price["output"]
        
        return input_cost + output_cost
    
    def _estimate_tokens(self, text: str) -> int:
        """估算文本中的token数量（粗略估计）"""
        chars = len(text)
        return math.ceil(chars / 3)
    
    async def _make_xai_request(self, messages, **kwargs):
        """
        发送请求到x.ai API
        
        Args:
            messages: 消息列表
            **kwargs: 其他参数
            
        Returns:
            API响应和token使用统计
        """
        max_retries = 5
        initial_retry_delay = 3
        max_retry_delay = 60
        
        for attempt in range(max_retries):
            try:
                print(f"发送请求到x.ai API (尝试 {attempt+1}/{max_retries})...")
                logger.info(f"向x.ai发送请求 (尝试 {attempt+1}/{max_retries})")
                start_time = time.time()
                
                # 创建httpx客户端
                async with httpx.AsyncClient(timeout=60.0) as client:
                    # 构建请求数据
                    request_data = {
                        "model": self.model,
                        "messages": messages,
                        "temperature": 0.3,  # 翻译任务使用较低的temperature
                        **kwargs
                    }
                    
                    # 发送请求
                    response = await client.post(
                        f"{self.base_url}/chat/completions",
                        json=request_data,
                        headers={
                            "Authorization": f"Bearer {self.api_key}",
                            "Content-Type": "application/json"
                        }
                    )
                    
                    response.raise_for_status()
                    result = response.json()
                
                elapsed_time = time.time() - start_time
                print(f"请求成功, 用时: {elapsed_time:.2f}秒")
                
                # 提取token使用情况
                usage = result.get("usage", {})
                token_usage = {
                    "input": usage.get("prompt_tokens", 0),
                    "output": usage.get("completion_tokens", 0)
                }
                
                logger.info(f"x.ai请求成功, 用时: {elapsed_time:.2f}秒, Token使用: {token_usage}")
                return result, token_usage
                
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:  # Rate limit
                    if attempt + 1 == max_retries:
                        logger.error(f"达到最大重试次数(速率限制): {str(e)}")
                        raise
                    
                    delay = min(initial_retry_delay * (3 ** attempt) + random.uniform(0, 3), 120)
                    print(f"API速率限制错误，{delay:.1f}秒后重试 ({attempt+1}/{max_retries})...")
                    logger.warning(f"API速率限制错误: {str(e)}, {delay:.1f}秒后重试")
                    await asyncio.sleep(delay)
                else:
                    print(f"HTTP错误: {e.response.status_code} - {e.response.text}")
                    logger.error(f"HTTP错误: {e.response.status_code} - {e.response.text}")
                    raise
                    
            except (httpx.ConnectError, httpx.TimeoutException) as e:
                if attempt + 1 == max_retries:
                    print(f"达到最大重试次数，错误: {str(e)}")
                    logger.error(f"达到最大重试次数: {str(e)}")
                    raise
                
                delay = min(initial_retry_delay * (2 ** attempt) + random.uniform(0, 1), max_retry_delay)
                print(f"API连接错误: {str(e)}")
                print(f"{delay:.1f}秒后重试 ({attempt+1}/{max_retries})...")
                logger.warning(f"API连接错误: {str(e)}, {delay:.1f}秒后重试")
                await asyncio.sleep(delay)
                
            except Exception as e:
                print(f"API请求出现意外错误: {str(e)}")
                logger.error(f"API请求意外错误: {str(e)}")
                raise
    
    async def _initial_translation(self, source_text: str, source_lang: str, target_lang: str,
                                 country: Optional[str], glossary: Optional[Dict[str, str]]) -> Tuple[str, Dict[str, int]]:
        """第一阶段：完成初步翻译"""
        language_spec = f"{target_lang}"
        if country:
            language_spec += f" as colloquially spoken in {country}"
        
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
        
        messages = [
            {"role": "system", "content": "You are a professional translator."},
            {"role": "user", "content": prompt}
        ]
        
        response, token_usage = await self._make_xai_request(messages)
        translation = response["choices"][0]["message"]["content"].strip()
        
        logger.info(f"阶段1: 初步翻译响应长度: {len(translation)} 字符, Token使用: {token_usage}")
        return translation, token_usage
    
    async def _reflection(self, source_text: str, initial_translation: str, source_lang: str,
                        target_lang: str, country: Optional[str], glossary: Optional[Dict[str, str]]) -> Tuple[List[str], Dict[str, int]]:
        """第二阶段：反思评估"""
        language_spec = f"{target_lang}"
        if country:
            language_spec += f" as spoken in {country}"
        
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
        
        messages = [
            {"role": "system", "content": "You are a translation quality evaluator with expertise in multiple languages."},
            {"role": "user", "content": prompt}
        ]
        
        response, token_usage = await self._make_xai_request(messages)
        reflection_text = response["choices"][0]["message"]["content"].strip()
        
        logger.info(f"阶段2: 反思评估响应长度: {len(reflection_text)} 字符, Token使用: {token_usage}")
        
        # 将反思文本拆分为具体建议列表
        suggestions = []
        for line in reflection_text.split("\n"):
            if line.strip() and any(line.startswith(prefix) for prefix in ["- ", "* ", "1. ", "2. ", "3. ", "4. ", "5. ", "6. ", "7. ", "8. ", "9. ", "Suggestion "]):
                suggestions.append(line.strip())
        
        # 如果没有找到格式化的建议，就将整个反思文本作为一个建议
        if not suggestions:
            suggestions = [reflection_text]
        
        return suggestions, token_usage
    
    async def _refined_translation(self, source_text: str, initial_translation: str, 
                                 reflection: List[str], source_lang: str,
                                 target_lang: str, country: Optional[str], 
                                 glossary: Optional[Dict[str, str]]) -> Tuple[str, Dict[str, int]]:
        """第三阶段：优化翻译"""
        language_spec = f"{target_lang}"
        if country:
            language_spec += f" as colloquially spoken in {country}"
        
        glossary_prompt = ""
        if glossary:
            glossary_prompt = "Please use the following glossary for consistency:\n"
            for term, translation in glossary.items():
                glossary_prompt += f"- {term}: {translation}\n"
        
        reflection_text = "\n".join(reflection)
        
        prompt = f"""Based on the following reflection suggestions, please improve the translation from {source_lang} to {language_spec}.

{glossary_prompt}

{source_lang} SOURCE:
{source_text}

INITIAL TRANSLATION:
{initial_translation}

IMPROVEMENT SUGGESTIONS:
{reflection_text}

Please provide an improved translation that addresses the suggestions above. Make sure the translation is accurate, natural, and maintains the appropriate tone and style.

CRITICAL REQUIREMENT: Return ONLY the improved {target_lang} translation. Do not include any commentary, explanations, or improvement notes. Wrap the final translation between <<<TRANSLATION>>> and <<<END>>> tags.

IMPROVED {target_lang} TRANSLATION:"""
        
        logger.info(f"阶段3: 发送优化翻译请求, 提示长度: {len(prompt)} 字符")
        print(f"发送优化翻译请求: {len(prompt)} 字符的提示")
        
        messages = [
            {"role": "system", "content": "You are a professional translator specializing in creating high-quality, refined translations."},
            {"role": "user", "content": prompt}
        ]
        
        response, token_usage = await self._make_xai_request(messages)
        refined_translation_raw = response["choices"][0]["message"]["content"].strip()
        
        # Extract the translation between markers if present
        marker_match = re.search(r"<<<TRANSLATION>>>\s*(.*?)\s*<<<END>>>", refined_translation_raw, flags=re.DOTALL)
        if marker_match:
            refined_translation = marker_match.group(1).strip()
            logger.info(f"阶段3: 成功提取标记内译文，长度: {len(refined_translation)} 字符")
        else:
            # Fallback: try to extract from first markdown heading
            first_heading = re.search(r'^# ', refined_translation_raw, flags=re.MULTILINE)
            if first_heading:
                refined_translation = refined_translation_raw[first_heading.start():].strip()
                logger.info(f"阶段3: 使用标题提取方式，长度: {len(refined_translation)} 字符")
            else:
                refined_translation = refined_translation_raw
                logger.warning(f"阶段3: 未找到标记或标题，使用原始内容")
        
        logger.info(f"阶段3: 优化翻译响应长度: {len(refined_translation)} 字符, Token使用: {token_usage}")
        return refined_translation, token_usage

# 便捷函数
async def translate_text(source_text: str, source_lang: str = "English", 
                       target_lang: str = "Chinese", country: Optional[str] = None,
                       glossary: Optional[Dict[str, str]] = None, 
                       model: str = "grok-3-mini",
                       api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    便捷的文本翻译函数
    """
    agent = TranslationAgent(model=model, api_key=api_key)
    return await agent.translate(
        source_text=source_text,
        source_lang=source_lang,
        target_lang=target_lang,
        country=country,
        glossary=glossary
    ) 
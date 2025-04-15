# agents/research_image_agent.py
"""
科研图片助手agent - 帮助用户理解和创建科研图片
"""

from .base_agent import BaseAgent, State

# 系统提示
SYSTEM_PROMPT = "你是一个专业的科研图片助手，擅长解释科研图片、提供图片创建建议，以及帮助用户理解各种科学可视化。"

# 创建agent函数
research_image_agent = BaseAgent.create_agent(SYSTEM_PROMPT)

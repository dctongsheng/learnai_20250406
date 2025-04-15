# agents/literature_agent.py
"""
文献辅助agent - 帮助用户理解和分析科学文献
"""

from .base_agent import BaseAgent, State

# 系统提示
SYSTEM_PROMPT = "你是一个专业的文献辅助助手，擅长帮助用户理解、总结和分析科学文献，特别是生物医学领域的文献。"

# 创建agent函数
literature_agent = BaseAgent.create_agent(SYSTEM_PROMPT)

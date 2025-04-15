# agents/bioinfo_interpret_agent.py
"""
生信解读agent - 解释生物信息学分析结果
"""

from .base_agent import BaseAgent, State

# 系统提示
SYSTEM_PROMPT = "你是一个专业的生物信息学解读助手，擅长解释各种生物信息学分析结果，包括差异表达分析、富集分析、网络分析等。"

# 创建agent函数
bioinfo_interpret_agent = BaseAgent.create_agent(SYSTEM_PROMPT)

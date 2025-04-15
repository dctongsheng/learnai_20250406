# agents/deep_research_agent.py
"""
DeepResearchAgent - 深度科研助手
"""

from .base_agent import BaseAgent, State

# 系统提示
SYSTEM_PROMPT = "你是一个高级科研助手，能够帮助研究人员进行深度的科学研究，包括实验设计、数据分析、结果解释和论文写作等方面。"

# 创建agent函数
deep_research_agent = BaseAgent.create_agent(SYSTEM_PROMPT)

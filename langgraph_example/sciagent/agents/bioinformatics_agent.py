# agents/bioinformatics_agent.py
"""
生信分析agent - 处理生物信息学分析请求
"""

from .base_agent import BaseAgent, State

# 系统提示
SYSTEM_PROMPT = "你是一个专业的生物信息学分析助手，擅长基因组学、转录组学、蛋白质组学等分析方法。"

# 创建agent函数
bioinformatics_agent = BaseAgent.create_agent(SYSTEM_PROMPT)

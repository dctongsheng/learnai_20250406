# agents/chat_agent.py
"""
简单聊天agent - 处理一般对话请求
"""

from .base_agent import BaseAgent, State

# 系统提示
SYSTEM_PROMPT = "你是一个友好的聊天助手，可以回答用户的一般性问题。"

# 创建agent函数
chat_agent = BaseAgent.create_agent(SYSTEM_PROMPT)

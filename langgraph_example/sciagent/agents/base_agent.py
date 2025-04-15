# agents/base_agent.py
"""
基础agent类，提供共享功能
"""

from typing_extensions import TypedDict
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# 导入共享的State类型
class State(TypedDict):
    input: str
    decision: str
    output: str

# 创建共享的LLM实例
llm = ChatOpenAI(model="gpt-4o")

class BaseAgent:
    """基础agent类，提供共享功能"""
    
    @staticmethod
    def create_agent(system_prompt):
        """创建一个agent函数，使用指定的系统提示"""
        
        def agent_function(state: State):
            result = llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=state["input"])
            ])
            return {"output": result.content}
        
        return agent_function

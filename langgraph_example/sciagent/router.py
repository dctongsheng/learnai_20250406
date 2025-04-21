from typing_extensions import Literal
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
load_dotenv("/mnt/shared_disk/.env")

from langchain_openai import ChatOpenAI

# 导入所有专业agent
from agents import (
    chat_agent,
    bioinformatics_agent,
    bioinfo_interpret_agent,
    literature_agent,
    research_image_agent,
    deep_research_agent
)

# 导入State类型
from agents.base_agent import State

# 创建LLM实例
llm = ChatOpenAI(model="gpt-4o")

# Schema for structured output to use as routing logic
class Route(BaseModel):
    step: Literal[
        "chat",                # 简单聊天agent
        "bioinformatics",      # 生信分析agent
        "bioinfo_interpret",   # 生信解读agent
        "literature",          # 文献辅助agent
        "research_image",      # 科研图片助手agent
        "deep_research"        # deepresearchagent
    ] = Field(
        None, description="The next step in the routing process"
    )


# Augment the LLM with schema for structured output
router = llm.with_structured_output(Route)


# 路由器节点


def llm_call_router(state: State):
    """Route the input to the appropriate node based on the query content"""

    # Run the augmented LLM with structured output to serve as routing logic
    decision = router.invoke(
        [
            SystemMessage(
                content="""根据用户的输入，将请求路由到最合适的专业agent处理。可选的agent有：
                - chat: 简单聊天agent，处理一般性对话和问题
                - bioinformatics: 生信分析agent，处理生物信息学分析请求
                - bioinfo_interpret: 生信解读agent，解释生物信息学分析结果
                - literature: 文献辅助agent，帮助用户理解和分析科学文献
                - research_image: 科研图片助手agent，帮助用户理解和创建科研图片
                - deep_research: DeepResearchAgent，提供深度科研支持

                请根据用户输入的内容和意图，选择最合适的agent。
                """
            ),
            HumanMessage(content=state["input"]),
        ]
    )
    print(decision)

    return {"decision": decision.step}


# Conditional edge function to route to the appropriate node
def route_decision(state: State):
    # Return the node name you want to visit next
    if state["decision"] == "chat":
        return "chat_agent"
    elif state["decision"] == "bioinformatics":
        return "bioinformatics_agent"
    elif state["decision"] == "bioinfo_interpret":
        return "bioinfo_interpret_agent"
    elif state["decision"] == "literature":
        return "literature_agent"
    elif state["decision"] == "research_image":
        return "research_image_agent"
    elif state["decision"] == "deep_research":
        return "deep_research_agent"
    else:
        # 默认使用聊天agent
        return "chat_agent"


# Build workflow
router_builder = StateGraph(State)

# Add nodes
router_builder.add_node("chat_agent", chat_agent)
router_builder.add_node("bioinformatics_agent", bioinformatics_agent)
router_builder.add_node("bioinfo_interpret_agent", bioinfo_interpret_agent)
router_builder.add_node("literature_agent", literature_agent)
router_builder.add_node("research_image_agent", research_image_agent)
router_builder.add_node("deep_research_agent", deep_research_agent)
router_builder.add_node("llm_call_router", llm_call_router)

# Add edges to connect nodes
router_builder.add_edge(START, "llm_call_router")
router_builder.add_conditional_edges(
    "llm_call_router",
    route_decision,
    {  # Name returned by route_decision : Name of next node to visit
        "chat_agent": "chat_agent",
        "bioinformatics_agent": "bioinformatics_agent",
        "bioinfo_interpret_agent": "bioinfo_interpret_agent",
        "literature_agent": "literature_agent",
        "research_image_agent": "research_image_agent",
        "deep_research_agent": "deep_research_agent",
    },
)
router_builder.add_edge("chat_agent", END)
router_builder.add_edge("bioinformatics_agent", END)
router_builder.add_edge("bioinfo_interpret_agent", END)
router_builder.add_edge("literature_agent", END)
router_builder.add_edge("research_image_agent", END)
router_builder.add_edge("deep_research_agent", END)

# Compile workflow
router_workflow = router_builder.compile()

# 如果需要可视化工作流，取消下面的注释
# from IPython.display import Image
# display(Image(router_workflow.get_graph().draw_mermaid_png()))

# 仅在直接运行此文件时执行测试
if __name__ == "__main__":
    # 简单聊天测试
    state = router_workflow.invoke({"input": "你好，今天天气怎么样？"})
    print("简单聊天示例输出:")
    print(state["output"])
    print("\n")

    # 生信分析测试
    state = router_workflow.invoke({"input": "我需要对RNA-seq数据进行差异表达分析，请给我一些建议。"})
    print("生信分析示例输出:")
    print(state["output"])
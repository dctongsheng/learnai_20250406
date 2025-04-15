from typing_extensions import Literal
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display
from dotenv import load_dotenv
load_dotenv("/Users/wenshuaibi/xm25/envabout/.env")

from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
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


# State
class State(TypedDict):
    input: str
    decision: str
    output: str


# Nodes
def chat_agent(state: State):
    """简单聊天agent - 处理一般对话请求"""

    result = llm.invoke([
        SystemMessage(content="你是一个友好的聊天助手，可以回答用户的一般性问题。"),
        HumanMessage(content=state["input"])
    ])
    return {"output": result.content}


def bioinformatics_agent(state: State):
    """生信分析agent - 处理生物信息学分析请求"""

    result = llm.invoke([
        SystemMessage(content="你是一个专业的生物信息学分析助手，擅长基因组学、转录组学、蛋白质组学等分析方法。"),
        HumanMessage(content=state["input"])
    ])
    return {"output": result.content}


def bioinfo_interpret_agent(state: State):
    """生信解读agent - 解释生物信息学分析结果"""

    result = llm.invoke([
        SystemMessage(content="你是一个专业的生物信息学解读助手，擅长解释各种生物信息学分析结果，包括差异表达分析、富集分析、网络分析等。"),
        HumanMessage(content=state["input"])
    ])
    return {"output": result.content}


def literature_agent(state: State):
    """文献辅助agent - 帮助用户理解和分析科学文献"""

    result = llm.invoke([
        SystemMessage(content="你是一个专业的文献辅助助手，擅长帮助用户理解、总结和分析科学文献，特别是生物医学领域的文献。"),
        HumanMessage(content=state["input"])
    ])
    return {"output": result.content}


def research_image_agent(state: State):
    """科研图片助手agent - 帮助用户理解和创建科研图片"""

    result = llm.invoke([
        SystemMessage(content="你是一个专业的科研图片助手，擅长解释科研图片、提供图片创建建议，以及帮助用户理解各种科学可视化。"),
        HumanMessage(content=state["input"])
    ])
    return {"output": result.content}


def deep_research_agent(state: State):
    """DeepResearchAgent - 深度科研助手"""

    result = llm.invoke([
        SystemMessage(content="你是一个高级科研助手，能够帮助研究人员进行深度的科学研究，包括实验设计、数据分析、结果解释和论文写作等方面。"),
        HumanMessage(content=state["input"])
    ])
    return {"output": result.content}


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

# Show the workflow
# display(Image(router_workflow.get_graph().draw_mermaid_png()))

# Example invocations for testing
# 简单聊天
state = router_workflow.invoke({"input": "你好，今天天气怎么样？"})
print("简单聊天示例输出:")
print(state["output"])
print("\n")

# 生信分析
state = router_workflow.invoke({"input": "我需要对RNA-seq数据进行差异表达分析，请给我一些建议。"})
print("生信分析示例输出:")
print(state["output"])
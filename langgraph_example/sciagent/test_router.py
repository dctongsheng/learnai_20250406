from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display
from dotenv import load_dotenv
load_dotenv("/Users/wenshuaibi/xm25/envabout/.env")

from router import router_workflow

# Test different types of queries
test_queries = [
    "你好，请问今天天气怎么样？",  # 简单聊天
    "我需要对RNA-seq数据进行差异表达分析，请给我一些建议。",  # 生信分析
    "我有一个差异表达基因列表，如何解释这些结果？",  # 生信解读
    "帮我分析一下这篇关于CRISPR的文献的主要发现。",  # 文献辅助
    "如何为我的论文创建一个清晰的实验流程图？",  # 科研图片助手
    "我正在研究癌症免疫治疗，需要设计一个完整的研究方案。"  # 深度研究
]

# Run each query through the router
for i, query in enumerate(test_queries):
    print(f"\n--- 测试 {i+1}: {query} ---")
    state = router_workflow.invoke({"input": query})
    print(f"输出结果:\n{state['output']}")
    print("-" * 50)

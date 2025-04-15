"""
科研助手路由系统 API

使用说明:
1. 安装依赖: pip install fastapi uvicorn
2. 启动服务: uvicorn api:app --reload
3. 访问API文档: http://localhost:8000/docs

API提供以下功能:
- POST /api/query: 发送查询并获取回答
- GET /api/agents: 获取所有可用的专业助手列表
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import time
import asyncio
from contextlib import asynccontextmanager

# 导入路由系统
try:
    from router import router_workflow, Route
except ImportError:
    raise ImportError("请确保router.py文件在同一目录下，并且已安装所有依赖")

# 定义请求和响应模型
class QueryRequest(BaseModel):
    query: str
    user_id: Optional[str] = None

class QueryResponse(BaseModel):
    response: str
    agent_type: str
    processing_time: float

class AgentInfo(BaseModel):
    id: str
    name: str
    description: str

# 创建应用实例
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时的操作
    print("科研助手路由系统API已启动")
    yield
    # 关闭时的操作
    print("科研助手路由系统API已关闭")

app = FastAPI(
    title="科研助手路由系统API",
    description="提供科研助手路由功能的API服务",
    version="1.0.0",
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境中应该限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 定义可用的专业助手
AGENTS = [
    AgentInfo(
        id="chat",
        name="简单聊天助手",
        description="处理一般性对话和问题"
    ),
    AgentInfo(
        id="bioinformatics",
        name="生信分析助手",
        description="处理生物信息学分析请求"
    ),
    AgentInfo(
        id="bioinfo_interpret",
        name="生信解读助手",
        description="解释生物信息学分析结果"
    ),
    AgentInfo(
        id="literature",
        name="文献辅助助手",
        description="帮助用户理解和分析科学文献"
    ),
    AgentInfo(
        id="research_image",
        name="科研图片助手",
        description="帮助用户理解和创建科研图片"
    ),
    AgentInfo(
        id="deep_research",
        name="深度科研助手",
        description="提供深度科研支持"
    ),
]

# 获取所有可用的专业助手
@app.get("/api/agents", response_model=List[AgentInfo], tags=["agents"])
async def get_agents():
    """获取所有可用的专业助手列表"""
    return AGENTS

# 处理查询请求
@app.post("/api/query", response_model=QueryResponse, tags=["query"])
async def process_query(request: QueryRequest):
    """
    处理用户查询并返回回答
    
    - **query**: 用户的查询文本
    - **user_id**: 可选的用户ID，用于未来的历史记录功能
    """
    try:
        # 记录开始时间
        start_time = time.time()
        
        # 使用异步方式调用路由系统
        # 由于LangGraph不是原生异步的，我们使用run_in_executor来避免阻塞
        def run_workflow():
            return router_workflow.invoke({"input": request.query})
        
        # 在线程池中运行同步代码
        state = await asyncio.get_event_loop().run_in_executor(None, run_workflow)
        
        # 计算处理时间
        processing_time = time.time() - start_time
        
        # 构建响应
        return QueryResponse(
            response=state["output"],
            agent_type=state["decision"],
            processing_time=processing_time
        )
    except Exception as e:
        # 记录错误并返回HTTP错误
        error_msg = f"处理查询时出错: {str(e)}"
        print(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

# 健康检查端点
@app.get("/health", tags=["system"])
async def health_check():
    """系统健康检查"""
    return {"status": "healthy", "timestamp": time.time()}

# 直接运行此文件时启动服务
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)

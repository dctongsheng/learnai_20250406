# 科研助手路由系统

这个系统可以根据用户的输入，自动将查询路由到最合适的专业助手，包括：
- 简单聊天助手
- 生信分析助手
- 生信解读助手
- 文献辅助助手
- 科研图片助手
- 深度科研助手

## 项目结构

```
langgraph_example/sciagent/
├── router.py           # 核心路由逻辑
├── api.py              # FastAPI API实现
├── test_router.py      # 路由测试脚本
├── interactive_router.py # 交互式命令行界面
├── serve_static.py     # 静态文件服务器
├── static/             # 静态文件目录
│   └── index.html      # Web客户端
└── README.md           # 本文档
```

## 安装依赖

确保已安装以下依赖：

```bash
pip install fastapi uvicorn langchain-openai langgraph
```

## 使用方法

### 命令行交互

运行交互式命令行界面：

```bash
python interactive_router.py
```

### API服务

启动API服务：

```bash
uvicorn api:app --reload
```

API服务将在 http://localhost:8000 上运行，可以通过 http://localhost:8000/docs 访问API文档。

### Web客户端

1. 首先启动API服务：

```bash
uvicorn api:app --reload
```

2. 然后启动静态文件服务器：

```bash
python serve_static.py
```

这将自动打开浏览器并访问 http://localhost:8080，显示Web客户端界面。

## API端点

- `GET /api/agents` - 获取所有可用的专业助手列表
- `POST /api/query` - 发送查询并获取回答
- `GET /health` - 系统健康检查

## 示例查询

以下是一些示例查询，可以测试不同类型的专业助手：

1. 简单聊天：
   - "你好，请问今天天气怎么样？"
   - "介绍一下你自己"

2. 生信分析：
   - "我需要对RNA-seq数据进行差异表达分析，请给我一些建议。"
   - "如何使用DESeq2进行差异表达分析？"

3. 生信解读：
   - "我有一个差异表达基因列表，如何解释这些结果？"
   - "KEGG富集分析结果如何解读？"

4. 文献辅助：
   - "帮我分析一下这篇关于CRISPR的文献的主要发现。"
   - "总结一下最近关于免疫治疗的研究进展"

5. 科研图片助手：
   - "如何为我的论文创建一个清晰的实验流程图？"
   - "如何制作高质量的蛋白质结构图？"

6. 深度研究：
   - "我正在研究癌症免疫治疗，需要设计一个完整的研究方案。"
   - "帮我设计一个CRISPR筛选实验"

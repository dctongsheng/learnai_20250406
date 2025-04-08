# LearnAI Project - 2025/04/06

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![Project Status](https://img.shields.io/badge/status-active-success)

A repository for exploring AI development patterns and Model Context Protocol (MCP) implementations.

## 📖 Table of Contents
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [MCP Integration](#-mcp-integration)
- [Development](#-development)
- [Contributing](#-contributing)
- [Resources](#-resources)

## 🌟 Features
- LangGraph implementation examples
- MCP client/server prototypes
- Tool memory management patterns
- Basic AI agent scaffolding

## 🚀 Quick Start
```bash
# Clone repository
git clone https://github.com/yourusername/learnai_20250406.git
cd learnai_20250406

# Install dependencies
uv pip install -r requirements.txt

# Run basic example
python main.py
```

## 📂 Project Structure
```
.
├── langgraph_0406/          # LangGraph implementation examples
│   ├── basic.py             # Basic graph setup
│   ├── basic_tool.py        # Tool integration example
│   └── basic_tool_memory.py # Memory-enhanced tools
│
├── mcp_0408/                # Model Context Protocol implementations
│   ├── mcp_client/          # Client-side implementations
│   └── mcp_server/          # Server-side configurations
│
├── main.py                  # Main entry point
├── pyproject.toml           # Project configuration
└── uv.lock                  # Dependency lock file
```

## 🔌 MCP Integration
This project integrates with the [Model Context Protocol Python SDK](https://github.com/modelcontextprotocol/python-sdk).

### Key MCP Features Used:
- Tool chaining patterns
- Context-aware AI agents
- Distributed tool execution

Example client setup:
```python
from mcp_sdk import MCPClient

client = MCPClient(
    server_url="localhost:8080",
    api_key="your_api_key"
)
```

## 🛠 Development
```bash
# Install development dependencies
uv pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Format code
ruff format .
```

## 🤝 Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📚 Resources
- [MCP Documentation](https://github.com/modelcontextprotocol/python-sdk/tree/main?tab=readme-ov-file#documentation)
- [LangChain Documentation](https://python.langchain.com/)
- [AI Engineering Patterns](https://martinfowler.com/articles/ai-engineering-patterns.html)

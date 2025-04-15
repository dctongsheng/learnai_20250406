# 专业Agent模块

这个目录包含了科研助手路由系统中的各种专业agent实现。

## 文件结构

- `__init__.py` - 导出所有agent函数
- `base_agent.py` - 基础agent类，提供共享功能
- `chat_agent.py` - 简单聊天agent
- `bioinformatics_agent.py` - 生信分析agent
- `bioinfo_interpret_agent.py` - 生信解读agent
- `literature_agent.py` - 文献辅助agent
- `research_image_agent.py` - 科研图片助手agent
- `deep_research_agent.py` - 深度科研助手agent

## 设计说明

每个专业agent都是基于BaseAgent类创建的，使用特定的系统提示来定义其专业领域和能力。这种模块化设计使得添加新的专业agent变得简单，只需要创建一个新的文件，定义系统提示，并使用BaseAgent.create_agent()方法创建agent函数即可。

## 使用方法

在router.py中，我们导入所有agent并将它们添加到路由图中：

```python
from agents import (
    chat_agent,
    bioinformatics_agent,
    bioinfo_interpret_agent,
    literature_agent,
    research_image_agent,
    deep_research_agent
)
```

## 添加新的Agent

要添加新的专业agent，请按照以下步骤操作：

1. 在agents目录中创建一个新的Python文件，例如`new_agent.py`
2. 导入BaseAgent和State
3. 定义系统提示
4. 使用BaseAgent.create_agent()创建agent函数
5. 在`__init__.py`中导入并导出新的agent函数
6. 在router.py中更新Route类、route_decision函数和路由图

示例：

```python
# agents/new_agent.py
from .base_agent import BaseAgent, State

# 系统提示
SYSTEM_PROMPT = "你是一个新的专业助手，擅长..."

# 创建agent函数
new_agent = BaseAgent.create_agent(SYSTEM_PROMPT)
```

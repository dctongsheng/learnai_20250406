import asyncio
import os
import json
from typing import Optional
from contextlib import AsyncExitStack

from openai import OpenAI
from dotenv import load_dotenv

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# 加载 .env 文件，确保 API Key 安全保护
load_dotenv("/Users/wenshuaibi/xm25/envabout/.env")

class MCPClient:
    def __init__(self):
        """初始化 MCP 客户端"""
        self.exit_stack = AsyncExitStack()
        self.openapi_api_key = os.getenv("OPENAI_API_KEY")  # 读取 OpenAI API Key
        self.base_url = os.getenv("BASE_URL")  # 读取 BASE URL
        self.model = "gpt-4o" # 读取 model

        if not self.openapi_api_key:
            raise ValueError("❌ 未找到 OpenAI API Key, 请在 .env 文件中设置 OPENAI_API_KEY")
        
        self.client = OpenAI(
            api_key=self.openapi_api_key,
            base_url=self.base_url
        )

    # 创建 OpenAI client
        self.session: Optional[ClientSession] = None  # 初始化 session
        self.exit_stack = AsyncExitStack()

    async def connect_to_server(self, server_script_path: str): 
        """连接到 MCP 服务器并进行调用工具"""
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')

        if not (is_python or is_js):
            raise ValueError("服务器脚本文件必须是 .py 或 .js 文件")

        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )

        # 启动 MCP 服务器并建立通信
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio,self.write = stdio_transport
        #  = stdio_transport.write
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio,self.write))

        # 初始化会话
        await self.session.initialize()

        # 列出 MCP 服务器上的工具
        response = await self.session.list_tools()
        tools = response.tools
        print(f"\n已连接到服务器，支持以下工具：\n", [tool.name for tool in tools])

    async def process_query(self, query: str) -> str:
        """
        使用大模型处理查询并调用 MCP 工具 (Function calling)
        """
        messages = [{"role": "user", "content": query}]
        response = await self.session.list_tools()

        available_tools = [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema,
                }
            }
            for tool in response.tools
        ]
    
    # 可供调试使用，打印可用工具
    # print(available_tools)

    # 请求模型生成响应
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=available_tools
        )

    # 处理返回的内容
        content = response.choices[0]
    
        if content.finish_reason == "tool_calls":
            # 如果返回的是调用工具的指示，则解析工具
            tool_call = content.message.tool_calls[0]
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

            # 执行工具
            result = await self.session.call_tool(tool_name, tool_args)
            print(f"\n\n[calls tool {tool_name} with args {tool_args}]\n\n")

            # 将模型返回的调用结果和工具执行的结果都记录到 messages 中
            messages.append(content.message.model_dump())
            if result and result.content and len(result.content) > 0:
                messages.append({
                    "role": "tool",
                    "content": result.content[0].text,
                    "tool_call_id": tool_call.id,
                })
            else:
                messages.append({
                    "role": "tool",
                    "content": "No weather data available",
                    "tool_call_id": tool_call.id,
                })

            # 将上面的结果再次传递给大模型用于产生最终的结果
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
                )

            return response.choices[0].message.content
        else:
            # 处理非工具调用的普通响应
            return content.message.content

    async def chat_loop(self):
        """运行交互式对话程序"""
        print("\n😃 MCP 客户端已启动！输入 'quit' 退出")
        while True:
            try:
                query = input("\n你: ").strip()
                if query.lower() == 'quit':
                    break
                
                response = await self.process_query(query)  # 发送用于输入到 OpenAI API
                
                print(f"🤖 OpenAI: {response}")
            
            except Exception as e:
                print(f"\n⚠️ 发生错误: {str(e)}")

    async def cleanup(self):
        """清理资源"""
        await self.exit_stack.aclose()

async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)

    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    import sys
    asyncio.run(main())

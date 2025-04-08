import asyncio
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from mcp import ClientSession
from contextlib import AsyncExitStack
# 加载 .env 文件，确保 API Key 受到保护
load_dotenv("/Users/wenshuaibi/xm25/envabout/.env")

class MCPClient:
    def __init__(self):
        """初始化 MCP 客户端"""
        self.exit_stack = AsyncExitStack()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")  # 获取 OpenAI API Key
        self.base_url = os.getenv("BASE_URL")  # 获取 BASE URL
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o")  # 从环境变量获取 model
        
        if not self.openai_api_key:
            raise ValueError("未找到 OpenAI API Key，请在 .env 文件中设置 OPENAI_API_KEY")

        self.client = AsyncOpenAI(api_key=self.openai_api_key, base_url=self.base_url)
    async def connect_to_mock_server(self):
        """模拟 MCP 服务器的连接(暂不连接真实服务器)"""
        print(" MCP 客户端已初始化，但未连接到服务器")

    async def process_query(self, query: str) -> str:
        """调用 OpenAI API 处理用户查询"""
        messages = [
            {"role": "system", "content": "你是一个智能助手，帮助用户回答问题。"},
            {"role": "user", "content": query}
        ]
        try:
            # 调用 OpenAI API
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"调用 OpenAI API 时出现: {str(e)}"

    async def chat_loop(self):
        """运行聊天获取用户输入"""
        print("\n欢迎使用 MCP 客户端！输入 'quit' 退出。")
        
        while True:
            try:
                query = await asyncio.get_event_loop().run_in_executor(
                    None, 
                    lambda: input("\n你: ").strip()
                )
                if query.lower() == 'quit':
                    break
                    
                response = await self.process_query(query)  # 发送用户输入到 OpenAI API
                print(f"\n🤖 OpenAI: {response}")

            except Exception as e:
                print(f"\n⚠️ 发生错误: {str(e)}")

    async def cleanup(self):
        """清理资源"""
        await self.exit_stack.aclose()

async def main():
    client = MCPClient()
    try:
        await client.connect_to_mock_server()
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())

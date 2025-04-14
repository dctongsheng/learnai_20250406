import asyncio
from typing import List, Optional, Any
import aiohttp
from mcp.client import AsyncClient

class AsyncArxivClient:
    """
    arXiv论文搜索异步客户端
    
    使用MCP（Model Context Protocol）异步连接到arXiv搜索服务器
    """
    
    def __init__(self, server_url: str = "http://localhost:8000"):
        """
        初始化arXiv异步客户端
        
        参数:
        - server_url: arXiv服务器URL，默认为http://localhost:8000
        """
        self.client = AsyncClient(server_url)
    
    async def search_arxiv(self, query: str, max_results: int = 10, sort_by: str = "submittedDate") -> List[dict]:
        """
        异步搜索arXiv论文
        
        参数:
        - query: 搜索关键词
        - max_results: 返回结果的最大数量，默认为10
        - sort_by: 排序方式，可选值为"submittedDate"(提交日期)、"lastUpdatedDate"(最后更新)、"relevance"(相关性)，默认为"submittedDate"
        
        返回:
        - 论文信息列表，每篇论文包含标题、作者、摘要、发布时间和PDF链接
        """
        try:
            return await self.client.search_arxiv(query=query, max_results=max_results, sort_by=sort_by)
        except aiohttp.ClientError as e:
            raise RuntimeError(f"arXiv搜索请求失败: {str(e)}") from e
        except asyncio.TimeoutError:
            raise RuntimeError("请求超时，请检查网络连接") from None
    
    async def get_paper_details(self, paper_id: str) -> dict:
        """
        异步获取指定ID的arXiv论文详细信息
        
        参数:
        - paper_id: arXiv论文ID
        
        返回:
        - 论文详细信息，包含标题、作者、摘要、发布时间、PDF链接等
        """
        try:
            return await self.client.get_paper_details(paper_id=paper_id)
        except aiohttp.ClientError as e:
            raise RuntimeError(f"获取论文详情失败: {str(e)}") from e
        except asyncio.TimeoutError:
            raise RuntimeError("请求超时，请检查网络连接") from None
    
    async def close(self):
        """关闭客户端连接"""
        await self.client.close()


async def search_and_get_details(query: str, max_results: int = 3):
    """
    示例函数：搜索论文并获取详细信息
    """
    client = AsyncArxivClient()
    
    try:
        # 异步搜索论文
        print(f"搜索关键词: {query}")
        papers = await client.search_arxiv(query, max_results=max_results)
        
        print(f"\n找到 {len(papers)} 篇相关论文:")
        for i, paper in enumerate(papers):
            print(f"\n论文 {i+1}:")
            print(f"标题: {paper['title']}")
            print(f"作者: {', '.join(paper['authors'])}")
            print(f"发布时间: {paper['published']}")
        
        # 如果有搜索结果，获取第一篇论文的详细信息
        if papers:
            paper_id = papers[0]['id'].split('/')[-1]  # arXiv ID格式通常为arXiv:1234.5678v1
            print(f"\n\n获取论文详情 (ID: {paper_id}):")
            
            details = await client.get_paper_details(paper_id)
            print(f"标题: {details['title']}")
            print(f"作者: {', '.join(details['authors'])}")
            print(f"摘要: {details['summary'][:200]}...")
            print(f"发布时间: {details['published']}")
            print(f"主要分类: {details['primary_category']}")
            print(f"DOI: {details['doi'] or '无'}")
            print(f"PDF链接: {details['pdf_url']}")
    finally:
        # 确保关闭客户端连接
        await client.close()


async def parallel_search(queries: List[str], max_results: int = 2):
    """
    示例函数：并行搜索多个关键词
    """
    client = AsyncArxivClient()
    
    try:
        print("并行搜索多个关键词:")
        # 创建多个搜索任务
        tasks = [client.search_arxiv(query, max_results=max_results) for query in queries]
        
        # 并行执行所有任务
        results = await asyncio.gather(*tasks)
        
        # 处理结果
        for i, (query, papers) in enumerate(zip(queries, results)):
            print(f"\n关键词 '{query}' 的搜索结果:")
            for j, paper in enumerate(papers):
                print(f"  {j+1}. {paper['title']} - {', '.join(paper['authors'][:2])}")
    finally:
        # 确保关闭客户端连接
        await client.close()


if __name__ == "__main__":
    # 运行异步示例
    print("示例1: 搜索并获取详情")
    asyncio.run(search_and_get_details("quantum machine learning"))
    
    print("\n\n" + "="*50 + "\n")
    
    print("示例2: 并行搜索多个关键词")
    asyncio.run(parallel_search([
        "quantum computing", 
        "artificial intelligence", 
        "machine learning"
    ]))

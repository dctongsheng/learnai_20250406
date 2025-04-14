from typing import List, Optional
from mcp.client.sse import sse_client

class ArxivClient:
    """
    arXiv论文搜索客户端
    
    使用MCP（Model Context Protocol）连接到arXiv搜索服务器
    """
    
    def __init__(self, server_url: str = "http://localhost:8000"):
        """
        初始化arXiv客户端
        
        参数:
        - server_url: arXiv服务器URL，默认为http://localhost:8000
        """
        self.client = sse_client(server_url)
    
    def search_arxiv(self, query: str, max_results: int = 10, sort_by: str = "submitted_date") -> List[dict]:
        """
        搜索arXiv论文
        
        参数:
        - query: 搜索关键词
        - max_results: 返回结果的最大数量，默认为10
        - sort_by: 排序方式，可选值为"submitted_date"(提交日期)、"relevance"(相关性)，默认为"submitted_date"
        
        返回:
        - 论文信息列表，每篇论文包含标题、作者、摘要、发布时间和PDF链接
        """
        return self.client.search_arxiv(query=query, max_results=max_results, sort_by=sort_by)
    
    def get_paper_details(self, paper_id: str) -> dict:
        """
        获取指定ID的arXiv论文详细信息
        
        参数:
        - paper_id: arXiv论文ID
        
        返回:
        - 论文详细信息，包含标题、作者、摘要、发布时间、PDF链接等
        """
        return self.client.get_paper_details(paper_id=paper_id)


if __name__ == "__main__":
    # 客户端使用示例
    client = ArxivClient()
    
    # 搜索论文
    print("搜索论文示例:")
    results = client.search_arxiv("quantum computing", max_results=3)
    for i, paper in enumerate(results):
        print(f"\n论文 {i+1}:")
        print(f"标题: {paper['title']}")
        print(f"作者: {', '.join(paper['authors'])}")
        print(f"发布时间: {paper['published']}")
        print(f"PDF链接: {paper['pdf_url']}")
    
    # 获取特定论文详情
    print("\n\n获取论文详情示例:")
    if results and len(results) > 0:
        # 使用搜索结果中的第一篇论文ID
        paper_id = results[0]['entry_id'].split('/')[-1]
        paper = client.get_paper_details(paper_id)
        print(f"标题: {paper['title']}")
        print(f"作者: {', '.join(paper['authors'])}")
        print(f"摘要: {paper['summary'][:200]}...")
        print(f"发布时间: {paper['published']}")
        print(f"更新时间: {paper['updated']}")
        print(f"主要分类: {paper['primary_category']}")
        print(f"PDF链接: {paper['pdf_url']}") 
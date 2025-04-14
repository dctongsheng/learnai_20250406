from typing import List, Optional
from mcp.server.fastmcp import FastMCP
import arxiv

mcp = FastMCP("ArxivSearch")

@mcp.tool()
async def search_arxiv(query: str, max_results: int = 10, sort_by: str = "submitted_date") -> List[dict]:
    """
    搜索arXiv论文。
    
    参数:
    - query: 搜索关键词
    - max_results: 返回结果的最大数量，默认为10
    - sort_by: 排序方式，可选值为"submitted_date"(提交日期)、"relevance"(相关性)，默认为"submitted_date"
    
    返回:
    - 论文信息列表，每篇论文包含标题、作者、摘要、发布时间和PDF链接
    """
    # 构建API客户端
    client = arxiv.Client()
    
    # 设置排序方式
    if sort_by == "submitted_date":
        sort_criterion = arxiv.SortCriterion.SubmittedDate
    elif sort_by == "relevance":
        sort_criterion = arxiv.SortCriterion.Relevance
    else:
        sort_criterion = arxiv.SortCriterion.SubmittedDate
    
    # 创建搜索对象
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=sort_criterion
    )
    
    # 获取搜索结果
    results = client.results(search)
    
    # 构建返回结果
    papers = []
    for result in results:
        paper = {
            "title": result.title,
            "authors": [author.name for author in result.authors],
            "summary": result.summary,
            "published": str(result.published),
            "pdf_url": result.pdf_url
        }
        papers.append(paper)
    
    return papers

@mcp.tool()
async def get_paper_details(paper_id: str) -> dict:
    """
    获取指定ID的arXiv论文详细信息。
    
    参数:
    - paper_id: arXiv论文ID
    
    返回:
    - 论文详细信息，包含标题、作者、摘要、发布时间、PDF链接等
    """
    # 构建API客户端
    client = arxiv.Client()
    
    # 搜索指定ID的论文
    search = arxiv.Search(id_list=[paper_id])
    results = client.results(search)
    
    # 获取论文详情
    for result in results:
        paper = {
            "title": result.title,
            "authors": [author.name for author in result.authors],
            "summary": result.summary,
            "published": str(result.published),
            "updated": str(result.updated),
            "pdf_url": result.pdf_url,
            "entry_id": result.entry_id,
            "primary_category": result.primary_category,
            "categories": result.categories,
            "comment": result.comment,
            "journal_ref": result.journal_ref,
            "doi": result.doi
        }
        return paper
    
    return {"error": "未找到指定ID的论文"}

if __name__ == "__main__":
    mcp.run(transport="sse") 
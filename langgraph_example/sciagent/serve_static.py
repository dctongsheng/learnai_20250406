"""
静态文件服务器

用于在开发环境中提供静态HTML文件服务
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

# 配置
PORT = 8080
DIRECTORY = Path(__file__).parent / "static"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def main():
    # 确保静态目录存在
    os.makedirs(DIRECTORY, exist_ok=True)
    
    # 启动服务器
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"静态文件服务器运行在 http://localhost:{PORT}")
        print(f"提供目录: {DIRECTORY}")
        print("按 Ctrl+C 停止服务器")
        
        # 自动打开浏览器
        webbrowser.open(f"http://localhost:{PORT}")
        
        # 启动服务器
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n服务器已停止")

if __name__ == "__main__":
    main()

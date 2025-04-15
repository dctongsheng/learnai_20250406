"""
启动API服务器和静态文件服务器

这个脚本会同时启动FastAPI服务器和静态文件服务器，方便开发和测试
"""

import subprocess
import sys
import time
import webbrowser
import os
from pathlib import Path

def main():
    print("启动科研助手路由系统...")
    
    # 检查依赖
    try:
        import fastapi
        import uvicorn
    except ImportError:
        print("错误: 缺少必要的依赖。")
        print("请运行: pip install fastapi uvicorn")
        return
    
    # 确保静态目录存在
    static_dir = Path(__file__).parent / "static"
    os.makedirs(static_dir, exist_ok=True)
    
    # 启动API服务器
    api_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "api:app", "--reload", "--port", "8000"],
        cwd=Path(__file__).parent
    )
    
    print("API服务器启动中...")
    time.sleep(2)  # 给API服务器一些启动时间
    
    # 启动静态文件服务器
    static_process = subprocess.Popen(
        [sys.executable, "serve_static.py"],
        cwd=Path(__file__).parent
    )
    
    print("静态文件服务器启动中...")
    time.sleep(1)
    
    print("\n=== 科研助手路由系统已启动 ===")
    print("API服务器: http://localhost:8000")
    print("API文档: http://localhost:8000/docs")
    print("Web客户端: http://localhost:8080")
    print("\n按 Ctrl+C 停止所有服务器")
    
    try:
        # 等待用户中断
        api_process.wait()
    except KeyboardInterrupt:
        print("\n正在停止服务器...")
    finally:
        # 确保两个进程都被终止
        api_process.terminate()
        static_process.terminate()
        print("服务器已停止")

if __name__ == "__main__":
    main()

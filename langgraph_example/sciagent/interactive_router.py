from dotenv import load_dotenv
load_dotenv("/Users/wenshuaibi/xm25/envabout/.env")

from router import router_workflow

def main():
    print("科研助手路由系统")
    print("=" * 50)
    print("可用的专业助手:")
    print("- 简单聊天助手: 处理一般性对话和问题")
    print("- 生信分析助手: 处理生物信息学分析请求")
    print("- 生信解读助手: 解释生物信息学分析结果")
    print("- 文献辅助助手: 帮助用户理解和分析科学文献")
    print("- 科研图片助手: 帮助用户理解和创建科研图片")
    print("- 深度科研助手: 提供深度科研支持")
    print("=" * 50)
    print("系统会自动将您的问题路由到最合适的专业助手。")
    print("输入 'exit' 或 'quit' 退出程序。")
    print("=" * 50)

    while True:
        user_input = input("\n请输入您的问题: ")

        if user_input.lower() in ['exit', 'quit', '退出']:
            print("感谢使用，再见！")
            break

        if not user_input.strip():
            continue

        try:
            # 调用路由系统处理用户输入
            state = router_workflow.invoke({"input": user_input})
            print("\n回答:")
            print(state["output"])
        except Exception as e:
            print(f"处理请求时出错: {str(e)}")

if __name__ == "__main__":
    main()

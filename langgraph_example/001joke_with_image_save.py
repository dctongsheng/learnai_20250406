from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display
from dotenv import load_dotenv
import os
from datetime import datetime

# Import our image saving utility
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.image_saver import save_image_from_bytes

load_dotenv("/Users/wenshuaibi/xm25/envabout/.env")

from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="qwen-max")
# Graph state
class State(TypedDict):
    topic: str
    joke: str
    improved_joke: str
    final_joke: str


# Nodes
def generate_joke(state: State):
    """First LLM call to generate initial joke"""

    msg = llm.invoke(f"Write a short joke about {state['topic']}")
    return {"joke": msg.content}


def check_punchline(state: State):
    """Gate function to check if the joke has a punchline"""

    # Simple check - does the joke contain "?" or "!"
    if "?" in state["joke"] or "!" in state["joke"]:
        return "Fail"
    return "Pass"


def improve_joke(state: State):
    """Second LLM call to improve the joke"""

    msg = llm.invoke(f"Make this joke funnier by adding wordplay: {state['joke']}")
    return {"improved_joke": msg.content}


def polish_joke(state: State):
    """Third LLM call for final polish"""

    msg = llm.invoke(f"Add a surprising twist to this joke: {state['improved_joke']}")
    return {"final_joke": msg.content}


# Build workflow
workflow = StateGraph(State)

# Add nodes
workflow.add_node("generate_joke", generate_joke)
workflow.add_node("improve_joke", improve_joke)
workflow.add_node("polish_joke", polish_joke)

# Add edges to connect nodes
workflow.add_edge(START, "generate_joke")
workflow.add_conditional_edges(
    "generate_joke", check_punchline, {"Fail": "improve_joke", "Pass": END}
)
workflow.add_edge("improve_joke", "polish_joke")
workflow.add_edge("polish_joke", END)

# Compile
chain = workflow.compile()

# Get the Mermaid diagram as PNG bytes
mermaid_png_bytes = chain.get_graph().draw_mermaid_png()

# Show workflow
display(Image(mermaid_png_bytes))

# Save the Mermaid diagram locally
# Create a directory for saved images if it doesn't exist
images_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "saved_images")
os.makedirs(images_dir, exist_ok=True)

# Generate a filename with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
image_filename = f"joke_workflow_{timestamp}.png"
image_path = os.path.join(images_dir, image_filename)

# Save the image
save_image_from_bytes(mermaid_png_bytes, image_path)

# Invoke
state = chain.invoke({"topic": "cats"})
print("Initial joke:")
print(state["joke"])
print("\n--- --- ---\n")
if "improved_joke" in state:
    print("Improved joke:")
    print(state["improved_joke"])
    print("\n--- --- ---\n")

    print("Final joke:")
    print(state["final_joke"])
else:
    print("Joke failed quality gate - no punchline detected!")

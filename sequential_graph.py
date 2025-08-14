import os
from typing import TypedDict, List

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph


load_dotenv()

# Use Google AI API (Gemini) with your API key
llm = ChatGoogleGenerativeAI(
    model=os.getenv("GOOGLE_MODEL_NAME", "gemini-2.5-flash"),
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

class AgentState(TypedDict):
    name: str
    age: str
    final: str


def first_node(state:AgentState) ->AgentState:
    state["final"]= f"Hello {state['name']}"
    return state

def second_node(state:AgentState) ->AgentState:
    state["final"] += f" You are {state['age']} years old."
    return state

graph_builder = StateGraph(AgentState)
graph_builder.add_node("first_node", first_node)
graph_builder.add_node("second_node", second_node)
graph_builder.add_edge("first_node", "second_node")
graph_builder.set_entry_point("first_node")
graph_builder.set_finish_point("second_node")

graph = graph_builder.compile()

result= graph.invoke({"name": "John", "age": "30"})

print(result["final"])  # Output: Hello John You are 30 years old.

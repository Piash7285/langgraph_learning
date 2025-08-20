import os
from typing import TypedDict, List
import random
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    name: str
    number: List[int]
    counter: int

def greeting_node(state: AgentState) -> AgentState:
    state["name"]= f"hey there{state['name']}"
    state["counter"] = 0
    return state

def random_number_node(state: AgentState) -> AgentState:
    state["number"].append(random.randint(1, 10))
    state["counter"] += 1
    return state

def should_continue_node(state: AgentState) -> AgentState:
    if state["counter"] < 5:
        return "random_number_node"
    else:
        return "end_node"

graph=StateGraph(AgentState)
graph.add_node("greeting_node", greeting_node)
graph.add_node("random_number_node", random_number_node)
graph.add_edge("greeting_node", "random_number_node")

graph.add_conditional_edges(
    "random_number_node",
    should_continue_node,
    {"random_number_node": "random_number_node", "end_node": END}
)
graph.set_entry_point("greeting_node")
app=graph.compile()

result=app.invoke({"name": "John", "number": [], "counter": -5})

print(result["name"])
print(result["number"])
print(result["counter"])
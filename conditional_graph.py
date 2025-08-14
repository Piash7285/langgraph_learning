import os
from typing import TypedDict, List

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END


load_dotenv()

# Use Google AI API (Gemini) with your API key
llm = ChatGoogleGenerativeAI(
    model=os.getenv("GOOGLE_MODEL_NAME", "gemini-2.5-flash"),
    google_api_key=os.getenv("GOOGLE_API_KEY")
)


class AgentState(TypedDict):
    first_num: int
    second_num: int
    operator: str
    result: int

def adder (state:AgentState)->AgentState:
    state["result"] = state["first_num"] + state["second_num"]
    return state

def subtractor (state:AgentState)->AgentState:
    state["result"] = state["first_num"] - state["second_num"]
    return state

def decide_next_node(state: AgentState) -> AgentState:
    if state["operator"] == "+":
        return "adder"
    elif state["operator"] == "-":
        return "subtractor"

graph = StateGraph(AgentState)
graph.add_node("add_node", adder)
graph.add_node("subtract_node", subtractor)
graph.add_node("decider", lambda state:state)

graph.add_edge(START, "decider")
graph.add_conditional_edges("decider",
                            decide_next_node,
                            {"adder": "add_node", "subtractor": "subtract_node"}
                            )
graph.add_edge("add_node", END)
graph.add_edge("subtract_node", END)

graph = graph.compile()

result= graph.invoke({
    "first_num": 10,
    "second_num": 5,
    "operator": "+"
})
print(result["result"])  # Should print 15

result = graph.invoke({
    "first_num": 10,
    "second_num": 5,
    "operator": "-"
})
print(result["result"])  # Should print 5
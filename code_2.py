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
    values: List[int]
    name: str
    result: str

def process_values(state: AgentState) -> AgentState:
    """
    this funtion handles multiple different inputs
    """

    state["result"]= f"hi there {state['name']}! Your sum is {sum(state['values'])}."
    return state

graph= StateGraph(AgentState)
graph.add_node("processor", process_values)

graph.set_entry_point("processor")
graph.set_finish_point("processor")
app=graph.compile()

result=app.invoke({"values": [1, 2, 3], "name": "John"})
print(result["result"])  # Output: hi there John! Your sum is 6.
print(result)


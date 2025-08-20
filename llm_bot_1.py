import os
from typing import TypedDict, List

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END

load_dotenv()

# Use Google AI API (Gemini) with your API key
llm = ChatGoogleGenerativeAI(
    model=os.getenv("GOOGLE_MODEL_NAME", "gemini-2.5-flash"),
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

class AgentState(TypedDict):
    messages: List[HumanMessage]

def process(state: AgentState) -> AgentState:
    """
    This function processes the messages and returns a response.
    """
    response = llm.invoke(state["messages"])
    state["messages"].append(response)
    print("response: ",response)
    print(response.content)
    return state

graph= StateGraph(AgentState)
graph.add_node("processor", process)
graph.set_entry_point("processor")
graph.set_finish_point("processor")
app = graph.compile()

user_input= input("Enter your message: ")
result = app.invoke({"messages": [HumanMessage(content=user_input)]})
print("Final response:", result["messages"][-1].content)  # Output: The final response from the LLM
print("All messages:", result["messages"])  # Output: List of all messages exchanged in the conversation
print("Result:", result)  # Output: The
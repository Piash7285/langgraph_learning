import os
from typing import TypedDict, List, Union

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END

load_dotenv()

# Use Google AI API (Gemini) with your API key
llm = ChatGoogleGenerativeAI(
    model=os.getenv("GOOGLE_MODEL_NAME", "gemini-2.5-flash"),
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]


def process_messages(state: AgentState) -> AgentState:
    """
    This function processes the messages and returns a response.
    """
    response = llm.invoke(state["messages"])
    state["messages"].append(AIMessage(content=response.content))
    print(f"\nai: {response.content}")
    return state

graph= StateGraph(AgentState)
graph.add_node("processor", process_messages)
graph.set_entry_point("processor")
graph.set_finish_point("processor")
app = graph.compile()

conversaton_history = []

user_input = input("Enter input: ")

while user_input.lower() != "exit":
    conversaton_history.append(HumanMessage(content=user_input))
    # result = app.invoke({"messages": conversaton_history})
    result = app.invoke({"messages": conversaton_history})
    conversaton_history = result["messages"]

    # Print the AI's response
    # print(f"AI: {result["messages"]}")

    # Get the next user input
    user_input = input("Enter input (or type 'exit' to quit): ")

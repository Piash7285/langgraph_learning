from dotenv import load_dotenv
from typing import Annotated, Literal
from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel
from typing_extensions import TypedDict
import os


load_dotenv()

# Use Google AI API (Gemini) with your API key
llm = ChatGoogleGenerativeAI(
    model=os.getenv("GOOGLE_MODEL_NAME", "gemini-2.5-flash"),
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

class State(TypedDict):
    messages: Annotated[list, add_messages]  # Fixed typo: messeges -> messages


graph_builder=StateGraph(State)

def chatbot(state:State):
    return {"messages": [llm.invoke(state["messages"])]}


graph_builder.add_node("chatbot",chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph= graph_builder.compile()

user_input=input("enter input: ")

state=graph.invoke({"messages": [{"role": "user", "content": user_input}]})

print(state["messages"])
print(state["messages"][-1].content)
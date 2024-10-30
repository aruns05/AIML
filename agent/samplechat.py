import random
from typing import TypedDict, Literal
from IPython.display import Image, display
from pprint import pprint
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, RemoveMessage
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
import os

from dotenv import load_dotenv
load_dotenv()

class State(MessagesState):
    summary: str

def call_model(state:State):
    summary = state.get("summary","")
    if summary:
        system_message = f"Summary of conversation earlier:{summary}"
        messages =[SystemMessage(content=system_message)] + state["messages"]
    else:
        messages = state["messages"]
    
    responses = model.invoke(messages)
    return{"messages": responses}

if __name__ == "__main__":
    os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
    model= ChatOpenAI(model="gpt-4o", temperature=0)
    call_model(State)
        


import random
from typing import TypedDict, Literal
from IPython.display import Image, display
from pprint import pprint
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
import os

from langgraph.graph  MessageState

from dotenv import load_dotenv
load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')


class State(TypedDict):
    graph_state: str

def tool_calling_llm(state: MessagesState):
    print("tool_calling_llm")
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

def Add(a: int, b:int) -> int:
    """Add a and b

    Args:
        a : first int
        b : second int
    """
    return a+b

def Multiply(a: int, b:int) -> int:
    """Multiply a and b

    Args:
        a : first int
        b : second int
    """
    return a*b

def Divide(a: int, b: int) -> float:
    """Division of 2 integers

    Args:
        a : First Integer
        b : Second Integer
    """
    return a/b

def SquareOfInt(a: int) -> int:
    """ Square of a

    Args:
        a : Input
    """
    return a*a

def assistant(state: MessagesState):
    return {"messages":[llm_with_tools.invoke([sys_msg] + state["messages"])]}

def node_1(state):
    print("---Node 1---")
    print("state['graph_state']", state['graph_state'])
    return {"graph_state": state['graph_state'] +  "I am"}

def node_2(state):
    print("---Node 2---")
    return {"graph_state": state['graph_state'] + "Happy"}

def node_3(state):
    print("---Node 3---")
    return {"graph_state": state['graph_state'] + "Sad"}


def decide_mood(state) -> Literal["node_2","node_3"]:
    user_input = state['graph_state']
    
    if random.random() <0.5:
        return "node_2"
    return "node_3"

if __name__ == "__main__":
    
    sys_msg=SystemMessage(content="You are a helpful assistant tasked with performing arithmetic on a set of inputs ")
    
    messages = [AIMessage(content =f"Hello My name is Arun, Are you a doctor", name="Arun")]
    messages.extend(HumanMessage(content =f"Yes I am a doctor", name="Ganesh"))
    
    llm= ChatOpenAI(model="gpt-4o")
    llm_with_tools = llm.bind_tools([Multiply,SquareOfInt, Divide]) 
    
    print("llm_with_tools")
    builder_tool = StateGraph(MessagesState)
   
    # Start edge 
    builder_tool.add_node("tool_calling_llm",tool_calling_llm)
    builder_tool.add_node("tools",ToolNode([Multiply,SquareOfInt,Divide]))
    print('ToolNode', ToolNode)
    builder_tool.add_edge(START,"tool_calling_llm")
    builder_tool.add_conditional_edges(
        "tool_calling_llm",
        #If the latest message (result) is a tool call -> tools_condition routes to tools
        #If the latest message (result) is not a tool call -> tools_condition routes to END
        tools_condition,
    )
    
    #This config variable needs to be on top of all invoke statements 
    # for it to be clubbed under one single execution.
    config = {"configurable": {"thread_id": "1"}}
    
    #print("tools_condition",tools_condition)
    builder_tool.add_edge("tools", END)
    memory = MemorySaver()
    graph_tool = builder_tool.compile(checkpointer = memory)
    
    messages = [HumanMessage(content ="Sum of 10 and 9")]
    messages =  graph_tool.invoke({"messages": messages}, config)
    for m in messages['messages']:
        m.pretty_print()
    
    messages = [HumanMessage(content ="Multiply that by 5")]
    messages =  graph_tool.invoke({"messages": messages}, config)
    for m in messages['messages']:
        m.pretty_print()
    
    #config = {"configurable": {"thread_id": "2"}}
    messages = [HumanMessage(content ="Divide that by 10")]
    messages =  graph_tool.invoke({"messages": messages},config)
    for m in messages['messages']:
        m.pretty_print()

    
    # print('MessagesState', MessagesState.values)
    # for m in MessagesState.values:
    #     print(m)

    
    # builder = StateGraph(State)
    # builder.add_node("tool_calling_llm",node_1)
    # builder.add_node("node_2",node_2)
    # builder.add_node("node_3",node_3)
    
    # builder.add_edge(START,"node_1")
    # builder.add_conditional_edges("node_1",decide_mood)
    # builder.add_edge("node_2",END)
    # builder.add_edge("node_3",END)

    # graph = builder.compile()
    # display(Image(graph.get_graph().draw_mermaid_png()))
    
    # graph.invoke({"graph_state":"Hi, I am Arun"})
    
    
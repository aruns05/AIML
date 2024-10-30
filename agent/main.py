from typing import Union, List

from dotenv import load_dotenv
from langchain.tools import Tool, tool
from langchain.tools.render import render_text_description
from langchain_core.prompts import PromptTemplate
from langchain.schema import AgentAction, AgentFinish
from langchain_openai import ChatOpenAI
from langchain.agents.output_parsers import ReActSingleInputOutputParser

from callback import AgentCallBackHandler 

load_dotenv()


# tool decorator is a langchain utility function, it is used to create tool.
@tool
def get_text_length(text: str) -> int:
    """Returns the length of a text by characters"""
    text = text.strip("\n").strip('"')
    return len(text)

@tool
def sum_2_numbers(x1: int, x2:int) ->int:
     """Returns the sum of 2 numbers"""
     return x1+x2

@tool
def generate_jira_stories(description : str) -> str:
    """Returns the user story and acceptance criteria based on input given"""
    return "" 
    


    
def find_tool_by_name(tools: List[Tool], tool_name: str) -> Tool:
    for tool in tools:
        if tool.name == tool_name:
            return tool
    raise ValueError(f"Tool wtih name {tool_name} not found")

if __name__ == "__main__":
    print("Hello ReAct Langchain")
    tools = [get_text_length, sum_2_numbers, generate_jira_stories]
    
    template ="""
        Answer the following questions as best you can. You have access to the following tools:
        {tools}
        Use the following format:
        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        Final Answer: the final answer to the original input question
        Begin!
        Question: {input}
        Thought:{agent_scratchpad}
    """
    
    prompt = PromptTemplate.from_template(template=template).partial(
        tools=render_text_description(tools),tool_names =",".join([t.name for t in tools])
    )
    
    llm = ChatOpenAI(model="gpt-4o",temperature=0,stop=["\nObservation"], callbacks=[AgentCallBackHandler()])
    intermediate_steps =[]
    agent = {"input":lambda x:x["input"], "agent_scratchpad": lambda x:x["agent_scratchpad"]}|prompt | llm | ReActSingleInputOutputParser()
    #agent = {"input":lambda x:x["input"]}|prompt | llm | ReActSingleInputOutputParser()

    
    print('intermediate_steps', intermediate_steps)
    agent_step: Union[AgentAction, AgentFinish] = agent.invoke(
                                                                {
                                                                    "input":"What is the length of 'DOG' in characters?",
                                                                    "agent_scratchpad":intermediate_steps,
                                                                }
                                                            )
    print(agent_step)
    
    if isinstance(agent_step, AgentAction):
        tool_name = agent_step.tool
        tool_to_use = find_tool_by_name(tools, tool_name)
        tool_input = agent_step.tool_input

        observation = tool_to_use.func(str(tool_input))
        intermediate_steps.append((agent_step, str(observation)))
        print(f"{observation=}")

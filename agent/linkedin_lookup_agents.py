from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)
from langchain import hub
from tools import get_profile_url

import os
from dotenv import load_dotenv

load_dotenv()


def lookup(name: str) -> str:
    OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
    print("OPENAI_API_KEY", OPENAI_API_KEY)
    llm = ChatOpenAI(
        temperature=0,
        model="gpt-3.5-turbo",
    )
    template = """
    Given the full name {name_of_person} I want you to get me link to their Linkedin Profile page. {name_of_person} is a software architect who works with Cognizant Technologies Bengaluru  . Your answer should
    contain only a url
    """
    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )

    tools_for_agent = [
        Tool(
            name="Crawl google 10 linkedin profiles",
            func=get_profile_url,
            description="Useful for when you need to get the linkedin url",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    linked_profile_url = result["output"]
    return linked_profile_url

    # LANGCHAIN O/P PARSER
    # return "https://www.linkedin.com/in/arun-sridhar-7402991a/"


if __name__ == "__main__":
    print(lookup("Arun Sridhar"))
    # link='https://gist.githubusercontent.com/aruns05/8c303b5aa3527f313f2efcc6c3bbece1/raw/e4e8104decd3bd9ba5b1be0da5ed57d81614ac29/gistfile1.txt'

from langchain_community.llms import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
import streamlit as st

## Function to load open ai
def get_openai_response(question):
    llm =OpenAI(api_key=os.environ["OPENAI_API_KEY"],temperature=0.5, model_name="gpt-3.5-turbo")
    response = llm(question)
    return response

##Streamlit app

st.set_page_config(page_title="Q&A Demo")
st.header("LANGCHAIN Application")
submit = st.button("Ask the Question")

input = st.text_input("Input :", key="input")
response=get_openai_response(input)

if submit:
    st.subheader("The response is")
    st.write(response)


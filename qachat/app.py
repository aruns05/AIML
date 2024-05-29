from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai


google_api_key =  os.environ['GOOGLE_API_KEY']
genai.configure(api_key=google_api_key)
model = genai.GenerativeModel('gemini-pro')

chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

st.set_page_config(page_title="QnA")
st.header("GEMINI LLM APPLICATION")

#SESSION STATE FOR CHAT HISTORY IF NOT EXISTS
if 'chat_history' not in st.session_state:
    st.session_state['chat_history']=[]

input = st.text_input("Input:", key="input")
submit = st.button("Ask the question!")

if submit and input:
    response = get_gemini_response(input)
    #ADD to Session
    st.session_state['chat_history'].append(("Arun", input + '\n'))
    st.subheader("The Response is:")
    for chunk in response:
        st.write(chunk.text)

    st.session_state['chat_history'].append(("Bot", chunk.text))
    op = st.session_state['chat_history']
    st.subheader(st.session_state['chat_history'])




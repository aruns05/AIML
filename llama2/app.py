import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers

#function to get response from Llama 
def getLlamarepo(input_text,no_words, blog_style):
    llm = CTransformers(model='models/llama-2-7b-chat.ggmlv3.q8_0.bin',model_type='llama', config={
        'max_new_tokens':256,
        'temperature':0.06
    })

    ##PROMPT TEMPLATE
    template=""" 
            Write a blog for {blog_style} job profile for a topic {input_text}
            within {no_words} words
        """

    prompt = PromptTemplate(input_variables=["blog_style","input_text","no_words"], template=template)
    response = llm(prompt.format(blog_style=blog_style,input_text=input_text,no_words=no_words))
    return response



st.set_page_config(page_title="Generate Blogs", layout="centered", initial_sidebar_state='collapsed')
st.header("Generate Blogs")

input_text = st.text_input("Enter the Blog topic")
col1,col2= st.columns([5,5])

with col1:
    no_words = st.text_input('No of words')
with col2:
    blog_style = st.selectbox('Writing Blog for',('Researchers','Data Scientists','Common People'),index=0)


submit = st.button("Generate")

if submit:
    st.write(getLlamarepo(input_text,no_words, blog_style))

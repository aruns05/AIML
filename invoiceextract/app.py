from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
from PIL import Image
#from google.generativeai import configure, GenerativeModel
import google.generativeai as genai


google_api_key =  os.environ['GOOGLE_API_KEY']
genai.configure(api_key=google_api_key)
#model=GenerativeModel('models/gemini-pro')
model = genai.GenerativeModel('models/gemini-pro')

def get_gemini_response(input_prompt,image,input):
    response = model.generate_content(input_prompt,image[0],input)
    print(response)
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts =[{
            "mime_type": uploaded_file.type,
            "data":bytes_data
        }]
        return image_parts


st.set_page_config(page_title ="Multi-language Invoice Extract")
st.header("Gemini Application")
input = st.text_input("Input Prompt:", key="input")
uploaded_file = st.file_uploader("Chose an image of invoice ...", type=["jpg","jpeg","png"])
image =""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption ="Uploaded Image.", use_column_width= True)

submit = st.button("Tell Me About the Invoice")

input_prompt =""""
You are an expert in understanding invoices. We will upload image as invoice and
you will have to answer any question based on the uploaded invoice image
"""

if submit:
    image_data = input_image_details(uploaded_file)
    response = get_gemini_response(input_prompt,image_data,input)
    st.subheader(" The Response is")
    st.write(response)





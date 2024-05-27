import os
import pathlib
import textwrap
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
from IPython.display import display
from IPython.display import Markdown
import pandas as pd
from PIL import Image

google_api_key =  os.environ['GOOGLE_API_KEY']
genai.configure(api_key=google_api_key)

#Models which you get form Gemini api
# for m in genai.list_models():
#   if 'generateContent' in m.supported_generation_methods:
#     print(m.name)

model = genai.GenerativeModel('models/gemini-pro')
response = model.generate_content('Who hit most number of fours in cricket for India')
print(response.candidates[0].content.parts[0].text)
#print(pd.DataFrame.to_markdown(response.text))


print('Streaming')
response = model.generate_content("Can you let me know the future of ", stream = True)
for chunk in response:
    print(chunk.text)
#print(response.candidates.content.parts.tex)
print(response.prompt_feedback)


#IMages
imgOp = Image.open('./images/idli.jpeg')
model2= genai.GenerativeModel('models/gemini-pro-vision')
response2= model2.generate_content(imgOp)
print(response2.text)



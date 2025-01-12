import os 
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
llm =OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def get_completion(prompt):
    try:
        response = llm.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a very helpful chat assistant."},
                {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
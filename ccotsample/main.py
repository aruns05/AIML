import os 
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
llm =OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def get_completion(prompt, system):
    response = llm.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content


if __name__ == "__main__":
    salary =2000000
    system="Calculate the income tax for the given input {salary} and return the result"
    cot_prompt=f"""
    Please use the following steps only to calculate taxable income
    1. standard_deduction = 50000
    2. taxable income = {salary} - standard_deduction
    3. Once you have calculated the taxable income,use the below tax slabs to calculate the tax
    4. 0-250000 - 0%
    5. 250001-500000 - 5%
    6. 500001-1000000 - 10%
    7. above 1000001 - 15%
    please return only the taxable income and income tax. Donot calculate anything else.
    """
    print("taxable Income and tax:")
    print(get_completion(cot_prompt, system))
    
    
    
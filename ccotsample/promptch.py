import os 
from openai import OpenAI
from dotenv import load_dotenv
from helpers.utilities import get_completion
load_dotenv()
#Client =OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def prompt_chain(initial_prompt, follow_up_prompts):
    result = get_completion(initial_prompt)
    if result is None:
        return "Initial prompt failed."
    print(f"Initial output: {result}\n")
    for i, prompt in enumerate(follow_up_prompts, 1):
        full_prompt = f"{prompt}\n\nPrevious output: {result}"
        result = get_completion(full_prompt)
        if result is None:
            return f"Prompt {i} failed."
        print(f"Step {i} output: {result}\n")
    return result

def analyze_sentiment(text):
    prompt = f"Analyze the sentiment of the following text and respond with only one word - 'positive', 'negative', or 'neutral': {text}"
    sentiment = get_completion(prompt)
    return sentiment.strip().lower()

def conditional_prompt_chain(initial_prompt):
    result = get_completion(initial_prompt)
    if result is None:
        return "Initial prompt failed."
    print(f"Initial output: {result}\n")
    sentiment = analyze_sentiment(result)
    print(f"Sentiment: {sentiment}\n")
    if sentiment == 'positive':
        follow_up = "Given this positive outlook, what are three potential opportunities we can explore?"
    elif sentiment == 'negative':
        follow_up = "Considering these challenges, what are three possible solutions we can implement?"
    else:  # neutral
        follow_up = "Based on this balanced view, what are three key areas we should focus on for a comprehensive approach?"
    final_result = get_completion(f"{follow_up}\n\nContext: {result}")
    return final_result
 
    
if __name__ == "__main__":
    # Example usage
    initial_prompt = "What is the impact of Donald Trump reelection on the H1B visas?"
    final_result = conditional_prompt_chain(initial_prompt)
    print("Final result:", final_result)
    
    # initial_prompt = "Summarize the key trends in global temperature changes over the past century."
    # follow_up_prompts = [
    #     "Based on the trends identified, list the major scientific studies that discuss the causes of these changes.",
    #     "Summarize the findings of the listed studies, focusing on the impact of climate change on marine ecosystems.",
    #     "Propose three strategies to mitigate the impact of climate change on marine ecosystems based on the summarized findings."
    # ]
    # final_result = prompt_chain(initial_prompt, follow_up_prompts)
    # print("Final result:", final_result)
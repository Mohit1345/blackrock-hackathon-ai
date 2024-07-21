import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

# def chat(question, aaple):
#     genai.configure(api_key=os.getenv("gemini_api"))

#     generation_config = {
#         "temperature": 0.9,
#         "top_p": 1,
#         "top_k": 1,
#         "max_output_tokens": 2048,
#     }
#     model = genai.GenerativeModel(
#         model_name="gemini-pro", generation_config=generation_config)

#     prompt_parts = [
#         f"""Answer following question: {question} in 20-30 words. 
#     Based on below data {aaple}
#     """,
#     ]
#     response = model.generate_content(prompt_parts)
#     output = response.text
#     print(response.text)
#     return output

# def motivation(stock, aaple):
#     genai.configure(api_key=os.getenv("gemini_api"))

#     generation_config = {
#         "temperature": 0.9,
#         "top_p": 1,
#         "top_k": 1,
#         "max_output_tokens": 2048,
#     }
#     model = genai.GenerativeModel(model_name="gemini-pro",
#                                   generation_config=generation_config)

#     prompt_parts = [
#         f"""Create a notification for user which can motivate them in Sustainable stocks to invest in this sustainable stock {stock} in 10-20 words.
#         Based on below data {aaple}
#         Keep it cool, engaging and short. Keep it trendy and genZ way.""",
#     ]
#     response = model.generate_content(prompt_parts)
#     output = response.text
#     print(response.text)
#     return output

from openai import OpenAI 

client = OpenAI(
        organization=os.getenv('organization'),
        project=os.getenv('project'),
        api_key=os.getenv('api_key'),
    )

import json

def chat(question, aaple):
    prompt = f"""Answer following question: {question} in 20-30 words. 
     Based on below data {aaple}
    """

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a expert stock market analyst , undertsand user query and resolve it"},
            {"role": "user", "content": prompt},
        ],
    )
    try:
        generated_text = completion.choices[0].message.content
        return generated_text
    except Exception as e:
        print(f"An error occurred: {e}")
        chat(question, aaple)



def motivation(stock, aaple):
    prompt = f"""Create a notification for user which can motivate them in Sustainable stocks to invest in this sustainable stock {stock} in 10-20 words.
        Based on below data {aaple}
        Keep it cool, engaging and short. Keep it trendy and genZ way.
    """

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a expert marketting specialist in a stock market invetment company"},
            {"role": "user", "content": prompt},
        ],
    )
    try:
        generated_text = completion.choices[0].message.content
        return generated_text
    except Exception as e:
        print(f"An error occurred: {e}")
        motivation(stock,aaple)


# print(motivation("AAPL","WHAT IS THIS STOCK"))
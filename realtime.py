# ----employee feedbacks (+1,0,-1)
# ----clients rating (+1,0,-1)
# ----commpany news sentiments (+1,0,-1)
# ----Company announcement specific to care of environment, climate change (compnay policies)
# ----Political and Geopoligical impact of company (+1,0,-1)

from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
import requests
from bs4 import BeautifulSoup
import re
import json
import google.generativeai as genai

def extract_from_search(input_string):
    # print(input_string)
    # Regular expression pattern to extract snippet, title, and link
    pattern = r'\[snippet: (.*?), title: (.*?), link: (.*?)\]'

    # Using re.findall to find all matches
    matches = re.findall(pattern, input_string)

    # List to store dictionaries of extracted data
    data_objects = []

    # Iterating over matches to create dictionaries
    # for match in matches:
    #     data_objects.append({
    #         'snippet': match[0],
    #         'title': match[1],
    #         'link': match[2]
    #     })
    for match in matches:
        data_objects.append(match[0])

    # Printing the extracted data
    # for data in data_objects:
    #     print(data)
    # print(data_objects)
    return data_objects


def get_article_text(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        article_text = ' '.join([p.get_text() for p in soup.find_all('p')])
        return article_text
    except:
        return "Error retrieving article text."


def get_realtime_info(company):
    realtime_info_types = {"employee_satisfaction":"Employee satisfaction and feedback ","client_feedbacks":"clients feedback for ","climate_policies":"climatic change and ESG policies of ","current_internation":"current internation geopolitical news "}

    search_results = {}
    wrapper = DuckDuckGoSearchAPIWrapper(time="y")

    search = DuckDuckGoSearchResults(api_wrapper=wrapper)
    for key, value in realtime_info_types.items(): 
        if value == "employee_satisfaction":
            search_results[key]= extract_from_search(search.run(value+company+" site:glassdoor.co.in"))
        else:
            search_results[key]= extract_from_search(search.run(value+company))
    

    search_data = []
    # print("search results are ",search_results)
    # for link in search_results.values():
    #     # search_data.append(get_article_text(link['link']))
    #     print(link)
    #     search_data.append(link['snippet'])
    # print(search_data)
    # with open("company_data.txt","w", encoding='utf-8') as file:
    #     file.write(f"{search_data}")
    # print(search_data)
    return search_results

# get_realtime_info("apple")


# def scoring(compnay_name,search_results):
#   genai.configure(api_key="Your_API_KEY")

# # Set up the model
#   generation_config = {
#     "temperature": 0.9,
#     "top_p": 1,
#     "top_k": 1,
#     "max_output_tokens": 2048,
#   }
#   model = genai.GenerativeModel(model_name="gemini-pro",
#                                 generation_config=generation_config)
#   json_formate = {
#       "key":"score_value"
#   }
#   output = []
#   for key,value in search_results.items():
#     prompt_parts = [
#         f"""Act as an expert stock analyst and tell {compnay_name} company rating in between [-1,1] for key {key} and data found is {value}.
#         score -1 if its sentiments are negative , 0 if neutral and , 1 if positive
#         provide result in json formate and no extra text
#         ###JSON FORMATE IS###
#         {str(json_formate)}
#         """,
#     ]
#     response = model.generate_content(prompt_parts)
#     output.append(response.text)
#     print(response.text)
#     # output = json.loads(response.text)
#     # print(output['what'])
#     # output = json.loads(response.text)
#   return output

# # search_results = get_realtime_info("apple")
# # print(scoring("apple",search_results))
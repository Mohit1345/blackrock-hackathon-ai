from openai import OpenAI
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the sort attribute from environment variables

client = OpenAI(
        organization=os.getenv('organization'),
        project=os.getenv('project'),
        api_key=os.getenv('api_key'),
    )

companies = ['AAPL',"TSLA",'DIS',"ABNB","ADBE","META","NVDA","JPM","KO","DPZ"]
company_map = {
    'AAPL':"Apple",
    "TSLA":"Tesla",
    "DIS":"Walt Disney Co",
    "ANBN":"Airbnb",
    "ADBE":"Adobe",
    "META":"Meta",
    "NVDA":"Nvidia",
    "JPM":"JP Morgan and Chase Co.",
    "KO":"Coca-cola",
    "DPZ":"Dominos"
}

def get_compnay_details(company):
    compnay_name = company_map[company]

    prompt = f"""Extract company details given ticker {compnay_name} which include what they do, what impact on enviroment do they have, what can be future impact on climate change?
    Provide result in json formate and no extra text.
    """

    completion = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Act as a market specialist and provide information about companies"},
            {"role": "user", "content": prompt},
        ],
        functions=[
            {
                "name": "company_details",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "what":{"type":"string","what":"description of what commpnay does?"},
                        "impact":{"type":"string","what":"description of what impact is in general of their work to environment and climate?"},
                        "future_scope":{"type":"string","what":"what can be their future impact on environment and climate?"}
                    }
                    , "required": ["what", "impact", "future_scope"]
                }
            }
        ],
    )
    try:
        generated_text = completion.choices[0].message.function_call.arguments
        print(generated_text)
        output = json.loads(generated_text)
        return output
    except Exception as e:
        print(f"An error occurred: {e}")
        get_compnay_details(compnay_name)

def scoring(compnay_name,search_results):
    output = []
    print(search_results)
    for key,value in search_results.items():
        prompt = f"""Act as an expert stock analyst and tell {compnay_name} company rating in between [-1,1] for key {key} and data found is {value}.
        Provide result in json formate and no extra text.
        """

        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a expert stock market analyst , undertsand situations and provide most suitable score as per them"},
                {"role": "user", "content": prompt},
            ],
            functions=[
                {
                    "name": "scoring",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "score":{"type":"integer","description":"Just provide score -1 if its sentiments are negative , 0 if neutral and , 1 if positive from complete tedxt data"}
                        }
                    }
                }
            ],
        )
        try:
            generated_text = completion.choices[0].message.function_call.arguments
            print("scoring output ",generated_text)
            ans = json.loads(generated_text)
            output.append(ans)
        except Exception as e:
            print(f"An error occurred: {e}")
            scoring(compnay_name,search_results)
    return output

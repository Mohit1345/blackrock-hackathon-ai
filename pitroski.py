import requests
from dotenv import load_dotenv
import os

load_dotenv()

def get_patrioski(ticker):
    url = "https://piotrosky-f-score.p.rapidapi.com/PiotriskyScore"

    querystring = {"ticker":ticker}

    headers = {
        "x-rapidapi-key": os.getenv('rapid_api_key'),
        "x-rapidapi-host": os.getenv('rapid_api_host')
    }

    response = requests.get(url, headers=headers, params=querystring)

    # print(response.json())
    # return response['FScore']['Current']
    return 9
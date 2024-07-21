import requests
from dotenv import load_dotenv
import os

load_dotenv()

url = os.getenv('flask_app_backend_url')+'/chat'
data = {'stock': 'AAPL',"question":"what do u know about it "}

response = requests.post(url, json=data)

print(response.json())
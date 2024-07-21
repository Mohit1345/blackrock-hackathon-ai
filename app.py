from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from main import get_recommendation
from chatbot import chat, motivation
from flask_cors import CORS
import yfinance as yf
import requests
import os

import json
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

app = Flask(__name__)
CORS(app)

@app.route('/get_score', methods=['GET'])
def recommendation():
    # data = request.get_json()
    # response = {
    #     "received_data": data['stock']
    # }
    # companies = ['AAPL','TSLA']
    companies = ['AAPL',"TSLA",'DIS',"ADBE","META","NVDA","JPM","KO","DPZ"]

    # if data is None:
    #     return jsonify({"error": "No input data provided"}), 400

    final_score = get_recommendation(companies)
    return final_score

@app.route('/chat', methods=['POST'])
def chatting():
    data = request.get_json()
    response = {
        "received_data": data['question'],
        "stock":data['stock']
    }
    if os.path.exists(f"company_data_{response['stock']}.json"):
        data = read_json_file(f"company_data_{response['stock']}.json")
        context = data
    else:
        final_score = get_recommendation(response['stock'])
        data = read_json_file(f"company_data_{response['stock']}.json")
        context = data

    final_score = chat(response['received_data'],context)
    return {"final_score":final_score}

@app.route('/notify/<ticker>')
def create_motivation(ticker='AAPL'):
    if os.path.exists(f"company_data_{ticker}.json"):
        data = read_json_file(f"company_data_{ticker}.json")
        context = data
    else:
        final_score = get_recommendation([f'{ticker}'])
        data = read_json_file(f"company_data_{ticker}.json")
        context = data

    final_score = motivation(ticker,context)
    return jsonify({"final_score":final_score})

@app.route('/stock/<ticker>')
def get_stock_data(ticker='AAPL', years=5):
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=years*365)

    stock = yf.Ticker(ticker)
    print(vars(stock).keys())

    hist_data = stock.history(start=start_date, end=end_date)
    balance_sheet = stock.balance_sheet
    financials = stock.financials
    news = stock.news
    return jsonify({ "hist_data": hist_data.to_json(orient="records"), "balance_sheet": balance_sheet.to_json(orient="records"), "financials": financials.to_json(orient="records"), "news": news })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
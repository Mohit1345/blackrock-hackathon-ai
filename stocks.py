import yfinance as yf
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import ast
import json

def get_article_text(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        article_text = ' '.join([p.get_text() for p in soup.find_all('p')])
        return article_text
    except:
        return "Error retrieving article text."

def get_stock_data(ticker, years):
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=years*365)

    stock = yf.Ticker(ticker)
    print(vars(stock).keys())

    # Retrieve historical price data
    hist_data = stock.history(start=start_date, end=end_date)

    # Retrieve balance sheet
    balance_sheet = stock.balance_sheet

    # Retrieve financial statements
    financials = stock.financials

    # Retrieve news articles
    news = stock.news

    return hist_data, balance_sheet, financials, news

def get_current_price(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period='1d', interval='1m')
    return data['Close'][-1]

if __name__ == "__main__":
    ticker = "NVDA"
    years = 2
    hist_data, balance_sheet, financials, news = get_stock_data(ticker, years)
  
    print('types of data')
    print(type(hist_data))
    print(type(balance_sheet))
    print(type(financials))
    print(type(news))

    print("news ",news)
    hist_data.to_csv("hist_data.csv")
    # balance_sheet.to_csv("balance.csv")
    # financials.to_csv("fianncials.csv")
    # fundamentals.to_csv("fundamentals.csv")

    main_data = {
        # 'hist_data': hist_data,
        # 'balance_sheet': str(balance_sheet),
        # 'financials': str(financials),
        'news': news
    }

    filename = 'data.json'
    with open(filename, 'w') as file:
        json.dump(main_data, file)

    print(f"Data saved to {filename}")
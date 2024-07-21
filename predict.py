import yfinance as yf
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from datetime import date

# Step 1: Retrieve Historical Stock Data from Yahoo Finance
def get_stock_data(symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date)
    return data

# Example: Get data for Apple (AAPL) for the last year
# symbol = 'ABNB'

def get_pf(symbol):
    start_date = '2021-07-01'
    end_date = date.today()
    stock_data = get_stock_data(symbol, start_date, end_date)
    curr_value = stock_data['Close'].values[-1]
    
    # print(stock_data.head())

    # Step 2: Preprocess Data (using Closing Prices)
    closing_prices = stock_data['Close'].values

    # Step 3: Train ARIMA Model
    # ARIMA parameters (p, d, q)
    p = 3  # Autoregressive (AR) order
    d = 1  # Integrated (I) order
    q = 2  # Moving Average (MA) order

    # Fit ARIMA model
    model = ARIMA(closing_prices, order=(p, d, q))
    model_fit = model.fit()

    # Print model summary
    print(model_fit.summary())

    # Step 4: Make Predictions for the Next Month (30 days)
    forecast_steps = 30
    forecast = model_fit.forecast(steps=forecast_steps)
    pred_value= forecast[-1]

    # Generate date range for forecast
    # forecast_dates = pd.date_range(start=end_date, periods=forecast_steps, freq='D')

    # # Plotting
    # plt.figure(figsize=(12, 6))
    # plt.plot(stock_data.index, closing_prices, label='Actual Prices')
    # plt.plot(forecast_dates, forecast, label='Forecasted Prices', linestyle='--')
    # plt.title(f'Stock Price Forecast for {symbol}')
    # plt.xlabel('Date')
    # plt.ylabel('Price')
    # plt.legend()
    # plt.grid(True)
    # plt.show()

    # # Display forecasted prices
    # forecast_df = pd.DataFrame({'Date': forecast_dates, 'Forecasted Price': forecast})
    # print("\nForecasted Prices for the Next Month:")
    # print(forecast_df)
    # return forecast
    check = pred_value-curr_value
    if check>=0:
        return 1
    else:
        return -1

if __name__ == "__main__":
    print(get_pf("AAPL"))
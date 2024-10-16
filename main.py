import pandas as pd
# will use later for dates
# from datetime import datetime, timedelta

import yfinance as yf

#will most likely use custom tkinter on top of matplotlib for visualization later
import matplotlib.pyplot as plt 
from matplotlib import style

#classes
from prediction_models.predict_regression import predict_regression
from visualization.plot_stock_data import plot_stock_data

# info NOTE: 
# ticker: A ticker is a symbol,a unique combination of letters and numbers
# representing a particular stock on an exchange

def get_stock_data(ticker):
    # TODO: Try except block for api call
    try:  
        stock_symbol = yf.Ticker(ticker)
        df = stock_symbol.history(period="3mo")
        if df.empty:
            raise ValueError(f"No data for ticker {ticker}")
        return df
    #testing with 1 month, pandas dataframe
    except Exception as err:
        print(f"error on retrieval {ticker}: {err}")
        return None

def main():

    # temporary styling
    plt.style.use('fivethirtyeight') 
    plt.style.use('dark_background') 

    # TODO: Potentially use a function to convert company name to ticker symbol?
    # FIXME: Current version uses hardcoded ticker 
    # NOTE: Research more on Yahoo Finance API or use different library for this conversion?
    ticker = "GOOG"
    stock_data = get_stock_data(ticker)
    if stock_data is not None:
        # print(stock_data.head())
        plot_stock_data(stock_data, ticker)
        predict_regression(stock_data, ticker)
    else:
        print("process error for stock data")
    
    
if __name__ == "__main__":
    main()
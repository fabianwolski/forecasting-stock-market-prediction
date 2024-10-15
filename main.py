import pandas as pd
# will use later for dates
# from datetime import datetime, timedelta

import yfinance as yf

#will most likely use custom tkinter on top of matplotlib for visualization later
import matplotlib.pyplot as plt 
from matplotlib import style

# info NOTE: 
# ticker: A ticker is a symbol,a unique combination of letters and numbers
# representing a particular stock on an exchange

def get_stock_data(ticker):
    # TODO: Try except block for api call

    stock_symbol = yf.Ticker(ticker)
    #testing with 1 month, pandas dataframe
    df = stock_symbol.history(period="1mo")

    return df

def main():
    # TODO: plot data
    #temporary styling
    # plt.style.use('dark_background') 

    # TODO: Potentially use a function to convert company name to ticker symbol?
    # FIXME: Current version uses hardcoded ticker 
    # NOTE: Research more on Yahoo Finance API or use different library for this conversion?
    ticker = "GOOG"
    
    stock_data = get_stock_data(ticker)
    
    print(stock_data.head())
    
    

    
if __name__ == "__main__":
    main()
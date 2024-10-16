import matplotlib.pyplot as plt 

def plot_stock_data(df, ticker):
    
    plt.figure(figsize=(16, 8))
    plt.title(f"stock visual {ticker}")
    plt.plot(df['Close'])
    plt.xlabel("Date", fontsize = 18)
    #USD to EUR converter function??
    plt.ylabel("Close price in USD",fontsize = 18)

    plt.show()
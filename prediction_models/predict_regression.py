from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


def prep_data(df):
    #Won't need the below columns to run model
    df = df.drop(columns=["Dividends", "Stock Splits"])
    #remove any duplicates 
    df = df.drop_duplicates(keep=False)
    
    #TODO: For Jupiter Notebooks add data visualization here
    #NOTE: I am just jumping straight to regression prep
    
    #dependant variable - so data worked on
    y = df["Close"].values
    #independant, so for change in x how does it affect y
    x = df[["Open", "High", "Low", "Volume"]].values
    
    #we need to split data training/test 80/20
    X_train, X_test, y_train, y_test = train_test_split(X,y, random_state=11, test_size=0.2)

    return X_train, X_test, y_train, y_test

def predict_regression(data, ticker):
    
    X_train, X_test, y_train, y_test = prep_data(data)
    
    reg = LinearRegression()
    #using train data
    reg_model = reg.fit(X_train, y_train)
    #predicting
    predict = reg.predict(X_test)
    
    #TODO: I need to think of what I want to return...
    #NOTE: I will have multiple models... How do I keep a consistant return structure????
    #NOTE: make a class for all predicitons???
    #NOTE: if I want to run API calls later? I need to have easy json convert.
    

    
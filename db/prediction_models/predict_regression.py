from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import root_mean_squared_error, r2_score
import numpy as np
from .base_predictor import BasePredictor
# from prediction_models.prediction_result import PredictionResult

class RegressionPredictor(BasePredictor):
    def __init__(self):
        self.model = LinearRegression()

        #TODO: Graph for all models
        #TODO: Architecture diagram
        #adavntages/disadvantages of your approach
        #computation time? user feedback -two types of visualization.
        #how do i assess my project? From user perspective, programming perspecitve, or ML? SImplicity.
    def prep_data(self, df):
        df = df.copy()
        #Won't need the below columns to run model
        df = df.drop(columns=["Dividends", "Stock Splits"])
        #remove any duplicates 
        df = df.drop_duplicates(keep=False)
    
        #TODO: For Jupiter Notebooks add data visualization here
        #NOTE: I am just jumping straight to regression prep
    
        #dependant variable - so data worked on
        y = df["Close"].values
        #independant, so for change in x how does it affect y
        X = df[["Open", "High", "Low", "Volume"]].values
    
        #we need to split data training/test 80/20
        X_train, X_test, y_train, y_test = train_test_split(X,y, random_state=11, test_size=0.2)

        return X_train, X_test, y_train, y_test

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)
        return self.model
    
    def predict(self, X):
        return self.model.predict(X)
    
    def evaluate(self, y_true, y_pred):
        mse_val = root_mean_squared_error(y_true, y_pred)
        rmse_val = np.sqrt(mse_val)
        r2_val = r2_score(y_true, y_pred)
        
        #additional calculations (may remove)
        mae_val = np.mean(np.abs(y_true - y_pred))
        mape_val = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
        
        return {
            "mse": float(mse_val), #Mean Squared Error
            "rmse": float(rmse_val), #Root Mean Squared Error
            "r2": float(r2_val),
            "mae": float(mae_val), #Mean Absolute Error
            "mape": float(mape_val) #Mean Absolute Percentage Error
        }
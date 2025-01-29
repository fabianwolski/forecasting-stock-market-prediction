from statsmodels.tsa.arima.model import ARIMA
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from .base_predictor import BasePredictor

class ARIMAPredictor(BasePredictor):
    def __init__(self):
        self.model = None
        self.order = (1, 1, 1)  #default ARIMA order
    
    def prep_data(self, df):
        df = df.copy()
        #drop unnecessary columns
        df = df.drop(columns=["Dividends", "Stock Splits"])
        df = df.drop_duplicates(keep=False)
        
        #target variable
        y = df["Close"].values
        X = df[["Open", "High", "Low", "Volume"]].values
        
        #train/test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=11, test_size=0.2)
        
        return X_train, X_test, y_train, y_test
    
    def train(self, X_train, y_train):
        #training data fitting
        self.model = ARIMA(y_train, order=self.order)
        self.fitted_model = self.model.fit()
        return self.fitted_model
    
    def predict(self, X):
        if self.fitted_model is None:
            raise ValueError("Model needs to be trained before predictions")
            
        #same num of points as input X
        predictions = self.fitted_model.forecast(steps=len(X))
        return predictions
    
    def evaluate(self, y_true, y_pred):
        mse = np.mean((y_true - y_pred) ** 2)
        rmse = np.sqrt(mse)
        r2 = np.corrcoef(y_true, y_pred)[0, 1]**2
        mae = np.mean(np.abs(y_true - y_pred))
        mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
        
        return {
            "mse": float(mse),
            "rmse": float(rmse),
            "r2": float(r2),
            "mae": float(mae),
            "mape": float(mape)
        }
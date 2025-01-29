from prophet import Prophet
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from .base_predictor import BasePredictor

class ProphetPredictor(BasePredictor):
    def __init__(self):
        self.model = Prophet()
    
    def prep_data(self, df):
        df = df.copy()
        # Drop unnecessary columns
        df = df.drop(columns=["Dividends", "Stock Splits"])
        df = df.drop_duplicates(keep=False)
        
        # Create X and y first
        X = df.index.tz_localize(None)  # dates without timezone
        y = df['Close'].values  # target values
        
        # Split the data first
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, random_state=11, test_size=0.2
        )
        
        # Create Prophet dataframes after splitting
        X_train_df = pd.DataFrame({'ds': X_train, 'y': y_train})
        X_test_df = pd.DataFrame({'ds': X_test, 'y': y_test})
        
        return X_train_df, X_test_df, y_train, y_test
    
    def train(self, X_train, y_train):
        # X_train is already in the correct format with 'ds' and 'y' columns
        self.model.fit(X_train)
        return self.model
    
    def predict(self, X):
        forecast = self.model.predict(X)
        return forecast['yhat'].values
    
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
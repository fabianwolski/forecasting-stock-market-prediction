from statsmodels.tsa.arima.model import ARIMA
import pandas as pd
import numpy as np
from .base_predictor import BasePredictor

class ARIMAPredictor(BasePredictor):
    def __init__(self):
        self.model = None
        self.order = (1,1,1)  #default ARIMA order
    
    def prep_data(self, df):
        df = df.copy()
        
        df['Prev_Close'] = df['Close'].shift(1)
        df = df.dropna()
        
        split_idx = int(len(df) * 0.8)
        train_df = df.iloc[:split_idx]
        test_df = df.iloc[split_idx:]
        
        train_dates = train_df.index
        test_dates = test_df.index
        
        y_train = train_df["Close"].values
        y_test = test_df["Close"].values
        
        X_train = train_df[["Prev_Close"]].values
        X_test = test_df[["Prev_Close"]].values
        
        return X_train, X_test, y_train, y_test, train_dates, test_dates
    
    def train(self, X_train, y_train):
        self.model = ARIMA(y_train, order=self.order, exog=X_train)
        self.fitted_model = self.model.fit()
        return self.fitted_model
    
    def predict(self, X, dates=None):
        if self.fitted_model is None:
            raise ValueError("Model needs to be trained before predictions")
            
        raw_predictions = self.fitted_model.forecast(steps=len(X), exog=X)
        
        if dates is not None:
            return {
                'values': raw_predictions,
                'formatted': [{
                    'Date': pd.Timestamp(date).strftime('%Y-%m-%d'),
                    'Prediction': float(pred)
                } for date, pred in zip(dates, raw_predictions)]
            }
        return raw_predictions
    
    def evaluate(self, y_true, predictions):
        y_pred = predictions['values'] if isinstance(predictions, dict) else predictions
        
        mse = np.mean((y_true - y_pred) ** 2)
        rmse = np.sqrt(mse)
        
        # Safe correlation calculation
        with np.errstate(divide='ignore', invalid='ignore'):
            r2 = np.corrcoef(y_true, y_pred)[0, 1]**2
            r2 = float(r2) if not np.isnan(r2) else 0.0
        
        mae = np.mean(np.abs(y_true - y_pred))
        mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
        
        return {
            "metrics": {
                "mse": float(mse),
                "rmse": float(rmse),
                "r2": r2,
                "mae": float(mae),
                "mape": float(mape)
            },
            "predictions": predictions['formatted'] if isinstance(predictions, dict) else None
        }
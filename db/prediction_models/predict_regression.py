from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
from .base_predictor import BasePredictor

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
        
        all_dates = df.index
        split_idx = int(len(df) * 0.8)
        
        X = pd.DataFrame(index=all_dates)
        
        X['sin_month'] = np.sin(2 * np.pi * all_dates.month / 12)
        X['cos_month'] = np.cos(2 * np.pi * all_dates.month / 12)
        X['sin_day'] = np.sin(2 * np.pi * all_dates.day / 31)
        X['cos_day'] = np.cos(2 * np.pi * all_dates.day / 31)
        X['sin_weekday'] = np.sin(2 * np.pi * all_dates.dayofweek / 7)
        X['cos_weekday'] = np.cos(2 * np.pi * all_dates.dayofweek / 7)
        
        lag = 3  
        X['lagged_close'] = df['Close'].shift(lag)
        X['lagged_volume'] = df['Volume'].shift(lag)
        
        X['ma10'] = df['Close'].shift(lag).rolling(window=10, min_periods=1).mean()
        X['ma30'] = df['Close'].shift(lag).rolling(window=30, min_periods=1).mean()
        X['ma50'] = df['Close'].shift(lag).rolling(window=50, min_periods=1).mean()
        
        X['vol_ma10'] = df['Volume'].shift(lag).rolling(window=10, min_periods=1).mean()
        
        X['weekly_return'] = (df['Close'] / df['Close'].shift(5) - 1).shift(lag).fillna(0)
        X['monthly_return'] = (df['Close'] / df['Close'].shift(20) - 1).shift(lag).fillna(0)
        
        X['trend_50_200'] = (X['ma50'] > df['Close'].shift(lag).rolling(window=200, min_periods=1).mean()).astype(int)
        

        X = X.fillna(method='bfill').fillna(method='ffill')
        

        X_train = X.iloc[:split_idx].values
        X_test = X.iloc[split_idx:].values
        y_train = df['Close'].iloc[:split_idx].values
        y_test = df['Close'].iloc[split_idx:].values
        
        return X_train, X_test, y_train, y_test, all_dates[:split_idx], all_dates[split_idx:]

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)
        return self.model
    
    def predict(self, X, dates=None):
        raw_predictions = self.model.predict(X)
        
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
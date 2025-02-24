import xgboost as xgb
import pandas as pd
import numpy as np
from .base_predictor import BasePredictor

class XGBoostPredictor(BasePredictor):
    def __init__(self):
        self.model = None
        self.params = {
            'objective': 'reg:squarederror',
            'learning_rate': 0.1,
            'max_depth': 6,
            'n_estimators': 100,
            'subsample': 0.8,
            'colsample_bytree': 0.8
        }
        
    def create_features(self, df):
        df = df.copy()
        
        initial_close = df['Close'].iloc[0]
        initial_volume = df['Volume'].iloc[0]
        
        df['MA5'] = df['Close'].rolling(window=5, min_periods=1).mean()
        df['MA20'] = df['Close'].rolling(window=20, min_periods=1).mean()
        df['VOL_MA5'] = df['Volume'].rolling(window=5, min_periods=1).mean()
        
        df['Returns'] = df['Close'].pct_change().fillna(0)
        
        delta = df['Close'].diff()
        delta = delta.fillna(0)
        gain = (delta.where(delta > 0, 0)).rolling(window=14, min_periods=1).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14, min_periods=1).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        df['RSI'] = df['RSI'].fillna(50) 
        
        return df
    
    def prep_data(self, df):
        all_dates = df.index
        split_idx = int(len(df) * 0.8)
        
        df = self.create_features(df)
        
        feature_cols = ['MA5', 'MA20', 'RSI', 'VOL_MA5', 'Returns']
        target = 'Close'
        
        train_df = df.iloc[:split_idx]
        test_df = df.iloc[split_idx:]
        
        X_train = train_df[feature_cols].values
        X_test = test_df[feature_cols].values
        y_train = train_df[target].values
        y_test = test_df[target].values
        
        return X_train, X_test, y_train, y_test, all_dates[:split_idx], all_dates[split_idx:]
    
    def train(self, X_train, y_train):
        self.model = xgb.XGBRegressor(**self.params)
        self.model.fit(X_train, y_train)
        return self.model
    
    def predict(self, X, dates=None):
        if self.model is None:
            raise ValueError("Model needs to be trained before predictions")
            
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
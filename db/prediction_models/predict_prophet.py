from prophet import Prophet
import pandas as pd
import numpy as np
from .base_predictor import BasePredictor

class ProphetPredictor(BasePredictor):
    def __init__(self):
        self.model = Prophet(
            changepoint_prior_scale=0.01,
            seasonality_prior_scale=0.01,
            seasonality_mode='multiplicative',
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=False,
            interval_width=0.95
        )
    
    def prep_data(self, df):

        df = df.copy()
        
        prophet_df = pd.DataFrame({
            'ds': df.index.tz_localize(None),
            'y': df['Close'].values
        })
        
        split_idx = int(len(df) * 0.8)
        
        train_df = prophet_df.iloc[:split_idx]
        test_df = prophet_df.iloc[split_idx:]
        
        train_dates = df.index[:split_idx]
        test_dates = df.index[split_idx:]
        
        y_train = train_df['y'].values
        y_test = test_df['y'].values
        
        return train_df, test_df, y_train, y_test, train_dates, test_dates
    
    def train(self, X_train, y_train):
        self.model.add_regressor('lower_bound', standardize=False)
        self.model.add_regressor('upper_bound', standardize=False)
        
        train_df = X_train.copy()
        y_std = np.std(y_train)
        y_mean = np.mean(y_train)
        
        train_df['lower_bound'] = y_mean - 2 * y_std
        train_df['upper_bound'] = y_mean + 2 * y_std
        
        self.y_mean = y_mean
        self.y_std = y_std
        
        self.model.fit(train_df)
        return self.model
    
    def predict(self, X, dates=None):
        if not isinstance(self.model, Prophet):
            raise ValueError("Model needs to be trained before predictions")
        
        future = X.copy()
        future['lower_bound'] = self.y_mean - 2 * self.y_std
        future['upper_bound'] = self.y_mean + 2 * self.y_std
        
        forecast = self.model.predict(future)
        raw_predictions = forecast['yhat'].values
        
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
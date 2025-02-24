import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from .base_predictor import BasePredictor

class LSTMPredictor(BasePredictor):
    def __init__(self):
        self.model = None
        self.scaler = MinMaxScaler()
        self.sequence_length = 10  #no of time steps to look back
        
    def create_sequences(self, data):
        X, y = [], []
        for i in range(len(data) - self.sequence_length):
            X.append(data[i:(i + self.sequence_length)])
            y.append(data[i + self.sequence_length])
        return np.array(X), np.array(y)
    
    def prep_data(self, df):
        df = df.copy()
        
        all_dates = df.index
        split_idx = int(len(df) * 0.8)
        
        #scaling
        scaled_data = self.scaler.fit_transform(df[['Close']].values)
        
        # Scaling
        pad_data = np.repeat(scaled_data[0], self.sequence_length).reshape(-1, 1)
        padded_data = np.vstack((pad_data, scaled_data))
        
        X, y = [], []
        for i in range(len(padded_data) - self.sequence_length):
            X.append(padded_data[i:(i + self.sequence_length)])
            y.append(padded_data[i + self.sequence_length])
        
        X = np.array(X)
        y = np.array(y)
        
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]
        train_dates = all_dates[:split_idx]
        test_dates = all_dates[split_idx:]
        
        return X_train, X_test, y_train, y_test, train_dates, test_dates
    
    def train(self, X_train, y_train):
        self.model = Sequential([
            LSTM(50, activation='relu', return_sequences=True, input_shape=(self.sequence_length, 1)),
            Dropout(0.2),
            LSTM(50, activation='relu'),
            Dropout(0.2),
            Dense(1)
        ])
        
        self.model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
        self.model.fit(X_train, y_train, epochs=50, batch_size=32, verbose=0)
        return self.model
    
    def predict(self, X, dates=None):
        if self.model is None:
            raise ValueError("Model needs to be trained before predictions")
            
        raw_predictions = self.model.predict(X)
        unscaled_predictions = self.scaler.inverse_transform(raw_predictions)
        
        if dates is not None:
            return {
                'values': unscaled_predictions.flatten(),
                'formatted': [{
                    'Date': pd.Timestamp(date).strftime('%Y-%m-%d'),
                    'Prediction': float(pred)
                } for date, pred in zip(dates, unscaled_predictions.flatten())]
            }
        return unscaled_predictions.flatten()

    def evaluate(self, y_true, predictions):
        y_pred = predictions['values'] if isinstance(predictions, dict) else predictions
        y_true_unscaled = self.scaler.inverse_transform(y_true.reshape(-1, 1)).flatten()
        
        mse = np.mean((y_true_unscaled - y_pred) ** 2)
        rmse = np.sqrt(mse)
        
        with np.errstate(divide='ignore', invalid='ignore'):
            r2 = np.corrcoef(y_true_unscaled, y_pred)[0, 1]**2
            r2 = float(r2) if not np.isnan(r2) else 0.0
        
        mae = np.mean(np.abs(y_true_unscaled - y_pred))
        mape = np.mean(np.abs((y_true_unscaled - y_pred) / y_true_unscaled)) * 100
        
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
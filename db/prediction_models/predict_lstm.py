import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
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
        #dropping unnecessary columns
        df = df.drop(columns=["Dividends", "Stock Splits"])
        df = df.drop_duplicates(keep=False)
        
        # Scaling
        features = ["Open", "High", "Low", "Close", "Volume"]
        scaled_data = self.scaler.fit_transform(df[features])
        
        #creating sequences
        X, y = self.create_sequences(scaled_data)
        
        #train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        return X_train, X_test, y_train, y_test

    def train(self, X_train, y_train):
        #LSTM definetion
        self.model = Sequential([
            LSTM(50, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])),
            Dropout(0.2),
            LSTM(50, return_sequences=False),
            Dropout(0.2),
            Dense(y_train.shape[1])
        ])
        
        #compiling model
        self.model.compile(optimizer=Adam(learning_rate=0.001), loss='mse')
        
        #training model
        self.model.fit(
            X_train, 
            y_train,
            epochs=50,
            batch_size=32,
            validation_split=0.1,
            verbose=0
        )
        
        return self.model

    def predict(self, X):
        if self.model is None:
            raise ValueError("Model needs to be trained before making predictions")
        return self.model.predict(X)

    def evaluate(self, y_true, y_pred):
        #converting predictions back to original scale for metrics
        # Getting close price
        y_true_close = self.scaler.inverse_transform(y_true)[:, 3] 
        y_pred_close = self.scaler.inverse_transform(y_pred)[:, 3]  
        
        #calculating 
        mse = np.mean((y_true_close - y_pred_close) ** 2)
        rmse = np.sqrt(mse)
        mae = np.mean(np.abs(y_true_close - y_pred_close))
        mape = np.mean(np.abs((y_true_close - y_pred_close) / y_true_close)) * 100
        
        #R2
        ss_res = np.sum((y_true_close - y_pred_close) ** 2)
        ss_tot = np.sum((y_true_close - np.mean(y_true_close)) ** 2)
        r2 = 1 - (ss_res / ss_tot)
        
        return {
            "mse": float(mse),
            "rmse": float(rmse),
            "r2": float(r2),
            "mae": float(mae),
            "mape": float(mape)
        }
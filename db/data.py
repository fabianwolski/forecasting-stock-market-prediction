from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd

from prediction_models import MODEL_REGISTRY 

app = Flask(__name__)
CORS(app)

def get_stock_data(ticker, start , end, model_type=None):
    try:  
        stock_symbol = yf.Ticker(ticker)
        df = stock_symbol.history( 
            start=start,
            end=end
            )
        print(f"Initial data shape: {df.shape}")
        print(f"Initial data columns: {df.columns}")
        print(f"NaN values in initial data:\n{df.isna().sum()}")
        if df.empty:
            raise ValueError(f"No data for ticker {ticker}")
        
        # Get predictions if model_type is specified
        predictions = None
        metrics = None
        if model_type is not None:
            if model_type not in MODEL_REGISTRY:
                raise ValueError(f"Invalid model type: {model_type}. Available models: {list(MODEL_REGISTRY.keys())}")
            
            predictor = MODEL_REGISTRY[model_type]()
            print(f"Using model type: {model_type}")
            X_train, X_test, y_train, y_test = predictor.prep_data(df.copy())
            print(f"After prep_data - X_train shape: {X_train.shape}")
            # Train model
            predictor.train(X_train, y_train)
            
            # Make predictions
            train_pred = predictor.predict(X_train)
            test_pred = predictor.predict(X_test)
            
            # Get metrics
            train_metrics = predictor.evaluate(y_train, train_pred)
            test_metrics = predictor.evaluate(y_test, test_pred)
            
            metrics = {
                "train": train_metrics,
                "test": test_metrics
            }
        
        # Convert datetime index to string for JSON
        #Convert datetime index to string for JSON 
        df.index = df.index.strftime('%Y-%m-%d')
        #dictionary conversion for JSON
        stock_data = df.reset_index().to_dict('records')

        
        return {
            "data": stock_data,
            "predictions": metrics
        }
        
    except Exception as err:
        print(f"error on retrieval {ticker}: {err}")
        raise Exception(f"Failed to get data for {ticker}: {str(err)}")


@app.route('/', methods = ['GET'])
def home():
    return jsonify({
        "success" : True,
        "message" : "Stock API is running. Use /stock for data request",
        "available_models": list(MODEL_REGISTRY.keys())
    })


@app.route('/stock', methods = ['GET', 'POST'])
def data():
    if request.method == 'POST':
        try:
            print("Received POST request")
            data = request.json
            print(f"Request data: {data}")

            ticker = data.get('ticker')
            start = data.get('start')
            end = data.get('end')
            model_type = data.get('model_type')
            
            if not all([ticker,start,end]):
                return jsonify({
                    "error" : "Missing Field",
                    "required": {
                        "ticker": bool(ticker),
                        "start": bool(start),
                        "end": bool(end)
                    }
                }), 400
        
            stock_data = get_stock_data(ticker, start=start,end=end, model_type=model_type)
            return jsonify({
                "success": True,
                "message": f"data retrieved success for {ticker}",
                "data": stock_data['data'],       #unpack dict
                "predictions": stock_data['predictions']
            }), 200
        
        except Exception as e:
            print(f"Error on request: {e}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 400
           
       
    #get request
    return jsonify({
        "success": True,
        "message": "Use POST method with ticker, start, and end dates",
        "available_models": list(MODEL_REGISTRY.keys())  
    }), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)

    
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd

from prediction_models import MODEL_REGISTRY 

app = Flask(__name__)
CORS(app)

def get_stock_data(ticker, start, end, model_type=None):
    try:  
        stock_symbol = yf.Ticker(ticker)
        
        # Get historical data
        df = stock_symbol.history(
            start=start,
            end=end
        )
        
        # Get additional stock information
        info = stock_symbol.info
        
        # Extract relevant stock information
        stock_info = {
            "longName": info.get("longName"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "marketCap": info.get("marketCap"),
            "currentPrice": info.get("currentPrice"),
            "fiftyTwoWeekHigh": info.get("fiftyTwoWeekHigh"),
            "fiftyTwoWeekLow": info.get("fiftyTwoWeekLow"),
            "volume": info.get("volume"),
            "averageVolume": info.get("averageVolume"),
            "peRatio": info.get("trailingPE"),
            "beta": info.get("beta"),
            "dividendYield": info.get("dividendYield"),
            "longBusinessSummary": info.get("longBusinessSummary"),
            "website": info.get("website"),
            "fullTimeEmployees": info.get("fullTimeEmployees"),
            "city": info.get("city"),
            "country": info.get("country"),
            "recommendationKey": info.get("recommendationKey"),
            "numberOfAnalystOpinions": info.get("numberOfAnalystOpinions")
        }
        
        # Handle predictions if model_type is specified
        predictions = None
        metrics = None
        if model_type is not None:
            if model_type not in MODEL_REGISTRY:
                raise ValueError(f"Invalid model type: {model_type}. Available models: {list(MODEL_REGISTRY.keys())}")
            
            predictor = MODEL_REGISTRY[model_type]()
            X_train, X_test, y_train, y_test = predictor.prep_data(df.copy())
            predictor.train(X_train, y_train)
            
            train_pred = predictor.predict(X_train)
            test_pred = predictor.predict(X_test)
            
            metrics = {
                "train": predictor.evaluate(y_train, train_pred),
                "test": predictor.evaluate(y_test, test_pred)
            }
        
        # Convert datetime index to string for JSON
        df.index = df.index.strftime('%Y-%m-%d')
        stock_data = df.reset_index().to_dict('records')
        
        return {
            "historical_data": stock_data,
            "stock_info": stock_info,
            "predictions": metrics
        }
        
    except Exception as err:
        print(f"Error retrieving data for {ticker}: {err}")
        raise Exception(f"Failed to get data for {ticker}: {str(err)}")

@app.route('/stock', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        try:
            data = request.json
            ticker = data.get('ticker')
            start = data.get('start')
            end = data.get('end')
            model_type = data.get('model_type')
            
            if not all([ticker, start, end]):
                return jsonify({
                    "error": "Missing Field",
                    "required": {
                        "ticker": bool(ticker),
                        "start": bool(start),
                        "end": bool(end)
                    }
                }), 400
        
            result = get_stock_data(ticker, start=start, end=end, model_type=model_type)
            return jsonify({
                "success": True,
                "message": f"Data retrieved successfully for {ticker}",
                "historical_data": result['historical_data'],
                "stock_info": result['stock_info'],
                "predictions": result['predictions']
            }), 200
        
        except Exception as e:
            print(f"Error on request: {e}")
            return jsonify({
                "success": False,
                "error": str(e)
            }), 400
    
    return jsonify({
        "success": True,
        "message": "Use POST method with ticker, start, and end dates",
        "available_models": list(MODEL_REGISTRY.keys())
    }), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)

    
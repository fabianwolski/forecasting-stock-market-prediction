from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd

app = Flask(__name__)
CORS(app)

def get_stock_data(ticker, start , end):
    try:  
        stock_symbol = yf.Ticker(ticker)
        df = stock_symbol.history( 
            start=start,
            end=end
            )
        
        if df.empty:
            raise ValueError(f"No data for ticker {ticker}")
        
        #Convert datetime index to string for JSON 
        df.index = df.index.strftime('%Y-%m-%d')
        #dictionary conversion for JSON
        stock_data = df.reset_index().to_dict('records')

    # TODO: Future ML integration
    #try:
        # Load model
        # model = load_model('path_to_model')
        
        #Make prediction
        # predictions = model.predict(df)
        
        # Add predictions to response request
        
        print(f"received {ticker} data")
        return stock_data
        
    except Exception as err:
        print(f"error on retrieval {ticker}: {err}")
        raise Exception(f"Failed to get data for {ticker}: {str(err)}")


@app.route('/', methods = ['GET'])
def home():
    return jsonify({
        "success" : True,
        "message" : "Stock API is running. Use /stock for data request"
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
            
            if not all([ticker,start,end]):
                return jsonify({
                    "error" : "Missing Field",
                    "required": {
                        "ticker": bool(ticker),
                        "start": bool(start),
                        "end": bool(end)
                    }
                }), 400
        
            stock_data = get_stock_data(ticker, start=start,end=end)
            return jsonify({
                "success": True,
                "message": f"data retrieved success for {ticker}",
                "data": stock_data
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
        "message": "Use POST method with ticker, start, and end dates"
    }), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)

    
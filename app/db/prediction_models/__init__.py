from .predict_regression import RegressionPredictor

MODEL_REGISTRY = {
    "regression": RegressionPredictor,
    # "lstm": LSTMPredictor,  #Future
    # "prophet": ProphetPredictor,  #Future 
    # "arima": ARIMAPredictor,  #Future 
}

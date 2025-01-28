from .predict_regression import RegressionPredictor
from .predict_lstm import LSTMPredictor
MODEL_REGISTRY = {
    "regression": RegressionPredictor,
    "lstm": LSTMPredictor
    # "prophet": ProphetPredictor,  #Future 
    # "arima": ARIMAPredictor,  #Future 
}

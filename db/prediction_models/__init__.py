from .predict_regression import RegressionPredictor
from .predict_lstm import LSTMPredictor
from .predict_prophet import ProphetPredictor
from .predict_arima import ARIMAPredictor
MODEL_REGISTRY = {
    "regression": RegressionPredictor,
    "lstm": LSTMPredictor,
    "prophet": ProphetPredictor, 
    "arima": ARIMAPredictor 
}

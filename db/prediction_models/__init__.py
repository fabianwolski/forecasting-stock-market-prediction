from .predict_regression import RegressionPredictor
from .predict_prophet import ProphetPredictor
from .predict_arima import ARIMAPredictor
from .predict_lstm import LSTMPredictor
from .predict_xgboost import XGBoostPredictor
MODEL_REGISTRY = {
    "regression": RegressionPredictor,
    "prophet": ProphetPredictor, 
    "arima": ARIMAPredictor,
    "lstm": LSTMPredictor,
    "xgboost": XGBoostPredictor 
}

from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple

class BasePredictor(ABC):
    @abstractmethod
    def prep_data(self, df: pd.DataFrame) -> Tuple:
        pass
    
    @abstractmethod
    def train(self, X_train, y_train) -> Any:
        pass
    
    @abstractmethod
    def predict(self, X) -> np.ndarray:
        pass
    
    @abstractmethod
    def evaluate(self, y_true, y_pred) -> Dict[str, float]:
        pass
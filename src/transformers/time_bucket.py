from typing import Optional, Iterable
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class TimeBucketTransformer(BaseEstimator, TransformerMixin):
    def __init__(self,use_cols: Optional[Iterable[str]] = None):
        self.use_cols = use_cols

    def fit(self, X, y=None):
        X_=self._to_dataframe(X)

        if self.use_cols is None:
            self.feature_names_in_ = X_.columns.tolist()
        else:
            self.feature_names_in_ = list(self.use_cols)
        
        return self
    
    def transform(self, X):
        X_ = self._to_dataframe(X).copy()

        X_["hour"] = pd.to_datetime(X_[self.feature_names_in_[0]]).dt.hour

        return X_
    
    def _to_dataframe(self, X):
        if isinstance(X, pd.DataFrame):
            return X
        return pd.DataFrame(X)
    
    def get_feature_names_out(self, input_features=None):
        return np.array(self.feature_names_in_ + ["hour"])


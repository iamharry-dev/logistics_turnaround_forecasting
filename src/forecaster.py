import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb
import joblib

class TurnaroundForecaster:
    def __init__(self):
        self.model = xgb.XGBRegressor(
            n_estimators=150,
            max_depth=6,
            learning_rate=0.1,
            random_state=42
        )
        self.label_encoders = {}
        self.feature_columns = None
        
    def encode_features(self, df, fit=True):
        df = df.copy()
        categorical_cols = ['route', 'traffic_level', 'weather']
        
        for col in categorical_cols:
            if fit:
                self.label_encoders[col] = LabelEncoder()
                df[col] = self.label_encoders[col].fit_transform(df[col])
            else:
                df[col] = self.label_encoders[col].transform(df[col])
        
        return df
    
    def prepare_features(self, df, fit=True):
        df = self.encode_features(df, fit)
        
        exclude_cols = ['turnaround_minutes', 'vehicle_id']
        self.feature_columns = [col for col in df.columns if col not in exclude_cols]
        
        return df[self.feature_columns]
    
    def train(self, df):
        X = self.prepare_features(df, fit=True)
        y = df['turnaround_minutes']
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_test)
        
        metrics = {
            'mae': mean_absolute_error(y_test, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'r2': r2_score(y_test, y_pred),
            'mape': np.mean(np.abs((y_test - y_pred) / y_test)) * 100
        }
        
        return metrics
    
    def predict(self, df):
        X = self.prepare_features(df, fit=False)
        predictions = self.model.predict(X)
        return predictions
    
    def save_model(self, path='turnaround_model.joblib'):
        joblib.dump({
            'model': self.model,
            'encoders': self.label_encoders,
            'features': self.feature_columns
        }, path)
    
    def load_model(self, path='turnaround_model.joblib'):
        data = joblib.load(path)
        self.model = data['model']
        self.label_encoders = data['encoders']
        self.feature_columns = data['features']

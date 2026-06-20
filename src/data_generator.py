import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_logistics_data(n_records=5000):
    np.random.seed(42)
    
    routes = [
        ('Chennai', 'Bangalore'), ('Chennai', 'Hyderabad'), ('Chennai', 'Mumbai'),
        ('Bangalore', 'Pune'), ('Hyderabad', 'Delhi'), ('Mumbai', 'Kolkata'),
        ('Delhi', 'Chennai'), ('Kolkata', 'Bangalore'), ('Pune', 'Hyderabad'),
        ('Mumbai', 'Bangalore'), ('Delhi', 'Mumbai'), ('Chennai', 'Kolkata')
    ]
    
    data = {
        'vehicle_id': [f'VH-{np.random.randint(100, 999)}' for _ in range(n_records)],
        'route': [f'{r[0]}-{r[1]}' for r in np.random.choice(routes, n_records)],
        'distance_km': np.random.randint(200, 1500, n_records),
        'load_weight_tons': np.random.uniform(5, 25, n_records),
        'arrival_hour': np.random.randint(0, 24, n_records),
        'day_of_week': np.random.randint(0, 7, n_records),
        'is_weekend': np.random.binomial(1, 0.28, n_records),
        'driver_experience_years': np.random.randint(1, 20, n_records),
        'vehicle_age_years': np.random.randint(1, 15, n_records),
        'traffic_level': np.random.choice(['Low', 'Medium', 'High'], n_records),
        'weather': np.random.choice(['Clear', 'Rain', 'Fog', 'Storm'], n_records, p=[0.5, 0.25, 0.15, 0.1])
    }
    
    df = pd.DataFrame(data)
    
    base_time = 90
    df['turnaround_minutes'] = (
        base_time
        + df['distance_km'] * 0.05
        + df['load_weight_tons'] * 2.5
        + df['vehicle_age_years'] * 3
        - df['driver_experience_years'] * 1.5
        + df['arrival_hour'].apply(lambda x: 15 if 8 <= x <= 10 else 0)
        + df['is_weekend'] * 20
        + df['traffic_level'].map({'Low': -10, 'Medium': 0, 'High': 25})
        + df['weather'].map({'Clear': 0, 'Rain': 15, 'Fog': 20, 'Storm': 40})
        + np.random.normal(0, 15, n_records)
    ).clip(45, 300).astype(int)
    
    return df

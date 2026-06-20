import streamlit as st
import pandas as pd
import plotly.express as px
from src.data_generator import generate_logistics_data
from src.forecaster import TurnaroundForecaster
from src.utils import generate_daily_report

st.set_page_config(page_title="Logistics Turnaround Forecasting", layout="wide")

st.title("🚛 Logistics Turnaround Forecasting")
st.markdown("*Predict vehicle turnaround time — optimize your fleet*")

@st.cache_data
def load_data():
    return generate_logistics_data(3000)

@st.cache_resource
def train_model():
    df = load_data()
    forecaster = TurnaroundForecaster()
    metrics = forecaster.train(df)
    return forecaster, metrics

df = load_data()
forecaster, metrics = train_model()

col1, col2, col3, col4 = st.columns(4)
col1.metric("MAE", f"{metrics['mae']:.1f} min")
col2.metric("RMSE", f"{metrics['rmse']:.1f} min")
col3.metric("R² Score", f"{metrics['r2']:.3f}")
col4.metric("MAPE", f"{metrics['mape']:.1f}%")

st.divider()

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📊 Turnaround by Route")
    route_avg = df.groupby('route')['turnaround_minutes'].mean().sort_values(ascending=True)
    fig = px.bar(x=route_avg.values, y=route_avg.index, orientation='h',
                 labels={'x': 'Avg Turnaround (min)', 'y': 'Route'},
                 color=route_avg.values, color_continuous_scale='RdYlGn_r')
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("🕐 Turnaround by Hour")
    hourly = df.groupby('arrival_hour')['turnaround_minutes'].mean()
    fig = px.line(x=hourly.index, y=hourly.values,
                  labels={'x': 'Arrival Hour', 'y': 'Avg Turnaround (min)'})
    st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("🔮 Live Predictions")
predictions = forecaster.predict(df.head(100))
df_display = df.head(100).copy()
df_display['predicted_turnaround'] = predictions.astype(int)
df_display['status'] = df_display['predicted_turnaround'].apply(
    lambda x: '✅ On-Time' if x <= 120 else '⚠️ Delayed' if x <= 180 else '🚨 Critical'
)

st.dataframe(
    df_display[['vehicle_id', 'route', 'arrival_hour', 'distance_km', 'predicted_turnaround', 'status']]
    .style.background_gradient(subset=['predicted_turnaround'], cmap='RdYlGn_r')
)

report = generate_daily_report(df_display)
st.code(report, language=None)

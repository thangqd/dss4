
import streamlit as st
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt

# Load your data from the CSV file into a DataFrame
@st.cache_data # Cache data to improve performance
def load_data():
    data = pd.read_csv('../data/dss4.csv')
    return data

# Function to create SARIMAX forecast and plot the chart
def create_sarimax_forecast(data, selected_column, forecast_steps):
    # Convert the date column to datetime if it's not already in datetime format
    data['Date'] = pd.to_datetime(data['Date'])
    # Set 'Date' column as index (assuming it contains the dates)
    # data.set_index('Date', inplace=True)

    # Create SARIMAX model
    model = SARIMAX(data[selected_column], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    fitted_model = model.fit()

    # Forecast using the fitted model
    forecast = fitted_model.get_forecast(steps=forecast_steps)

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(data[selected_column], label='Original Data')
    plt.plot(forecast.predicted_mean, label='Forecast', color='red')
    plt.fill_between(forecast.predicted_mean.index, forecast.conf_int().iloc[:, 0], forecast.conf_int().iloc[:, 1], color='pink', alpha=0.3)
    plt.legend()
    plt.title(f'SARIMAX Forecast for {selected_column}')
    plt.xlabel('Date')
    plt.ylabel('Value')
    return plt

# Main Streamlit app code
def main():
    st.title('SARIMAX Forecast with Streamlit')

    # Load data
    data = load_data()

    # Sidebar selection
    st.sidebar.title('Select Options')
    selected_column = st.sidebar.selectbox('Choose a Column for Forecasting:', data.columns)
    forecast_steps = st.sidebar.slider('Number of Forecast Steps:', 1, 50, 10)

    # Display forecast chart
    st.pyplot(create_sarimax_forecast(data, selected_column, forecast_steps))

if __name__ == '__main__':
    main()
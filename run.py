import streamlit as st
from datetime import date
import yfinance as yf
#from fbprophet import Prophet
#from fbprophet.plot import plot_plotly
from plotly import graph_objs as go
import pandas as pd
import numpy as np


START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title("Historical Stock price visualization and forecasting")

stocks = ["TCS.NS","LT.NS", "LTI.NS", "LTI.BO", "HDFCBANK.NS","HDFC.NS", "INFY.NS","TECHM.NS","WIPRO.NS", "RELIANCE.NS", "HINDUNILVR.NS", "ITC.NS", "MARUTI.NS", "MCDOWELL-N.NS", "AMBUJACEM.NS", "SIEMENS.NS", "TATAMOTORS.NS", "TATASTEEL.NS", "TATAPOWER.NS", "HCLTECH.NS", "SBIN.NS", "ONGC.NS"]

selected_stock = st.selectbox("Select Company for prediction", stocks)


@st.cache
#load stock data. 
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    #returns pandas df
    data.reset_index(inplace = True)
    #puts date in first column
    return data

data_load_state = st.text("Loading data...")
data = load_data(selected_stock)

data_load_state.text("Loading data done!") #See streamlit tut


#Plot data



def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y = data['Open'], name = 'stock_open'))
    fig.add_trace(go.Scatter(x=data['Date'], y = data['Close'], name = 'stock_close'))
    fig.layout.update(title_text = "Time Series Data", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_raw_data()

#st.subheader("Forecast time series data using Facebook Prophet")
#n_years = st.slider("Years of Prediction:", 1, 4)
#period = n_years*365

#Forecasting

#data_load_state = st.text("Forecasting data...Please wait")

#df_train = data[['Date', 'Close']]
#df_train = df_train.rename(columns = {"Date":"ds", "Close":"y"})




#m = Prophet()
#m.fit(df_train)

#future = m.make_future_dataframe(periods = period)
#forecast = m.predict(future)

#st.write('Forecast data')
#fig1 = plot_plotly(m, forecast)
#st.plotly_chart(fig1)

#st.write('forecast components')
#fig2 = m.plot_components(forecast)
#st.write(fig2)

#data_load_state.text("Forecasting data done!")










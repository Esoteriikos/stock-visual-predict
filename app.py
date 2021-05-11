from datetime import date, timedelta
import yfinance as yf
from plotly import graph_objs as go
import plotly
import pandas as pd
import numpy as np
import json
from flask import Flask, render_template, request, send_from_directory, Response
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing

app = Flask(__name__)


START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")


stocks = ["TCS.NS","LT.NS", "LTI.NS", "LTI.BO", "HDFCBANK.NS","HDFC.NS", "INFY.NS","TECHM.NS","WIPRO.NS", "RELIANCE.NS", "HINDUNILVR.NS", "ITC.NS", "MARUTI.NS", "MCDOWELL-N.NS", "AMBUJACEM.NS", "SIEMENS.NS", "TATAMOTORS.NS", "TATASTEEL.NS", "TATAPOWER.NS", "HCLTECH.NS", "SBIN.NS", "ONGC.NS"]

#load stock data. 
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    #returns pandas df
    data.reset_index(inplace = True)
    #puts date in first column
    return data


@app.route('/')
def home():
    return render_template('home.html', stocks=stocks)

@app.route('/process', methods =["GET", "POST"])
def process():
    #stock_name = "haha"
    #if request.method == "POST":
    stock_name = request.args.get('stock_name')
    data = load_data(str(stock_name))
    
    current_data = pd.DataFrame()
    current_data["Close"] = list(data['Close'])
    current_data.index = pd.to_datetime(data['Date'])

    ####### Graphs #######
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y = data['Open'], name = 'stock_open'))
    fig.add_trace(go.Scatter(x=data['Date'], y = data['Close'], name = 'stock_close'))
    fig.layout.update(title_text = "Time Series Data", xaxis_rangeslider_visible=True)
    fig_1 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    fig = go.Figure(data=go.Ohlc(x=data['Date'],
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close']))
    fig.layout.update(title_text = "Open-High-Low-Close chart ", xaxis_rangeslider_visible=True)
    fig_2 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


    ####### FUTURE PREDICTION #######
    forecast_time = len(data)//2
    x_last_date = data[-1:]['Date']
    X_prediction_df = data[-forecast_time:].drop(['Date'], 1)

    data['prediction'] = data['Close'].shift(-forecast_time)
    data.dropna(inplace=True)

    X = np.array(data.drop(['prediction', 'Date'], 1))
    Y = np.array(data['prediction'])
    X = preprocessing.scale(X)
    X_prediction = preprocessing.scale(X_prediction_df)

    clf = LinearRegression()
    clf.fit(X, Y)
    prediction = (clf.predict(X_prediction))

    end_date = x_last_date
    while 1:
        end_date = end_date + timedelta(days=(1))
        date_range = pd.Series(pd.date_range(x_last_date.astype(str).iloc[0], end_date.astype(str).iloc[0], freq='B'))
        if len(pd.Series(pd.date_range(x_last_date.astype(str).iloc[0], end_date.astype(str).iloc[0], freq='B')))==forecast_time:
            break
    X_prediction_df.index = date_range
    X_prediction_df['prediction'] = prediction

    X_prediction_df['prediction'][0] = current_data['Close'][-1]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=X_prediction_df.index, y = X_prediction_df['prediction'], name = 'future'))
    fig.add_trace(go.Scatter(x=current_data.index, y = current_data['Close'], name = 'past'))
    fig.layout.update(title_text = "Time Series Data", xaxis_rangeslider_visible=True)
    #fig.show()
    fig_3 = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('process.html',
                            graphJSON_1=fig_1,
                            graphJSON_2=fig_2,
                            graphJSON_3=fig_3)
 
    
    
if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True, threaded=True, use_reloader=False)

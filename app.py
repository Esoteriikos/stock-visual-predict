from datetime import date
import yfinance as yf
from plotly import graph_objs as go
import plotly
import pandas as pd
import numpy as np
import json
from flask import Flask, render_template, request, send_from_directory, Response

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
    print(data)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y = data['Open'], name = 'stock_open'))
    fig.add_trace(go.Scatter(x=data['Date'], y = data['Close'], name = 'stock_close'))
    fig.layout.update(title_text = "Time Series Data", xaxis_rangeslider_visible=True)
    #fig.show()
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('process.html',
                       graphJSON=graphJSON)

if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True, threaded=True, use_reloader=False)

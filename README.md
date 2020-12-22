# Live-Candlestick-plotting-of-Stocks-Live-Price

Here, it is an application which fetches live data of stock's price and then with help of it, live plotting of candlestick chart is done. There are various indicators for stock's buying ans selling signal, and they are made through data processing and statistical techniques. This application takes help of alphavantage api, which is a free api for stock market data.

api_test.py : python program to check if your api works properly or not.

candle_live_final.py : Main file, where everything on application runs with the help of various functions, live plotting of candlesticks with live data, data processing in pandas, and differnt stock analysis indicators.

candles.py : Static candlestick plotting, for data fetched with alphavantage api.

dash_chart.py, dash_chart.py, live_plot_simple_data.py   : Live plotting of scatter graph, to test live update of graph.

live_plot.py : Live plot of line graph, data update from basic.txt file.

static_candlestick.py : static candlestick plot.

stock_indicators.py : Stock candlestick chart analysis indicators for buying and selling signals, functions with data processing.

JCP.csv, JNJ.csv, jpm.csv, tesla.csv : Csv files of different companies' stock price data. 

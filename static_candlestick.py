import plotly.graph_objs as go

import pandas as pd
from datetime import datetime

df = pd.read_csv('JNJ.csv')

fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])

fig.show()


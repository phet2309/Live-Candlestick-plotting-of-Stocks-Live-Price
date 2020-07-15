import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
import pandas as pd
import chart_studio.plotly as py
import datetime
from alpha_vantage.timeseries import TimeSeries
from plotly.offline import *



# TS data acessor
ts = TimeSeries(key='YOUR API KEY',output_format='pandas')
stock_code = 'NSE:TITAN'

def read_stock(stock_code, interval = '5min'):

    df, _ = ts.get_intraday(symbol= stock_code,interval=interval,outputsize='full')
    # trim the df 

    df.rename(index= pd.to_datetime,columns = lambda x : x.split(' ')[-1],inplace = True) 
    #print(df)
    return df


df_5min = read_stock(stock_code)
#print(df_5min)
df_1min = read_stock(stock_code, interval= '1min')
df_1min.dropna(inplace=True)
#print(df_1min)
cur_dt = datetime.datetime.now()
#print(cur_dt)
dt_str = cur_dt.strftime('%Y-%m-%d')
#print(df_5min)
#_________________________________________________________________________________________________________________________________

updatemenus = list([
    dict(type="buttons",
         active=99,
         x = 0.05,
         y = 0.99,
         bgcolor = '#000000',
         bordercolor = '#FFFFFF',
         font = dict( color='#FFFFFF', size=11 ),
         direction = 'left',
         xanchor = 'left',
         yanchor = 'top',
         buttons=list([
            dict(label = 'Close',
                 method = 'update',
                 args = [{'visible': [False, True, False, False]},
                         {'title': 'Minute Trading Data for Square, Inc.'}]),
            dict(label = 'Candlestick',
                 method = 'update',
                 args = [{'visible': [True, False, False, False]},
                         {'title': stock_code + ' Candlestick'}])
            
        ]),
    )
])


app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(id='live-plotting', animate=True),
        dcc.Interval(
            id='update-plot',
            interval=60*1000
        ),
    ]
)

@app.callback(output = Output('live-plotting', 'figure'),inputs = [Input('update-plot', 'n_intervals')])


def update_plot_scatter(n):
    df_1min = read_stock(stock_code, interval= '1min')

    data= go.Candlestick(x=df_1min.index,
                       open=df_1min.open,
                       high=df_1min.high,
                       low=df_1min.low,
                       close=df_1min.close,
                       name = 'Candlestick')

    data1 = go.Scatter(x=list(df_1min.index),
                            y=list(df_1min.close),
                            name='Close',
                            line=dict(color='#87CEFA'))

    

    return {'data':[data,data1],'layout' : go.Layout(    xaxis=dict(range=[min((df_1min.index).tolist()),max((df_1min.index).tolist())]),
                                                    yaxis=dict(range=[min((df_1min.low).tolist()),max((df_1min.high).tolist())]),
                                                    title='Minute Trading Data for Square, Inc.',
                                                    autosize = False,
                                                    width=1500,
                                                    height=1000,
                                                    plot_bgcolor = '#000000',
                                                    showlegend=False,
                                                    updatemenus=updatemenus
                                                )}






if __name__ == '__main__':
    app.run_server(debug=True)


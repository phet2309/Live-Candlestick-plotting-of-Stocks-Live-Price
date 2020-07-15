import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import time

api_key='YOUR API KEY'

ts=TimeSeries(key=api_key,output_format='pandas')
data=ts.get_intraday(symbol='MSFT',interval='1min',outputsize='full')
print(data)



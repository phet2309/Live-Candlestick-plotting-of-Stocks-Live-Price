# import pandas_datareader as datareader
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
from matplotlib.widgets import Cursor
import urllib.request, urllib.error, urllib.parse
import time
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import matplotlib
import pylab
import matplotlib.pyplot as plt
import pandas_datareader.data as web
from alpha_vantage.timeseries import TimeSeries
import time

print('*** Program Started ***')


def moving_average(x, n, type='simple'):
	
	x = np.asarray(x)
	if type == 'simple':
		weights = np.ones(n)
	else:
		weights = np.exp(np.linspace(-1., 0., n))

	weights /= weights.sum()

	a = np.convolve(x, weights, mode='full')[:len(x)]
	a[:n] = a[n]
	return a


def moving_average_convergence(x, nslow=26, nfast=12):          
	"""
	compute the MACD (Moving Average Convergence/Divergence) using a fast and slow exponential moving avg'
	return value is emaslow, emafast, macd which are len(x) arrays
	"""
	emaslow = moving_average(x, nslow, type='exponential')
	emafast = moving_average(x, nfast, type='exponential')
	return emaslow, emafast, emafast - emaslow

def MACD(str): 
    df=pd.read_csv('{}.csv'.format(str))
    prices = pd.Series(df['Close'])
    nslow = 26
    nfast = 12
    nema = 9
    emaslow, emafast, macd = moving_average_convergence(prices, nslow=nslow, nfast=nfast)
    ema9 = moving_average(macd, nema, type='exponential')
    
    wins = 80


    plt.figure(1)

    ### prices
    
    plt.subplot2grid((8, 1), (0, 0), rowspan = 4)
    plt.plot(prices[-wins:], 'k', lw = 1)
    plt.title('Sinple Graph For Candlestick')

    ## MACD

    plt.subplot2grid((8, 1), (6, 0))

    plt.plot(ema9[-wins:], 'red', lw=1)
    plt.plot(macd[-wins:], 'blue', lw=1)


    plt.subplot2grid((8, 1), (7, 0))

    plt.plot(macd[-wins:]-ema9[-wins:], 'k', lw = 2)
    plt.axhline(y=0, color='b', linestyle='-')
    plt.legend()
    plt.show()


#Getting stock data
def get_data(str):
    start=datetime.datetime(2015,1,1)
    end=datetime.datetime(2019,8,22)
    df=web.DataReader(str,'yahoo',start,end)
    #api_key='Y9AHX32YU1JIRCEJ'

    #ts=TimeSeries(key=api_key,output_format='csv')
    #df=ts.get_intraday(symbol=str,interval='1min',outputsize='full')
        
    df=pd.read_csv("{}.csv".format(str))
    df.to_csv("{}.csv".format(str))
    df=pd.read_csv("{}.csv".format(str))
    #print(df.tail())
    return df

#Bollinger Bands
def BollingerBands(data):
    symbol=str
    data = pd.read_csv('{}.csv'.format(symbol), index_col='Date',
                 parse_dates=True, usecols=['Date', 'Close'],
                 na_values='nan')
    # rename the column header with symbol name
    data = data.rename(columns={'Close': symbol})
    data.dropna(inplace=True)
    # calculate Simple Moving Average with 20 days window
    sma = data.rolling(window=20).mean()

    # calculate the standar deviation
    rstd = data.rolling(window=20).std()

    upper_band = sma + 2 * rstd
    upper_band = upper_band.rename(columns={symbol: 'upper'})
    lower_band = sma - 2 * rstd
    lower_band = lower_band.rename(columns={symbol: 'lower'})

    f1, ax1 = plt.subplots(figsize = (10,5))
    data = data.join(upper_band).join(lower_band)
    ax1 = data.plot(title='{} Price and BollingerBands'.format(symbol))
    ax1.fill_between(df.index, lower_band['lower'], upper_band['upper'],color='#ADCCFF', alpha='0.4')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('SMA and BB')
    ax1.grid(True)
    
    cursor = Cursor(ax1, useblit=True, color='#C0C0C0', linewidth=0.8)
    #plt.legend()
    plt.show()
    
    

#pivot points
def PPSR(data):  
    PP = ((data.iloc[1168]['High'] + data.iloc[1168]['Low'] + data.iloc[1168]['Close']) / 3)  
    R1 = (2 * PP - data.iloc[1168]['Low'])  
    S1 = (2 * PP - data.iloc[1168]['High'])  
    R2 = (PP + data.iloc[1168]['High'] - data.iloc[1168]['Low'])  
    S2 = (PP - data.iloc[1168]['High'] + data.iloc[1168]['Low'])  
    R3 = (data.iloc[1168]['High'] + 2 * (PP - data.iloc[1168]['Low']))  
    S3 = (data.iloc[1168]['Low'] - 2 * (data.iloc[1168]['High'] - PP))  
    #psr = {'PP':PP, 'R1':R1, 'S1':S1, 'R2':R2, 'S2':S2, 'R3':R3, 'S3':S3}  
    #PSR = pd.DataFrame(psr)  
    #data= data.join(PSR)
    arr=[PP,R1,S1,R2,S2,R3,S3]
    return arr

##Commodity Channel Index
def Fun_CCI(data, ndays):
    TP = (data['High'] + data['Low'] + data['Close']) / 3
    CCI = pd.Series((TP - TP.rolling(ndays).mean()) / (0.015 * TP.rolling(ndays).std()),
    name = 'CCI') 
    data = data.join(CCI)
    return data

#switch statement
def get_index_number():
        print('1) Pivot Points')
        print('2) Bollinger Bands')
        print('3) CCI')
        print('4) MACD')
        a=input('Which indicator you want to use : ')
        if a == '1':

            df=get_data(str)
            tdf=get_data(str)
            # Converting date to pandas datetime format
            df['Date'] = pd.to_datetime(df['Date'])
            #print(df.tail())
            df["Date"] = df["Date"].apply(mdates.date2num)

            # Creating required data in new DataFrame OHLC
            ohlc= df[['Date', 'Open', 'High', 'Low','Close']].copy()
            #print(ohlc.tail())
            # In case you want to check for shorter timespan

            ohlc =ohlc.tail(100)

            f1, ax = plt.subplots(figsize = (10,5))

            # plot the candlesticks
            candlestick_ohlc(ax, ohlc.values, width=.6, colorup='green', colordown='red')
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax.grid(True)

            tarr=PPSR(tdf)
            #print(tarr)
            ax.axhline(float(tarr[0]), color='brown', linestyle='--',label='PP')
            ax.axhline(float(tarr[1]), color='blue', linestyle='--',label='Resistance 1')
            ax.axhline(float(tarr[2]), color='black', linestyle='--',label='Support 1')
            ax.axhline(float(tarr[3]), color='blue', linestyle='--',label='Resistance 2')
            ax.axhline(float(tarr[4]), color='black', linestyle='--',label='Support 2')
            ax.axhline(float(tarr[5]), color='blue', linestyle='--',label='Resistance 3')
            ax.axhline(float(tarr[6]), color='black', linestyle='--',label='Support 3')
            cursor = Cursor(ax, useblit=True, color='#C0C0C0', linewidth=0.8)
            plt.legend()
            plt.show()

            c=input('Do you want to continue ? (Y/N)')
            if(c=='Y'or c=='y'):
                get_index_number()
            
        
        elif a == '2':
            df=get_data(str)
            tdf=get_data(str)
            BollingerBands(tdf)
            c=input('Do you want to continue ? (Y/N)')
            if(c=='Y' or c=='y'):
                get_index_number()
        elif a == '3':
            df=get_data(str)
            tdf=get_data(str)
            n=int(input('Enter Window : '))
            STOCK_CCI = Fun_CCI(tdf, n) 
            CCI = STOCK_CCI['CCI']
            x=df['Date'].tolist()
            #ax1 = plt.subplots(figsize = (10,5))
            f2,ax2=plt.subplots()
            ax2.fill_between(x,CCI,100,where=(100<CCI),alpha=1.0)
            ax2.fill_between(x,CCI,100,where=(CCI<-100),alpha=0.3)
            #ax2.grid(True)
            plt.plot(x,CCI,lw=0.75,linestyle='-',label='CCI')
            #ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            cursor = Cursor(ax2, useblit=True, color='#C0C0C0', linewidth=0.8)
            plt.legend()
            plt.show()
            c=input('Do you want to continue ? (Y/N)')
            if(c=='Y' or c=='y'):
                get_index_number()
        elif a == '4':
            MACD(str)
            c=input('Do you want to continue ? (Y/N)')
            if(c=='Y' or c=='y'):
                get_index_number()
        else:
        
            print('Wrong Input')
            print('Try Again')
            c=input('Do you want to continue ? (Y/N)')
            if(c=='Y'or c=='y'):
                get_index_number()








    

str=input('Enter the name of script : ')
df=get_data(str)
tdf=get_data(str)

#get_index_number(a)
#df = pd.read_csv("{}.csv".format(str))
#tdf = pd.read_csv("{}.csv".format(str))
#print(tdf.iloc[1168]['High'])
# ensuring only equity series is considered
#df = df.loc[df['Series'] == 'EQ']
# Converting date to pandas datetime format
df['Date'] = pd.to_datetime(df['Date'])
#print(df.tail())
df["Date"] = df["Date"].apply(mdates.date2num)
# Creating required data in new DataFrame OHLC
ohlc= df[['Date', 'Open', 'High', 'Low','Close']].copy()
#print(ohlc.tail())
# In case you want to check for shorter timespan
ohlc =ohlc.tail(100)
f1, ax = plt.subplots(figsize = (10,5))
# plot the candlesticks
candlestick_ohlc(ax, ohlc.values, width=.6, colorup='green', colordown='red')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
# Saving image
#plt.savefig('OHLC HDFC.png')
'''
n = 20
NIFTY_CCI = CCI(tdf, n)
CCI = NIFTY_CCI['CCI']
x=df['Date'].tolist()
#ax1 = plt.subplots(figsize = (10,5))
f2,ax2=plt.subplots()
ax2.fill_between(x,CCI,100,where=(100<CCI),alpha=1.0)
ax2.fill_between(x,CCI,100,where=(CCI<-100),alpha=0.3)
plt.plot(x,CCI,lw=0.75,linestyle='-',label='CCI')
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
'''
'''
tarr=PPSR(tdf)
#print(tarr)
ax.axhline(float(tarr[0]), color='brown', linestyle='--',label='PP')
ax.axhline(float(tarr[1]), color='blue', linestyle='--',label='Resistance 1')
ax.axhline(float(tarr[2]), color='pink', linestyle='--',label='Support 1')
ax.axhline(float(tarr[3]), color='blue', linestyle='--',label='Resistance 2')
ax.axhline(float(tarr[4]), color='pink', linestyle='--',label='Support 2')
ax.axhline(float(tarr[5]), color='blue', linestyle='--',label='Resistance 3')
ax.axhline(float(tarr[6]), color='pink', linestyle='--',label='Support 3')
#plt.show()
# In case you dont want to save image but just displya it
'''


cursor = Cursor(ax, useblit=True, color='black', linewidth=0.8)
#plt.legend()
plt.show()

get_index_number()
print('*** Program ended ***')


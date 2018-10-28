import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import quandl
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like # allows for pandas_datareader to be imported
import pandas_datareader.data as web # access data from web

style.use('ggplot')
quandl.ApiConfig.api_key = "z5tYZu1pYFBfskkoNK29"

#part 1

start = dt.datetime(2013,1,1)
end = dt.datetime(2017,12,31)
df = web.DataReader('TSLA', 'quandl', start, end)

#order each row by date from earliest to latest
df = df.sort_values(by='Date', ascending=True)
df.to_csv('tsla.csv')

df = pd.read_csv('tsla.csv', parse_dates=True, index_col=0)

#part 2
#print(df[['Open', 'High']].head())

#df['Open'].plot()
#plt.show()

#part 3
'''
df['100ma'] = df['AdjClose'].rolling(window=100, min_periods = 0).mean()
# (6,1) represents grid size
# starting point (0,0)

ax1 = plt.subplot2grid((6,1), (0,0), rowspan = 5, colspan = 1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan = 1, colspan = 1, sharex=ax1)

ax1.plot(df.index, df['AdjClose'])
ax1.plot(df.index, df['100ma'])
ax2.plot(df.index, df['Volume'])
plt.show()
'''
#part 4

df_ohlc = df['AdjClose'].resample('10D').ohlc()
df_volume = df['Volume'].resample('10D').sum()

df_ohlc.reset_index(inplace=True)

df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)
print(df_ohlc.head())

ax1 = plt.subplot2grid((6,1), (0,0), rowspan = 5, colspan = 1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan = 1, colspan = 1, sharex=ax1)
ax1.xaxis_date()

candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0 )
plt.show()






import bs4 as bs
import datetime as dt
import os
import quandl
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like # allows for pandas_datareader to be imported
import pandas_datareader.data as web
import pickle
import requests
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np

style.use('ggplot')


quandl.ApiConfig.api_key = "z5tYZu1pYFBfskkoNK29"

def save_sp500_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find('table', {'class':'wikitable sortable'})
    tickers = []
    #for every tr in the table excluding the first row
    for row in table.findAll('tr')[1:50]:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)
    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)
    
    print(tickers)
    return tickers


def get_data_from_quandl(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)
    
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    start = dt.datetime(2013,1,1)
    end = dt.datetime(2017,12,31)

    for ticker in tickers[:50]:
        print(ticker)
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            df = web.DataReader(ticker, 'quandl', start, end)
            df = df.sort_values(by='Date', ascending=True)
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('already have {}'.format(ticker))

def compile_data():
    with open("sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f)
    
    main_df = pd.DataFrame()

    for count, ticker in enumerate(tickers):
        if count == 50:
            break
        
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
        df.set_index('Date', inplace=True)
        df.rename(columns = {'AdjClose':ticker}, inplace=True)
        df.drop(['Open', 'High', 'Low', 'Close', 'Volume', 'ExDividend', 'SplitRatio', 'AdjOpen', 'AdjHigh', 'AdjLow', 'AdjVolume'], 1, inplace=True)

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')
        
        if count % 10 == 0:
            print(count)

        print(main_df.head())
        main_df.to_csv('sp500_joined_closes.csv')

def visualize_data():
    df = pd.read_csv('sp500_joined_closes.csv')
    #df['AAL'].plot()
    #plt.show()
    df_corr = df.corr()
    #create heatmap
    data1 = df_corr.values

    df_corr.to_csv('sp500corr.csv')
    #build figure and axis
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    #red = negative corr, yellow = no correlation, green = positive corr
    heatmap1 = ax1.pcolor(data1, cmap=plt.cm.plasma)
    #add legend for colors
    fig1.colorbar(heatmap1)
    #set up x and y axis tick markers
    ax1.set_xticks(np.arange(data1.shape[1]) + 0.5, minor=False)
    ax1.set_yticks(np.arange(data1.shape[0]) + 0.5, minor=False)
    #flip yaxis, so that graph is easier to read
    #flip xaxis to be at the top of the graph rather than the bottom
    ax1.invert_yaxis()
    ax1.xaxis.tick_top()
    #add company names
    column_labels = df_corr.columns
    row_labels = df_corr.index
    ax1.set_xticklabels(column_labels)
    ax1.set_yticklabels(row_labels)
    #rotate x ticks (tickers) 
    plt.xticks(rotation=90)
    #range will be from -1 to 1
    heatmap1.set_clim(-1,1)

    plt.tight_layout()
    plt.savefig("correlations.png", dpi=(300))
    plt.show()

    
#visualize_data()
save_sp500_tickers()
#compile_data()
   

        




    





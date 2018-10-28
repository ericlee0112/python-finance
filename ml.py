import numpy as np
import pandas as pd
import pickle 
from collections import Counter
#features are the pricing changes that day for all companies
#label will be whether or not we actually want to buy a specific company

def process_data_for_labels(ticker):
    hm_days = 7
    df = pd.read_csv('sp500_joined_closes.csv', index_col=0)
    tickers = df.columns.values.tolist()
    #fill any missing cells with 0
    df.fillna(0, inplace=True)

    #1 to 8
    for i in range(1, hm_days+1):
        #gives us future values i days in advance, which we can calculate percent change against
        df['{}_{}d'.format(ticker,i)] = (df[ticker].shift(-i) - df[ticker]) / df[ticker]
    
    df.fillna(0, inplace=True)
    return tickers, df

def buy_sell_hold(*args):
    cols = [c for c in args]
    req = 0.02
    for col in cols:
        if col > req:
            return 1
        if col < -req:
            return -1

    return 0

def extract_featuresets(ticker):
    tickers, df = process_data_for_labels(ticker)
    df['{}_target'.format(ticker)] = list(map( buy_sell_hold, 
                                                df['{}_1d'.format(ticker,i)],
                                                df['{}_2d'.format(ticker,i)],
                                                df['{}_3d'.format(ticker,i)],
                                                df['{}_4d'.format(ticker,i)],
                                                df['{}_5d'.format(ticker,i)],
                                                df['{}_6d'.format(ticker,i)],
                                                df['{}_7d'.format(ticker,i)]
                                                 ))
    vals = df['{}_target'.format(ticker)].values.tolist()
    str_vals = [str(i) for i in vals]
    print('Data spread: ', Counter(str_vals))

    df.fillna(0, inplace=True)
    df = df.replace([np.inf, -np.inf], np.nan)
    df.dropna(inplace=True)

    df_vals = 

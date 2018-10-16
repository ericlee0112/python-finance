import numpy as np
import pandas as pd
import pickle 

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

tickers, df = process_data_for_labels('AAL')
df.to_csv('AAL.csv')

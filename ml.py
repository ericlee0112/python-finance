import numpy as np
import pandas as pd
import pickle 
from collections import Counter
from sklearn import svm, model_selection, neighbors
from sklearn.ensemble import VotingClassifier, RandomForestClassifier
#features are the pricing changes that day for all companies
#label will be whether or not we actually want to buy a specific company

def process_data_for_labels(ticker):
    hm_days = 7
    df = pd.read_csv('sp500_joined_closes.csv', index_col=0, skipinitialspace=True)
    tickers = df.columns.values.tolist()
    #fill any missing cells with 0
    df.fillna(0, inplace=True)

    #1 to 8
    for i in range(1, hm_days + 1):
        #gives us future values i days in advance, which we can calculate percent change against
        df['{}_{}d'.format(ticker,i)] = (df[ticker].shift(-i) - df[ticker]) / df[ticker]
    df.fillna(0, inplace=True)
    return tickers, df

def buy_sell_hold(*args):
    cols = [c for c in args]
    req = 0.02
    for col in cols:
        if col >= req:
            return 1
        if col < -req:
            return -1

    return 0

def extract_featuresets(ticker):
    tickers, df = process_data_for_labels(ticker)
    df['{}_target'.format(ticker)] = list(map( buy_sell_hold, 
                                            df['{}_1d'.format(ticker)], 
                                            df['{}_2d'.format(ticker)], 
                                            df['{}_3d'.format(ticker)], 
                                            df['{}_4d'.format(ticker)], 
                                            df['{}_5d'.format(ticker)], 
                                            df['{}_6d'.format(ticker)], 
                                            df['{}_7d'.format(ticker)]))
    vals = df['{}_target'.format(ticker)].values.tolist()
    str_vals = [str(i) for i in vals]
    print('Data spread: ', Counter(str_vals))

    df.fillna(0, inplace=True)
    df = df.replace([np.inf, -np.inf], np.nan)
    df.dropna(inplace=True)

    df_vals = df[[t for t in tickers]].pct_change()
    df_vals = df_vals.replace([np.inf, -np.inf], 0)
    df_vals.fillna(0, inplace=True)

    X = df_vals.values
    y = df['{}_target'.format(ticker)].values

    return X, y, df

def do_ml(ticker):
    X, y, df = extract_featuresets(ticker)
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size = 0.25)

    #clf = neighbors.KNeighborsClassifier()
    clf = VotingClassifier([('lsvc', svm.LinearSVC()), 
                            ('knn', neighbors.KNeighborsClassifier()),
                            ('rfor', RandomForestClassifier())
                            ])

    clf.fit(X_train, y_train)
    confidence = clf.score(X_test, y_test)
    print('Accuracy', confidence)
    predictions = clf.predict(X_test)
    print('Predicted data:', Counter(predictions))

    return confidence

do_ml('APA')

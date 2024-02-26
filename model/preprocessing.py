import pandas as pd
import numpy as np
from constant.fieldnames import upbit_btc_fields
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def load_data(path='../data/UPBIT_HISTORY.csv'):
    df = pd.read_csv(path)
    df.columns = upbit_btc_fields
    return df


def split_and_scale(df, target='trade_price'):
    """
    :param df:
    :param target:
    :return: X_train: dataframe, X_test: dataframe, y_train: dataframe, t_test: dataframe
    """
    X = df.drop(columns=[target])
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, y_train, y_test


def drop_field(df):
    df.drop(['type', 'code', 'highest_52_week_date', 'lowest_52_week_date',
             'market_state', 'is_trading_suspended', 'delisting_date', 'market_warning',
             'timestamp', 'stream_type', 'trade_date'], inplace=True, axis=1)


def dig_encode(df):
    df['change'] = df['change'].apply(lambda x: 1 if x == 'FALL' else 2 if x == 'RISE' else 0)
    df['ask_bid'] = df['ask_bid'].apply(lambda x: 1 if x == 'ASK' else 0)


def test():
    df = load_data()
    drop_field(df)
    dig_encode(df)
    X_train, X_test, y_train, y_test = split_and_scale(df)

    print(df.head())

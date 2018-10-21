import pandas as pd
import talib as ta


class DataProcessing:

    def __init__(self, data):
        self._file = data

    def Preprocessing(self, df):
        df['dt'] = df['Date'].astype(str) + " " + df['Time'].astype(str)
        df['DateTime'] = pd.to_datetime(df['dt'], format=' % Y % m % d % H: % M: % S', errors='ignore')
        df = df.set_index(['DateTime'])
        df = df.drop(['General', 'Date', 'Time', 'dt'], axis=1)

        df['EMA10'] = ta.EMA(df['Close'], timeperiod=10)
        df['EMA30'] = ta.EMA(df['Close'], timeperiod=30)
        df['EMA60'] = ta.EMA(df['Close'], timeperiod=60)

        df['SMA10'] = ta.SMA(df['Close'], timeperiod=10)
        df['SMA30'] = ta.SMA(df['Close'], timeperiod=30)
        df['SMA60'] = ta.SMA(df['Close'], timeperiod=60)

        df['WMA10'] = ta.WMA(df['Close'], timeperiod=10)
        df['WMA30'] = ta.WMA(df['Close'], timeperiod=30)
        df['WMA60'] = ta.WMA(df['Close'], timeperiod=60)

        df['RSI10'] = ta.RSI(df['Close'], timeperiod=10)
        df['RSI30'] = ta.RSI(df['Close'], timeperiod=30)
        df['RSI60'] = ta.RSI(df['Close'], timeperiod=60)

        df['MOM10'] = ta.MOM(df['Close'], timeperiod=10)
        df['MOM30'] = ta.MOM(df['Close'], timeperiod=30)
        df['MOM60'] = ta.MOM(df['Close'], timeperiod=60)

        df['ROC10'] = ta.ROC(df['Close'], timeperiod=10)
        df['ROC50'] = ta.ROC(df['Close'], timeperiod=30)
        df['ROC60'] = ta.ROC(df['Close'], timeperiod=60)

        df.to_csv('data/TrainDataWithInds.csv')
        return df

import pandas as pd
import talib as ta


class DataProcessing_Daily:

    def __init__(self, data):
        self._file = data

    def Preprocessing_Daily(self, df):
        df = df.drop(['General', 'Time'], axis=1)

        openGrouped = df['Open'].groupby(df['Date']).first()
        highGrouped = df['High '].groupby(df['Date']).max()
        lowGrouped = df['Low'].groupby(df['Date']).min()
        closeGrouped = df['Close'].groupby(df['Date']).last()
        volumeGrouped = df['Volume '].groupby(df['Date']).sum()

        df = pd.DataFrame(
            {'Open': openGrouped, 'High ': highGrouped, 'Low': lowGrouped, 'Close': closeGrouped,
             'Volume ': volumeGrouped})
        df['dt'] = df.index.astype(str)
        df['DateTime'] = pd.to_datetime(df['dt'], format=' % Y % m % d % H: % M: % S', errors='ignore')
        df = df.set_index(['DateTime'])
        df = df.drop(['dt'], axis=1)

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
        df.to_csv('data/TrainDataWithInds_Daily.csv')
        return df

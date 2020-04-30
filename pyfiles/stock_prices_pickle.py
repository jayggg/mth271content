import pandas_datareader.data as web

s = web.DataReader(['AAPL', 'GOOG', 'TSLA'],  data_source='yahoo', start='2020')
s.to_pickle('../../data_external/stock_prices.pkl')

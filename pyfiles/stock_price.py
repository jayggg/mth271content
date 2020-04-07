import pandas_datareader.data as web
import seaborn; seaborn.set()

tsl = web.DataReader('TSLA', data_source='yahoo', start='2020')
tsl = tsl.rename(columns={'Close': 'Daily Closing'})
tsl['Weekly Mean'] = tsl['Daily Closing'].rolling(7).mean()
tsl.loc[:, ['Daily Closing', 'Weekly Mean']].plot(title='Price of TSLA stock', style=[':','-'])



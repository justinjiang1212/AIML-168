#classes for trading bot

from enum import Enum
#import Data
#from yahoo_fin import stock_info as si
from datetime import datetime, timedelta, date
from iexfinance.stocks import Stock
from iexfinance.stocks import get_historical_intraday
import pandas as pd
import os

IEX_TOKEN='sk_434806dae94a4ee69daa8375f33da6f5'
TIMEOFFSET = timedelta(hours = 3)

'''class EquityType(Enum):
  STOCK = 1
  FUTURE = 2
  OPTION = 3
  BOND = 4'''

def daterange(start_date, end_date):
  for n in range(int ((end_date - start_date).days)):
    yield start_date + timedelta(n)


class Equity:
  def __init__(self, name=None, ticker = None):
    self.name = name                                                 #String, colloquial name of equity 
    self.ticker = ticker                                             #String, ticker name of equity
    self.dayData = pd.DataFrame(columns=['DateTime','Price'])        #Data Frame, contains trading data starting from 12:00 am EST of the current day
    self.historicalData = pd.DataFrame()                                          #dictionary of data frames of Day, with the key being a date in format MM/DD/YYYY and the value being a data frame of that day's trading data
    self.iexVar = Stock(ticker, token = IEX_TOKEN)


  def updateLiveData(self):
    length = len(self.dayData)
    self.dayData.loc[length + 1] = [datetime.now() + TIMEOFFSET] + [self.iexVar.get_price()]
  
  def getHistoricalData(self, StartDate, EndDate):
    '''StartDate and EndDate are date objects'''

    #for date in daterange(StartDate, EndDate):
    #  self.historicalData[date] = get_historical_intraday(self.ticker, date, output_format='pandas', token = IEX_TOKEN)

    for date in daterange(StartDate, EndDate):
      day_data = get_historical_intraday(self.ticker, date, output_format = 'pandas', token = IEX_TOKEN)
      self.historicalData = self.historicalData.append(day_data)


aapl = Equity(name='Apple', ticker = 'AAPL') 

start_date = date(2020, 5, 14)
end_date = date(2020, 6, 9)

aapl.getHistoricalData(start_date,end_date)
print("done collecting data, starting analysis")


from gluonts.dataset import common
from gluonts.model import deepar
from gluonts.trainer import Trainer
from gluonts.dataset.field_names import FieldName
from gluonts.dataset.common import ListDataset

import pandas as pd
from gluonts.model.simple_feedforward import SimpleFeedForwardEstimator
from gluonts.evaluation.backtest import make_evaluation_predictions
import matplotlib.pyplot as plt
import numpy as np

prices_csv = "aapl_20190401-20200605_minute.csv"


df = pd.read_csv(prices_csv, index_col =0)
#df = df.rename(columns={"marketClose":"Close"})

df_cols = ['DateTime', 'Open', 'High', 'Low', 'Close', 'Volume']

df0 = pd.read_csv('AAPL_2000_2009.txt', index_col =0, names = df_cols)
df1 = pd.read_csv('AAPL_2010_2019.txt', index_col =0, names = df_cols)
df2 = pd.read_csv('AAPL_2020_2020.txt', index_col =0, names = df_cols)
updated_data = aapl.historicalData
updated_data = updated_data.filter(['marketClose'])
updated_data = updated_data.rename(columns={"marketClose":"Close"})


frames = [df0, df1, df2, updated_data]
new_data = pd.concat(frames)


#df.drop(columns=['label', 'high', 'low', 'volume', 'notional', 'numberOfTrades', "marketHigh", "marketLow", "marketAverage", "marketNotional", "marketNumberOfTrades", "open", "close", "marketOpen", "marketClose", "changeOverTime", "marketChangeOverTime"])
#prices = df.filter(['date','average', 'marketClose'])

'''
train_ds = ListDataset([{
  "start": df.index[0], 
  "target": df.marketClose[:"2020-06-02 04:29:00"]
  }], freq="1min")

test_ds = ListDataset([{
  "start": df.index[-390], 
  "target": df.marketClose["2020-06-05 09:30:00": '2020-06-05 15:59:00' ]
  }], freq="1min")
'''


data = common.ListDataset([{
    "start": df.index[0],
    "target": df.marketClose[:"2020-06-08 15:59:00"]
}],
                          freq="1min")



lots_of_data = common.ListDataset([{
    "start": new_data.index[0],
    "target": new_data.Close[:-1]
}],
                          freq="1min")

trainer = Trainer(epochs=10, ctx="cpu", num_batches_per_epoch=50)
estimator = deepar.DeepAREstimator(
    freq="1min", prediction_length=390, trainer=trainer, num_layers = 2)
#predictor = estimator.train(training_data=data)

trial_estimator = SimpleFeedForwardEstimator(
    num_hidden_dimensions=[10],
    prediction_length=390,
    context_length=780,
    freq="1min",
    trainer=Trainer(ctx="cpu",
                    epochs=5,
                    learning_rate=1e-30,
                    hybridize = False,
                    num_batches_per_epoch=100
                   )
)
predictor = estimator.train(lots_of_data)

prediction = next(predictor.predict(data))
print(prediction.mean)
#prediction.plot(output_file='graph.png')

forecast_it, ts_it = make_evaluation_predictions(
    dataset=data,  # test dataset
    predictor=predictor,  # predictor
    num_samples=500,  # number of sample paths we want for evaluation
)

forecasts = list(forecast_it)
tss = list(ts_it)

ts_entry = tss[0]
#np.array(ts_entry[:5]).reshape(-1,)
test_ds_entry = next(iter(test_ds))
forecast_entry = forecasts[0]

print(f"Number of sample paths: {forecast_entry.num_samples}")
print(f"Dimension of samples: {forecast_entry.samples.shape}")
print(f"Start date of the forecast window: {forecast_entry.start_date}")
print(f"Frequency of the time series: {forecast_entry.freq}")

def plot_prob_forecasts(TS_entry, Forecast_entry):
    plot_length = 390
    prediction_intervals = (50.0, 90.0)
    legend = ["observations", "median prediction"] + [f"{k}% prediction interval" for k in prediction_intervals][::-1]

    fig, ax = plt.subplots(1, 1, figsize=(10, 7))
    TS_entry[-plot_length:].plot(ax=ax)  # plot the time series
    Forecast_entry.plot(prediction_intervals=prediction_intervals, color='g')
    plt.grid(which="both")
    plt.legend(legend, loc="upper left")
    plt.show()


plot_prob_forecasts(ts_entry, forecast_entry)
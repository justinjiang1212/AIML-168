#classes for trading bot

from enum import Enum
import Data
from yahoo_fin import stock_info as si

class EquityType(Enum):
  STOCK = 1
  FUTURE = 2
  OPTION = 3
  BOND = 4

class Equity:
  def __init__(self, name=None, ticker = None):
        self.name = name                  #String, colloquial name of equity 
        self.ticker = ticker              #String, ticker name of equity
        self.dayData = None               #Data Frame, contains trading data starting from 12:00 am EST of the current day
        self.historicalData = None        #dictionary of data frames of Day, with the key being a date in format MM/DD/YYYY and the value being a data frame of that day's trading data


        def download_dayData(ticker, startDate, endDate):
          data = si.get_data(ticker, start_date = startDate, end_date = endDate)




# classes for trading bot

# import Data
from datetime import datetime, timedelta, date
import pandas as pd
from iexfinance.stocks import Stock
from iexfinance.stocks import get_historical_intraday

IEX_TOKEN = 'sk_434806dae94a4ee69daa8375f33da6f5'
TIMEOFFSET = timedelta(hours=3)

'''class EquityType(Enum):
  STOCK = 1
  FUTURE = 2
  OPTION = 3
  BOND = 4'''


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


class Equity:
    def __init__(self, name=None, ticker=None):
        self.name = name  # String, colloquial name of equity
        self.ticker = ticker  # String, ticker name of equity
        self.dayData = pd.DataFrame(columns=['DateTime',
                                             'Price'])  # Data Frame, contains trading data starting from 12:00 am EST of the current day
        self.historicalData = {}  # dictionary of data frames of Day, with the key being a date in format MM/DD/YYYY and the value being a data frame of that day's trading data
        self.iexVar = Stock(ticker, token=IEX_TOKEN)

    def updateLiveData(self):
        length = len(self.dayData)
        self.dayData.loc[length + 1] = [datetime.now() + TIMEOFFSET] + [self.iexVar.get_price()]

    def getHistoricalData(self, StartDate, EndDate):
        """StartDate and EndDate are date objects"""

        for date in daterange(StartDate, EndDate):
            self.historicalData[date] = get_historical_intraday(self.ticker, date, output_format='pandas',
                                                                token=IEX_TOKEN)


aapl = Equity(name='Apple', ticker='AAPL')

start_date = date(2020, 5, 22)
end_date = date(2020, 6, 2)

aapl.getHistoricalData(start_date, end_date)
print(aapl)

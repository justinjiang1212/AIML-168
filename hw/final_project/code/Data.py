#get data from stock market

from datetime import datetime, timedelta
from iexfinance.stocks import Stock
import time as Time
import matplotlib
import matplotlib.pyplot as plt


a = Stock("AAPL", token="sk_434806dae94a4ee69daa8375f33da6f5")

time_offset = timedelta(hours = 3)
nyc_time = datetime.now() + time_offset

intraday_prices = []
time = []

while (nyc_time.hour < 16) and (nyc_time.minute < 30):
  intraday_prices.append(a.get_price())
  
  time.append(str(nyc_time.hour) + str(":") + str(nyc_time.minute))

  Time.sleep(600)
  nyc_time = datetime.now() + time_offset



fig, ax = plt.subplots()
ax.plot(time, intraday_prices, color="green")

ax.set(xlabel='Time', ylabel='Price',
       title='Apple Intraday Prices')
ax.grid()

plt.show()

#get data from stock market

from datetime import datetime, timedelta
from iexfinance.stocks import Stock
import time as Time
import matplotlib
import matplotlib.pyplot as plt


a = Stock("AAPL", token="sk_434806dae94a4ee69daa8375f33da6f5") #token is the secret API key for our account

time_offset = timedelta(hours = 3)
nyc_time = datetime.now() + time_offset

intraday_prices = []
time = []
#counter = 0

#while counter < 5:
while (nyc_time.hour > 9) and (nyc_time.minute > 30):
  intraday_prices.append(a.get_price())
  
  time.append(str(nyc_time.hour) + str(":") + str(nyc_time.minute))

  Time.sleep(60)
  nyc_time = datetime.now() + time_offset

  if (nyc_time.hour > 14) and (nyc_time.minute > 30) and (nyc_time.second > 0):
    break
  #counter +=1



fig, ax = plt.subplots()
ax.plot(time, intraday_prices, color="green")

ax.set(xlabel='Time', ylabel='Price',
       title='Apple Intraday Prices')
ax.grid()

plt.show()

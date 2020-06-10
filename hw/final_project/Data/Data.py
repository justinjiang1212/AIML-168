# get data from stock market

import time as Time
from datetime import datetime, timedelta

import matplotlib
import matplotlib.pyplot as plt
from iexfinance.iexdata import get_last
from iexfinance.stocks import Stock

a = Stock("AAPL", token="sk_434806dae94a4ee69daa8375f33da6f5")  # token is the secret API key for our account
IEX_TOKEN = 'sk_434806dae94a4ee69daa8375f33da6f5'

time_offset = timedelta(hours=3)
nyc_time = datetime.now() + time_offset

intraday_prices = []
time = []
counter = 0

while counter < 180:
    # while (nyc_time.hour > 9) and (nyc_time.minute > 30):
    # intraday_prices.append(a.get_price())

    print(counter)
    df = get_last(symbols="AAPL", output_format='pandas', token=IEX_TOKEN)
    intraday_prices.append(df['price'])

    time.append(str(nyc_time.minute) + str(":") + str(nyc_time.second))
    # time.append(nyc_time)

    Time.sleep(1)
    nyc_time = datetime.now() + time_offset

    if (nyc_time.hour > 14) and (nyc_time.minute > 30) and (nyc_time.second > 0):
        break
    counter += 1

fig, ax = plt.subplots()
ax.plot(time, intraday_prices, color="green")

ax.set(xlabel='Time', ylabel='Price',
       title='Apple Intraday Prices')

# formatter = matplotlib.dates.DateFormatter('%H:%M:%S')
# ax.xaxis.set_major_formatter(formatter)
ax.grid()

plt.show()

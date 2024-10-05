'''
This program queries coingecko for ethereum prices in USD
It only runs for one coin, ethereum
The urls require a specific date, and are generated using the datetime timedelta library, to handle things like leap year(s)
The data is written to a csv
'''


import requests
import json
import time
from datetime import datetime, timedelta
import os
import sys
import code

# os.system(sys.executable + " -m pip install requests") you can install pip packages this way

code.interact(local=locals())



# example url for coingecko.com
example_url = "https://api.coingecko.com/api/v3/coins/ethereum/history?date=23-09-2024&localization=false"

key1='market_data'
key2='current_price'
key3='usd'

result = requests.get(example_url).json()

print(result)

usd_price = result[key1][key2][key3]

print('usd price for one ethereum bitcoin: ' + str(usd_price))


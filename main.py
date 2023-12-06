import requests
import time
import json
from datetime import date

API_KEY = "PKMRS0PD5QOPSB14455X"
API_SECRET = "RooSe7SdHmP3vQB1cshk2LxHZ5vY2lbjDu7v5cWD"
BASIC_URL = "https://paper-api.alpaca.markets/v2"
symbol = "AAPL"
last_trade_url = f"https://data.alpaca.markets/v2/stocks/{symbol}/trades/latest"

headers = {
  'APCA-API-KEY-ID': "PK42I07MH09F0ORJLLC1",
  'APCA-API-SECRET-KEY': "3UQQh5eNtNRdlcUgespElmCD3JqW2iDOd6AiruZd"
}

def PlaceBuyAAPL(actual_price):
  order_data = {
      "symbol": "AAPL",
      "qty": 1,
      "side": "buy",
      "type": "market",
      "time_in_force": "day",
  }

  ORDER_URL = "https://paper-api.alpaca.markets/v2/orders"

  r = requests.post(ORDER_URL, json=order_data, headers=headers)
  
  print(f"{order_data['qty']} {order_data['symbol']} stock(s) bought at {actual_price} each!")

  return actual_price

def PlaceSellAPPL(actual_price):
  order_data = {
      "symbol": "AAPL",
      "qty": 1,
      "side": "sell",
      "type": "market",
      "time_in_force": "day",
  }

  ORDER_URL = "https://paper-api.alpaca.markets/v2/orders"

  r = requests.post(ORDER_URL, json=order_data, headers=headers)

  print(order_data['qty'], order_data['symbol'], "stocks sold at", actual_price, "each!")

  return actual_price

def FindPrice():
  current = requests.get(last_trade_url, headers=headers)
  current_json = current.json()
  current_price = current_json['trade']
  actual_price = current_price['p']

  return actual_price

def CalculateAv(url, headers):
  #Calculates the average price of a time interval according to the amount of data (probably wrong)

  response = requests.get(url, headers=headers)

  data = json.loads(response.text)

  arr = []
  for day in data["quotes"]:
    arr.append(day["ap"])
  
  sum = 0
  count = 0

  for number in arr:
    if number != 0:
      count += 1
      sum += number

  return sum/count


def Strategy():
  Bullish = False
  Bearish = False

  while True:
    endDate1 = date.today()
    endDate2 = date.today()

    #For endDate1 (20 days off)
    if endDate1.day >= 20:
      endDate1.day -= 20
    else: 
      if endDate1.month > 1:
        endDate1 = endDate1.replace(month=(endDate1.month - 1))
        endDate1 = endDate1.replace(day=(endDate1.day + 10))
      else:
        endDate1 = endDate1.replace(year=(endDate1.year - 1))
        endDate1 = endDate1.replace(month=(endDate1.month + 11))
        endDate1 = endDate1.replace(day=(endDate1.day + 10))

    print(endDate1)

    #For endDate2 (50 days off)
    if endDate2.month > 2 or (endDate2.month == 2 and endDate2.day > 20):
      endDate2 = endDate2.replace(month=(endDate2.month - 1))
      if endDate2.day > 20:
        endDate2 = endDate2.replace(day=(endDate2 - 20))
      else:
        endDate2 = endDate2.replace(month=(endDate2.month - 1))
        endDate2 = endDate2.replace(day=(endDate2.day + 10))
    else:
      endDate2 = endDate2.replace(year=(endDate2.year - 1)) #JUNTAR TODO!!!
      endDate2 = endDate2.replace(month=(endDate2.month + 10))
      if endDate2.day <= 20:
        endDate2 = endDate2.replace(day=(endDate2 + 10))
      else:
        print("If this prints, dates are wrong :P")


    print(endDate2)

    url1 = "https://data.alpaca.markets/v2/stocks/AAPL/quotes?start=2023-11-25&end=2023-12-04&limit=10000&feed=iex&sort=asc"
    url2 = "https://data.alpaca.markets/v2/stocks/AAPL/quotes?start=2023-10-01&end=2023-12-04&limit=10000&feed=iex&sort=asc"

    headers1 = {
      "accept": "application/json",
      "APCA-API-KEY-ID": "PK42I07MH09F0ORJLLC1",
      "APCA-API-SECRET-KEY": "3UQQh5eNtNRdlcUgespElmCD3JqW2iDOd6AiruZd"
    }

    Average1 = CalculateAv(url1, headers1)
    Average2 = CalculateAv(url2, headers1)

    print(Average1)    #Calculate the average price of the first URL
    print(Average2)    #Calculate the average price of the second URL

    if round(Average1, 1) == round(Average2, 1):      # If the lines cross,
      if Bullish:                                     # find out if it crosses under or above 
        PlaceBuyAAPL()  #Long                         # and respond accordingly (buying or selling)
      elif Bearish:
        PlaceSellAPPL()  #Short

    if Average1 > Average2:     #If the average of less time is above the one with more time,
      Bullish = True            # it means that the price is higher than what is was before
      Bearish = False           # and thus we're in an uptrend / bullish trend. And viceversa.
      print("Bullish")
    else:
      Bearish = True
      Bullish = False
      print("Bearish")
    


    time.sleep(60)

Strategy()
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

def AveragePrices(positive, days):
  response = requests.get(url, headers=headers)

  data = json.loads(response.text)


def Strategy():
  Bullish = False
  Bearish = False

  while True:
    print("")
    endDate1 = date.today()
    endDate2 = date.today()

    #For endDate1 (2 days off)
    if endDate1.day > 2:
      endDate1 = endDate1.replace(day = (endDate1.day - 2))
    else: 
      if endDate1.month > 1:
        if endDate1.month == 2:
          endDate1 = endDate1.replace(month = (endDate1.month - 1), day = (endDate1.day + 26))
        else:
          endDate1 = endDate1.replace(month = (endDate1.month - 1), day = (endDate1.day + 28))
      else: 
        endDate1 = endDate1.replace(year=(endDate1.year - 1), month=(endDate1.month + 11), day=(endDate1.day + 29))

    #print(endDate1)

    #For endDate2 (6 days off)
    if endDate2.day > 6:
      endDate2 = endDate2.replace(day = (endDate2.day - 6))
    else: 
      if endDate2.month > 1:
        if endDate2.month == 2:
          endDate2 = endDate2.replace(month = (endDate2.month - 1), day = (endDate2.day + 22))
        else:
          endDate2 = endDate2.replace(month = (endDate2.month - 1), day = (endDate2.day + 24))
      else: 
        endDate2 = endDate2.replace(year=(endDate2.year - 1), month=(endDate2.month + 11), day=(endDate2.day + 25))

    #print(endDate2)

    url1 = "https://data.alpaca.markets/v2/stocks/AAPL/quotes?start=" + str(endDate1) + "&end="+ str(date.today()) + "&limit=10000&feed=iex&sort=asc"
    url2 = "https://data.alpaca.markets/v2/stocks/AAPL/quotes?start=" + str(endDate2) + "&end=" + str(date.today()) + "&limit=10000&feed=iex&sort=asc"

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
      #print("Bullish")
    else:
      Bearish = True
      Bullish = False
      #print("Bearish")


      #Calculate RSI

      #Averages = for each dataPoint in data[highest price - lowest price] (in 14 intervals)
      #Positive Averages >> If dataPoint > 0: positiveSum += dataPoint
      #Negative Averages >> else: negativeSum -= dataPoint

      #RS = positiveSum / negativeSum 
      #RSI = 100- (100/(1 + RS))
      #If Average Wins = 14: RSI = 100 (exception)

      
    
    time.sleep(60)

AveragePrices(True, 14, url)
Strategy()
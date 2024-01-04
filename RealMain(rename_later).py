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
  for day in data["bars"]:
    arr.append(day["c"])
  
  sum = 0
  count = 0

  for number in arr:
    if number != 0:
      count += 1
      sum += number

  return sum/count

def RSCal(url):
  response = requests.get(url, headers=headers)

  data = json.loads(response.text)

  arr = []

  for DP in data["bars"]:
    arr.append(DP["c"])

  WinsSum = 0
  Wins = 0
  LossSum = 0
  Losses = 0
  LastPrice = arr[0]

  for DP in arr:
    if (DP - LastPrice) > 0:
      #Positive
      Wins += 1
      WinsSum += (DP - LastPrice)
    elif (DP - LastPrice) < 0:
      #Negative
      Losses += 1
      LossSum -= (DP - LastPrice)

    LastPrice = DP

  if WinsSum == 0:
    return 0
  if LossSum == 0:
    return 100000

  AvWin = WinsSum/Wins
  AvLoss = LossSum/Losses
  
  return (AvWin/AvLoss)
    

def ExponentialAv(url, T):
  response = requests.get(url, headers=headers)

  data = json.loads(response.text)

  arr = []
  lastExp = 0

  for DP in data["bars"]:
    c = DP["c"]
    Exp = (c * (2 / (1 + T)) + lastExp * (1- (2 / (1 + T))))
    arr.append(Exp)
    lastExp = Exp
  
  sum = 0

  for price in arr:
    sum += price

  return (sum / len(arr))


def Strategy():
  BullishS = False
  BearishS = False

  BullishE = False
  BearishE = False

  while True:

    # MEDIAS MÓVILES SIMPLES (SMA)

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


    url1 = "https://data.alpaca.markets/v2/stocks/AAPL/bars?timeframe=15Min&start=" + str(endDate1) + "&end=" + str(date.today()) + "&limit=10000&adjustment=raw&feed=iex&sort=asc"
    url2 = "https://data.alpaca.markets/v2/stocks/AAPL/bars?timeframe=15Min&start=" + str(endDate2) + "&end=" + str(date.today()) + "&limit=10000&adjustment=raw&feed=iex&sort=asc"

    headers1 = {
      "accept": "application/json",
      "APCA-API-KEY-ID": "PK42I07MH09F0ORJLLC1",
      "APCA-API-SECRET-KEY": "3UQQh5eNtNRdlcUgespElmCD3JqW2iDOd6AiruZd"
    }

    Average1 = CalculateAv(url1, headers1)    #Calculate the average price of the first URL
    Average2 = CalculateAv(url2, headers1)    #Calculate the average price of the second URL

    print("SMA1:", Average1)    
    print("SMA2:", Average2)    

    if round(Average1, 1) == round(Average2, 1):      # If the lines cross,
      if BullishS:                                     # find out if it crosses under or above 
        PlaceBuyAAPL()  #Long                         # and respond accordingly (buying or selling)
      elif BearishS:
        PlaceSellAPPL()  #Short

    if Average1 > Average2:     #If the average of less time is above the one with more time,
      BullishS = True            # it means that the price is higher than what is was before
      BearishS = False           # and thus we're in an uptrend / bullish trend. And viceversa.
      #print("Bullish")
    else:
      BearishS = True
      BullishS = False
      #print("Bearish")


    # ÍNDICE DE FUERZA RELATIVO (RSI)

    endDate3 = date.today()

    #Calculate endDate3 (14 days off)
    if endDate3.day > 14:          
      endDate3 = endDate3.replace(day = (endDate3.day - 14))
    else: 
      if endDate3.month > 1:
        if endDate3.month == 2:
          endDate3 = endDate3.replace(month = (endDate3.month - 1), day = (endDate3.day + 14))
        else:
          endDate3 = endDate3.replace(month = (endDate3.month - 1), day = (endDate3.day + 16))
      else: 
        endDate3 = endDate3.replace(year=(endDate3.year - 1), month=(endDate3.month + 11), day=(endDate3.day + 17))

    url3 = "https://data.alpaca.markets/v2/stocks/AAPL/bars?timeframe=15Min&start=" + str(endDate3) + "&end=" + str(date.today()) + "&limit=10000&adjustment=raw&feed=iex&sort=asc"

    RS = RSCal(url3)

    RSI = (100 -(100/(1+RS)))
    print("RSI: ", RSI)

    if RSI > 70:
      PlaceSellAPPL()
    elif RSI < 30:
      PlaceBuyAAPL()

    # MEDIA MÓVIL EXPONENCIAL (EMA)

    endDate4 = date.today()
    endDate5 = date.today()

    # endDate4 (5 days off)

    if endDate4.day > 5:          
      endDate4 = endDate4.replace(day = (endDate4.day - 5))
    else: 
      if endDate4.month > 1:
        if endDate4.month == 2:
          endDate4 = endDate4.replace(month = (endDate4.month - 1), day = (endDate4.day + 23))
        else:
          endDate4 = endDate4.replace(month = (endDate4.month - 1), day = (endDate4.day + 25))
      else: 
        endDate4 = endDate4.replace(year=(endDate4.year - 1), month=(endDate4.month + 11), day=(endDate4.day + 26))

    # endDate5 (15 days off)

    if endDate5.day > 15:          
      endDate5 = endDate5.replace(day = (endDate5.day - 15))
    else: 
      if endDate5.month > 1:
        if endDate5.month == 2:
          endDate5 = endDate5.replace(month = (endDate5.month - 1), day = (endDate5.day + 13))
        else:
          endDate5 = endDate5.replace(month = (endDate5.month - 1), day = (endDate5.day + 15))
      else: 
        endDate5 = endDate5.replace(year=(endDate5.year - 1), month=(endDate5.month + 11), day=(endDate5.day + 16))

    url4 = "https://data.alpaca.markets/v2/stocks/AAPL/bars?timeframe=15Min&start=" + str(endDate4) + "&end=" + str(date.today()) + "&limit=10000&adjustment=raw&feed=iex&sort=asc"
    url5 = "https://data.alpaca.markets/v2/stocks/AAPL/bars?timeframe=15Min&start=" + str(endDate5) + "&end=" + str(date.today()) + "&limit=10000&adjustment=raw&feed=iex&sort=asc"

    EMA1 = ExponentialAv(url4, 5)
    EMA2 = ExponentialAv(url5, 15) 

    print("EMA1:", EMA1)
    print("EMA2:", EMA2)


    if round(EMA1, 1) == round(EMA2, 1):
      if BullishE:
        print("Would buy! (EMA)")
      if BearishE:
        print("Would sell! (EMA)")

    if Average1 > Average2:    
      BullishE = True           
      BearishE = False           
    else:
      BearishE = True
      BullishE = False
    
    time.sleep(60)

Strategy()
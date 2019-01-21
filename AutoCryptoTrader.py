
import time
import datetime
import pprint


api_key = "6iUWY4TXdLWw94AOi3Jdm4WRQFl6Eif2jUOK1suDSQxMc0QVNBUL70hrjZ1a3K03"

api_secret = "yPWub1YdqI174nN1WF6TjT9HWvMWH9hRqz9Ds9BpambcCR9MjNgXvd375E9krXiN"

#ATTENTION:  Always start with a buy first time through

coin = 'ETHBTC'                     #Choose the coin you want to auto trade
ping_rate = 1                       #Checks Price every given  amount of seconds                                    
wiggle = 0.0015                    #Percent Profit on each trade

from binance.enums import *
from binance.client import Client
client = Client(api_key, api_secret)




def find_price(coin):
    try:
        prices = client.get_all_tickers()

        for cryptoPrice in prices: 
   
            if cryptoPrice['symbol'] == coin:
                return float(cryptoPrice['price'])

            else:
                continue
    except Exception as e: 
        print("from: find_price() " + str(e))
        pass


def max_amount():
    try:
        balance = client.get_asset_balance(asset='BTC')
        your_balance = balance['free']
        return (float(your_balance)/float(find_price(coin)))  #ether
    except Exception as e: 
        print("from: max_amount() " + str(e))
        pass

def coins_held():
    try:
        balance = client.get_asset_balance(asset= coin[:-3])
        your_balance = balance['free']
        return float(your_balance)  #ether
    except Exception as e: 
        print("from: coins_held() " + str(e))
        pass

def get_balance():
    try:
        balance = client.get_asset_balance(asset='BTC')
        return float(balance['free'])
    except Exception as e: 
        print("from: get_balance() " + str(e))
        pass


def total_coin_value():
    try:
        i = 0
        acount_total = 0.0
        info = client.get_account()
        while i < len(info['balances']):
            if info['balances'][i]['asset'] == coin[:-3]:
                acount_total = acount_total + float(info['balances'][i]['locked']) + float(info['balances'][i]['free'])
                return acount_total
            i+=1

    except Exception as e: 
        print("from: total_asset_value() " + str(e))
        pass

def total_BTC_value():
    try:
        i = 0
        acount_total = 0.0
        info = client.get_account()
        while i < len(info['balances']):
            if info['balances'][i]['asset'] == 'BTC':
                acount_total = acount_total + float(info['balances'][i]['locked']) + float(info['balances'][i]['free'])
                return acount_total
            i+=1

    except Exception as e: 
        print("from: total_asset_value() " + str(e))
        pass


def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '%.12f' % f
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])


#####  The Main Loop #####
time_counter = 0
trades = 0
buy_price = find_price(coin) - find_price(coin) * wiggle
bought = False

orders = client.get_open_orders(symbol= coin)

print(orders)



while True:

    
    
    try:  
        orders = client.get_open_orders(symbol= coin)
    

        if not(not orders):  
        
            if time_counter/300 == 1:
                print("BTC balance: " + str('{:.8f}'.format(total_BTC_value())))
                print(coin[:-3] + " balance: " + str('{:.5f}'.format(total_coin_value())))
                print("running...")
                time_counter = 0
                if orders[0]['side'] == 'BUY':
                    result = client.cancel_order(symbol=coin, orderId= orders[0]['orderId'])
                    print("Canceled Buy order for " + str(buy_price) + " BTC")
                    trades  = trades - 1
        
            else:
                time.sleep(ping_rate)
                time_counter = time_counter + 1


    
        else:
            if bought and coins_held() > 0.02:  #ether
                try:
                    max_coins = truncate(coins_held(),3) #ether

                    #sell_price = '{:.8f}'.format(float(buy_price) + float(buy_price) * wiggle)
                    sell_price = '{:.6f}'.format(float(buy_price) + float(buy_price) * wiggle)
                    order = client.order_limit_sell(symbol = coin, quantity= (float(max_coins)), price= sell_price)
                    #order = client.create_test_order(
                    #symbol=coin,
                    #side=SIDE_SELL,
                    #type=ORDER_TYPE_LIMIT,
                    #timeInForce=TIME_IN_FORCE_GTC,
                    #quantity=270,
                    #price= sell_price)
                    bought = False
                    
                    print("Selling " + str(max_coins) + " " + str(coin[:-3]) + " for " + str(sell_price) + "BTC each")
                    time.sleep(1)
                except Exception as e: 
                    print("from: order_limit_sell() " + str(e))
                    pass

            else:
                try:
                    maxCoins = max_amount()
                    #buy_price = '{:.8f}'.format(find_price(coin) - (find_price(coin) * 0.0025))    #ether
                    buy_price = '{:.6f}'.format(find_price(coin) - (find_price(coin) * wiggle))
                    order = client.order_limit_buy( symbol= coin, quantity= truncate(max_amount(),3), price= buy_price)
                   #order = client.create_test_order(
                   #symbol=coin,
                   #side=SIDE_BUY,
                   #type=ORDER_TYPE_LIMIT,
                   #timeInForce=TIME_IN_FORCE_GTC,
                   #quantity=270,
                   #price= buy_price)
                    time.sleep(5)
                    bought = True
                    print(str(trades) + " successful trades")
                    print(datetime.datetime.now().time())
                    print("Buying " + str(truncate(maxCoins,3)) + " " + str(coin[:-3]) + " for " + str(buy_price) + "BTC each")
                    trades  = trades + 1
                    time.sleep(1)
                except Exception as e: 
                    print("from: order_limit_buy() " + str(e))
                    pass
    except Exception as e: 
        print("from: Main Loop get_open_orders() " + str(e))
        pass







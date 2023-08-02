import os, time, config, requests
from webhook_launcher import telegram_bot_sendtext
from binance.client import Client
from termcolor import colored

api_key     = ''
api_secret  = ''
client      = Client(api_key, api_secret)
live_trade  = config.live_trade

#To send webhook or telegram notification
active_webhook = True

def get_timestamp():
    server_time = client.get_server_time()["serverTime"]
    time_difference = server_time - int(time.time() * 1000)
    timestamp = int(time.time() * 1000) + time_difference
    return timestamp

def position_information(pair):
    # time.sleep(1)
    return client.futures_position_information(symbol=pair, timestamp=get_timestamp())

def get_lastest_price(pair):
    # time.sleep(1)
    return client.futures_symbol_ticker(symbol=pair, timestamp=get_timestamp())    

def get_asset_balance(asset):
    # time.sleep(1)
    return client.get_asset_balance(asset=asset, timestamp=get_timestamp())        

def futures_account_balance(asset):
    # time.sleep(1)
    acc_balance = client.futures_account_balance()
    for check_balance in acc_balance:
        if check_balance["asset"] == asset:
            balance = check_balance["withdrawAvailable"]
            return balance
    # return client.futures_account_balance(asset=asset, timestamp=get_timestamp())         

def get_take_profit_order(pair):
    orders = client.futures_get_open_orders(symbol=pair)
    for order in orders:
        if order["type"] == "TAKE_PROFIT_MARKET":
            return order
    # return client.futures_account_balance(asset=asset, timestamp=get_timestamp())  

def account_trades(pair, timestamp):
    time.sleep(1)
    return client.futures_account_trades(symbol=pair, timestamp=get_timestamp(), startTime=timestamp)

def LONG_SIDE(response):
    # time.sleep(1)
    if float(response.get('positionAmt')) > 0: return "LONGING"
    elif float(response.get('positionAmt')) == 0: return "NO_POSITION"

def SHORT_SIDE(response):
    # time.sleep(1)
    if float(response.get('positionAmt')) < 0 : return "SHORTING"
    elif float(response.get('positionAmt')) == 0: return "NO_POSITION"

def change_leverage(pair, leverage):
    return client.futures_change_leverage(symbol=pair, leverage=leverage, timestamp=get_timestamp())

def change_margin_to_ISOLATED(pair):
    return client.futures_change_margin_type(symbol=pair, marginType="ISOLATED", timestamp=get_timestamp())

def Change_margin_to_CROSSED(pair):
    return client.futures_change_margin_type(symbol=pair, marginType="CROSSED", timestamp=get_timestamp())    

def set_hedge_mode():
    if not client.futures_get_position_mode(timestamp=get_timestamp()).get('dualSidePosition'):
        return client.futures_change_position_mode(dualSidePosition="true", timestamp=get_timestamp())

def set_hedge_mode_off():
    if client.futures_get_position_mode(timestamp=get_timestamp()).get('dualSidePosition'):
        return client.futures_change_position_mode(dualSidePosition="false", timestamp=get_timestamp())

def cancel_open_order(pair, order):
    time.sleep(1)
    if live_trade:
        client.futures_cancel_order(symbol=pair, 
                                    orderId= order, 
                                    timestamp=get_timestamp())
    print("CANCEL ORDER")
    if active_webhook:
        telegram_bot_sendtext(" CANCEL TAKE PROFIT ORDER "+str(pair)+ " | OrderId: "+ str(order))

def take_profit_market_long(pair, stopPrice):
    time.sleep(1)
    if live_trade:
        client.futures_create_order(symbol=pair,
                                    closePosition=True,
                                    timeInForce="GTE_GTC",
                                    side="SELL",
                                    stopPrice=stopPrice,
                                    priceProtect=True,
                                    type="TAKE_PROFIT_MARKET",
                                    workingType= "MARK_PRICE",
                                    timestamp=get_timestamp())
    print("OPEN TAKE PROFIT LONG")
    if active_webhook:
        telegram_bot_sendtext(" PLACE TAKE PROFIT LONG "+str(pair)+ " | Take Profit Price: "+ str(stopPrice))

def take_profit_market_short(pair, stopPrice):
    time.sleep(1)
    if live_trade:
        client.futures_create_order(symbol=pair,
                                    closePosition=True,
                                    timeInForce="GTE_GTC",
                                    side="BUY",
                                    stopPrice=stopPrice,
                                    priceProtect=True,
                                    type="TAKE_PROFIT_MARKET",
                                    workingType= "MARK_PRICE",
                                    timestamp=get_timestamp())
    print("OPEN TAKE PROFIT SHORT")
    if active_webhook:
        telegram_bot_sendtext(" PLACE TAKE PROFIT SHORT "+pair+" | Take Profit Price: "+ str(stopPrice))

def market_open_long(pair, quantity):
    time.sleep(1)
    if live_trade:
        client.futures_create_order(symbol=pair,
                                    quantity=quantity,
                                    # positionSide="LONG",
                                    type="MARKET",
                                    side="BUY",
                                    timestamp=get_timestamp())
    print(colored("GO_LONG", "green"))
    if active_webhook:
        telegram_bot_sendtext(" GO_LONG "+ str(pair) + " "+ str(quantity) + " BUY MARKET ")

def market_open_short(pair, quantity):
    time.sleep(1)
    if live_trade:
        client.futures_create_order(symbol=pair,
                                    quantity=quantity,
                                    # positionSide="SHORT",
                                    type="MARKET",
                                    side="SELL",
                                    timestamp=get_timestamp())
    print(colored("GO_SHORT", "red"))
    if active_webhook:
        telegram_bot_sendtext(" GO_SHORT "+ str(pair) + " "+ str(quantity) + " SELL MARKET ")


def market_close_long(pair, response):
    if live_trade:
        client.futures_create_order(symbol=pair,
                                    quantity=abs(float(response.get('positionAmt'))),
                                    # positionSide="LONG",
                                    side="SELL",
                                    type="MARKET",
                                    timestamp=get_timestamp())
    print("CLOSE_LONG")
    if active_webhook:
        telegram_bot_sendtext(" CLOSE_LONG "+str(pair)+ " | Position: "+ str(abs(float(response.get('positionAmt')))) + "| X"+ str(response.get('leverage')) + " | Market Price: "+ str(float(response.get('markPrice'))) + " Profit: "+ str(float(response.get('unRealizedProfit'))) + " SELL MARKET ")

def market_close_short(pair, response):
    if live_trade:
        client.futures_create_order(symbol=pair,
                                    quantity=abs(float(response.get('positionAmt'))),
                                    # positionSide="SHORT",
                                    side="BUY",
                                    type="MARKET",
                                    timestamp=get_timestamp())
    print("CLOSE_SHORT")
    if active_webhook:
        telegram_bot_sendtext(" CLOSE_SHORT "+pair+" | Position: "+ str(abs(float(response.get('positionAmt')))) + "| X"+ str(response.get('leverage')) + " | Market Price: "+ str(float(response.get('markPrice'))) + " Profit: "+ str(float(response.get('unRealizedProfit'))) + "   BUY MARKET ")

# set_hedge_mode_off()
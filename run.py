import api_binance
import time
import config
import random
import strategies.combined
import strategies.ichimoku
import strategies.volume
import strategies.william_fractal
import os, requests, socket, urllib3
from webhook_launcher import telegram_bot_sendtext
from datetime import datetime
from termcolor import colored
import pytz

from binance.exceptions import BinanceAPIException
print(colored("------ LIVE TRADE IS ENABLED ------\n", "green")) if config.live_trade else print(colored("THIS IS BACKTESTING\n", "red")) 

tz = pytz.timezone('Asia/Ho_Chi_Minh')
now = datetime.now()
current_time = now.strftime("%H:%M:%S")

choose_your_fighter = strategies.combined
#fees 
taker_fees    = 0.2

def lets_make_some_money(pair, leverage, quantity):
    print("--------------")
    print(pair)

    # Retrieve Infomation for Initial Trade Setup
    response = api_binance.position_information(pair)
    if response[0].get('marginType') != "isolated": api_binance.change_margin_to_ISOLATED(pair)
    if int(response[0].get("leverage")) != leverage: api_binance.change_leverage(pair, leverage)

    hero = choose_your_fighter.futures_hero(pair)
    # print(hero)

    if api_binance.LONG_SIDE(response) == "NO_POSITION":
        if hero["GO_LONG"].iloc[-1]:
            api_binance.market_open_long(pair, quantity)
        else: print("_LONG_SIDE : WAIT ")

    if api_binance.LONG_SIDE(response) == "LONGING":
        liquidationpricemarklong = round((float(response[1].get('markPrice')) - float(response[1].get('liquidationPrice'))) / float(response[1].get('markPrice')) * 100, 2)
        addlong = round((float(response[1].get('entryPrice')) - float(response[1].get('markPrice'))) / float(response[1].get('entryPrice')) * 100, 2)
        takeprofitlong = (float(response[1].get('unRealizedProfit')))
        new_quantity_long = round(float(response[1].get('positionAmt')) * config.new_quantity_long_multiplier, 2)
        new_quantity_long_become = round(float(response[1].get('positionAmt')) * config.new_quantity_long_multiplier, 2) + round(float(response[1].get('positionAmt')), 2)
        new_price_long = round((float(response[1].get('entryPrice'))) - (config.add_long_measure * (float(response[1].get('entryPrice'))) / 100), 2)
        if current_time=='10:30:00' or current_time == '2:30:00':
            telegram_bot_sendtext("new_quantity_long " + str(new_quantity_long)+" | new_quantity_long_become " + str(new_quantity_long_become)+" | new_price_long " + str(new_price_long))
            # telegram_bot_sendtext_delay("new_quantity_long " + str(new_quantity_long))
            # telegram_bot_sendtext_delay("new_quantity_long_become " + str(new_quantity_long_become))
            # telegram_bot_sendtext_delay("new_price_long " + str(new_price_long))
        print("new_quantity_long " + str(new_quantity_long))
        print("new_quantity_long_become " + str(new_quantity_long_become))
        print("new_price_long " + str(new_price_long))
        if hero["EXIT_LONG"].iloc[-1] and in_Profit(response[1]):
            api_binance.market_close_long(pair, response)
            # wait for 1-3 seconds
            time.sleep(random.randint(1, 3))
            # after take profit again open long
            api_binance.market_open_long(pair, quantity)
            print("EXIT "+str(float(response[1].get('entryPrice')))+" | Actual: "+str(float(response[1].get('markPrice')))+" | liquidationPrice: "+str(float(response[1].get('liquidationPrice')))+" | positionAmt: "+str(float(response[1].get('positionAmt')))+" | unRealizedProfit "+str(float(response[1].get('unRealizedProfit')))+"| InProfit "+str(in_Profit_show(response[1])))
        else: 
            print(colored("_LONG_SIDE : HOLDING_LONG", "green"))
            print("LiquidationPriceMarkLong "+ str(liquidationpricemarklong))
            print("addlong " + str(addlong))
            if addlong > config.add_long_measure:
                api_binance.market_open_long(pair, new_quantity_long)
                # wait for 1-3 seconds
                time.sleep(random.randint(1, 3))
            if liquidationpricemarklong < config.liquidationpricemarklong_percent:
                api_binance.market_open_long(pair, new_quantity_long)
                # wait for 1-3 seconds
                time.sleep(random.randint(1, 3))
            print("takeprofitlong " + str(takeprofitlong))
            if takeprofitlong > config.takeprofitlong_usd:
                api_binance.market_close_long(pair, response)
                # wait for 1-3 seconds
                time.sleep(random.randint(1, 3))
                # after take profit again open long
                api_binance.market_open_long(pair, quantity)

            print("Entry Price "+str(float(response[1].get('entryPrice')))+" | Actual: "+str(float(response[1].get('markPrice')))+" | liquidationPrice: "+str(float(response[1].get('liquidationPrice')))+" | positionAmt: "+str(float(response[1].get('positionAmt')))+" | unRealizedProfit "+str(float(response[1].get('unRealizedProfit')))+"| InProfit "+str(in_Profit_show(response[1])))

    if api_binance.SHORT_SIDE(response) == "NO_POSITION":
        if hero["GO_SHORT"].iloc[-1]:
            api_binance.market_open_short(pair, quantity)
        else: print("SHORT_SIDE : WAIT")

    if api_binance.SHORT_SIDE(response) == "SHORTING":
        liquidationpricemarkshort = round((float(response[2].get('liquidationPrice')) - float(response[2].get('markPrice'))) / float(response[2].get('markPrice')) * 100, 2)
        addshort = round((float(response[2].get('markPrice')) - float(response[2].get('entryPrice'))) / float(response[2].get('markPrice')) * 100, 2)
        takeprofitshort = (float(response[2].get('unRealizedProfit')))
        new_quantity_short = round(abs(float(response[2].get('positionAmt'))) * config.new_quantity_short_multiplier, 2)
        new_quantity_short_become = round(abs(float(response[2].get('positionAmt'))) * config.new_quantity_short_multiplier, 2) + round(abs(float(response[2].get('positionAmt'))), 2)
        new_price_short = round(((float(response[2].get('entryPrice'))) / (100 - config.add_short_measure)) * 100, 2)
        # if api_binance.active_webhook:
        if current_time=='10:30:00' or current_time == '2:30:00':
            telegram_bot_sendtext("new_quantity_short " + str(new_quantity_short)+" | new_quantity_short_become " + str(new_quantity_short_become)+" | new_price_short " + str(new_price_short))
            # telegram_bot_sendtext_delay("new_quantity_short " + str(new_quantity_short))
            # telegram_bot_sendtext_delay("new_quantity_short_become " + str(new_quantity_short_become))
            # telegram_bot_sendtext_delay("new_price_short " + str(new_price_short))
        print("new_quantity_short " + str(new_quantity_short))
        print("new_quantity_short_become " + str(new_quantity_short_become))
        print("new_price_short " + str(new_price_short))
        if hero["EXIT_SHORT"].iloc[-1] and in_Profit(response[2]):
            api_binance.market_close_short(pair, response)
            # wait for 1-3 seconds
            time.sleep(random.randint(1, 3))
            # after take profit open short again
            api_binance.market_open_short(pair, quantity)
            print("EXIT "+str(round(float(response[2].get('entryPrice')), 2))+" | Actual: "+str(float(response[2].get('markPrice')))+" | liquidationPrice: "+str(float(response[2].get('liquidationPrice')))+" | positionAmt: "+str(float(response[2].get('positionAmt')))+" | unRealizedProfit "+str(float(response[2].get('unRealizedProfit')))+"| InProfit "+str(in_Profit_show(response[2])))
        else: 
            print(colored("SHORT_SIDE : HOLDING_SHORT", "red"))
            print("LiquidationPriceMarkShort " + str(liquidationpricemarkshort))
            print("addshort " + str(addshort))
            if addshort > config.add_short_measure:
                api_binance.market_open_short(pair, new_quantity_short)
                # wait for 1-3 seconds
                time.sleep(random.randint(1, 3))
            if liquidationpricemarkshort < config.liquidationpricemarkshort_percent:
                api_binance.market_open_short(pair, new_quantity_short)
                # wait for 1-3 seconds
                time.sleep(random.randint(1, 3))
            print("takeprofitshort " + str(takeprofitshort))
            if takeprofitshort > config.takeprofitshort_usd:
                api_binance.market_close_short(pair, response)
                # wait for 1-3 seconds
                time.sleep(random.randint(1, 3))
                # after take profit open short again
                api_binance.market_open_short(pair, quantity)
            print("Entry Price "+str(float(response[2].get('entryPrice')))+" | Actual: "+str(float(response[2].get('markPrice')))+" | liquidationPrice: "+str(float(response[2].get('liquidationPrice')))+" | positionAmt: "+str(float(response[2].get('positionAmt')))+" | unRealizedProfit "+str(float(response[2].get('unRealizedProfit')))+"| InProfit "+str(in_Profit_show(response[2])))

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

def in_Profit(response):
    # taker_fees    = 0.2 changed to 0.3 to tried
    global taker_fees
    markPrice     = float(response.get('markPrice'))
    positionAmt   = abs(float(response.get('positionAmt')))
    unRealizedPNL = round(float(response.get('unRealizedProfit')), 2)
    breakeven_PNL = (markPrice * positionAmt * taker_fees) / 100
    return True if unRealizedPNL > breakeven_PNL else False

def in_Profit_show(response):
    # taker_fees    = 0.2 changed to 0.3 to tried
    #taker_fees    = 0.2
    global taker_fees
    markPrice     = float(response.get('markPrice'))
    positionAmt   = abs(float(response.get('positionAmt')))
    unRealizedPNL = round(float(response.get('unRealizedProfit')), 2)
    breakeven_PNL = (markPrice * positionAmt * taker_fees) / 100
    return round(breakeven_PNL,4)

try:
    while True:
        try:
            for i in range(len(config.pair)):
                pair     = config.pair[i]
                leverage = config.leverage[i]
                quantity = config.quantity[i]
                lets_make_some_money(pair, leverage, quantity)
                time.sleep(random.randint(1, 3)) # sleep to avoid penality

        except (socket.timeout,
                BinanceAPIException,
                urllib3.exceptions.ProtocolError,
                urllib3.exceptions.ReadTimeoutError,
                requests.exceptions.ConnectionError,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ReadTimeout,
                ConnectionResetError, KeyError, OSError) as e:

            if not os.path.exists("ERROR"): os.makedirs("ERROR")
            with open((os.path.join("ERROR", config.pair[i] + ".txt")), "a", encoding="utf-8") as error_message:
                error_message.write("[!] " + config.pair[i] + " - " + "Created at : " + datetime.today().strftime("%d-%m-%Y @ %H:%M:%S") + "\n" + str(e) + "\n\n")
                print(e)
                telegram_bot_sendtext(" ERROR RESPONSE API BINANCE: "+ str(e)+"")

except KeyboardInterrupt: print("\n\nAborted.\n")


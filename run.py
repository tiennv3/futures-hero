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
now = datetime.now(tz)
current_time = now.strftime("%H:%M:%S")

choose_your_fighter = strategies.combined
#fees 
taker_fees    = 0.2

def lets_make_some_money(pair, leverage, amount, token_decimal, price_decimal):
    print("--------------")
    print(pair)

    # Retrieve Infomation for Initial Trade Setup
    response = api_binance.position_information(pair)
    lastest_price = api_binance.get_lastest_price(pair)

    if response[0].get('marginType') != "isolated": api_binance.change_margin_to_ISOLATED(pair)
    if int(response[0].get("leverage")) != leverage: api_binance.change_leverage(pair, leverage)

    hero = choose_your_fighter.futures_hero(pair)
    # print(hero)

    if api_binance.LONG_SIDE(response) == "NO_POSITION":
        if hero["GO_LONG"].iloc[-1]:
            init_quantity = round((leverage * amount / float(lastest_price.get('price'))), token_decimal)
            api_binance.market_open_long(pair, init_quantity)
        else: print("_LONG_SIDE : WAIT ")

    if api_binance.LONG_SIDE(response) == "LONGING":

        unRealizedProfit_long = (float(response[1].get('unRealizedProfit')))
        colateralAmount_long = round((abs(float(response[1].get('notional'))) / leverage), price_decimal)
        marginAmount_long = round(abs(float(response[1].get('notional'))), price_decimal)

        add_amount_long = round(colateralAmount_long * config.dca_amount_percent, price_decimal)
        add_quantity_long = round((add_amount_long * leverage) / float(lastest_price.get('price')) , token_decimal)
        next_dca_price_long = round((marginAmount_long - colateralAmount_long) / float(response[1].get('positionAmt')), token_decimal)
        takeProfit_long_atPrice = round((marginAmount_long + colateralAmount_long) / float(response[1].get('positionAmt')), token_decimal)

        if str(current_time) =='9:30:00' or str(current_time) == '17:30:00':
            telegram_bot_sendtext("unRealizedProfit_long " + str(unRealizedProfit_long)
                                + " | positionQty " + response[1].get('positionAmt')
                                + " | marginAmount_long " + str(marginAmount_long)
                                + " | colateralAmount_long " + str(colateralAmount_long)
                                + " | entryPrice " + response[1].get('entryPrice')
                                + " | markPrice " + response[1].get('markPrice')
                                + " | liquidationPrice " + response[1].get('liquidationPrice')
                                + " | next_dca_price_long " + str(next_dca_price_long)
                                + " | takeProfit_long_atPrice " + str(takeProfit_long_atPrice))

        print("unRealizedProfit_long " + str(unRealizedProfit_long))          
        print("positionQty " + response[1].get('positionAmt'))
        print("marginAmount_long " + str(marginAmount_long))
        print("colateralAmount_long " + str(colateralAmount_long))
        print("entryPrice " + response[1].get('entryPrice'))
        print("markPrice " + response[1].get('markPrice'))
        print("liquidationPrice " + response[1].get('liquidationPrice'))
        print("next_dca_price_long " + str(next_dca_price_long))
        print("add_quantity_long " + str(add_quantity_long))
        print("takeProfit_long_atPrice " + str(takeProfit_long_atPrice))
        
        if unRealizedProfit_long >= (round(float(colateralAmount_long * config.takeProfit_percent), price_decimal)):
            api_binance.market_close_long(pair, response)
            # wait for 1-3 seconds
            time.sleep(random.randint(1, 3))
            # after take profit again open long
            init_quantity = round((leverage * amount / float(lastest_price.get('price'))), token_decimal)            
            api_binance.market_open_long(pair, init_quantity)

            print(colored("_LONG_SIDE : Take Profit", "green"))
            print("_LONG_SIDE : Take Profit" + str(unRealizedProfit_long))
            telegram_bot_sendtext("_LONG_SIDE : Take Profit "
                                + " | PNL " + str(unRealizedProfit_long))
        else: 
            if unRealizedProfit_long <= (round(float(colateralAmount_long * config.dca_percent), price_decimal)):

                api_binance.market_open_long(pair, add_quantity_long)
                # wait for 1-3 seconds
                time.sleep(random.randint(1, 3))
                print(colored("_LONG_SIDE : ADD LONG ", "green"))
                print("_LONG_SIDE : add_quantity_long" + str(add_quantity_long))
                telegram_bot_sendtext("_LONG_SIDE : ADD LONG "
                                    + " | add_quantity_long " + str(add_quantity_long))     
            else: print(colored("_LONG_SIDE : HOLDING_LONG", "green"))         

    if api_binance.SHORT_SIDE(response) == "NO_POSITION":
        if hero["GO_SHORT"].iloc[-1]:
            init_quantity = round((leverage * amount / float(lastest_price.get('price'))), token_decimal)
            api_binance.market_open_short(pair, init_quantity)
        else: print("SHORT_SIDE : WAIT")

    if api_binance.SHORT_SIDE(response) == "SHORTING":
        
        unRealizedProfit_short = (float(response[2].get('unRealizedProfit')))
        colateralAmount_short = round((abs(float(response[2].get('notional'))) / leverage), price_decimal)
        marginAmount_short = round(abs(float(response[2].get('notional'))), price_decimal)

        add_amount_short = round(colateralAmount_short * config.dca_amount_percent, price_decimal)
        add_quantity_short = round((add_amount_short * leverage) / float(lastest_price.get('price')) , token_decimal)
        next_dca_price_short = round((marginAmount_short + colateralAmount_short) / abs(float(response[2].get('positionAmt'))), token_decimal)
        takeProfit_short_atPrice = round((marginAmount_short - colateralAmount_short) / abs(float(response[2].get('positionAmt'))), token_decimal)

        if str(current_time) =='9:30:00' or str(current_time) == '17:30:00':
            telegram_bot_sendtext("unRealizedProfit_short " + str(unRealizedProfit_short)
                                + " | positionQty " + response[2].get('positionAmt')
                                + " | marginAmount_short " + str(marginAmount_short)
                                + " | colateralAmount_short " + str(colateralAmount_short)
                                + " | entryPrice " + response[2].get('entryPrice')
                                + " | markPrice " + response[2].get('markPrice')
                                + " | liquidationPrice " + response[2].get('liquidationPrice')
                                + " | next_dca_price_short " + str(next_dca_price_short)
                                + " | takeProfit_short_atPrice " + str(takeProfit_short_atPrice))

        print("unRealizedProfit_short " + str(unRealizedProfit_short))  
        print("positionQty " + response[2].get('positionAmt'))
        print("marginAmount_short " + str(marginAmount_short))
        print("colateralAmount_short " + str(colateralAmount_short))
        print("entryPrice " + response[2].get('entryPrice'))
        print("markPrice " + response[2].get('markPrice'))
        print("liquidationPrice " + response[2].get('liquidationPrice'))
        print("next_dca_price_short " + str(next_dca_price_short))
        print("add_quantity_short " + str(add_quantity_short))
        print("takeProfit_short_atPrice " + str(takeProfit_short_atPrice))

        if unRealizedProfit_short >= (round(float(colateralAmount_short * config.takeProfit_percent), price_decimal)):
            api_binance.market_close_short(pair, response)
            # wait for 1-3 seconds
            time.sleep(random.randint(1, 3))
            # after take profit open short again
            init_quantity = round((leverage * amount / float(lastest_price.get('price'))), token_decimal)
            api_binance.market_open_short(pair, init_quantity)
            print(colored("SHORT_SIDE : Take Profit", "red"))
            print("SHORT_SIDE : Take Profit" + str(unRealizedProfit_short))
            telegram_bot_sendtext("SHORT_SIDE : Take Profit "
                                + " | PNL " + str(unRealizedProfit_short))
        else: 
            if unRealizedProfit_short <= (round(float(colateralAmount_short * config.dca_percent), price_decimal)):
                api_binance.market_open_short(pair, add_quantity_short)
                # wait for 1-3 seconds
                time.sleep(random.randint(1, 3))
                print(colored("SHORT_SIDE : ADD SHORT", "red"))
                print("SHORT_SIDE : add_quantity_short" + str(add_quantity_short))
                telegram_bot_sendtext("SHORT_SIDE : ADD SHORT "
                                    + " | add_quantity_short " + str(add_quantity_short))
            else: print(colored("SHORT_SIDE : HOLDING_SHORT", "red"))                

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

try:
    while True:
        try:
            for i in range(len(config.pair)):
                pair          = config.pair[i]
                leverage      = config.leverage[i]
                token_decimal = config.token_decimal[i]
                price_decimal = config.price_decimal[i]
                amount        = config.amount[i] 
                lets_make_some_money(pair, leverage, amount, token_decimal, price_decimal)
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


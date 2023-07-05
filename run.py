import api_binance
import time
import config
import random
import strategies.price_support
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

choose_your_fighter = strategies.price_support

def lets_make_some_money(pair_config):

    print("--------------")
    print(pair_config["pair"])

    # Retrieve Infomation for Initial Trade Setup
    response = api_binance.position_information(pair_config["pair"])[0]
    lastest_price = api_binance.get_lastest_price(pair_config["pair"])
    asset_balance = float(api_binance.futures_account_balance(pair_config["asset"]))

    if response.get('marginType') != "cross": api_binance.Change_margin_to_CROSSED(pair_config["pair"])
    if int(response.get("leverage")) != pair_config["leverage"]: api_binance.change_leverage(pair_config["pair"], int(pair_config["leverage"]))
              
    if api_binance.LONG_SIDE(response) == "NO_POSITION" and api_binance.SHORT_SIDE(response) == "NO_POSITION":
        hero = choose_your_fighter.futures_hero(pair_config)
        print(hero)

        # posAmount = float(asset_balance) / 4
        posAmount = CALC_ORDER_AMOUNT(asset_balance)
        print("posAmount: " + str(posAmount))
        init_quantity = round((float(pair_config["leverage"]) * posAmount / float(lastest_price.get('price'))), int(pair_config["token_decimal"]))
        print("init_quantity: " + str(init_quantity))
        if hero["GO_LONG"].iloc[-1] and float(asset_balance) > 100:           
            api_binance.market_open_long(pair_config["pair"], init_quantity)
            telegram_bot_sendtext("LONG_SIDE : OPEN LONG "
                        + " | init_quantity " + str(init_quantity))             
        else: print("LONG_SIDE : WAIT ")     

        if hero["GO_SHORT"].iloc[-1] and float(asset_balance) > 100:
            api_binance.market_open_short(pair_config["pair"], init_quantity)
            telegram_bot_sendtext("SHORT_SIDE : OPEN SHORT "
                            + " | init_quantity " + str(init_quantity))            
        else: print("SHORT_SIDE : WAIT")    

    else:
        if api_binance.LONG_SIDE(response) == "LONGING":   
            
            unRealizedProfit_long = (float(response.get('unRealizedProfit')))
            colateralAmount_long = round((abs(float(response.get('notional'))) / pair_config["leverage"]), pair_config["price_decimal"])
            marginAmount_long = round(abs(float(response.get('notional'))), int(pair_config["price_decimal"]))

            add_amount_long = round(colateralAmount_long * float(pair_config["dca_amount_ratio"]), pair_config["price_decimal"])
            add_quantity_long = round((add_amount_long * float(pair_config["leverage"])) / float(lastest_price.get('price')) , pair_config["token_decimal"])
            next_dca_price_long = round((marginAmount_long - unRealizedProfit_long - abs(colateralAmount_long * float(pair_config["dca_percent"]))) / float(response.get('positionAmt')), pair_config["price_decimal"])
            takeProfit_long_atPrice = round((marginAmount_long + abs(colateralAmount_long * float(pair_config["takeProfit_percent"])) - unRealizedProfit_long) / float(response.get('positionAmt')), pair_config["price_decimal"])

            print("Asset Balance: " + str(asset_balance))
            print("unRealizedProfit_long " + str(unRealizedProfit_long))          
            print("positionQty " + response.get('positionAmt'))
            print("marginAmount_long " + str(marginAmount_long))
            print("colateralAmount_long " + str(colateralAmount_long))
            print("entryPrice " + response.get('entryPrice'))
            print("markPrice " + response.get('markPrice'))
            print("liquidationPrice " + response.get('liquidationPrice'))
            print("next_dca_price_long " + str(next_dca_price_long))
            print("add_quantity_long " + str(add_quantity_long))
            print("takeProfit_long_atPrice " + str(takeProfit_long_atPrice))

            open_take_Profit_order_long = api_binance.get_take_profit_order(pair_config["pair"])
            #Take Long profit:
            if unRealizedProfit_long >= (round(float(colateralAmount_long * float(pair_config["takeProfit_percent"])), int(pair_config["price_decimal"]))):
                # api_binance.market_close_long(pair_config["pair"], response)
                print(colored("LONG_SIDE : Take Profit ", "green"))
                print("LONG_SIDE : Take Profit " + str(unRealizedProfit_long))
                telegram_bot_sendtext("LONG_SIDE : Take Profit "
                                    + " | PNL " + str(unRealizedProfit_long))                
                # wait for 1-3 seconds
                time.sleep(random.randint(1, 3))
            else: 
                if unRealizedProfit_long <= (round(float(colateralAmount_long * float(pair_config["dca_percent"])), int(pair_config["price_decimal"]))) and \
                    colateralAmount_long < float(asset_balance) / config.fund_ratio and \
                    colateralAmount_long < config.max_amount:

                    api_binance.market_open_long(pair_config["pair"], add_quantity_long)
                    # wait for 1-3 seconds
                    time.sleep(random.randint(1, 3))

                    if open_take_Profit_order_short is not None:
                        api_binance.cancel_open_order(pair_config["pair"], open_take_Profit_order_long["orderId"]) 

                    print(colored("LONG_SIDE : ADD LONG ", "green"))
                    print("LONG_SIDE : add_quantity_long " + str(add_quantity_long))
                    telegram_bot_sendtext("LONG_SIDE : ADD LONG "
                                        + " | add_quantity_long " + str(add_quantity_long))     
                else: 
                    response_long = api_binance.position_information(pair_config["pair"])[0]
                    if open_take_Profit_order_long is None and api_binance.LONG_SIDE(response_long) == "LONGING":
                        api_binance.take_profit_market_long(pair_config["pair"], round(takeProfit_long_atPrice, pair_config["price_decimal"]))
                    print(colored("LONG_SIDE : HOLDING_LONG ", "green"))
        print("**********************************************************")         
        print("\n")

        if api_binance.SHORT_SIDE(response) == "SHORTING":
            
            unRealizedProfit_short = (float(response.get('unRealizedProfit')))
            colateralAmount_short = round((abs(float(response.get('notional'))) / float(pair_config["leverage"])), int(pair_config["price_decimal"]))
            marginAmount_short = round(abs(float(response.get('notional'))), int(pair_config["price_decimal"]))

            add_amount_short = round(colateralAmount_short * float(pair_config["dca_amount_ratio"]), int(pair_config["price_decimal"]))
            add_quantity_short = round((add_amount_short * float(pair_config["leverage"])) / float(lastest_price.get('price')) , int(pair_config["token_decimal"]))
            next_dca_price_short = round((marginAmount_short + unRealizedProfit_short  + abs(colateralAmount_short * float(pair_config["dca_percent"]))) / abs(float(response.get('positionAmt'))), int(pair_config["price_decimal"]))
            takeProfit_short_atPrice = round((marginAmount_short - abs(colateralAmount_short * float(pair_config["takeProfit_percent"])) + unRealizedProfit_short ) / abs(float(response.get('positionAmt'))), int(pair_config["price_decimal"]))
            
            print("Asset Balance: " + str(asset_balance))
            print("unRealizedProfit_short " + str(unRealizedProfit_short))  
            print("positionQty " + response.get('positionAmt'))
            print("marginAmount_short " + str(marginAmount_short))
            print("colateralAmount_short " + str(colateralAmount_short))
            print("entryPrice " + response.get('entryPrice'))
            print("markPrice " + response.get('markPrice'))
            print("liquidationPrice " + response.get('liquidationPrice'))
            print("next_dca_price_short " + str(next_dca_price_short))
            print("add_quantity_short " + str(add_quantity_short))
            print("takeProfit_short_atPrice " + str(takeProfit_short_atPrice))

            open_take_Profit_order_short = api_binance.get_take_profit_order(pair_config["pair"])

            if unRealizedProfit_short >= (round(float(colateralAmount_short * float( pair_config["takeProfit_percent"])), int(pair_config["price_decimal"]))):
                # api_binance.market_close_short(pair_config["pair"], response)
                print(colored("SHORT_SIDE : Take Profit ", "red"))
                print("SHORT_SIDE : Take Profit " + str(unRealizedProfit_short))
                telegram_bot_sendtext("SHORT_SIDE : Take Profit "
                                    + " | PNL " + str(unRealizedProfit_short))
                # wait for 1-3 seconds
                time.sleep(random.randint(1, 3))
            else: 
                if unRealizedProfit_short <= (round(float(colateralAmount_short * pair_config["dca_percent"]), int(pair_config["price_decimal"]))) and \
                    colateralAmount_short < float(asset_balance) / config.fund_ratio and \
                    colateralAmount_short < config.max_amount:
                    api_binance.market_open_short(pair_config["pair"], add_quantity_short)
                    # wait for 1-3 seconds
                    time.sleep(random.randint(1, 3))
                    if open_take_Profit_order_short is not None:
                        api_binance.cancel_open_order(pair_config["pair"], open_take_Profit_order_short["orderId"]) 

                    print(colored("SHORT_SIDE : ADD SHORT", "red"))
                    print("SHORT_SIDE : add_quantity_short " + str(add_quantity_short))
                    telegram_bot_sendtext("SHORT_SIDE : ADD SHORT "
                                        + " | add_quantity_short " + str(add_quantity_short))
                else:                    
                    response_short = api_binance.position_information(pair_config["pair"])[0]
                    if open_take_Profit_order_short is None and api_binance.SHORT_SIDE(response_short) == "SHORTING":
                        api_binance.take_profit_market_short(pair_config["pair"], round(takeProfit_short_atPrice, pair_config["price_decimal"]))

                    print(colored("SHORT_SIDE : HOLDING_SHORT ", "red"))           
    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

def CALC_ORDER_AMOUNT(asset_balance):
    pair_count = len(config.pairs)
    print("pair_count: " + str(pair_count))
    print("asset_balance: " + str(asset_balance))
    return asset_balance / (pair_count * 10)

try:
    while True:
        try:
            for i in range(len(config.pairs)):
                pair_config = config.pairs[i]

                lets_make_some_money(pair_config)
                time.sleep(random.randint(1, 3)) # sleep to avoid penality

        except (socket.timeout,
                BinanceAPIException,
                urllib3.exceptions.ProtocolError,
                urllib3.exceptions.ReadTimeoutError,
                requests.exceptions.ConnectionError,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ReadTimeout,
                ConnectionResetError, KeyError, OSError) as e:

            # if not os.path.exists("ERROR"):
                print(e)
                telegram_bot_sendtext(" ERROR RESPONSE API BINANCE: "+ str(e)+"")

except KeyboardInterrupt: print("\n\nAborted.\n")


# import api_binance
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
#fees 
taker_fees    = 0.2

def lets_make_some_money(pair_config):
    print(pair_config["pair"])
    hero = choose_your_fighter.futures_hero(pair_config["pair"], pair_config["tick_size"])
    print("--------------")
    
    print(hero)
              

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

try:
    while True:
        try:
            for i in range(len(config.pairs)):
                pair_config = config.pairs[i]
                # print(str(config.pairs[i]))

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

            if not os.path.exists("ERROR"): os.makedirs("ERROR")
            with open((os.path.join("ERROR", config.pair[i] + ".txt")), "a", encoding="utf-8") as error_message:
                error_message.write("[!] " + config.pair[i] + " - " + "Created at : " + datetime.today().strftime("%d-%m-%Y @ %H:%M:%S") + "\n" + str(e) + "\n\n")
                print(e)
                telegram_bot_sendtext(" ERROR RESPONSE API BINANCE: "+ str(e)+"")

except KeyboardInterrupt: print("\n\nAborted.\n")


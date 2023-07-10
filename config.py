live_trade = True
# ETH BTC XRP
coin     = ["ETH", "BTC", "XRP"]
asset     = ["USDT", "USDT", "USDT"]

init_amount = [30, 30, 20]
leverage = [25, 30, 25]
token_decimal = [3, 3, 1]
price_decimal = [2, 1, 4]
tick_size = ["1d", "1d", "1d"]
#DCA
amplitude = [3, 2.5, 4]
takeProfit_percent = [0.25, 0.3, 0.25]
dca_percent = [-1.2, -1.2, -1.3]
dca_amount_ratio = [0.25, 0.25, 0.25]

fund_ratio = 0.8
max_amount = 450

pairs = []

for i in range(len(coin)):
    pair = {}
    pair["pair"] = coin[i] + asset[i]
    pair["asset"] = asset[i]
    pair["init_amount"] = float(init_amount[i])
    pair["leverage"] = int(leverage[i])
    pair["token_decimal"] = int(token_decimal[i])
    pair["price_decimal"] = int(price_decimal[i])
    pair["tick_size"] = str(tick_size[i])     
    pair["amplitude"] = float(amplitude[i])
    pair["takeProfit_percent"] = float(takeProfit_percent[i])
    pair["dca_percent"] = float(dca_percent[i])      
    pair["dca_amount_ratio"] = float(dca_amount_ratio[i])         
    pairs.append(pair)

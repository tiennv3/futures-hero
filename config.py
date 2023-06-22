live_trade = True

coin     = ["ETH", "BTC"]
asset     = ["USDT", "USDT"]
# BNB
init_amount = [30, 30]
# 0.75
leverage = [30, 30]
token_decimal = [2, 4]
price_decimal = [2, 2]
tick_size = ["1d", "1d"]
#DCA
amplitude = [2.5, 1.5]
takeProfit_percent = [0.3, 0.3]
dca_percent = [-1.2, -1.2]
dca_amount_ratio = [0.5, 0.5]

fund_ratio = 0.8
max_amount = 300

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

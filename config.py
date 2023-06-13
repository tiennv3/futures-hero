live_trade = True

coin     = ["ETH"]
asset     = ["USDT"]
# BNB
amount = [100]
# 0.75
leverage = [30]
token_decimal = [2]
price_decimal = [2, ]
tick_size = ["1d", "1d"]
#DCA
amplitude = [2]
takeProfit_percent = [0.3]
dca_percent = [-1]
dca_amount_percent = [1]

fund_ratio = 3
max_amount = 70

pairs = []

for i in range(len(coin)):
    pair = {}
    pair["pair"] = coin[i] + asset[i]
    pair["asset"] = asset[i]
    pair["amount"] = float(amount[i])
    pair["leverage"] = int(leverage[i])
    pair["token_decimal"] = int(token_decimal[i])
    pair["price_decimal"] = int(price_decimal[i])
    pair["tick_size"] = str(tick_size[i])     
    pair["amplitude"] = str(amplitude[i])
    pair["takeProfit_percent"] = float(takeProfit_percent[i])
    pair["dca_percent"] = float(dca_percent[i])      
    pair["dca_amount_percent"] = float(dca_amount_percent[i])         
    pairs.append(pair)

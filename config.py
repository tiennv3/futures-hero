live_trade = True

coin     = ["BTCUSDT", "ETHUSDT"]
# BNB
amount = [100, 100]
# 0.75
leverage = [30, 30]
token_decimal = [4, 4]
price_decimal = [2, 2]
tick_size = ["1d", "1d"]
#DCA
amplitude = [10, 10]
takeProfit_percent = [30, 30]
dca_percent = [-1, -1]

pairs = []

for i in range(len(coin)):
    pair = {}
    pair["pair"] = coin[i]
    pair["amount"] = str(amount[i])
    pair["leverage"] = leverage[i]
    pair["token_decimal"] = str(token_decimal[i])
    pair["price_decimal"] = price_decimal[i]
    pair["tick_size"] = str(tick_size[i])     
    pair["amplitude"] = str(amplitude[i])
    pair["takeProfit_percent"] = takeProfit_percent[i]
    pair["dca_percent"] = str(dca_percent[i])           
    pairs.append(pair)
    print()

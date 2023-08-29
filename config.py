live_trade = True
# ETH BTC XRP
coin     = ["ETH",  "XRP", "BNB"]
asset     = ["USDT", "USDT", "USDT"]

init_amount = [20, 20, 100]
leverage = [20, 15, 15]
token_decimal = [3, 1, 2]
price_decimal = [2, 4, 2]
tick_size = ["1d", "1d", "1w"]
#DCA
amplitude = [3, 4, 11]
takeProfit_percent = [0.3, 0.35, 0.3]
dca_percent = [-1.2, -1.3, -1.2]
dca_amount_ratio = [0.25, 0.25, 0.25]
ceiling_price = [0.25, 0.25, 0.25]
floor_price = [0.25, 0.25, 0.25]

fund_ratio = 0.8
max_amount = 450
init_amount_divide = 15
auto_amount = False
pairs = []

for i in range(len(coin)):
    pair = {}
    pair["pair"] = coin[i] + asset[i]
    pair["asset"] = asset[i]
    pair["ceiling_price"] = float(ceiling_price[i])
    pair["floor_price"] = float(floor_price[i])
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

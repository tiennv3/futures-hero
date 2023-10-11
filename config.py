live_trade = True
# ETH BTC XRP
coin     = ["ETH", "BTC", "LTC", "TOMO"]
asset     = ["USDT", "USDT", "USDT", "USDT"]

init_amount = [15, 15, 20, 50] 
leverage = [20, 20, 15, 10]
token_decimal = [3, 3, 3, 0]
price_decimal = [2, 1, 2, 4]
tick_size = ["1d", "1d", "1d", "1d"]
#DCA
amplitude = [2.5, 2, 4, 1]
takeProfit_percent = [0.3, 0.3, 0.35, 0.5]
dca_percent = [-1.2, -1.2, -1.3, -1.3]
dca_amount_ratio = [0.25, 0.25, 0.25, 0.25]
long_Price_limit = [3000, 50000, 500, 1.42]
short_Price_limit = [1400, 20000, 50, 0.9]

fund_ratio = 0.8
max_amount = 150
init_amount_divide = 15
auto_amount = False

pairs = []

for i in range(len(coin)):
    pair = {}
    pair["pair"] = coin[i] + asset[i]
    pair["asset"] = asset[i]
    pair["long_Price_limit"] = float(long_Price_limit[i])
    pair["short_Price_limit"] = float(short_Price_limit[i])
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

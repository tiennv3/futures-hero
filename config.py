live_trade = True

coin     = ["BNB"]
# BNB
amount = [5]
# 0.75
leverage = [20]
token_decimal = [2]
price_decimal = [2]

pair = []

for i in range(len(coin)):
    pair.append(coin[i] + "USDT")

    print("Pair Name        :   " + pair[i])
    print("Trade amount   :   " + str(amount[i]) + " " + "USDT")
    print("Leverage         :   " + str(leverage[i]))
    print()

#DCA
dca_percent = -1
dca_amount_percent = 0.25
takeProfit_percent = 0.1
# dca_measure = 100

# # long
# add_long_measure = 35
# new_quantity_long_multiplier = 0.30
# takeprofitlong_usd = 0.5
# liquidationpricemarklong_percent = 5

# # short
# add_short_measure = 35
# new_quantity_short_multiplier = 0.30
# takeprofitshort_usd = 0.5
# liquidationpricemarkshort_percent = 5

# long position / short position
# "add_long_measure" is a % between entry and current positions, when exceed % add "new_quantity_long"
# "new_quantity_long_multiplier" is a multiplier for every next order, if multiplier smaller than every next
# order will be smaller than order before
# "liquidationpricemarkshort_percent" % before liqudation add "quantity", better to keep around 5-10%

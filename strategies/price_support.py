import modules.candlestick
import pandas

def futures_hero(pair_config):
    # Fetch the raw klines data
    main_raw = modules.candlestick.get_klines(pair_config["pair"], pair_config["tick_size"])
    # Process Technical Analysis
    dataset   = modules.candlestick.candlestick(main_raw)[["timestamp", "open", "high", "low", "close"]].copy()
    main_can = modules.candlestick.candlestick(main_raw)[["timestamp", "color"]].copy()

    # Rename the column to avoid conflict
    main_can = main_can.rename(columns={'color': 'main_candle'})

    # Merge all the necessarily data into one Dataframe
    dataset = pandas.merge_asof(dataset, main_can, on='timestamp')
    
    dataset["APMLITUDE"] = dataset.apply(CALC_APMLITUDE, axis=1)
    dataset["GO_LONG"] = dataset.apply(GO_LONG_CONDITION, args=(pair_config, ), axis=1)
    dataset["GO_SHORT"] = dataset.apply(GO_SHORT_CONDITION, args=(pair_config, ), axis=1)
    
    last_tick = dataset.iloc[-1:]
    return last_tick

def CALC_APMLITUDE(dataset):
    return abs((dataset['close'] - dataset['high']) / dataset['high'] * 100)
   
def GO_LONG_CONDITION(dataset, pair_config):
    color = "RED"
    x = dataset['high'] - ((dataset['high'] - dataset['low']) * 0.9)
    if  dataset['main_candle'] == color and \
        dataset['close'] < dataset['open'] and \
        dataset['close'] < x and \
        abs(dataset['APMLITUDE']) >= float(pair_config['amplitude']) : return True    
    else : return False

def GO_SHORT_CONDITION(dataset, pair_config):
    color = "GREEN"
    x = dataset['low'] + ((dataset['high'] - dataset['low']) * 0.9)
    if  dataset['main_candle'] == color and \
        dataset['close'] > dataset['open'] and \
        dataset['close'] > x and \
        abs(dataset['APMLITUDE']) >= float(pair_config['amplitude']) : return True     
    else : return False

def NEED_DCA_CONDITION(pair_config, unRealizedProfit, colateralAmount):
    if  unRealizedProfit >= (round(float(colateralAmount * pair_config['dca_percent']), pair_config['price_decimal'])): return True     
    else : return False

def TAKE_PROFIT_CONDITION(pair_config, unRealizedProfit, colateralAmount):
    if  unRealizedProfit >= (round(float(colateralAmount * pair_config['takeProfit_percent']), pair_config['price_decimal'])): return True     
    else : return False
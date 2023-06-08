import modules.candlestick
import pandas

test_module = False

def futures_hero(pair, tick_size):
    # Fetch the raw klines data
    main_raw = modules.candlestick.get_klines(pair, tick_size)
    # Process Technical Analysis
    dataset   = modules.candlestick.candlestick(main_raw)[["timestamp", "open", "high", "low", "close"]].copy()
    main_can = modules.candlestick.candlestick(main_raw)[["timestamp", "color"]].copy()

    # Rename the column to avoid conflict
    main_can = main_can.rename(columns={'color': 'main_candle'})

    # Merge all the necessarily data into one Dataframe
    dataset = pandas.merge_asof(dataset, main_can, on='timestamp')
    
    dataset["GO_LONG"] = dataset.apply(GO_LONG_CONDITION, axis=1)
    dataset["GO_SHORT"] = dataset.apply(GO_SHORT_CONDITION, axis=1)
    # dataset["EXIT_LONG"] = dataset.apply(EXIT_LONG_CONDITION, axis=1)
    # dataset["EXIT_SHORT"] = dataset.apply(EXIT_SHORT_CONDITION, axis=1)
    last_tick = dataset.iloc[-1:]
    return last_tick

def GO_LONG_CONDITION(dataset):
    color = "GREEN"
    if  dataset['main_candle'] == color: return True    
    else : return False

def GO_SHORT_CONDITION(dataset):
    color = "RED"
    if  dataset['main_candle'] == color: return True    
    else : return False

def EXIT_LONG_CONDITION(dataset):
    if dataset['price_short']: return True
    else : return False

def EXIT_SHORT_CONDITION(dataset):
    if dataset['price_long']: return True
    else : return False

if test_module:
    run = futures_hero("ETHUSDT")
    print(run)
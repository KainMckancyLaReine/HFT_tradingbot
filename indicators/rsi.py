import ta

def calculate_rsi(prices, timeperiod=14):
    return ta.momentum.rsi(prices, window=timeperiod)

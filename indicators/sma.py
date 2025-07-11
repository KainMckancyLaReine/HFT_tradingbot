import ta

def calculate_sma(prices, timeperiod):
    return prices.rolling(window=timeperiod).mean()

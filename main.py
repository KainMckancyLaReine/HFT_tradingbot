import pandas as pd
from strategies.sma_rsi_strategy import sma_rsi_strategy
from indicators.sma import calculate_sma
from indicators.rsi import calculate_rsi

# Haal historische data op of gebruik live data
data = pd.read_csv('./data/xau_usd_data.csv', index_col='Date', parse_dates=True)

# Bereken indicatoren
data['SMA20'] = calculate_sma(data['Close'], timeperiod=20)
data['SMA50'] = calculate_sma(data['Close'], timeperiod=50)
data['RSI'] = calculate_rsi(data['Close'], timeperiod=14)

# Voer de strategie uit
resultaten = sma_rsi_strategy(data)
print(f"Gemiddelde winst per trade: {sum(resultaten)/len(resultaten):.2f}%")

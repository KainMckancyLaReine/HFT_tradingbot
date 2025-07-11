def sma_rsi_strategy(df):
    position = 0
    buy_price = 0
    returns = []

    for i in range(1, len(df)):
        # Koopconditie: prijs boven SMA en RSI onder 70
        if df['Close'][i] > df['SMA20'][i] and df['RSI'][i] < 70:
            if position == 0:
                position = 1
                buy_price = df['Close'][i]
                print(f"Koop op {df.index[i]} voor {buy_price}")

        # Verkoopconditie: prijs onder SMA of RSI boven 70
        elif df['Close'][i] < df['SMA50'][i] or df['RSI'][i] > 70:
            if position == 1:
                position = 0
                sell_price = df['Close'][i]
                profit = (sell_price - buy_price) / buy_price * 100
                returns.append(profit)
                print(f"Verkoop op {df.index[i]} voor {sell_price} - Winst: {profit:.2f}%")

    return returns

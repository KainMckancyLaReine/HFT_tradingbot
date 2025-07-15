import pandas as pd
import os
from data.download_data import download_xau_usd_data
from indicators.sma import calculate_sma
from indicators.rsi import calculate_rsi
from indicators.vwap import calculate_vwap
from strategies.enhanced_sma_rsi_strategy import enhanced_sma_rsi_vwap_strategy
from trading.live_trading import LiveTrader

def run_backtest():
    """
    Run backtest on historical data
    """
    print("📊 Running backtest...")
    
    # Download data if not exists
    if not os.path.exists('./data/xau_usd_data.csv'):
        print("Downloading historical data...")
        download_xau_usd_data()
    
    # Load data
    data = pd.read_csv('./data/xau_usd_data.csv', index_col='Date', parse_dates=True)
    
    # Calculate indicators
    data['SMA20'] = calculate_sma(data['Close'], timeperiod=20)
    data['SMA50'] = calculate_sma(data['Close'], timeperiod=50)
    data['RSI'] = calculate_rsi(data['Close'], timeperiod=14)
    data['VWAP'] = calculate_vwap(data['High'], data['Low'], data['Close'], data['Volume'])
    
    # Run strategy
    returns, signals = enhanced_sma_rsi_vwap_strategy(data)
    
    # Display results
    if returns:
        avg_return = sum(returns) / len(returns)
        win_rate = len([r for r in returns if r > 0]) / len(returns) * 100
        total_return = sum(returns)
        
        print(f"\n📈 BACKTEST RESULTS:")
        print(f"Total trades: {len(returns)}")
        print(f"Average return per trade: {avg_return:.2f}%")
        print(f"Win rate: {win_rate:.1f}%")
        print(f"Total return: {total_return:.2f}%")
        print(f"Total signals: {len(signals)}")
    else:
        print("No trades were executed in the backtest period")

def main():
    """
    Main function
    """
    print("🤖 XAU/USD Trading Bot")
    print("=" * 50)
    
    choice = input("Choose mode:\n1. Run Backtest\n2. Start Live Trading\n\nEnter choice (1 or 2): ")
    
    if choice == "1":
        run_backtest()
    elif choice == "2":
        trader = LiveTrader()
        trader.run_live_trading()
    else:
        print("Invalid choice. Exiting...")

if __name__ == "__main__":
    main()
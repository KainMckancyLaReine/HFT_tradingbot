import pandas as pd
import yfinance as yf
import time
from datetime import datetime, timedelta
import json
import os
from indicators.sma import calculate_sma
from indicators.rsi import calculate_rsi
from indicators.vwap import calculate_vwap
from strategies.enhanced_sma_rsi_strategy import enhanced_sma_rsi_vwap_strategy
from trading.signal_sender import SignalSender
from trading.alpaca_api import AlpacaTrader

class LiveTrader:
    def __init__(self, config_file='config.json'):
        self.config = self.load_config(config_file)
        self.signal_sender = SignalSender(self.config)
        self.alpaca_trader = AlpacaTrader(self.config) if self.config.get('alpaca_enabled') else None
        self.last_signal_time = None
        
    def load_config(self, config_file):
        """
        Load configuration from JSON file
        """
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
        else:
            # Create default config
            default_config = {
                "telegram_enabled": False,
                "telegram_bot_token": "",
                "telegram_chat_id": "",
                "email_enabled": False,
                "email_from": "",
                "email_to": "",
                "email_password": "",
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "alpaca_enabled": False,
                "alpaca_api_key": "",
                "alpaca_secret_key": "",
                "trading_interval": 300,  # 5 minutes
                "min_signal_interval": 3600  # 1 hour between signals
            }
            
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            
            print(f"Created default config file: {config_file}")
            print("Please update the configuration with your API keys and preferences.")
            return default_config
    
    def get_live_data(self, symbol="GC=F", period="5d"):
        """
        Get live market data
        """
        try:
            data = yf.download(symbol, period=period, interval="1h")
            return data
        except Exception as e:
            print(f"Error getting live data: {e}")
            return None
    
    def process_live_data(self, data):
        """
        Process live data and calculate indicators
        """
        if data is None or len(data) < 50:
            return None
            
        # Calculate indicators
        data['SMA20'] = calculate_sma(data['Close'], timeperiod=20)
        data['SMA50'] = calculate_sma(data['Close'], timeperiod=50)
        data['RSI'] = calculate_rsi(data['Close'], timeperiod=14)
        data['VWAP'] = calculate_vwap(data['High'], data['Low'], data['Close'], data['Volume'])
        
        return data
    
    def should_send_signal(self):
        """
        Check if enough time has passed since last signal
        """
        if self.last_signal_time is None:
            return True
            
        time_diff = datetime.now() - self.last_signal_time
        min_interval = timedelta(seconds=self.config['min_signal_interval'])
        
        return time_diff > min_interval
    
    def run_live_trading(self):
        """
        Main live trading loop
        """
        print("🚀 Starting live trading bot...")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                print(f"\n⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Checking market...")
                
                # Get live data
                live_data = self.get_live_data()
                processed_data = self.process_live_data(live_data)
                
                if processed_data is not None:
                    # Run strategy on recent data
                    recent_data = processed_data.tail(100)  # Use last 100 periods
                    returns, signals = enhanced_sma_rsi_vwap_strategy(recent_data)
                    
                    # Check for new signals
                    if signals and self.should_send_signal():
                        latest_signal = signals[-1]
                        
                        # Send signal
                        self.signal_sender.send_telegram_signal(latest_signal)
                        self.signal_sender.send_email_signal(latest_signal)
                        
                        # Execute trade if enabled
                        if self.alpaca_trader:
                            self.alpaca_trader.execute_signal(latest_signal)
                        
                        self.last_signal_time = datetime.now()
                        
                        print(f"📡 Signal sent: {latest_signal['action']} at {latest_signal['price']}")
                    else:
                        print("📊 No new signals generated")
                
                # Wait for next check
                time.sleep(self.config['trading_interval'])
                
        except KeyboardInterrupt:
            print("\n🛑 Trading bot stopped by user")
        except Exception as e:
            print(f"❌ Error in live trading: {e}")

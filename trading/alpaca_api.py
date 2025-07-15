import alpaca_trade_api as tradeapi
from datetime import datetime

class AlpacaTrader:
    def __init__(self, config):
        self.config = config
        self.api = tradeapi.REST(
            config['alpaca_api_key'],
            config['alpaca_secret_key'],
            'https://paper-api.alpaca.markets',  # Paper trading
            api_version='v2'
        )
        
    def execute_signal(self, signal):
        """
        Execute trading signal on Alpaca
        """
        try:
            symbol = "GLD"  # Gold ETF as proxy for XAU/USD
            
            if signal['action'] == 'BUY':
                order = self.api.submit_order(
                    symbol=symbol,
                    qty=signal['quantity'],
                    side='buy',
                    type='market',
                    time_in_force='gtc'
                )
                print(f"✅ Buy order executed: {order.id}")
                
            elif signal['action'] == 'SELL':
                order = self.api.submit_order(
                    symbol=symbol,
                    qty=signal['quantity'],
                    side='sell',
                    type='market',
                    time_in_force='gtc'
                )
                print(f"✅ Sell order executed: {order.id}")
                
        except Exception as e:
            print(f"❌ Error executing trade: {e}")
    
    def get_account_info(self):
        """
        Get account information
        """
        try:
            account = self.api.get_account()
            return {
                'equity': float(account.equity),
                'cash': float(account.cash),
                'buying_power': float(account.buying_power)
            }
        except Exception as e:
            print(f"Error getting account info: {e}")
            return None

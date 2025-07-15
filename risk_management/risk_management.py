def check_stop_loss(buy_price, current_price, stop_loss_pct=2):
    """
    Check if stop loss should be triggered
    """
    loss_pct = (current_price - buy_price) / buy_price * 100
    return loss_pct <= -stop_loss_pct

def calculate_position_size(capital, price, risk_pct=2):
    """
    Calculate position size based on risk management
    """
    max_risk_amount = capital * (risk_pct / 100)
    position_size = max_risk_amount / price
    return round(position_size, 4)

def check_take_profit(buy_price, current_price, take_profit_pct=5):
    """
    Check if take profit should be triggered
    """
    profit_pct = (current_price - buy_price) / buy_price * 100
    return profit_pct >= take_profit_pct

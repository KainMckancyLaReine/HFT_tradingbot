def check_stop_loss(buy_price, current_price, stop_loss_pct=2):
    return (current_price - buy_price) / buy_price * 100 <= -stop_loss_pct

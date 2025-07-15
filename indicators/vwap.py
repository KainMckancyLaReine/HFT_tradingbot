import pandas as pd
import numpy as np

def calculate_vwap(high, low, close, volume):
    """
    Calculate Volume Weighted Average Price (VWAP)
    """
    typical_price = (high + low + close) / 3
    vwap = (typical_price * volume).cumsum() / volume.cumsum()
    return vwap

def calculate_vwap_bands(high, low, close, volume, std_dev=2):
    """
    Calculate VWAP with standard deviation bands
    """
    vwap = calculate_vwap(high, low, close, volume)
    typical_price = (high + low + close) / 3
    
    # Calculate standard deviation
    variance = ((typical_price - vwap) ** 2 * volume).cumsum() / volume.cumsum()
    std_dev_val = np.sqrt(variance)
    
    upper_band = vwap + (std_dev_val * std_dev)
    lower_band = vwap - (std_dev_val * std_dev)
    
    return vwap, upper_band, lower_band
#!/usr/bin/env python3
"""
Test script to get real IBM stock price using yfinance
"""

import yfinance as yf
import sys
from datetime import datetime

def get_real_ibm_price():
    """Get real IBM stock price"""
    print("🔍 FETCHING REAL IBM STOCK PRICE")
    print("=" * 40)
    
    try:
        # Get IBM stock data
        ticker = yf.Ticker('IBM')
        
        # Get historical data (most reliable)
        hist = ticker.history(period='5d')
        
        if not hist.empty:
            latest_close = hist['Close'].iloc[-1]
            latest_date = str(hist.index[-1].date())
            
            print(f"✅ IBM Stock Price:")
            print(f"   Price: ${latest_close:.2f}")
            print(f"   Date: {latest_date}")
            
            # Get additional info
            info = ticker.info
            company_name = info.get('longName', 'IBM')
            sector = info.get('sector', 'Unknown')
            
            print(f"   Company: {company_name}")
            print(f"   Sector: {sector}")
            
            print()
            print(f"🔍 COMPARISON:")
            print(f"   TradeThrust shows: $120.00 (FAKE)")
            print(f"   Real price: ${latest_close:.2f}")
            print(f"   Error: ${abs(latest_close - 120):.2f}")
            
            if latest_close > 120:
                error_pct = ((latest_close / 120) - 1) * 100
                print(f"   TradeThrust is {error_pct:.1f}% too LOW")
            else:
                error_pct = ((120 / latest_close) - 1) * 100
                print(f"   TradeThrust is {error_pct:.1f}% too HIGH")
            
            return latest_close
            
        else:
            print("❌ No historical data available")
            return None
            
    except Exception as e:
        print(f"❌ Error fetching IBM data: {e}")
        return None

if __name__ == "__main__":
    price = get_real_ibm_price()
    if price:
        print(f"\n✅ SUCCESS: Real IBM price is ${price:.2f}")
    else:
        print("\n❌ FAILED to get real IBM price")
        sys.exit(1)
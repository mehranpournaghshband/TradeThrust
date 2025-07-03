#!/usr/bin/env python3
"""
Test script to demonstrate IBM price accuracy issue in TradeThrust
"""

def test_current_tradethrust_ibm_price():
    """Test the current price calculation for IBM"""
    print("🚨 TESTING IBM PRICE ACCURACY ISSUE")
    print("=" * 50)
    
    # Current price_ranges from tradethrust_complete_algorithm.py
    price_ranges = {
        'NOW': (900, 1100), 'AAPL': (150, 200), 'TSLA': (200, 300),
        'NVDA': (800, 1200), 'MSFT': (300, 450), 'META': (400, 600)
    }
    
    symbol = 'IBM'
    min_price, max_price = price_ranges.get(symbol, (50, 150))
    current_price = min_price + (max_price - min_price) * 0.7
    
    print(f"Symbol: {symbol}")
    print(f"Price range used: ${min_price}-${max_price}")
    print(f"TradeThrust shows IBM at: ${current_price:.2f}")
    print()
    print(f"❌ PROBLEM:")
    print(f"   Real IBM price (approx): ~$290.00")
    print(f"   TradeThrust price: ${current_price:.2f}")
    print(f"   Error: ${290 - current_price:.2f} ({((290/current_price - 1)*100):+.1f}%)")
    print()
    print("🔍 ROOT CAUSE:")
    print("   - TradeThrust uses _generate_realistic_data() with hardcoded ranges")
    print("   - IBM not in price_ranges dict, so defaults to (50, 150)")
    print("   - No real stock data API being used")
    print()
    print("✅ SOLUTION NEEDED:")
    print("   - Replace fake data with real stock price API")
    print("   - Use yfinance, Alpha Vantage, or Polygon.io")
    print("   - Ensure all calculations use real prices")

if __name__ == "__main__":
    test_current_tradethrust_ibm_price()
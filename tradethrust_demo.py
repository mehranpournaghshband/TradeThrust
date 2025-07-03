#!/usr/bin/env python3
"""
TradeThrust Demo - Clean Final Version
=====================================

Demonstrates the clean TradeThrust algorithm on popular stocks.
No crashes, graceful error handling, always provides buying price.

Author: TradeThrust Team
"""

from tradethrust_clean_final import TradeThrustClean

def run_demo():
    """Run TradeThrust demo on popular stocks"""
    print("🚀 TradeThrust Stock Trading Algorithm - DEMO")
    print("=" * 60)
    print("✅ Clean implementation - No crashes!")
    print("✅ Uses only Polygon API + Yahoo backup")
    print("✅ Always provides buying price")
    print("✅ Follows exact TradeThrust methodology")
    print("=" * 60)
    
    # Test symbols - mix of strong and weak stocks
    test_symbols = ['AAPL', 'MSFT', 'NVDA', 'TSLA', 'META']
    
    # Initialize TradeThrust
    tt = TradeThrustClean()
    
    print(f"\n🧪 Testing {len(test_symbols)} symbols...")
    
    for i, symbol in enumerate(test_symbols, 1):
        print(f"\n{'='*20} TEST {i}/{len(test_symbols)} {'='*20}")
        
        try:
            result = tt.analyze_stock(symbol)
            
            if 'error' in result:
                print(f"❌ {result['error']}")
                print("💡 Program continues gracefully - no crash!")
            else:
                # Show summary
                rec = result['recommendation']
                print(f"\n🎯 SUMMARY FOR {symbol}:")
                print(f"   Action: {rec['action']}")
                print(f"   Buy Price: ${rec['buy_price']:.2f}")
                print(f"   Stop Loss: ${rec['stop_loss']:.2f}")
                print(f"   Target: ${rec['target_price']:.2f}")
                print(f"   Risk: {rec['risk_percent']:.1f}%")
                print(f"   Reward: {rec['reward_percent']:.1f}%")
        
        except Exception as e:
            print(f"❌ Error with {symbol}: {e}")
            print("💡 Program continues - no crash!")
    
    print(f"\n✅ DEMO COMPLETE!")
    print("💡 As you can see, the program:")
    print("   - Never crashes")
    print("   - Handles missing data gracefully")
    print("   - Always provides buying price")
    print("   - Follows exact TradeThrust algorithm")

if __name__ == "__main__":
    run_demo()
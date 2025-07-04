#!/usr/bin/env python3
"""
Quick Test Script for TradeThrust Yahoo Finance Edition
=======================================================

Tests the Yahoo Finance version with sample stocks
"""

from tradethrust_yahoo import TradeThrustYahoo

def main():
    print("🧪 Testing TradeThrust Yahoo Finance Edition")
    print("=" * 60)
    
    # Initialize TradeThrust Yahoo
    tt = TradeThrustYahoo()
    
    # Test stocks
    test_symbols = ['AAPL', 'MSFT', 'ORCL']
    
    for symbol in test_symbols:
        print(f"\n🔬 Testing {symbol}...")
        try:
            result = tt.analyze_stock(symbol)
            
            if 'error' in result:
                print(f"❌ Error with {symbol}: {result['error']}")
            else:
                recommendation = result['recommendation']
                print(f"✅ {symbol} Analysis Complete:")
                print(f"   Recommendation: {recommendation['action']}")
                print(f"   Confidence: {recommendation['confidence_score']:.0f}/100")
                print(f"   Entry: ${recommendation['entry_price']:.2f}")
                print(f"   Stop: ${recommendation['stop_loss']:.2f}")
                print(f"   Target: ${recommendation['target_price']:.2f}")
                
        except Exception as e:
            print(f"❌ Exception with {symbol}: {e}")
    
    print("\n✅ Testing complete!")

if __name__ == "__main__":
    main()
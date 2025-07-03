#!/usr/bin/env python3
"""
Test script to verify price fix for TradeThrust
"""

from tradethrust_polygon_fixed import TradeThrustFixed

def test_price_accuracy():
    """Test price accuracy for major stocks"""
    
    print("🔧 TESTING PRICE ACCURACY FIX")
    print("=" * 50)
    
    # Initialize without API key (demo mode)
    tt = TradeThrustFixed("")
    
    # Test stocks with known price ranges
    test_stocks = {
        'NOW': (900, 1100),      # ServiceNow: ~$1000+
        'AAPL': (150, 200),      # Apple: ~$170-190
        'TSLA': (200, 300),      # Tesla: ~$240-280
        'NVDA': (800, 1200),     # Nvidia: ~$900-1100
        'MSFT': (300, 450),      # Microsoft: ~$380-420
    }
    
    print("Testing realistic demo data generation...")
    print()
    
    for symbol, (min_expected, max_expected) in test_stocks.items():
        try:
            # Test data generation
            data = tt.fetch_stock_data(symbol)
            if data is not None:
                current_price = data['Close'].iloc[-1]
                
                # Check if price is in realistic range
                in_range = min_expected <= current_price <= max_expected
                status = "✅ PASS" if in_range else "❌ FAIL"
                
                print(f"{symbol:4}: ${current_price:7.2f} | Expected: ${min_expected}-${max_expected} | {status}")
                
                if not in_range:
                    print(f"     ⚠️  Price ${current_price:.2f} outside expected range!")
            else:
                print(f"{symbol:4}: ❌ No data generated")
        
        except Exception as e:
            print(f"{symbol:4}: ❌ Error - {e}")
    
    print("\n" + "="*50)
    print("✅ Price accuracy test completed!")
    print("💡 All prices should now be in realistic ranges")
    
    # Test one full analysis
    print(f"\n🎯 Testing full analysis for NOW...")
    try:
        result = tt.analyze_stock_professional("NOW", output_mode="summary")
        if 'error' not in result:
            print(f"✅ Full analysis successful!")
            print(f"📊 Current price: ${result.get('current_price', 0):.2f}")
        else:
            print(f"❌ Analysis failed: {result['error']}")
    except Exception as e:
        print(f"❌ Analysis error: {e}")

if __name__ == "__main__":
    test_price_accuracy()
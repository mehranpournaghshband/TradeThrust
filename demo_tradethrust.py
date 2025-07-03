#!/usr/bin/env python3
"""
TradeThrust Professional Edition - Demo Script
==============================================

Quick demo of TradeThrust analysis without requiring Polygon.io API key
Perfect for testing and showcasing the system

Author: TradeThrust Team
"""

from tradethrust_polygon_complete import TradeThrustPolygonComplete

def demo_analysis():
    """Run demo analysis on popular stocks"""
    
    print("🚀 TradeThrust Professional Edition - Demo")
    print("=" * 50)
    print("📊 Running demo analysis on popular stocks...")
    print("💡 Using realistic demo data (no API key required)")
    print()
    
    # Initialize without API key (demo mode)
    tt = TradeThrustPolygonComplete("")
    
    # Demo stocks
    demo_stocks = ["AAPL", "TSLA", "NVDA", "MSFT"]
    
    for i, symbol in enumerate(demo_stocks, 1):
        print(f"\n{i}. Analyzing {symbol}...")
        print("-" * 30)
        
        try:
            # Run summary analysis
            result = tt.analyze_stock_professional(symbol, output_mode="summary")
            
            if 'error' not in result:
                print(f"✅ Analysis completed for {symbol}")
            else:
                print(f"❌ Error analyzing {symbol}: {result['error']}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "="*50)
    
    print("\n🎯 Demo completed!")
    print("💡 To run with real data:")
    print("   1. Get free API key from polygon.io")
    print("   2. Set POLYGON_API_KEY environment variable")
    print("   3. Run: python tradethrust_polygon_complete.py")

if __name__ == "__main__":
    demo_analysis()
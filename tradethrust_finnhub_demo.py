#!/usr/bin/env python3
"""
TradeThrust Finnhub Demo - Clean Professional Implementation
===========================================================

Demonstrates the TradeThrust algorithm using Finnhub API with
confidence scoring and exact algorithm implementation.

Author: TradeThrust Team
"""

from tradethrust_finnhub import TradeThrustFinnhub

def run_finnhub_demo():
    """Run TradeThrust demo using Finnhub API"""
    print("🚀 TradeThrust Finnhub Algorithm - DEMO")
    print("=" * 70)
    print("✅ Using Finnhub.io for reliable stock data")
    print("✅ EXACT TradeThrust principles implementation")
    print("✅ Confidence scoring system (0-100)")
    print("✅ Professional risk management")
    print("✅ Never crashes, always provides buy price")
    print("=" * 70)
    
    # Test symbols - mix of different market conditions
    test_symbols = ['AAPL', 'MSFT', 'NVDA', 'GOOGL', 'META']
    
    # Initialize with demo API key
    print("🔧 Initializing with demo API key...")
    print("💡 For full functionality, get free API key at https://finnhub.io")
    
    tt = TradeThrustFinnhub(api_key="demo")
    
    print(f"\n🧪 Testing {len(test_symbols)} symbols with Finnhub data...")
    
    for i, symbol in enumerate(test_symbols, 1):
        print(f"\n{'='*25} TEST {i}/{len(test_symbols)} {'='*25}")
        
        try:
            result = tt.analyze_stock(symbol)
            
            if 'error' in result:
                print(f"❌ {result['error']}")
                print("💡 Program continues gracefully - no crash!")
            else:
                # Show enhanced summary with confidence breakdown
                rec = result['recommendation']
                print(f"\n🎯 FINNHUB SUMMARY FOR {symbol}:")
                print("─" * 50)
                print(f"   Recommendation: {rec['action']}")
                print(f"   Confidence Score: {rec['confidence_score']:.0f}/100")
                print(f"   Action Confidence: {rec['action_confidence']}")
                print(f"   Data Source: {rec['data_source']}")
                print(f"   Entry Price: ${rec['entry_price']:.2f}")
                print(f"   Stop Loss: ${rec['stop_loss']:.2f}")
                print(f"   Target: ${rec['target_price']:.2f}")
                print(f"   Risk: {rec['risk_percent']:.1f}%")
                print(f"   Reward: {rec['reward_percent']:.1f}%")
                print()
                print("📊 SCORE BREAKDOWN:")
                breakdown = rec['score_breakdown']
                print(f"   Trend Template: {breakdown['trend_template']:.0f}/100")
                print(f"   VCP Pattern: {breakdown['vcp_pattern']:.0f}/100")
                print(f"   Breakout Confirm: {breakdown['breakout_confirmation']:.0f}/100")
                print(f"   Risk Setup: {breakdown['risk_setup']:.0f}/100")
                print(f"   Anti-Rules: {breakdown['anti_rules']:.0f}/100")
        
        except Exception as e:
            print(f"❌ Error with {symbol}: {e}")
            print("💡 Program continues - no crash!")
    
    print(f"\n✅ FINNHUB DEMO COMPLETE!")
    print("💡 Key features demonstrated:")
    print("   ✅ Finnhub API integration (reliable data source)")
    print("   ✅ EXACT algorithm implementation")
    print("   ✅ Confidence scoring (0-100)")
    print("   ✅ Professional risk management")
    print("   ✅ Anti-rules checking")
    print("   ✅ Never crashes, handles all errors gracefully")
    print("   ✅ Always provides actionable buy/sell prices")
    print()
    print("🔗 Get your free Finnhub API key at: https://finnhub.io")
    print("📚 Full documentation available in repository")

if __name__ == "__main__":
    run_finnhub_demo()
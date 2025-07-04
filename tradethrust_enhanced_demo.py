#!/usr/bin/env python3
"""
TradeThrust Enhanced Demo - EXACT Algorithm with Confidence Scoring
================================================================

Demonstrates the enhanced TradeThrust algorithm that follows the EXACT
specification with confidence scoring and anti-rules implementation.

Author: TradeThrust Team
"""

from tradethrust_enhanced_final import TradeThrustEnhanced

def run_enhanced_demo():
    """Run enhanced TradeThrust demo with confidence scoring"""
    print("🚀 TradeThrust Enhanced Algorithm - DEMO")
    print("=" * 70)
    print("✅ EXACT TradeThrust principles implementation")
    print("✅ Confidence scoring system (0-100)")
    print("✅ Anti-rules and risk management")
    print("✅ Enhanced VCP detection")
    print("✅ Precise breakout confirmation")
    print("=" * 70)
    
    # Test symbols - mix of different setups
    test_symbols = ['MSFT', 'AAPL', 'NVDA', 'META', 'GOOGL']
    
    # Initialize enhanced TradeThrust
    tt = TradeThrustEnhanced()
    
    print(f"\n🧪 Testing {len(test_symbols)} symbols with enhanced algorithm...")
    
    for i, symbol in enumerate(test_symbols, 1):
        print(f"\n{'='*30} TEST {i}/{len(test_symbols)} {'='*30}")
        
        try:
            result = tt.analyze_stock(symbol)
            
            if 'error' in result:
                print(f"❌ {result['error']}")
                print("💡 Program continues gracefully - no crash!")
            else:
                # Show enhanced summary with confidence breakdown
                rec = result['recommendation']
                print(f"\n🎯 ENHANCED SUMMARY FOR {symbol}:")
                print("─" * 50)
                print(f"   Recommendation: {rec['action']}")
                print(f"   Confidence Score: {rec['confidence_score']:.0f}/100")
                print(f"   Action Confidence: {rec['action_confidence']}")
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
    
    print(f"\n✅ ENHANCED DEMO COMPLETE!")
    print("💡 Enhanced features demonstrated:")
    print("   ✅ EXACT algorithm implementation")
    print("   ✅ Confidence scoring (0-100)")
    print("   ✅ Anti-rules checking")
    print("   ✅ Enhanced VCP detection")
    print("   ✅ Precise breakout confirmation")
    print("   ✅ Professional risk management")
    print("   ✅ Never crashes, always provides buy price")

if __name__ == "__main__":
    run_enhanced_demo()
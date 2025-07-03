#!/usr/bin/env python3
"""
TradeThrust Commercial Enhanced Edition - Dual Output Demo
=========================================================

Demonstrates both Summary and Detailed output modes side by side
Shows the difference between the two analysis formats

Run this to see both output modes in action!
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tradethrust_commercial_enhanced import TradeThrustCommercial

def demo_dual_output():
    """
    Demonstrate both output modes for comparison
    """
    print("🚀" + "=" * 78 + "🚀")
    print("🏆      TRADETHRUST DUAL OUTPUT MODE DEMONSTRATION     🏆")
    print("🚀" + "=" * 78 + "🚀")
    print("📊 Comparing Summary vs Detailed Output Formats")
    print("🎯 See the difference between quick and comprehensive analysis")
    print("=" * 80)
    
    # Demo stocks
    demo_stocks = ['AAPL', 'MSFT', 'GOOGL']
    
    print(f"\n📋 DEMO STOCKS:")
    for i, stock in enumerate(demo_stocks, 1):
        print(f"   {i}. {stock}")
    
    # Let user choose stock or use default
    try:
        choice = input(f"\nEnter stock symbol (or press Enter for AAPL): ").strip().upper()
        symbol = choice if choice else 'AAPL'
        
        tt = TradeThrustCommercial()
        
        print(f"\n" + "🔄" * 40)
        print(f"🔄 ANALYZING {symbol} IN BOTH OUTPUT MODES")
        print("🔄" * 40)
        
        # First show summary mode
        print(f"\n" + "📋" * 40)
        print(f"📋 SUMMARY OUTPUT MODE")
        print("📋" * 40)
        
        try:
            result_summary = tt.analyze_stock_commercial(symbol, output_mode="summary")
        except Exception as e:
            print(f"❌ Error in summary analysis: {e}")
            return
        
        input(f"\n⏸️  Press Enter to see DETAILED output mode...")
        
        # Then show detailed mode
        print(f"\n" + "📊" * 40)
        print(f"📊 DETAILED OUTPUT MODE")
        print("📊" * 40)
        
        try:
            result_detailed = tt.analyze_stock_commercial(symbol, output_mode="detailed")
        except Exception as e:
            print(f"❌ Error in detailed analysis: {e}")
            return
        
        # Show comparison summary
        print(f"\n" + "🏆" * 40)
        print(f"🏆 OUTPUT MODE COMPARISON SUMMARY")
        print("🏆" * 40)
        
        print(f"\n📋 SUMMARY MODE FEATURES:")
        print(f"   ✅ Quick overview format")
        print(f"   ✅ Key metrics at a glance")
        print(f"   ✅ Clear trade setup information")
        print(f"   ✅ Position sizing guidelines")
        print(f"   ✅ Warning and anti-rules")
        print(f"   ✅ Pivot point information")
        print(f"   ✅ Final recommendation with action steps")
        
        print(f"\n📊 DETAILED MODE FEATURES:")
        print(f"   ✅ Complete analysis explanations")
        print(f"   ✅ Educational content")
        print(f"   ✅ Peer comparison")
        print(f"   ✅ Professional scorecard")
        print(f"   ✅ Enhanced trend template details")
        print(f"   ✅ VCP confidence scoring")
        print(f"   ✅ Advanced breakout confirmation")
        
        print(f"\n🎯 WHEN TO USE EACH MODE:")
        print(f"   📋 Summary: Quick decisions, screening multiple stocks")
        print(f"   📊 Detailed: Learning, education, comprehensive analysis")
        
        print(f"\n📊 ANALYSIS RESULTS FOR {symbol}:")
        print(f"   Minervini Score: {result_summary.get('minervini_score', 'N/A')}/100")
        print(f"   Trend Template: {'✅ PASSED' if result_summary.get('trend_results', {}).get('passed') else '❌ FAILED'}")
        print(f"   VCP Pattern: {'✅ DETECTED' if result_summary.get('vcp_results', {}).get('detected') else '❌ NOT DETECTED'}")
        print(f"   Breakout: {'✅ CONFIRMED' if result_summary.get('breakout_results', {}).get('confirmed') else '❌ NOT CONFIRMED'}")
        
        # Ask for another demo
        another = input(f"\nDemo another stock? (y/n): ").strip().lower()
        if another == 'y':
            demo_dual_output()
        
    except KeyboardInterrupt:
        print(f"\n\n👋 Demo interrupted by user. Thank you for trying TradeThrust!")
        return
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        print("🔄 This might be due to missing dependencies or network issues")

def show_usage_examples():
    """Show usage examples for both modes"""
    print(f"\n" + "💡" * 40)
    print(f"💡 USAGE EXAMPLES")
    print("💡" * 40)
    
    print(f"\n🔹 PYTHON SCRIPT USAGE:")
    print(f"""
from tradethrust_commercial_enhanced import TradeThrustCommercial

tt = TradeThrustCommercial()

# Summary mode - quick analysis
result = tt.analyze_stock_commercial('AAPL', output_mode='summary')

# Detailed mode - comprehensive analysis  
result = tt.analyze_stock_commercial('AAPL', output_mode='detailed')

# Interactive mode - user chooses
result = tt.analyze_stock_commercial('AAPL', output_mode='ask')
""")
    
    print(f"\n🔹 COMMAND LINE USAGE:")
    print(f"   python tradethrust_commercial_enhanced.py")
    print(f"   # Then select option 2 for Summary or 3 for Detailed")
    
    print(f"\n🔹 BATCH ANALYSIS EXAMPLE:")
    print(f"""
stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
results = {{}}

for symbol in stocks:
    # Use summary mode for quick screening
    result = tt.analyze_stock_commercial(symbol, output_mode='summary')
    results[symbol] = result['minervini_score']
    
# Find top scoring stocks
top_stocks = sorted(results.items(), key=lambda x: x[1], reverse=True)
print(f"Top stock: {{top_stocks[0][0]}} with score {{top_stocks[0][1]}}")
""")

if __name__ == "__main__":
    try:
        demo_dual_output()
        show_usage_examples()
        
        print(f"\n🏆 Thank you for trying TradeThrust Commercial Enhanced Edition!")
        print(f"🎯 Both output modes are now available for your trading analysis")
        
    except KeyboardInterrupt:
        print(f"\n\n👋 Demo cancelled by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        print(f"📧 Please ensure you have all dependencies installed")
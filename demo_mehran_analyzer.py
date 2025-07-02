#!/usr/bin/env python3
"""
Interactive Demo: Mehran Stock Buying Checklist
=============================================

This interactive demo allows you to test multiple stocks and learn how 
Mehran's buying criteria work in practice.

Usage: python demo_mehran_analyzer.py
"""

from mehran_stock_analyzer import MehranAnalyzer
import matplotlib.pyplot as plt
import sys

def interactive_analysis():
    """Interactive stock analysis demo"""
    print("=" * 70)
    print("🎯 INTERACTIVE MEHRAN STOCK ANALYSIS DEMO")
    print("=" * 70)
    print("\nThis demo will help you understand Mehran's 3-phase buying system:")
    print("📊 Phase 1: Trend Template (Strong uptrend confirmation)")
    print("📈 Phase 2: VCP Base Formation (Volatility contraction)")
    print("🚀 Phase 3: Entry Trigger (Breakout with volume)")
    print("\n" + "=" * 70)
    
    analyzed_stocks = []
    
    while True:
        print(f"\n{'='*20} STOCK ANALYSIS {'='*20}")
        
        # Get stock symbol
        symbol = input("\nEnter stock symbol (or 'quit' to exit): ").strip().upper()
        
        if symbol.lower() in ['quit', 'q', 'exit']:
            break
            
        if not symbol:
            print("❌ Please enter a valid stock symbol")
            continue
        
        print(f"\n🔄 Analyzing {symbol} using Mehran's criteria...")
        print("-" * 50)
        
        # Run analysis
        analyzer = MehranAnalyzer(symbol)
        result = analyzer.analyze_stock()
        
        if result:
            analyzed_stocks.append(result)
            
            # Ask if user wants to see chart
            show_chart = input(f"\nWould you like to see the technical chart for {symbol}? (y/n): ").strip().lower()
            if show_chart in ['y', 'yes']:
                print(f"📊 Generating chart for {symbol}...")
                analyzer.create_chart()
            
        else:
            print(f"❌ Could not analyze {symbol}. Please check the symbol and try again.")
        
        # Ask if they want to analyze another stock
        continue_analysis = input("\nAnalyze another stock? (y/n): ").strip().lower()
        if continue_analysis not in ['y', 'yes']:
            break
    
    # Summary of all analyzed stocks
    if analyzed_stocks:
        print("\n" + "=" * 70)
        print("📋 ANALYSIS SUMMARY")
        print("=" * 70)
        
        print(f"\n{'Symbol':<8} {'Recommendation':<12} {'Phase 1':<8} {'Phase 2':<8} {'Price':<10} {'Risk %'}")
        print("-" * 65)
        
        buy_candidates = []
        
        for stock in analyzed_stocks:
            status_emoji = "🟢" if stock['recommendation'] == 'BUY' else "🔴"
            risk_str = f"{stock['risk_percent']:.1f}%"
            
            print(f"{stock['symbol']:<8} {status_emoji}{stock['recommendation']:<11} {stock['phase1_score']:<8} {stock['phase2_score']:<8} ${stock['current_price']:<9.2f} {risk_str}")
            
            if stock['recommendation'] == 'BUY':
                buy_candidates.append(stock)
        
        # Educational summary
        print("\n" + "=" * 70)
        print("🎓 EDUCATIONAL INSIGHTS")
        print("=" * 70)
        
        if buy_candidates:
            print(f"\n✅ BUY CANDIDATES FOUND: {len(buy_candidates)}")
            print("\nThese stocks meet Mehran's strict criteria:")
            
            for stock in buy_candidates:
                print(f"\n🎯 {stock['symbol']}:")
                print(f"   Current Price: ${stock['current_price']:.2f}")
                print(f"   Suggested Stop: ${stock['stop_loss']:.2f}")
                print(f"   Risk Level: {stock['risk_percent']:.1f}%")
                print(f"   Strength: Phase 1 ({stock['phase1_score']}) + Phase 2 ({stock['phase2_score']})")
        else:
            print("\n⚠️ NO BUY CANDIDATES FOUND")
            print("\nThis is actually GOOD! Mehran's system is designed to be selective.")
            print("Key lessons:")
            print("• Only buy stocks that meet ALL criteria")
            print("• Wait for proper setups rather than forcing trades")
            print("• The best traders are patient and disciplined")
        
        print(f"\n📚 EDUCATIONAL NOTES:")
        print(f"• Phase 1 checks trend strength (need 4/5 criteria)")
        print(f"• Phase 2 identifies low-risk entry zones")
        print(f"• Successful traders often have 40-60% win rates")
        print(f"• Risk management is more important than being right")
        
        total_analyzed = len(analyzed_stocks)
        buy_rate = (len(buy_candidates) / total_analyzed) * 100 if total_analyzed > 0 else 0
        print(f"\n📊 Today's Buy Rate: {len(buy_candidates)}/{total_analyzed} ({buy_rate:.1f}%)")
        
        if buy_rate < 20:
            print("   This selectivity protects your capital! 💪")
        elif buy_rate > 50:
            print("   Unusual - verify market conditions! 🤔")
        
    print(f"\n🎯 Thank you for using Mehran's Stock Analysis Demo!")
    print(f"Remember: Patience and discipline are a trader's best tools.")
    print("=" * 70)

def batch_analysis():
    """Analyze a predefined list of popular stocks"""
    print("🔄 Running batch analysis on popular stocks...")
    
    # Popular stocks to analyze
    stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX']
    
    results = []
    
    for symbol in stocks:
        print(f"\n📊 Analyzing {symbol}...")
        analyzer = MehranAnalyzer(symbol)
        result = analyzer.analyze_stock()
        
        if result:
            results.append(result)
            
            # Brief summary
            status = "✅ BUY" if result['recommendation'] == 'BUY' else "❌ HOLD"
            print(f"   Result: {status} | Phase 1: {result['phase1_score']} | Phase 2: {result['phase2_score']}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 BATCH ANALYSIS SUMMARY")
    print("=" * 60)
    
    buy_candidates = [r for r in results if r['recommendation'] == 'BUY']
    
    print(f"\nAnalyzed: {len(results)} stocks")
    print(f"Buy Candidates: {len(buy_candidates)}")
    print(f"Success Rate: {(len(buy_candidates)/len(results)*100):.1f}%")
    
    if buy_candidates:
        print(f"\n🎯 BUY CANDIDATES:")
        for stock in buy_candidates:
            print(f"   {stock['symbol']}: ${stock['current_price']:.2f} (Stop: ${stock['stop_loss']:.2f})")

def educational_mode():
    """Educational walkthrough of Mehran's system"""
    print("=" * 70)
    print("🎓 EDUCATIONAL MODE: Understanding Mehran's System")
    print("=" * 70)
    
    print("""
📚 MEHRAN'S 3-PHASE BUYING SYSTEM EXPLAINED:

🔍 PHASE 1: TREND TEMPLATE (Foundation)
   ✓ Stock price above 50, 150, 200 SMAs
   ✓ Moving averages in proper order (50>150>200)  
   ✓ Price at least 30% above 52-week low
   ✓ Price within 25% of 52-week high
   ✓ Price above 10 and 21 EMAs
   
   WHY? This confirms the stock is in a strong uptrend
   and institutions are accumulating shares.

📈 PHASE 2: VCP BASE FORMATION (Timing)
   ✓ Series of pullbacks getting smaller (contraction)
   ✓ Volume dries up during pullbacks  
   ✓ Price range tightening (coiling)
   
   WHY? This shows supply is being absorbed and 
   the stock is ready for next major move up.

🚀 PHASE 3: ENTRY TRIGGER (Execution)
   ✓ Price breaks above recent resistance
   ✓ Volume surges 50%+ above average
   
   WHY? This confirms institutional buying is returning
   and new uptrend is beginning.

💰 RISK MANAGEMENT:
   • Stop loss 2% below recent support
   • Risk only 1-2% of portfolio per trade
   • Cut losses quickly, let winners run

📊 PSYCHOLOGY:
   • Most traders buy too early (hope)
   • Mehran waits for confirmation (evidence)
   • Better to miss first 10% than lose 50%
""")
    
    input("\nPress Enter to continue...")
    
    # Example analysis
    print(f"\n🔍 Let's analyze a stock using this system...")
    symbol = input("Enter a stock symbol for educational analysis: ").strip().upper()
    
    if symbol:
        analyzer = MehranAnalyzer(symbol)
        print(f"\n📊 Educational Analysis of {symbol}:")
        print("=" * 50)
        result = analyzer.analyze_stock()
        
        if result:
            print(f"\n🎓 LEARNING POINTS:")
            
            if result['recommendation'] == 'BUY':
                print(f"✅ This stock shows a strong setup!")
                print(f"• All major criteria are met")
                print(f"• Risk is controlled at {result['risk_percent']:.1f}%")
                print(f"• This is what we look for in quality setups")
            else:
                print(f"❌ This stock doesn't meet our standards")
                print(f"• Some criteria are failing")
                print(f"• Patient traders wait for better setups")
                print(f"• Discipline prevents costly mistakes")
        
        show_chart = input(f"\nSee visual chart analysis? (y/n): ").strip().lower()
        if show_chart in ['y', 'yes']:
            analyzer.create_chart()

def main():
    """Main demo function"""
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode == 'batch':
            batch_analysis()
        elif mode == 'education':
            educational_mode()
        else:
            print("Usage: python demo_mehran_analyzer.py [batch|education]")
            print("Or run without arguments for interactive mode")
    else:
        interactive_analysis()

if __name__ == "__main__":
    main()
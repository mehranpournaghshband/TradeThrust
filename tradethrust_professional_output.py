#!/usr/bin/env python3
"""
TradeThrust Professional - Enhanced Output Version
=================================================

Professional stock analysis with enhanced formatting, detailed explanations,
and exact buy/sell price recommendations based on TradeThrust methodology.

Features:
- Professional table formatting
- Clear reasoning for each decision
- Exact buy and sell price recommendations
- Detailed phase-by-phase analysis
- Risk management calculations

Author: TradeThrust Team
Version: 2.0.0 (Professional Output)
"""

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import warnings

warnings.filterwarnings('ignore')

class TradeThrustProfessional:
    """
    Enhanced TradeThrust with professional output formatting
    """
    
    def __init__(self):
        self.analysis_results = {}
        self.watchlist = []
        
    def fetch_stock_data(self, symbol: str, period: str = "2y") -> Optional[pd.DataFrame]:
        """Fetch comprehensive stock data"""
        try:
            ticker = yf.Ticker(symbol.upper())
            data = ticker.history(period=period)
            
            if data.empty:
                return None
            
            # Calculate all technical indicators
            data = self._calculate_indicators(data)
            return data
            
        except Exception as e:
            print(f"❌ Error fetching data for {symbol}: {e}")
            return None
    
    def _calculate_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate all technical indicators"""
        df = data.copy()
        
        # Simple Moving Averages
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        df['SMA_150'] = df['Close'].rolling(window=150).mean()
        df['SMA_200'] = df['Close'].rolling(window=200).mean()
        
        # Exponential Moving Averages
        df['EMA_10'] = df['Close'].ewm(span=10).mean()
        df['EMA_21'] = df['Close'].ewm(span=21).mean()
        
        # 52-week high and low
        df['52W_High'] = df['High'].rolling(window=252).max()
        df['52W_Low'] = df['Low'].rolling(window=252).min()
        
        # Volume indicators
        df['Avg_Volume_20'] = df['Volume'].rolling(window=20).mean()
        df['Avg_Volume_50'] = df['Volume'].rolling(window=50).mean()
        
        # Price ranges and volatility
        df['Daily_Range'] = df['High'] - df['Low']
        df['Avg_Range_20'] = df['Daily_Range'].rolling(window=20).mean()
        
        # Support and resistance
        df['Support'] = df['Low'].rolling(window=20).min()
        df['Resistance'] = df['High'].rolling(window=20).max()
        
        return df
    
    def analyze_stock_professional(self, symbol: str) -> Dict:
        """Complete professional stock analysis with enhanced formatting"""
        symbol = symbol.upper()
        
        # Header
        self._print_header(symbol)
        
        # Fetch data
        data = self.fetch_stock_data(symbol)
        if data is None:
            print(f"❌ Unable to fetch data for {symbol}")
            return {'error': f'No data available for {symbol}'}
        
        latest = data.iloc[-1]
        current_price = latest['Close']
        
        # Phase 1: Trend Template Analysis
        trend_results = self._analyze_trend_template(data, symbol)
        
        # Phase 2: VCP Analysis
        vcp_results = self._analyze_vcp_pattern(data, symbol)
        
        # Phase 3: Entry Signal Analysis
        entry_results = self._analyze_entry_signals(data, symbol)
        
        # Calculate exact buy/sell prices
        buy_sell_prices = self._calculate_buy_sell_prices(data, trend_results, entry_results)
        
        # Final recommendation with reasoning
        final_recommendation = self._generate_final_recommendation(
            trend_results, vcp_results, entry_results, buy_sell_prices
        )
        
        # Display buy/sell prices prominently
        self._display_buy_sell_prices(buy_sell_prices)
        
        # Risk management section
        self._display_risk_management(data, buy_sell_prices)
        
        # Summary and next steps
        self._display_summary_and_next_steps(final_recommendation, symbol)
        
        return {
            'symbol': symbol,
            'current_price': current_price,
            'trend_results': trend_results,
            'vcp_results': vcp_results,
            'entry_results': entry_results,
            'buy_sell_prices': buy_sell_prices,
            'recommendation': final_recommendation
        }
    
    def _print_header(self, symbol: str):
        """Print professional header"""
        print("\n" + "═" * 80)
        print(f"🚀 TRADETHRUST PROFESSIONAL ANALYSIS")
        print(f"📊 Symbol: {symbol} | Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("📚 Based on TradeThrust Professional Trading Methodology")
        print("═" * 80)
    
    def _analyze_trend_template(self, data: pd.DataFrame, symbol: str) -> Dict:
        """Phase 1: Comprehensive trend template analysis with professional formatting"""
        print(f"\n📊 PHASE 1: TRADETHRUST TREND TEMPLATE ANALYSIS")
        print("─" * 60)
        
        latest = data.iloc[-1]
        recent_30 = data.tail(30)
        
        # Get current values
        price = latest['Close']
        sma_50 = latest['SMA_50']
        sma_150 = latest['SMA_150']
        sma_200 = latest['SMA_200']
        high_52w = latest['52W_High']
        low_52w = latest['52W_Low']
        
        # Calculate percentages
        pct_above_low = ((price - low_52w) / low_52w) * 100
        pct_from_high = ((high_52w - price) / high_52w) * 100
        
        # Trend checks
        sma_200_trend = recent_30['SMA_200'].iloc[-1] > recent_30['SMA_200'].iloc[0]
        
        # Create detailed criteria table
        criteria = [
            {
                'criterion': 'Price Above 50-day SMA',
                'current': f"${price:.2f}",
                'target': f">${sma_50:.2f}",
                'status': price > sma_50,
                'reason': f"Price is {((price - sma_50) / sma_50) * 100:+.1f}% vs 50 SMA"
            },
            {
                'criterion': 'Price Above 150-day SMA',
                'current': f"${price:.2f}",
                'target': f">${sma_150:.2f}",
                'status': price > sma_150,
                'reason': f"Price is {((price - sma_150) / sma_150) * 100:+.1f}% vs 150 SMA"
            },
            {
                'criterion': 'Price Above 200-day SMA',
                'current': f"${price:.2f}",
                'target': f">${sma_200:.2f}",
                'status': price > sma_200,
                'reason': f"Price is {((price - sma_200) / sma_200) * 100:+.1f}% vs 200 SMA"
            },
            {
                'criterion': '150 SMA > 200 SMA',
                'current': f"${sma_150:.2f}",
                'target': f">${sma_200:.2f}",
                'status': sma_150 > sma_200,
                'reason': f"150 SMA is {((sma_150 - sma_200) / sma_200) * 100:+.1f}% vs 200 SMA"
            },
            {
                'criterion': '50 SMA > 150 SMA',
                'current': f"${sma_50:.2f}",
                'target': f">${sma_150:.2f}",
                'status': sma_50 > sma_150,
                'reason': f"50 SMA is {((sma_50 - sma_150) / sma_150) * 100:+.1f}% vs 150 SMA"
            },
            {
                'criterion': '200 SMA Trending Up',
                'current': "Trend Direction",
                'target': "Upward",
                'status': sma_200_trend,
                'reason': f"200 SMA {'rising' if sma_200_trend else 'falling'} over 30 days"
            },
            {
                'criterion': '≥30% Above 52W Low',
                'current': f"{pct_above_low:.1f}%",
                'target': "≥30%",
                'status': pct_above_low >= 30,
                'reason': f"Stock has recovered {pct_above_low:.1f}% from 52W low of ${low_52w:.2f}"
            },
            {
                'criterion': '≤25% From 52W High',
                'current': f"{pct_from_high:.1f}%",
                'target': "≤25%",
                'status': pct_from_high <= 25,
                'reason': f"Stock is {pct_from_high:.1f}% below 52W high of ${high_52w:.2f}"
            }
        ]
        
        # Display professional table
        print(f"{'Criterion':<25} {'Current':<12} {'Target':<12} {'Status':<8} Reasoning")
        print("─" * 95)
        
        passed_criteria = 0
        for c in criteria:
            status_symbol = "✅ PASS" if c['status'] else "❌ FAIL"
            print(f"{c['criterion']:<25} {c['current']:<12} {c['target']:<12} {status_symbol:<8} {c['reason']}")
            if c['status']:
                passed_criteria += 1
        
        print("─" * 95)
        trend_strength = "STRONG" if passed_criteria >= 6 else "WEAK" if passed_criteria >= 4 else "POOR"
        print(f"📊 TREND TEMPLATE SCORE: {passed_criteria}/8 - {trend_strength} TREND")
        
        if passed_criteria >= 6:
            print("✅ Stock shows excellent trend characteristics per TradeThrust methodology")
        elif passed_criteria >= 4:
            print("⚠️  Stock shows mixed trend signals - proceed with caution")
        else:
            print("❌ Stock fails trend template - high risk, avoid for now")
        
        return {
            'score': passed_criteria,
            'total': 8,
            'strength': trend_strength,
            'criteria': criteria,
            'passed': passed_criteria >= 6
        }
    
    def _analyze_vcp_pattern(self, data: pd.DataFrame, symbol: str) -> Dict:
        """Phase 2: VCP Pattern Analysis with detailed formatting"""
        print(f"\n📈 PHASE 2: VCP (VOLATILITY CONTRACTION PATTERN) ANALYSIS")
        print("─" * 60)
        
        # Analyze recent 15 weeks for VCP pattern
        analysis_period = data.tail(75)  # ~15 weeks
        contractions = self._find_contractions(analysis_period)
        
        if len(contractions) < 2:
            print("❌ VCP PATTERN: NOT DETECTED")
            print(f"   Reason: Only {len(contractions)} contractions found (need ≥2)")
            print("   Action: Wait for proper base formation")
            return {'detected': False, 'reason': 'Insufficient contractions'}
        
        # Analyze contraction characteristics
        vcp_criteria = []
        
        # Check if contractions are decreasing
        contractions_decreasing = True
        for i in range(1, len(contractions)):
            if contractions[i]['percentage'] >= contractions[i-1]['percentage']:
                contractions_decreasing = False
                break
        
        vcp_criteria.append({
            'criterion': 'Contractions Decreasing',
            'status': contractions_decreasing,
            'detail': 'Each pullback smaller than previous' if contractions_decreasing else 'Pullbacks not getting smaller'
        })
        
        # Check volume behavior
        volume_declining = True
        for contraction in contractions:
            if contraction.get('volume_ratio', 1) > 0.8:
                volume_declining = False
                break
        
        vcp_criteria.append({
            'criterion': 'Volume Declining',
            'status': volume_declining,
            'detail': 'Volume dries up during pullbacks' if volume_declining else 'Volume remains high during pullbacks'
        })
        
        # Check final contraction tightness
        final_tight = contractions[-1]['percentage'] < 15 if contractions else False
        vcp_criteria.append({
            'criterion': 'Tight Final Action',
            'status': final_tight,
            'detail': f"Final pullback: -{contractions[-1]['percentage']:.1f}%" if contractions else "No contractions"
        })
        
        # Display VCP analysis table
        print(f"{'VCP Criterion':<25} {'Status':<10} Description")
        print("─" * 65)
        
        vcp_score = 0
        for criteria in vcp_criteria:
            status_symbol = "✅ PASS" if criteria['status'] else "❌ FAIL"
            print(f"{criteria['criterion']:<25} {status_symbol:<10} {criteria['detail']}")
            if criteria['status']:
                vcp_score += 1
        
        # Show contraction details
        if contractions:
            print(f"\n📉 CONTRACTION DETAILS:")
            for i, c in enumerate(contractions, 1):
                print(f"   Pullback {i}: -{c['percentage']:.1f}% over {c['duration']} days")
        
        vcp_detected = vcp_score >= 2
        print("─" * 65)
        print(f"📈 VCP PATTERN SCORE: {vcp_score}/3 - {'DETECTED' if vcp_detected else 'NOT DETECTED'}")
        
        if vcp_detected:
            print("✅ Stock shows proper VCP base formation - coiled spring effect")
        else:
            print("❌ Stock lacks proper VCP pattern - wait for better base")
        
        return {
            'detected': vcp_detected,
            'score': vcp_score,
            'contractions': contractions,
            'criteria': vcp_criteria
        }
    
    def _analyze_entry_signals(self, data: pd.DataFrame, symbol: str) -> Dict:
        """Phase 3: Entry Signal Analysis"""
        print(f"\n🎯 PHASE 3: ENTRY SIGNAL ANALYSIS")
        print("─" * 45)
        
        latest = data.iloc[-1]
        recent_data = data.tail(20)
        
        # Find resistance level
        resistance = recent_data['High'].max()
        current_price = latest['Close']
        
        # Volume analysis
        avg_volume = data.tail(50)['Volume'].mean()
        current_volume = latest['Volume']
        volume_surge = current_volume > avg_volume * 1.4
        
        # Breakout analysis
        price_breakout = current_price > resistance * 1.001
        
        # Entry signals table
        signals = [
            {
                'signal': 'Price Breakout',
                'current': f"${current_price:.2f}",
                'target': f">${resistance:.2f}",
                'status': price_breakout,
                'strength': 'Strong' if current_price > resistance * 1.02 else 'Weak'
            },
            {
                'signal': 'Volume Surge',
                'current': f"{current_volume:,.0f}",
                'target': f">{avg_volume * 1.4:,.0f}",
                'status': volume_surge,
                'strength': f"{((current_volume / avg_volume) - 1) * 100:+.0f}% vs avg"
            }
        ]
        
        print(f"{'Entry Signal':<15} {'Current':<12} {'Target':<12} {'Status':<10} Strength")
        print("─" * 65)
        
        signals_count = 0
        for signal in signals:
            status_symbol = "✅ PASS" if signal['status'] else "❌ FAIL"
            print(f"{signal['signal']:<15} {signal['current']:<12} {signal['target']:<12} {status_symbol:<10} {signal['strength']}")
            if signal['status']:
                signals_count += 1
        
        entry_signal_present = signals_count >= 1
        print("─" * 65)
        print(f"🎯 ENTRY SIGNALS: {signals_count}/2 - {'PRESENT' if entry_signal_present else 'ABSENT'}")
        
        if entry_signal_present:
            print("✅ Entry conditions met - ready for position")
        else:
            print("❌ Entry signals weak - wait for better timing")
        
        return {
            'present': entry_signal_present,
            'signals_count': signals_count,
            'resistance': resistance,
            'volume_surge': volume_surge,
            'price_breakout': price_breakout,
            'volume_ratio': current_volume / avg_volume
        }
    
    def _calculate_buy_sell_prices(self, data: pd.DataFrame, trend_results: Dict, entry_results: Dict) -> Dict:
        """Calculate exact buy and sell prices"""
        latest = data.iloc[-1]
        current_price = latest['Close']
        
        # Buy price calculation
        if entry_results.get('present', False):
            # Buy at current price if breaking out with volume
            buy_price = current_price
            buy_timing = "IMMEDIATE"
        else:
            # Buy on breakout above resistance
            resistance = entry_results.get('resistance', current_price)
            buy_price = resistance * 1.005  # 0.5% above resistance
            buy_timing = "ON BREAKOUT"
        
        # Stop loss calculation
        recent_support = data.tail(20)['Low'].min()
        stop_loss_support = recent_support * 0.98  # 2% below support
        stop_loss_percentage = buy_price * 0.92   # 8% below buy price
        stop_loss = max(stop_loss_support, stop_loss_percentage)
        
        # Profit targets
        target_1 = buy_price * 1.20  # 20% profit (first scale out)
        target_2 = buy_price * 1.35  # 35% profit (second scale out)
        target_3 = buy_price * 1.50  # 50% profit (final target)
        
        return {
            'buy_price': buy_price,
            'buy_timing': buy_timing,
            'stop_loss': stop_loss,
            'target_1': target_1,
            'target_2': target_2,
            'target_3': target_3,
            'risk_percent': ((buy_price - stop_loss) / buy_price) * 100,
            'reward_risk_ratio': ((target_1 - buy_price) / (buy_price - stop_loss))
        }
    
    def _display_buy_sell_prices(self, prices: Dict):
        """Display exact buy and sell prices prominently"""
        print(f"\n💰 EXACT BUY & SELL PRICES")
        print("═" * 50)
        
        # Buy Line
        print(f"🟢 BUY PRICE:  ${prices['buy_price']:.2f} ({prices['buy_timing']})")
        print(f"🔴 SELL PRICE: ${prices['stop_loss']:.2f} (STOP LOSS)")
        
        print("\n📊 COMPLETE PRICE LEVELS:")
        print("─" * 35)
        print(f"🛒 Entry Price:    ${prices['buy_price']:.2f}")
        print(f"🛑 Stop Loss:      ${prices['stop_loss']:.2f} (-{prices['risk_percent']:.1f}%)")
        print(f"🎯 Target 1:       ${prices['target_1']:.2f} (+20%)")
        print(f"🎯 Target 2:       ${prices['target_2']:.2f} (+35%)")
        print(f"🎯 Target 3:       ${prices['target_3']:.2f} (+50%)")
        print(f"⚖️  Risk/Reward:    1:{prices['reward_risk_ratio']:.1f}")
    
    def _display_risk_management(self, data: pd.DataFrame, prices: Dict):
        """Display comprehensive risk management"""
        print(f"\n🛡️  RISK MANAGEMENT STRATEGY")
        print("─" * 40)
        
        # Position sizing (assuming 1% portfolio risk)
        portfolio_risk = 1.0  # 1% of portfolio
        risk_per_share = prices['buy_price'] - prices['stop_loss']
        
        print(f"💼 Position Sizing (1% Portfolio Risk):")
        print(f"   Risk per Share: ${risk_per_share:.2f}")
        print(f"   Max Position Size: Calculate based on portfolio size")
        print(f"   Example: $100,000 portfolio → ${(1000 / risk_per_share):.0f} shares max")
        
        print(f"\n📋 Trading Rules:")
        print(f"   ✅ Never risk more than 1-2% of portfolio")
        print(f"   ✅ Set stop loss BEFORE buying")
        print(f"   ✅ Take partial profits at targets")
        print(f"   ✅ Trail stop higher as stock advances")
        print(f"   ✅ Cut losses quickly, let winners run")
    
    def _generate_final_recommendation(self, trend_results: Dict, vcp_results: Dict, 
                                     entry_results: Dict, prices: Dict) -> Dict:
        """Generate final recommendation with detailed reasoning"""
        trend_score = trend_results['score']
        vcp_detected = vcp_results['detected']
        entry_present = entry_results['present']
        
        # Overall scoring
        total_score = 0
        if trend_score >= 6: total_score += 3
        elif trend_score >= 4: total_score += 1
        
        if vcp_detected: total_score += 2
        if entry_present: total_score += 2
        
        # Generate recommendation
        if total_score >= 6 and entry_present:
            recommendation = "🟢 STRONG BUY"
            action = "BUY NOW"
            confidence = "HIGH"
            reasoning = "Meets all TradeThrust criteria with strong entry signal"
        elif total_score >= 4 and trend_score >= 6:
            recommendation = "🟡 WATCH LIST"
            action = "MONITOR"
            confidence = "MEDIUM"
            reasoning = "Good trend setup, wait for proper entry signal"
        elif total_score >= 3:
            recommendation = "🟡 POTENTIAL"
            action = "MONITOR"
            confidence = "LOW"
            reasoning = "Some positive signals, needs improvement"
        else:
            recommendation = "🔴 AVOID"
            action = "WAIT"
            confidence = "LOW"
            reasoning = "Does not meet TradeThrust's strict criteria"
        
        return {
            'recommendation': recommendation,
            'action': action,
            'confidence': confidence,
            'reasoning': reasoning,
            'total_score': total_score,
            'max_score': 7
        }
    
    def _display_summary_and_next_steps(self, recommendation: Dict, symbol: str):
        """Display final summary and next steps"""
        print(f"\n🎯 FINAL RECOMMENDATION")
        print("═" * 50)
        
        print(f"📊 Overall Score: {recommendation['total_score']}/7")
        print(f"🎯 Recommendation: {recommendation['recommendation']}")
        print(f"🎬 Action: {recommendation['action']}")
        print(f"🎯 Confidence: {recommendation['confidence']}")
        print(f"💭 Reasoning: {recommendation['reasoning']}")
        
        print(f"\n📋 NEXT STEPS:")
        if recommendation['action'] == 'BUY NOW':
            print(f"   1. ✅ Set buy order at recommended price")
            print(f"   2. ✅ Set stop loss order immediately")
            print(f"   3. ✅ Monitor for profit targets")
            print(f"   4. ✅ Trail stop higher as stock advances")
        elif recommendation['action'] == 'MONITOR':
            print(f"   1. 📊 Add {symbol} to watchlist")
            print(f"   2. 🔍 Monitor daily for entry signals")
            print(f"   3. ⏰ Re-analyze weekly for changes")
            print(f"   4. 🚨 Set alerts for breakout levels")
        else:
            print(f"   1. ❌ Avoid this stock for now")
            print(f"   2. ⏰ Re-evaluate in 2-4 weeks")
            print(f"   3. 🔍 Look for better opportunities")
            print(f"   4. 📚 Focus on higher-scoring stocks")
        
        print(f"\n⚠️  IMPORTANT REMINDERS:")
        print(f"   • This is educational analysis, not financial advice")
        print(f"   • Always do your own research before trading")
        print(f"   • Never risk more than you can afford to lose")
        print(f"   • Past performance doesn't guarantee future results")
        
        print("═" * 50)
        print(f"✅ Analysis Complete | TradeThrust Professional v2.0")
        print("═" * 50)
    
    def _find_contractions(self, data: pd.DataFrame) -> List[Dict]:
        """Find price contractions in the data"""
        contractions = []
        
        # Simple swing analysis for demo
        highs = []
        lows = []
        
        for i in range(3, len(data) - 3):
            # Find swing highs
            if (data.iloc[i]['High'] > data.iloc[i-1]['High'] and 
                data.iloc[i]['High'] > data.iloc[i+1]['High']):
                highs.append((i, data.iloc[i]['High']))
            
            # Find swing lows
            if (data.iloc[i]['Low'] < data.iloc[i-1]['Low'] and 
                data.iloc[i]['Low'] < data.iloc[i+1]['Low']):
                lows.append((i, data.iloc[i]['Low']))
        
        # Match highs with subsequent lows
        for i, (high_idx, high_price) in enumerate(highs):
            subsequent_lows = [low for low in lows if low[0] > high_idx]
            if subsequent_lows:
                low_idx, low_price = min(subsequent_lows, key=lambda x: x[1])
                contraction_pct = ((high_price - low_price) / high_price) * 100
                duration = low_idx - high_idx
                
                contractions.append({
                    'percentage': contraction_pct,
                    'duration': duration,
                    'high_price': high_price,
                    'low_price': low_price
                })
        
        return contractions

def main():
    """Main function for professional TradeThrust"""
    print("🚀 Welcome to TradeThrust Professional")
    print("Enhanced Output with Detailed Analysis Tables")
    print("=" * 60)
    
    tt = TradeThrustProfessional()
    
    while True:
        print("\n📋 TRADETHRUST PROFESSIONAL MENU")
        print("-" * 35)
        print("1. 📊 Analyze Stock (Professional Output)")
        print("2. 🚪 Exit")
        
        choice = input("\nSelect option (1-2): ").strip()
        
        if choice == '1':
            symbol = input("Enter stock symbol: ").strip().upper()
            if symbol:
                try:
                    result = tt.analyze_stock_professional(symbol)
                    
                    # Ask if user wants another analysis
                    another = input(f"\nAnalyze another stock? (y/n): ").strip().lower()
                    if another != 'y':
                        break
                        
                except Exception as e:
                    print(f"❌ Error analyzing {symbol}: {e}")
        
        elif choice == '2':
            print("\n🚀 Thank you for using TradeThrust Professional!")
            print("Remember: Trade safely and follow your risk management rules!")
            break
        
        else:
            print("❌ Invalid option. Please select 1-2.")

if __name__ == "__main__":
    main()
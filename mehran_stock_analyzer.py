#!/usr/bin/env python3
"""
Mehran Stock Buying Checklist Analyzer
=======================================

This program implements Mehran's stock buying criteria including:
- Trend Template (Phase 1)
- VCP Base Formation (Phase 2) 
- Entry Trigger Analysis

Usage: python mehran_stock_analyzer.py SYMBOL
Example: python mehran_stock_analyzer.py AAPL
"""

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import sys
import warnings
warnings.filterwarnings('ignore')

class MehranAnalyzer:
    def __init__(self, symbol):
        self.symbol = symbol.upper()
        self.data = None
        self.analysis_results = {}
        
    def fetch_data(self, period="2y"):
        """Fetch stock data with sufficient history for analysis"""
        try:
            ticker = yf.Ticker(self.symbol)
            self.data = ticker.history(period=period)
            
            if self.data.empty:
                raise ValueError(f"No data found for symbol {self.symbol}")
                
            # Calculate technical indicators
            self._calculate_indicators()
            return True
            
        except Exception as e:
            print(f"Error fetching data for {self.symbol}: {e}")
            return False
    
    def _calculate_indicators(self):
        """Calculate all required technical indicators"""
        if self.data is None:
            return
            
        df = self.data
        
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
        
        # Average volume (20-day)
        df['Avg_Volume'] = df['Volume'].rolling(window=20).mean()
        
        # Price volatility (20-day)
        df['Price_Range'] = df['High'] - df['Low']
        df['Avg_Range'] = df['Price_Range'].rolling(window=20).mean()
        
        self.data = df
    
    def check_trend_template(self):
        """Phase 1: Check Mehran's Trend Template criteria"""
        if self.data is None:
            return {}
            
        latest = self.data.iloc[-1]
        prev_50 = self.data.iloc[-50] if len(self.data) >= 50 else self.data.iloc[0]
        
        results = {}
        
        # 1. Price above 50, 150, 200 SMAs
        price = latest['Close']
        sma_50 = latest['SMA_50']
        sma_150 = latest['SMA_150'] 
        sma_200 = latest['SMA_200']
        
        results['price_above_smas'] = {
            'pass': price > sma_50 and price > sma_150 and price > sma_200,
            'details': f"Price: ${price:.2f} | 50SMA: ${sma_50:.2f} | 150SMA: ${sma_150:.2f} | 200SMA: ${sma_200:.2f}"
        }
        
        # 2. SMA stacking order (50 > 150 > 200)
        results['sma_stacking'] = {
            'pass': sma_50 > sma_150 > sma_200,
            'details': f"50SMA > 150SMA: {sma_50 > sma_150} | 150SMA > 200SMA: {sma_150 > sma_200}"
        }
        
        # 3. Price at least 30% above 52-week low
        week_52_low = latest['52W_Low']
        pct_above_low = ((price - week_52_low) / week_52_low) * 100
        results['above_52w_low'] = {
            'pass': pct_above_low >= 30,
            'details': f"52W Low: ${week_52_low:.2f} | Current: {pct_above_low:.1f}% above low (need ≥30%)"
        }
        
        # 4. Price within 25% of 52-week high
        week_52_high = latest['52W_High']
        pct_below_high = ((week_52_high - price) / week_52_high) * 100
        results['near_52w_high'] = {
            'pass': pct_below_high <= 25,
            'details': f"52W High: ${week_52_high:.2f} | Current: {pct_below_high:.1f}% below high (need ≤25%)"
        }
        
        # 5. Price above 10 and 21 EMAs
        ema_10 = latest['EMA_10']
        ema_21 = latest['EMA_21']
        results['above_emas'] = {
            'pass': price > ema_10 and price > ema_21,
            'details': f"Price: ${price:.2f} | 10EMA: ${ema_10:.2f} | 21EMA: ${ema_21:.2f}"
        }
        
        return results
    
    def detect_vcp_pattern(self, lookback_days=60):
        """Phase 2: Detect VCP (Volatility Contraction Pattern)"""
        if self.data is None or len(self.data) < lookback_days:
            return {'vcp_detected': False, 'reason': 'Insufficient data for VCP analysis'}
        
        recent_data = self.data.tail(lookback_days)
        results = {}
        
        # Find potential contractions (pullbacks from highs)
        contractions = self._find_contractions(recent_data)
        
        # Check if contractions are getting smaller
        contraction_analysis = self._analyze_contractions(contractions)
        
        # Check volume behavior during contractions
        volume_analysis = self._analyze_volume_pattern(recent_data, contractions)
        
        # Check for tight consolidation in recent bars
        tightness_analysis = self._analyze_tightness(recent_data.tail(10))
        
        results.update(contraction_analysis)
        results.update(volume_analysis)
        results.update(tightness_analysis)
        
        return results
    
    def _find_contractions(self, data):
        """Find pullback periods in the data"""
        contractions = []
        
        # Simple peak detection - find local highs and subsequent lows
        highs = []
        lows = []
        
        for i in range(2, len(data) - 2):
            # Local high
            if (data.iloc[i]['High'] > data.iloc[i-1]['High'] and 
                data.iloc[i]['High'] > data.iloc[i-2]['High'] and
                data.iloc[i]['High'] > data.iloc[i+1]['High'] and
                data.iloc[i]['High'] > data.iloc[i+2]['High']):
                highs.append((i, data.iloc[i]['High']))
            
            # Local low
            if (data.iloc[i]['Low'] < data.iloc[i-1]['Low'] and 
                data.iloc[i]['Low'] < data.iloc[i-2]['Low'] and
                data.iloc[i]['Low'] < data.iloc[i+1]['Low'] and
                data.iloc[i]['Low'] < data.iloc[i+2]['Low']):
                lows.append((i, data.iloc[i]['Low']))
        
        # Match highs with subsequent lows to find contractions
        for i, (high_idx, high_price) in enumerate(highs):
            subsequent_lows = [(idx, price) for idx, price in lows if idx > high_idx]
            if subsequent_lows:
                low_idx, low_price = min(subsequent_lows, key=lambda x: x[1])
                contraction_pct = ((high_price - low_price) / high_price) * 100
                contractions.append({
                    'high_idx': high_idx,
                    'low_idx': low_idx,
                    'high_price': high_price,
                    'low_price': low_price,
                    'contraction_pct': contraction_pct
                })
        
        return contractions
    
    def _analyze_contractions(self, contractions):
        """Analyze if contractions are getting progressively smaller"""
        if len(contractions) < 2:
            return {
                'contractions_decreasing': {
                    'pass': False,
                    'details': f"Found only {len(contractions)} contractions, need at least 2 for VCP"
                }
            }
        
        # Check if each contraction is smaller than the previous
        decreasing = True
        contraction_details = []
        
        for i in range(len(contractions)):
            pct = contractions[i]['contraction_pct']
            contraction_details.append(f"Pullback {i+1}: -{pct:.1f}%")
            
            if i > 0 and pct >= contractions[i-1]['contraction_pct']:
                decreasing = False
        
        return {
            'contractions_decreasing': {
                'pass': decreasing and len(contractions) >= 2,
                'details': " | ".join(contraction_details)
            }
        }
    
    def _analyze_volume_pattern(self, data, contractions):
        """Analyze volume during contractions"""
        if not contractions:
            return {
                'volume_declining': {
                    'pass': False,
                    'details': "No contractions found to analyze volume"
                }
            }
        
        # Check if volume declines during pullbacks
        volume_declining = True
        avg_volume = data['Volume'].tail(20).mean()
        
        for contraction in contractions:
            pullback_data = data.iloc[contraction['high_idx']:contraction['low_idx']+1]
            pullback_avg_volume = pullback_data['Volume'].mean()
            
            if pullback_avg_volume > avg_volume * 0.8:  # Allow some tolerance
                volume_declining = False
                break
        
        return {
            'volume_declining': {
                'pass': volume_declining,
                'details': f"Average volume: {avg_volume:,.0f} | Volume declined during pullbacks: {volume_declining}"
            }
        }
    
    def _analyze_tightness(self, recent_data):
        """Check for price tightening in recent bars"""
        if self.data is None or len(recent_data) < 5:
            return {
                'price_tightening': {
                    'pass': False,
                    'details': "Insufficient data for tightness analysis"
                }
            }
        
        # Calculate average range for recent periods
        recent_range = recent_data['Price_Range'].mean()
        longer_range = self.data['Price_Range'].tail(30).mean()
        
        # Price is tightening if recent range is smaller
        tightening = recent_range < longer_range * 0.7
        
        return {
            'price_tightening': {
                'pass': tightening,
                'details': f"Recent avg range: ${recent_range:.2f} | 30-day avg: ${longer_range:.2f} | Tightening: {tightening}"
            }
        }
    
    def check_breakout_signal(self):
        """Check for breakout entry signal"""
        if self.data is None or len(self.data) < 20:
            return {'breakout_signal': False, 'reason': 'Insufficient data'}
        
        latest = self.data.iloc[-1]
        recent_20 = self.data.tail(20)
        
        # Find resistance level (recent highs)
        resistance = recent_20['High'].max()
        avg_volume = recent_20['Volume'].mean()
        
        # Check if price broke above resistance
        price_breakout = latest['Close'] > resistance * 1.001  # Small buffer
        
        # Check for volume surge (50%+ above average)
        volume_surge = latest['Volume'] > avg_volume * 1.5
        
        return {
            'breakout_signal': {
                'pass': price_breakout and volume_surge,
                'details': f"Resistance: ${resistance:.2f} | Current: ${latest['Close']:.2f} | Volume: {latest['Volume']:,.0f} (avg: {avg_volume:,.0f})"
            }
        }
    
    def analyze_stock(self):
        """Perform complete Mehran analysis"""
        if not self.fetch_data() or self.data is None:
            return None
        
        print(f"\n🔍 MEHRAN STOCK ANALYSIS: {self.symbol}")
        print("=" * 60)
        
        # Phase 1: Trend Template
        print("\n📊 PHASE 1: TREND TEMPLATE")
        print("-" * 30)
        
        trend_results = self.check_trend_template()
        phase1_score = 0
        
        for criterion, result in trend_results.items():
            status = "✅ PASS" if result['pass'] else "❌ FAIL"
            print(f"{status} {criterion.replace('_', ' ').title()}")
            print(f"    {result['details']}")
            if result['pass']:
                phase1_score += 1
        
        phase1_pass = phase1_score >= 4  # Allow 1 failure
        print(f"\nPhase 1 Score: {phase1_score}/5 {'✅ PASS' if phase1_pass else '❌ FAIL'}")
        
        # Phase 2: VCP Pattern
        print("\n📈 PHASE 2: VCP BASE FORMATION")
        print("-" * 35)
        
        vcp_results = self.detect_vcp_pattern()
        phase2_score = 0
        
        for criterion, result in vcp_results.items():
            if isinstance(result, dict) and 'pass' in result:
                status = "✅ PASS" if result['pass'] else "❌ FAIL"
                print(f"{status} {criterion.replace('_', ' ').title()}")
                print(f"    {result['details']}")
                if result['pass']:
                    phase2_score += 1
        
        phase2_pass = phase2_score >= 2  # Flexible scoring for VCP
        print(f"\nPhase 2 Score: {phase2_score}/3 {'✅ PASS' if phase2_pass else '❌ FAIL'}")
        
        # Entry Signal
        print("\n🚀 ENTRY SIGNAL CHECK")
        print("-" * 25)
        
        breakout_results = self.check_breakout_signal()
        entry_signal = breakout_results['breakout_signal']['pass']
        status = "✅ PASS" if entry_signal else "❌ FAIL"
        print(f"{status} Breakout Signal")
        print(f"    {breakout_results['breakout_signal']['details']}")
        
        # Final Decision
        print("\n" + "=" * 60)
        overall_pass = phase1_pass and (phase2_pass or entry_signal)
        
        if overall_pass:
            print("🎯 RECOMMENDATION: 🟢 BUY CANDIDATE")
            print("This stock meets Mehran's criteria and shows strong setup!")
        else:
            print("⚠️  RECOMMENDATION: 🔴 DO NOT BUY")
            print("This stock does not meet sufficient criteria. Wait for better setup.")
        
        # Risk management
        print(f"\n💰 RISK MANAGEMENT")
        print("-" * 20)
        latest_price = self.data.iloc[-1]['Close']
        
        # Suggest stop loss below recent support
        recent_lows = self.data.tail(20)['Low']
        support_level = recent_lows.min()
        stop_loss = support_level * 0.98  # 2% below support
        risk_pct = ((latest_price - stop_loss) / latest_price) * 100
        
        print(f"Current Price: ${latest_price:.2f}")
        print(f"Suggested Stop Loss: ${stop_loss:.2f} ({risk_pct:.1f}% risk)")
        print(f"Position Size: Risk no more than 1-2% of portfolio on this trade")
        
        return {
            'symbol': self.symbol,
            'recommendation': 'BUY' if overall_pass else 'HOLD/AVOID',
            'phase1_score': f"{phase1_score}/5",
            'phase2_score': f"{phase2_score}/3",
            'entry_signal': entry_signal,
            'current_price': latest_price,
            'stop_loss': stop_loss,
            'risk_percent': risk_pct
        }
    
    def create_chart(self, save_path=None):
        """Create educational chart showing all indicators"""
        if self.data is None:
            print("No data available for charting")
            return
        
        # Use recent 6 months for cleaner chart
        chart_data = self.data.tail(120)
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 12), 
                                       gridspec_kw={'height_ratios': [3, 1]})
        
        # Price and moving averages
        ax1.plot(chart_data.index, chart_data['Close'], label='Price', linewidth=2, color='black')
        ax1.plot(chart_data.index, chart_data['SMA_50'], label='50 SMA', alpha=0.7, color='blue')
        ax1.plot(chart_data.index, chart_data['SMA_150'], label='150 SMA', alpha=0.7, color='orange')
        ax1.plot(chart_data.index, chart_data['SMA_200'], label='200 SMA', alpha=0.7, color='red')
        ax1.plot(chart_data.index, chart_data['EMA_10'], label='10 EMA', alpha=0.7, color='green', linestyle='--')
        ax1.plot(chart_data.index, chart_data['EMA_21'], label='21 EMA', alpha=0.7, color='purple', linestyle='--')
        
        # 52-week high/low reference lines
        latest = chart_data.iloc[-1]
        ax1.axhline(y=latest['52W_High'], color='green', linestyle=':', alpha=0.5, label='52W High')
        ax1.axhline(y=latest['52W_Low'], color='red', linestyle=':', alpha=0.5, label='52W Low')
        
        ax1.set_title(f'{self.symbol} - Mehran Analysis Chart', fontsize=16, fontweight='bold')
        ax1.set_ylabel('Price ($)', fontsize=12)
        ax1.legend(loc='upper left')
        ax1.grid(True, alpha=0.3)
        
        # Volume
        ax2.bar(chart_data.index, chart_data['Volume'], alpha=0.7, color='skyblue')
        ax2.plot(chart_data.index, chart_data['Avg_Volume'], color='red', linewidth=2, label='20-day Avg Volume')
        ax2.set_ylabel('Volume', fontsize=12)
        ax2.set_xlabel('Date', fontsize=12)
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Format x-axis
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Chart saved to {save_path}")
        else:
            plt.savefig(f'{self.symbol}_mehran_analysis.png', dpi=300, bbox_inches='tight')
            print(f"Chart saved to {self.symbol}_mehran_analysis.png")
        
        plt.show()

def main():
    """Main function to run the analyzer"""
    if len(sys.argv) != 2:
        print("Usage: python mehran_stock_analyzer.py <SYMBOL>")
        print("Example: python mehran_stock_analyzer.py AAPL")
        sys.exit(1)
    
    symbol = sys.argv[1]
    analyzer = MehranAnalyzer(symbol)
    
    # Run analysis
    result = analyzer.analyze_stock()
    
    if result:
        # Create chart
        print(f"\n📊 Generating educational chart for {symbol}...")
        analyzer.create_chart()
        
        # Export results to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"{symbol}_mehran_report_{timestamp}.txt"
        
        with open(report_file, 'w') as f:
            f.write(f"Mehran Stock Analysis Report\n")
            f.write(f"Symbol: {result['symbol']}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Recommendation: {result['recommendation']}\n")
            f.write(f"Phase 1 Score: {result['phase1_score']}\n")
            f.write(f"Phase 2 Score: {result['phase2_score']}\n")
            f.write(f"Entry Signal: {result['entry_signal']}\n")
            f.write(f"Current Price: ${result['current_price']:.2f}\n")
            f.write(f"Suggested Stop Loss: ${result['stop_loss']:.2f}\n")
            f.write(f"Risk Percentage: {result['risk_percent']:.1f}%\n")
        
        print(f"\n📄 Analysis report saved to {report_file}")

if __name__ == "__main__":
    main()
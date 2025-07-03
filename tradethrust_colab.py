#!/usr/bin/env python3
"""
TradeThrust for Google Colab - ENHANCED WITH PIVOT POINT ANALYSIS
================================================================

Google Colab optimized version of TradeThrust - Professional Stock Trading System
🎯 NOW INCLUDES: Advanced Pivot Point Analysis for Precise Entry Timing

Features:
- Complete TradeThrust Trend Template (5 criteria)
- Advanced Pivot Point Analysis (7 criteria)
- Volume Breakout Confirmation
- Professional Risk Management
- Interactive Charts with Pivot Points

Instructions:
1. Run this cell to install dependencies and set up TradeThrust
2. Use tt.analyze_stock('SYMBOL') to get complete analysis
3. Add stocks to watchlist and monitor for opportunities
4. Get professional-grade entry/exit signals

Based on TradeThrust's proven trading methodology with institutional-quality pivot point analysis.
"""

# Install required packages for Colab
import subprocess
import sys

def install_packages():
    """Install required packages in Colab environment"""
    packages = [
        'yfinance',
        'pandas',
        'numpy', 
        'matplotlib',
        'seaborn'
    ]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])
            print(f"✅ Installed {package}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")

# Auto-install packages when running in Colab
try:
    import google.colab
    print("🔧 Setting up TradeThrust for Google Colab...")
    install_packages()
    print("✅ Setup complete!")
except ImportError:
    print("📱 Running locally - ensure requirements are installed")

# Import all required libraries
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import json
import warnings
from typing import Dict, List, Optional

warnings.filterwarnings('ignore')

class TradeThrustColab:
    """
    Simplified TradeThrust for Colab/Jupyter environments
    """
    
    def __init__(self):
        self.watchlist = []
        self.analysis_results = {}
        print("🚀 TradeThrust Colab Edition - Enhanced with Pivot Point Analysis!")
        print("🎯 Professional-Grade Entry Timing Now Available!")
        print("=" * 65)
    
    def analyze_stock(self, symbol: str, show_chart: bool = True) -> Dict:
        """
        Quick stock analysis with TradeThrust methodology
        Perfect for Colab notebooks
        """
        symbol = symbol.upper()
        print(f"\n🔍 ANALYZING: {symbol}")
        print("-" * 30)
        
        # Fetch data
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="2y")
            
            if data.empty:
                return {'error': f'No data found for {symbol}'}
                
            # Calculate indicators
            data = self._calculate_indicators(data)
            
        except Exception as e:
            return {'error': f'Error fetching data: {e}'}
        
        # TradeThrust Analysis
        analysis = self._tradethrust_analysis(data, symbol)
        
        # Store results
        self.analysis_results[symbol] = analysis
        
        # Show chart if requested
        if show_chart:
            self._create_chart(data, symbol)
        
        # Display recommendation
        self._display_recommendation(analysis)
        
        return analysis
    
    def _calculate_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate technical indicators"""
        df = data.copy()
        
        # Moving averages
        df['SMA_50'] = df['Close'].rolling(50).mean()
        df['SMA_150'] = df['Close'].rolling(150).mean()
        df['SMA_200'] = df['Close'].rolling(200).mean()
        df['EMA_21'] = df['Close'].ewm(span=21).mean()
        
        # 52-week levels
        df['52W_High'] = df['High'].rolling(252).max()
        df['52W_Low'] = df['Low'].rolling(252).min()
        
        # Volume
        df['Avg_Volume'] = df['Volume'].rolling(20).mean()
        
        return df
    
    def _tradethrust_analysis(self, data: pd.DataFrame, symbol: str) -> Dict:
        """Core TradeThrust analysis with advanced pivot point system"""
        latest = data.iloc[-1]
        
        # Get current values
        price = latest['Close']
        sma_50 = latest['SMA_50']
        sma_150 = latest['SMA_150']
        sma_200 = latest['SMA_200']
        high_52w = latest['52W_High']
        low_52w = latest['52W_Low']
        
        # Phase 1: TradeThrust Trend Template
        trend_criteria = {}
        
        # 1. Price above all SMAs
        trend_criteria['price_above_smas'] = price > sma_50 and price > sma_150 and price > sma_200
        
        # 2. SMA stacking order
        trend_criteria['sma_stacking'] = sma_50 > sma_150 > sma_200
        
        # 3. 200 SMA trending up
        sma_200_month_ago = data['SMA_200'].iloc[-22] if len(data) >= 22 else data['SMA_200'].iloc[0]
        trend_criteria['sma_200_up'] = latest['SMA_200'] > sma_200_month_ago
        
        # 4. Price 30%+ above 52W low
        pct_above_low = ((price - low_52w) / low_52w) * 100
        trend_criteria['above_52w_low'] = pct_above_low >= 30
        
        # 5. Price within 25% of 52W high
        pct_from_high = ((high_52w - price) / high_52w) * 100
        trend_criteria['near_52w_high'] = pct_from_high <= 25
        
        trend_score = sum(trend_criteria.values())
        trend_pass = trend_score >= 4
        
        # Phase 2: Pivot Point Analysis (NEW!)
        pivot_analysis = self._analyze_pivot_point_colab(data)
        
        # Phase 3: Volume Analysis
        recent_volume = latest['Volume']
        avg_volume = latest['Avg_Volume']
        volume_surge = recent_volume > avg_volume * 1.5
        
        # Enhanced Recommendation Logic
        if trend_pass and pivot_analysis['valid_breakout'] and volume_surge:
            recommendation = "🟢 STRONG BUY"
            action = "BUY NOW"
            confidence = "HIGH"
        elif trend_pass and pivot_analysis['valid_pivot'] and volume_surge:
            recommendation = "� WATCH - BREAKOUT PENDING"
            action = "MONITOR CLOSELY"
            confidence = "MEDIUM"
        elif trend_pass:
            recommendation = "🟡 WATCH"
            action = "MONITOR"
            confidence = "MEDIUM"
        else:
            recommendation = "🔴 AVOID"
            action = "WAIT"
            confidence = "LOW"
        
        # Enhanced Risk Management
        support_level = data.tail(20)['Low'].min()
        pivot_point = pivot_analysis.get('pivot_point', price)
        
        # Use pivot-based stop loss if available
        if pivot_analysis['valid_pivot']:
            stop_loss = max(pivot_point * 0.97, support_level * 0.98)  # 3% below pivot or 2% below support
        else:
            stop_loss = max(support_level * 0.98, price * 0.92)  # 2% below support or 8% max risk
        
        risk_pct = ((price - stop_loss) / price) * 100
        
        return {
            'symbol': symbol,
            'price': price,
            'recommendation': recommendation,
            'action': action,
            'confidence': confidence,
            'trend_score': f"{trend_score}/5",
            'pivot_score': pivot_analysis['score'],
            'overall_score': f"{trend_score + pivot_analysis['score_numeric']}/12",
            'trend_criteria': trend_criteria,
            'pivot_analysis': pivot_analysis,
            'stop_loss': stop_loss,
            'risk_percent': risk_pct,
            'support': support_level,
            'resistance': pivot_analysis.get('pivot_point', high_52w),
            'volume_surge': volume_surge,
            'metrics': {
                'sma_50': sma_50,
                'sma_150': sma_150,
                'sma_200': sma_200,
                'pct_above_low': pct_above_low,
                'pct_from_high': pct_from_high,
                'volume_ratio': recent_volume / avg_volume if avg_volume > 0 else 1,
                'pivot_point': pivot_analysis.get('pivot_point'),
                'base_quality': pivot_analysis['base_quality']
            }
        }
    
    def _analyze_pivot_point_colab(self, data: pd.DataFrame) -> Dict:
        """🎯 Advanced Pivot Point Analysis for Colab"""
        if len(data) < 75:  # Need 15 weeks minimum
            return {
                'valid_pivot': False,
                'valid_breakout': False,
                'pivot_point': None,
                'score': "0/7",
                'score_numeric': 0,
                'base_quality': 'Insufficient Data',
                'reason': 'Need at least 15 weeks of data'
            }
        
        # Analyze last 15 weeks for base pattern
        base_period = data.tail(75)
        current_price = data.iloc[-1]['Close']
        
        # Find contractions in the base
        contractions = self._find_colab_contractions(base_period)
        
        # Base validation criteria
        base_weeks = len(base_period) / 5
        criteria = {
            'base_duration': 5 <= base_weeks <= 15,
            'min_contractions': len(contractions) >= 2,
            'contractions_decreasing': self._contractions_decreasing_colab(contractions),
            'volume_contracts': self._volume_contracts_colab(contractions),
            'final_tight': self._final_tight_colab(contractions),
            'orderly_base': self._orderly_base_colab(contractions)
        }
        
        # Find pivot point
        pivot_point = None
        pivot_valid = False
        
        if contractions and criteria['min_contractions']:
            final_contraction = contractions[-1]
            pre_contraction_data = base_period.iloc[:final_contraction['start_idx']]
            
            if len(pre_contraction_data) > 0:
                pivot_point = pre_contraction_data['High'].max()
                criteria['within_5_percent'] = abs(current_price - pivot_point) / pivot_point <= 0.05
                pivot_valid = all(criteria.values())
        else:
            criteria['within_5_percent'] = False
        
        # Breakout validation (if pivot is valid)
        breakout_valid = False
        if pivot_valid and pivot_point is not None:
            breakout_valid = self._validate_breakout_colab(data, pivot_point)
        
        # Scoring
        score_numeric = sum(criteria.values())
        base_quality = "Excellent" if score_numeric >= 6 else "Good" if score_numeric >= 4 else "Poor"
        
        return {
            'valid_pivot': pivot_valid,
            'valid_breakout': breakout_valid,
            'pivot_point': pivot_point,
            'score': f"{score_numeric}/7",
            'score_numeric': score_numeric,
            'base_quality': base_quality,
            'criteria': criteria,
            'contractions_count': len(contractions),
            'base_weeks': base_weeks
        }
    
    def _find_colab_contractions(self, data: pd.DataFrame) -> List[Dict]:
        """Find price contractions for pivot analysis"""
        contractions = []
        if len(data) < 10:
            return contractions
        
        # Simple swing high/low detection
        highs = []
        lows = []
        window = 3
        
        for i in range(window, len(data) - window):
            # Swing high
            if all(data.iloc[i]['High'] >= data.iloc[j]['High'] for j in range(i-window, i+window+1) if j != i):
                highs.append({'index': i, 'price': data.iloc[i]['High']})
            
            # Swing low  
            if all(data.iloc[i]['Low'] <= data.iloc[j]['Low'] for j in range(i-window, i+window+1) if j != i):
                lows.append({'index': i, 'price': data.iloc[i]['Low']})
        
        # Match highs with subsequent lows
        for high in highs:
            subsequent_lows = [low for low in lows if low['index'] > high['index']]
            if subsequent_lows:
                lowest_low = min(subsequent_lows, key=lambda x: x['price'])
                decline_pct = ((high['price'] - lowest_low['price']) / high['price']) * 100
                
                # Calculate volume during contraction
                contraction_data = data.iloc[high['index']:lowest_low['index']+1]
                if len(contraction_data) > 0 and decline_pct >= 3:  # At least 3% pullback
                    avg_volume = contraction_data['Volume'].mean()
                    base_volume = data['Volume'].mean()
                    volume_ratio = avg_volume / base_volume if base_volume > 0 else 1
                    
                    contractions.append({
                        'start_idx': high['index'],
                        'end_idx': lowest_low['index'],
                        'decline_pct': decline_pct,
                        'volume_ratio': volume_ratio
                    })
        
        return contractions[-5:] if len(contractions) > 5 else contractions  # Keep latest 5
    
    def _contractions_decreasing_colab(self, contractions: List[Dict]) -> bool:
        """Check if contractions are getting smaller"""
        if len(contractions) < 2:
            return False
        for i in range(1, len(contractions)):
            if contractions[i]['decline_pct'] >= contractions[i-1]['decline_pct']:
                return False
        return True
    
    def _volume_contracts_colab(self, contractions: List[Dict]) -> bool:
        """Check if volume contracts during pullbacks"""
        return all(c['volume_ratio'] < 0.9 for c in contractions)
    
    def _final_tight_colab(self, contractions: List[Dict]) -> bool:
        """Check if final contraction is tight"""
        return len(contractions) > 0 and contractions[-1]['decline_pct'] < 15
    
    def _orderly_base_colab(self, contractions: List[Dict]) -> bool:
        """Check if base is orderly"""
        return all(c['decline_pct'] <= 25 for c in contractions)
    
    def _validate_breakout_colab(self, data: pd.DataFrame, pivot_point: float) -> bool:
        """Validate breakout above pivot point"""
        latest = data.iloc[-1]
        recent_50 = data.tail(50)
        
        current_price = latest['Close']
        daily_high = latest['High']
        daily_low = latest['Low']
        current_volume = latest['Volume']
        avg_volume_50 = recent_50['Volume'].mean()
        
        # Simplified breakout criteria for Colab
        criteria = {
            'breaks_pivot': current_price > pivot_point,
            'closes_near_high': (current_price / daily_high) >= 0.95,
            'no_failure': daily_low >= pivot_point * 0.98,
            'volume_surge': current_volume >= avg_volume_50 * 1.4
        }
        
        return sum(criteria.values()) >= 3  # Need 3 out of 4 criteria
    
    def _display_recommendation(self, analysis: Dict):
        """Display enhanced analysis results with pivot point analysis"""
        print(f"\n{analysis['recommendation']}")
        print(f"Action: {analysis['action']}")
        print(f"Confidence: {analysis['confidence']}")
        print(f"Overall Score: {analysis['overall_score']}")
        print(f"Current Price: ${analysis['price']:.2f}")
        print(f"Stop Loss: ${analysis['stop_loss']:.2f} ({analysis['risk_percent']:.1f}% risk)")
        
        # Pivot Point Information
        pivot_analysis = analysis['pivot_analysis']
        if pivot_analysis['pivot_point']:
            print(f"Pivot Point: ${pivot_analysis['pivot_point']:.2f}")
            print(f"Base Quality: {pivot_analysis['base_quality']}")
        
        print(f"\n📊 PHASE 1: TREND TEMPLATE ({analysis['trend_score']}):")
        criteria_names = {
            'price_above_smas': 'Price above SMAs',
            'sma_stacking': 'SMA stacking order',
            'sma_200_up': '200 SMA trending up',
            'above_52w_low': '30%+ above 52W low',
            'near_52w_high': 'Within 25% of 52W high'
        }
        
        for key, name in criteria_names.items():
            status = "✅" if analysis['trend_criteria'][key] else "❌"
            print(f"  {status} {name}")
        
        print(f"\n🎯 PHASE 2: PIVOT POINT ANALYSIS ({pivot_analysis['score']}):")
        print(f"  {'✅' if pivot_analysis['valid_pivot'] else '❌'} Valid Pivot Point")
        print(f"  {'✅' if pivot_analysis['valid_breakout'] else '❌'} Valid Breakout")
        print(f"  Base Duration: {pivot_analysis.get('base_weeks', 0):.1f} weeks")
        print(f"  Contractions: {pivot_analysis.get('contractions_count', 0)} found")
        
        print(f"\n📈 PHASE 3: VOLUME ANALYSIS:")
        if analysis['volume_surge']:
            print(f"  ✅ Volume surge detected ({analysis['metrics']['volume_ratio']:.1f}x avg)")
        else:
            print(f"  ❌ No volume surge ({analysis['metrics']['volume_ratio']:.1f}x avg)")
        
        # Action Items
        print(f"\n🎬 NEXT STEPS:")
        if analysis['action'] == 'BUY NOW':
            print(f"  1. ✅ Execute buy order at current price")
            print(f"  2. ✅ Set stop loss at ${analysis['stop_loss']:.2f}")
            print(f"  3. ✅ Monitor for profit targets (20%, 35%, 50%)")
        elif 'MONITOR' in analysis['action']:
            print(f"  1. 📊 Add to active watchlist")
            print(f"  2. 🚨 Watch for breakout confirmation")
            print(f"  3. 📈 Monitor volume for entry signal")
        else:
            print(f"  1. ❌ Avoid this stock for now")
            print(f"  2. ⏰ Re-evaluate in 2-4 weeks")
            print(f"  3. 🔍 Look for better opportunities")
    
    def _create_chart(self, data: pd.DataFrame, symbol: str):
        """Create clean chart for Colab"""
        # Use last 6 months for clarity
        chart_data = data.tail(120)
        
        # Set up the plot
        plt.figure(figsize=(14, 10))
        
        # Main price chart
        plt.subplot(2, 1, 1)
        plt.plot(chart_data.index, chart_data['Close'], 'k-', linewidth=2, label='Price')
        plt.plot(chart_data.index, chart_data['SMA_50'], 'b-', alpha=0.7, label='50 SMA')
        plt.plot(chart_data.index, chart_data['SMA_150'], 'orange', alpha=0.7, label='150 SMA')
        plt.plot(chart_data.index, chart_data['SMA_200'], 'r-', alpha=0.7, label='200 SMA')
        
        # 52-week levels and pivot point
        latest = chart_data.iloc[-1]
        plt.axhline(y=latest['52W_High'], color='green', linestyle='--', alpha=0.5, label='52W High')
        plt.axhline(y=latest['52W_Low'], color='red', linestyle='--', alpha=0.5, label='52W Low')
        
        # Add pivot point if available
        pivot_point = self.analysis_results.get(symbol, {}).get('pivot_analysis', {}).get('pivot_point')
        if pivot_point:
            plt.axhline(y=pivot_point, color='purple', linestyle='-', alpha=0.8, linewidth=2, label=f'Pivot Point ${pivot_point:.2f}')
        
        plt.title(f'{symbol} - TradeThrust Analysis', fontsize=16, fontweight='bold')
        plt.ylabel('Price ($)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Volume chart
        plt.subplot(2, 1, 2)
        colors = ['red' if vol > chart_data['Avg_Volume'].iloc[i] * 1.5 else 'lightblue' 
                 for i, vol in enumerate(chart_data['Volume'])]
        plt.bar(chart_data.index, chart_data['Volume'], color=colors, alpha=0.7)
        plt.plot(chart_data.index, chart_data['Avg_Volume'], 'r-', linewidth=2, label='Avg Volume')
        
        plt.ylabel('Volume')
        plt.xlabel('Date')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def add_to_watchlist(self, symbol: str):
        """Add stock to watchlist"""
        symbol = symbol.upper()
        if symbol not in self.watchlist:
            self.watchlist.append(symbol)
            print(f"✅ {symbol} added to watchlist")
        else:
            print(f"ℹ️ {symbol} already in watchlist")
    
    def scan_watchlist(self, show_charts: bool = False):
        """Scan watchlist for opportunities"""
        if not self.watchlist:
            print("📋 Watchlist is empty")
            return
        
        print(f"\n🔍 SCANNING WATCHLIST ({len(self.watchlist)} stocks)")
        print("=" * 50)
        
        buy_signals = []
        watch_list = []
        avoid_list = []
        
        for symbol in self.watchlist:
            try:
                result = self.analyze_stock(symbol, show_chart=show_charts)
                
                if result.get('action') == 'BUY NOW':
                    buy_signals.append(result)
                elif result.get('action') == 'MONITOR':
                    watch_list.append(result)
                else:
                    avoid_list.append(result)
                    
            except Exception as e:
                print(f"❌ Error analyzing {symbol}: {e}")
        
        # Summary
        print(f"\n🎯 WATCHLIST SUMMARY")
        print("-" * 30)
        
        if buy_signals:
            print(f"\n🟢 BUY OPPORTUNITIES ({len(buy_signals)}):")
            for stock in buy_signals:
                print(f"  • {stock['symbol']}: ${stock['price']:.2f} - {stock['score']}")
        
        if watch_list:
            print(f"\n🟡 MONITOR CLOSELY ({len(watch_list)}):")
            for stock in watch_list:
                print(f"  • {stock['symbol']}: ${stock['price']:.2f} - {stock['score']}")
        
        if avoid_list:
            print(f"\n🔴 AVOID FOR NOW ({len(avoid_list)}):")
            for stock in avoid_list:
                print(f"  • {stock['symbol']}: ${stock['price']:.2f} - {stock['score']}")
    
    def view_watchlist(self):
        """Display current watchlist"""
        if self.watchlist:
            print(f"\n📋 Current Watchlist ({len(self.watchlist)} stocks):")
            for i, symbol in enumerate(self.watchlist, 1):
                print(f"  {i}. {symbol}")
        else:
            print("📋 Watchlist is empty")
    
    def quick_screen(self, symbols: List[str]):
        """Quick screening of multiple stocks"""
        print(f"\n🔍 QUICK SCREEN ({len(symbols)} stocks)")
        print("=" * 40)
        
        results = []
        for symbol in symbols:
            try:
                result = self.analyze_stock(symbol, show_chart=False)
                results.append(result)
            except Exception as e:
                print(f"❌ Error with {symbol}: {e}")
        
        # Sort by score
        valid_results = [r for r in results if 'error' not in r]
        valid_results.sort(key=lambda x: int(x['score'].split('/')[0]), reverse=True)
        
        print(f"\n📊 SCREENING RESULTS (sorted by score):")
        for result in valid_results:
            print(f"  {result['recommendation']} {result['symbol']}: ${result['price']:.2f} - Score: {result['score']}")

# Initialize TradeThrust for Colab
print("🚀 TRADETHRUST COLAB EDITION - ENHANCED!")
print("🎯 NOW WITH ADVANCED PIVOT POINT ANALYSIS")
print("=" * 50)
print("Ready to analyze stocks with institutional-quality precision!")
print("\nQuick Start:")
print("1. tt = TradeThrustColab()")
print("2. tt.analyze_stock('AAPL')  # Complete analysis with pivot points")
print("3. tt.add_to_watchlist('AAPL')  # Add to watchlist") 
print("4. tt.scan_watchlist()  # Scan for opportunities")
print("\n✨ NEW: Advanced pivot point analysis for precise entry timing!")
print("📊 Professional 3-phase analysis: Trend + Pivot + Volume")
print("\n" + "=" * 50)

# Example usage functions for Colab users
def demo_tradethrust():
    """Demo function showing TradeThrust capabilities"""
    print("🎬 TRADETHRUST DEMO")
    print("=" * 30)
    
    tt = TradeThrustColab()
    
    # Demo stocks
    demo_stocks = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA']
    
    print(f"Analyzing demo stocks: {', '.join(demo_stocks)}")
    
    for stock in demo_stocks:
        tt.add_to_watchlist(stock)
    
    # Quick screen without charts for demo
    tt.scan_watchlist(show_charts=False)
    
    return tt

def analyze_single_stock(symbol: str):
    """Quick function to analyze a single stock"""
    tt = TradeThrustColab()
    return tt.analyze_stock(symbol)

# Make it easy for users to get started
def get_started():
    """Helper function to get users started quickly"""
    print("🚀 GETTING STARTED WITH TRADETHRUST - ENHANCED EDITION")
    print("🎯 NOW WITH ADVANCED PIVOT POINT ANALYSIS")
    print("=" * 55)
    print("\n1. Create TradeThrust instance:")
    print("   tt = TradeThrustColab()")
    print("\n2. Analyze any stock (with pivot points!):")
    print("   tt.analyze_stock('AAPL')")
    print("\n3. Build your watchlist:")
    print("   tt.add_to_watchlist('AAPL')")
    print("   tt.add_to_watchlist('MSFT')")
    print("\n4. Scan for opportunities:")
    print("   tt.scan_watchlist()")
    print("\n5. Quick screen multiple stocks:")
    print("   stocks = ['AAPL', 'MSFT', 'GOOGL', 'TSLA']")
    print("   tt.quick_screen(stocks)")
    print("\n✨ NEW FEATURES:")
    print("   • Advanced 7-criteria pivot point analysis")
    print("   • Professional 3-phase scoring system")
    print("   • Precise entry timing validation")
    print("   • Enhanced charts with pivot points")
    print("\n💡 Pro tip: Set show_chart=False for faster analysis")
    print("=" * 55)

# Auto-run demo if this is the main execution
if __name__ == "__main__":
    get_started()
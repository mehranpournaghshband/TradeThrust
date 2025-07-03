#!/usr/bin/env python3
"""
TradeThrust for Google Colab
===========================

Google Colab optimized version of TradeThrust - Professional Stock Trading System
Run this complete notebook to start using the TradeThrust system immediately.

Instructions:
1. Run this cell to install dependencies and set up TradeThrust
2. Use the provided functions to analyze stocks
3. Add stocks to watchlist and monitor for opportunities

Based on Mark Minervini's proven trading methodology.
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
        print("🚀 TradeThrust Colab Edition - Ready for Analysis!")
        print("=" * 50)
    
    def analyze_stock(self, symbol: str, show_chart: bool = True) -> Dict:
        """
        Quick stock analysis with Minervini methodology
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
        
        # Minervini Analysis
        analysis = self._minervini_analysis(data, symbol)
        
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
    
    def _minervini_analysis(self, data: pd.DataFrame, symbol: str) -> Dict:
        """Core Minervini trend template analysis"""
        latest = data.iloc[-1]
        
        # Get current values
        price = latest['Close']
        sma_50 = latest['SMA_50']
        sma_150 = latest['SMA_150']
        sma_200 = latest['SMA_200']
        high_52w = latest['52W_High']
        low_52w = latest['52W_Low']
        
        # Minervini Criteria Checks
        criteria = {}
        
        # 1. Price above all SMAs
        criteria['price_above_smas'] = price > sma_50 and price > sma_150 and price > sma_200
        
        # 2. SMA stacking order
        criteria['sma_stacking'] = sma_50 > sma_150 > sma_200
        
        # 3. 200 SMA trending up
        sma_200_month_ago = data['SMA_200'].iloc[-22] if len(data) >= 22 else data['SMA_200'].iloc[0]
        criteria['sma_200_up'] = latest['SMA_200'] > sma_200_month_ago
        
        # 4. Price 30%+ above 52W low
        pct_above_low = ((price - low_52w) / low_52w) * 100
        criteria['above_52w_low'] = pct_above_low >= 30
        
        # 5. Price within 25% of 52W high
        pct_from_high = ((high_52w - price) / high_52w) * 100
        criteria['near_52w_high'] = pct_from_high <= 25
        
        # Volume breakout check
        recent_volume = latest['Volume']
        avg_volume = latest['Avg_Volume']
        volume_surge = recent_volume > avg_volume * 1.5
        
        # Overall score
        score = sum(criteria.values())
        total_criteria = len(criteria)
        
        # Recommendation logic
        if score >= 4 and volume_surge:
            recommendation = "🟢 STRONG BUY"
            action = "BUY NOW"
        elif score >= 3:
            recommendation = "🟡 WATCH"
            action = "MONITOR"
        else:
            recommendation = "🔴 AVOID"
            action = "WAIT"
        
        # Risk management
        support_level = data.tail(20)['Low'].min()
        stop_loss = max(support_level * 0.98, price * 0.92)  # 2% below support or 8% max risk
        risk_pct = ((price - stop_loss) / price) * 100
        
        return {
            'symbol': symbol,
            'price': price,
            'recommendation': recommendation,
            'action': action,
            'score': f"{score}/{total_criteria}",
            'criteria': criteria,
            'stop_loss': stop_loss,
            'risk_percent': risk_pct,
            'support': support_level,
            'resistance': high_52w,
            'volume_surge': volume_surge,
            'metrics': {
                'sma_50': sma_50,
                'sma_150': sma_150,
                'sma_200': sma_200,
                'pct_above_low': pct_above_low,
                'pct_from_high': pct_from_high,
                'volume_ratio': recent_volume / avg_volume if avg_volume > 0 else 1
            }
        }
    
    def _display_recommendation(self, analysis: Dict):
        """Display analysis results in a clean format"""
        print(f"\n{analysis['recommendation']}")
        print(f"Action: {analysis['action']}")
        print(f"Score: {analysis['score']}")
        print(f"Current Price: ${analysis['price']:.2f}")
        print(f"Stop Loss: ${analysis['stop_loss']:.2f} ({analysis['risk_percent']:.1f}% risk)")
        
        print(f"\n📊 Criteria Check:")
        criteria_names = {
            'price_above_smas': 'Price above SMAs',
            'sma_stacking': 'SMA stacking order',
            'sma_200_up': '200 SMA trending up',
            'above_52w_low': '30%+ above 52W low',
            'near_52w_high': 'Within 25% of 52W high'
        }
        
        for key, name in criteria_names.items():
            status = "✅" if analysis['criteria'][key] else "❌"
            print(f"  {status} {name}")
        
        if analysis['volume_surge']:
            print(f"  ✅ Volume surge detected ({analysis['metrics']['volume_ratio']:.1f}x avg)")
        else:
            print(f"  ❌ No volume surge ({analysis['metrics']['volume_ratio']:.1f}x avg)")
    
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
        
        # 52-week levels
        latest = chart_data.iloc[-1]
        plt.axhline(y=latest['52W_High'], color='green', linestyle='--', alpha=0.5, label='52W High')
        plt.axhline(y=latest['52W_Low'], color='red', linestyle='--', alpha=0.5, label='52W Low')
        
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
print("🚀 TRADETHRUST COLAB EDITION")
print("=" * 40)
print("Ready to analyze stocks using Minervini's methodology!")
print("\nQuick Start:")
print("1. tt = TradeThrustColab()")
print("2. tt.analyze_stock('AAPL')  # Analyze Apple")
print("3. tt.add_to_watchlist('AAPL')  # Add to watchlist") 
print("4. tt.scan_watchlist()  # Scan for opportunities")
print("\n" + "=" * 40)

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
    print("🚀 GETTING STARTED WITH TRADETHRUST")
    print("=" * 40)
    print("\n1. Create TradeThrust instance:")
    print("   tt = TradeThrustColab()")
    print("\n2. Analyze any stock:")
    print("   tt.analyze_stock('AAPL')")
    print("\n3. Build your watchlist:")
    print("   tt.add_to_watchlist('AAPL')")
    print("   tt.add_to_watchlist('MSFT')")
    print("\n4. Scan for opportunities:")
    print("   tt.scan_watchlist()")
    print("\n5. Quick screen multiple stocks:")
    print("   stocks = ['AAPL', 'MSFT', 'GOOGL', 'TSLA']")
    print("   tt.quick_screen(stocks)")
    print("\n💡 Pro tip: Set show_chart=False for faster analysis")
    print("=" * 40)

# Auto-run demo if this is the main execution
if __name__ == "__main__":
    get_started()
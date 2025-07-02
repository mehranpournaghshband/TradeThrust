# ==========================================
# CELL 1: INSTALLATION
# ==========================================
# Copy this into a CODE CELL in Google Colab

# Install required packages
!pip install yfinance pandas numpy matplotlib

print("✅ All packages installed successfully!")

# ==========================================
# CELL 2: MAIN ANALYZER CODE  
# ==========================================
# Copy this into a CODE CELL in Google Colab

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
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
        latest = self.data.iloc[-1]
        
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
        if len(self.data) < lookback_days:
            return {'vcp_detected': False, 'reason': 'Insufficient data for VCP analysis'}
        
        recent_data = self.data.tail(lookback_days)
        results = {}
        
        # Simplified VCP analysis for Colab
        # Check if recent volatility is decreasing
        recent_range = recent_data['Price_Range'].tail(10).mean()
        longer_range = recent_data['Price_Range'].head(20).mean()
        
        # Volume analysis
        recent_volume = recent_data['Volume'].tail(10).mean()
        avg_volume = recent_data['Volume'].mean()
        
        results['contractions_decreasing'] = {
            'pass': recent_range < longer_range * 0.8,
            'details': f"Recent range: ${recent_range:.2f} vs Earlier: ${longer_range:.2f}"
        }
        
        results['volume_declining'] = {
            'pass': recent_volume < avg_volume * 0.9,
            'details': f"Recent volume: {recent_volume:,.0f} vs Average: {avg_volume:,.0f}"
        }
        
        results['price_tightening'] = {
            'pass': recent_range < longer_range * 0.7,
            'details': f"Price tightening: {recent_range < longer_range * 0.7}"
        }
        
        return results
    
    def check_breakout_signal(self):
        """Check for breakout entry signal"""
        if len(self.data) < 20:
            return {'breakout_signal': False, 'reason': 'Insufficient data'}
        
        latest = self.data.iloc[-1]
        recent_20 = self.data.tail(20)
        
        # Find resistance level (recent highs)
        resistance = recent_20['High'].max()
        avg_volume = recent_20['Volume'].mean()
        
        # Check if price broke above resistance
        price_breakout = latest['Close'] > resistance * 0.99  # Small buffer
        
        # Check for volume surge (50%+ above average)
        volume_surge = latest['Volume'] > avg_volume * 1.2  # Relaxed for demo
        
        return {
            'breakout_signal': {
                'pass': price_breakout and volume_surge,
                'details': f"Resistance: ${resistance:.2f} | Current: ${latest['Close']:.2f} | Volume: {latest['Volume']:,.0f} (avg: {avg_volume:,.0f})"
            }
        }
    
    def analyze_stock(self):
        """Perform complete Mehran analysis"""
        if not self.fetch_data():
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
    
    def create_chart(self):
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
        
        plt.tight_layout()
        plt.show()
        
        print(f"📊 Chart generated for {self.symbol}")

print("✅ Mehran Analyzer class loaded successfully!")

# ==========================================
# CELL 3: ANALYZE SINGLE STOCK
# ==========================================
# Copy this into a CODE CELL in Google Colab

# 🎯 ANALYZE A SINGLE STOCK
# Change the symbol below to any stock you want to analyze

STOCK_SYMBOL = "AAPL"  # Change this to any stock symbol (MSFT, GOOGL, TSLA, etc.)

print(f"🔍 Analyzing {STOCK_SYMBOL}...")
print("This may take a moment to fetch real-time data...\n")

# Create analyzer and run analysis
analyzer = MehranAnalyzer(STOCK_SYMBOL)
result = analyzer.analyze_stock()

if result:
    print("\n📊 Generating chart...")
    analyzer.create_chart()
else:
    print("❌ Analysis failed. Please check the stock symbol.")

# ==========================================
# CELL 4: BATCH ANALYSIS (OPTIONAL)
# ==========================================
# Copy this into a CODE CELL in Google Colab

# 📊 ANALYZE MULTIPLE STOCKS AT ONCE
# Add or remove stock symbols from this list

stocks_to_analyze = ['AAPL', 'MSFT', 'GOOGL', 'NVDA', 'TSLA']

print("🚀 BATCH STOCK ANALYSIS")
print("=" * 50)
print(f"Analyzing {len(stocks_to_analyze)} stocks...\n")

results = []
buy_candidates = []
avoid_stocks = []

for stock in stocks_to_analyze:
    print(f"🔍 Analyzing {stock}...")
    
    analyzer = MehranAnalyzer(stock)
    result = analyzer.analyze_stock()
    
    if result:
        results.append(result)
        if result['recommendation'] == 'BUY':
            buy_candidates.append(result)
        else:
            avoid_stocks.append(result)
    
    print("\n" + "="*80 + "\n")

# Summary Report
print("📊 BATCH ANALYSIS SUMMARY")
print("=" * 40)

print(f"\n🟢 BUY CANDIDATES ({len(buy_candidates)}):")
for stock in buy_candidates:
    print(f"  • {stock['symbol']}: ${stock['current_price']:.2f} "
          f"(Risk: {stock['risk_percent']:.1f}%, Stop: ${stock['stop_loss']:.2f})")

print(f"\n🔴 AVOID/HOLD ({len(avoid_stocks)}):")
for stock in avoid_stocks:
    print(f"  • {stock['symbol']}: ${stock['current_price']:.2f} "
          f"(Phase 1: {stock['phase1_score']}, Phase 2: {stock['phase2_score']})")

print(f"\n📈 Analysis completed for {len(results)} stocks!")
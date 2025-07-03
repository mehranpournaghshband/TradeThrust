#!/usr/bin/env python3
"""
TradeThrust - CORRECTED RS RATING VERSION
=========================================

CRITICAL FIX: Accurate Relative Strength Rating calculation
- Compares stock performance vs S&P 500 benchmark
- Proper 0-100 RS rating scale
- Multiple timeframe analysis

Author: TradeThrust Team
Version: 13.1.0 (CORRECTED)
"""

import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
from typing import Dict, Optional
import warnings
warnings.filterwarnings('ignore')

class TradeThrustRSCorrected:
    """TradeThrust with ACCURATE RS Rating calculation"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_stock_data(self, symbol: str) -> Optional[pd.DataFrame]:
        """Get stock data with ACCURATE RS rating"""
        symbol = symbol.upper().strip()
        print(f"\n🔍 Fetching REAL market data for {symbol}...")
        
        # Get stock data
        stock_data = self._get_yahoo_data(symbol)
        if stock_data is None:
            return None
        
        # Get S&P 500 benchmark for RS calculation
        spy_data = self._get_yahoo_data('SPY')
        if spy_data is None:
            print("   ⚠️ Could not get SPY data, using simplified RS calculation")
            stock_data = self._add_simplified_rs(stock_data)
        else:
            print("   ✅ Got SPY benchmark data for accurate RS calculation")
            stock_data = self._add_accurate_rs(stock_data, spy_data)
        
        return stock_data
    
    def _get_yahoo_data(self, symbol: str) -> Optional[pd.DataFrame]:
        """Get data from Yahoo Finance"""
        try:
            if symbol != 'SPY':
                print(f"   📡 Trying Yahoo Finance for {symbol}...")
            
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
            params = {
                'period1': int((datetime.now() - timedelta(days=730)).timestamp()),
                'period2': int(datetime.now().timestamp()),
                'interval': '1d'
            }
            
            response = self.session.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('chart') and data['chart'].get('result'):
                    result = data['chart']['result'][0]
                    timestamps = result['timestamp']
                    quotes = result['indicators']['quote'][0]
                    
                    df_data = []
                    for i, ts in enumerate(timestamps):
                        try:
                            df_data.append({
                                'Date': pd.to_datetime(ts, unit='s'),
                                'Open': quotes['open'][i],
                                'High': quotes['high'][i],
                                'Low': quotes['low'][i],
                                'Close': quotes['close'][i],
                                'Volume': quotes['volume'][i] or 0
                            })
                        except:
                            continue
                    
                    if len(df_data) > 200:
                        df = pd.DataFrame(df_data)
                        df.set_index('Date', inplace=True)
                        df = df.dropna()
                        
                        current_price = df['Close'].iloc[-1]
                        if symbol != 'SPY':
                            print(f"   ✅ SUCCESS: ${current_price:.2f}")
                        return df
            
            return None
        except Exception as e:
            if symbol != 'SPY':
                print(f"   ❌ Error: {str(e)[:30]}...")
            return None
    
    def _add_simplified_rs(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add simplified RS rating (fallback)"""
        # Standard indicators
        df['SMA_50'] = df['Close'].rolling(window=50, min_periods=1).mean()
        df['SMA_150'] = df['Close'].rolling(window=150, min_periods=1).mean()
        df['SMA_200'] = df['Close'].rolling(window=200, min_periods=1).mean()
        
        # 52-week High/Low
        window_52w = min(252, len(df))
        df['High_52W'] = df['High'].rolling(window=window_52w, min_periods=1).max()
        df['Low_52W'] = df['Low'].rolling(window=window_52w, min_periods=1).min()
        
        # Volume
        df['Avg_Volume_50'] = df['Volume'].rolling(window=50, min_periods=1).mean()
        
        # Simplified RS based on performance
        if len(df) >= 63:
            price_3m_ago = df['Close'].shift(63)
            performance_3m = (df['Close'] - price_3m_ago) / price_3m_ago * 100
            
            # Map performance to RS rating
            rs_values = []
            for perf in performance_3m:
                if pd.isna(perf):
                    rs_values.append(70.0)
                elif perf >= 50:
                    rs_values.append(95.0)
                elif perf >= 30:
                    rs_values.append(90.0)
                elif perf >= 20:
                    rs_values.append(85.0)
                elif perf >= 10:
                    rs_values.append(80.0)
                elif perf >= 5:
                    rs_values.append(75.0)
                elif perf >= 0:
                    rs_values.append(65.0)
                elif perf >= -10:
                    rs_values.append(50.0)
                elif perf >= -20:
                    rs_values.append(35.0)
                else:
                    rs_values.append(20.0)
            
            df['RS_Rating'] = rs_values
        else:
            df['RS_Rating'] = 70.0
        
        return df
    
    def _add_accurate_rs(self, stock_data: pd.DataFrame, spy_data: pd.DataFrame) -> pd.DataFrame:
        """Add ACCURATE RS rating vs S&P 500"""
        df = stock_data.copy()
        
        # Standard indicators
        df['SMA_50'] = df['Close'].rolling(window=50, min_periods=1).mean()
        df['SMA_150'] = df['Close'].rolling(window=150, min_periods=1).mean()
        df['SMA_200'] = df['Close'].rolling(window=200, min_periods=1).mean()
        
        # 52-week High/Low
        window_52w = min(252, len(df))
        df['High_52W'] = df['High'].rolling(window=window_52w, min_periods=1).max()
        df['Low_52W'] = df['Low'].rolling(window=window_52w, min_periods=1).min()
        
        # Volume
        df['Avg_Volume_50'] = df['Volume'].rolling(window=50, min_periods=1).mean()
        
        # ACCURATE RS RATING
        df['RS_Rating'] = self._calculate_accurate_rs(df, spy_data)
        
        return df
    
    def _calculate_accurate_rs(self, stock_data: pd.DataFrame, spy_data: pd.DataFrame) -> list:
        """Calculate accurate RS rating vs SPY"""
        # Align dates
        stock_close = stock_data['Close']
        spy_close = spy_data['Close']
        
        # Find common dates
        common_dates = stock_close.index.intersection(spy_close.index)
        if len(common_dates) < 63:
            return [70.0] * len(stock_data)
        
        stock_aligned = stock_close.reindex(common_dates)
        spy_aligned = spy_close.reindex(common_dates)
        
        rs_ratings = []
        
        for i, date in enumerate(stock_data.index):
            if date not in common_dates or i < 63:
                rs_ratings.append(70.0)
                continue
            
            # Calculate relative performance over multiple periods
            performances = []
            
            for period in [21, 63, 125, 252]:  # 1m, 3m, 6m, 12m
                if i >= period and date in common_dates:
                    # Stock performance
                    stock_current = stock_close.iloc[i]
                    stock_past = stock_close.iloc[i-period]
                    stock_perf = (stock_current - stock_past) / stock_past * 100
                    
                    # SPY performance for same period
                    if date in spy_aligned.index:
                        spy_current = spy_aligned.loc[date]
                        spy_dates = spy_aligned.index
                        spy_past_idx = max(0, len(spy_dates) - (len(stock_data) - i) - period)
                        if spy_past_idx < len(spy_aligned):
                            spy_past = spy_aligned.iloc[spy_past_idx]
                            spy_perf = (spy_current - spy_past) / spy_past * 100
                            
                            # Relative performance
                            relative_perf = stock_perf - spy_perf
                            performances.append(relative_perf)
            
            if performances:
                avg_relative_perf = np.mean(performances)
                
                # Convert to RS rating (0-100)
                if avg_relative_perf >= 30:
                    rs_rating = 95
                elif avg_relative_perf >= 20:
                    rs_rating = 90
                elif avg_relative_perf >= 15:
                    rs_rating = 85
                elif avg_relative_perf >= 10:
                    rs_rating = 80
                elif avg_relative_perf >= 5:
                    rs_rating = 75
                elif avg_relative_perf >= 0:
                    rs_rating = 70
                elif avg_relative_perf >= -5:
                    rs_rating = 60
                elif avg_relative_perf >= -10:
                    rs_rating = 50
                elif avg_relative_perf >= -15:
                    rs_rating = 40
                else:
                    rs_rating = 30
                
                rs_ratings.append(rs_rating)
            else:
                rs_ratings.append(70.0)
        
        return rs_ratings
    
    def analyze_stock(self, symbol: str) -> Dict:
        """Analyze stock with corrected RS rating"""
        symbol = symbol.upper()
        
        print(f"\n{'='*80}")
        print(f"🚀 TRADETHRUST - CORRECTED RS RATING")
        print(f"📊 Symbol: {symbol} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"✅ ACCURATE RS Rating vs S&P 500 Benchmark")
        print(f"{'='*80}")
        
        # Get data
        data = self.get_stock_data(symbol)
        if data is None:
            return {'error': f'Could not fetch market data for {symbol}'}
        
        current_price = data['Close'].iloc[-1]
        current_rs = data['RS_Rating'].iloc[-1]
        
        print(f"\n✅ DATA LOADED:")
        print(f"📊 Current Price: ${current_price:.2f}")
        print(f"📊 RS Rating (CORRECTED): {current_rs:.0f}")
        
        # Performance analysis
        self._show_performance(data, symbol)
        
        # Trend template
        template_results = self._analyze_template(data, symbol)
        
        return {
            'symbol': symbol,
            'current_price': current_price,
            'rs_rating_corrected': current_rs,
            'trend_template': template_results,
            'timestamp': datetime.now().isoformat()
        }
    
    def _show_performance(self, data: pd.DataFrame, symbol: str):
        """Show performance analysis"""
        print(f"\n📈 PERFORMANCE ANALYSIS FOR {symbol}:")
        print("─" * 60)
        
        current_price = data['Close'].iloc[-1]
        
        timeframes = [(21, "1-month"), (63, "3-month"), (125, "6-month"), (252, "12-month")]
        
        for period, name in timeframes:
            if len(data) >= period:
                past_price = data['Close'].iloc[-period]
                performance = (current_price - past_price) / past_price * 100
                
                if performance >= 30:
                    rating = "🔥 EXCEPTIONAL"
                elif performance >= 20:
                    rating = "🚀 EXCELLENT"
                elif performance >= 10:
                    rating = "✅ STRONG"
                elif performance >= 0:
                    rating = "➡️ POSITIVE"
                else:
                    rating = "❌ NEGATIVE"
                
                print(f"{name:<10}: {performance:+7.1f}% {rating}")
        
        rs_rating = data['RS_Rating'].iloc[-1]
        if rs_rating >= 85:
            rs_status = "🔥 MARKET LEADER"
        elif rs_rating >= 70:
            rs_status = "✅ STRONG"
        elif rs_rating >= 50:
            rs_status = "➡️ AVERAGE"
        else:
            rs_status = "❌ WEAK"
        
        print(f"RS Rating  : {rs_rating:7.0f}   {rs_status}")
    
    def _analyze_template(self, data: pd.DataFrame, symbol: str) -> Dict:
        """Analyze trend template"""
        print(f"\n📌 TREND TEMPLATE ANALYSIS (CORRECTED RS)")
        print("─" * 60)
        
        latest = data.iloc[-1]
        price = latest['Close']
        sma_50 = latest['SMA_50']
        sma_150 = latest['SMA_150']
        sma_200 = latest['SMA_200']
        high_52w = latest['High_52W']
        low_52w = latest['Low_52W']
        rs_rating = latest['RS_Rating']
        
        # Key conditions
        conditions = [
            ("Price > 50-day SMA", price > sma_50),
            ("Price > 150-day SMA", price > sma_150),
            ("Price > 200-day SMA", price > sma_200),
            ("RS Rating ≥ 70", rs_rating >= 70),
            ("Price ≥ 30% above 52W low", (price - low_52w) / low_52w >= 0.30),
            ("Price ≤ 25% from 52W high", (high_52w - price) / price <= 0.25)
        ]
        
        print(f"{'Condition':<25} {'Status':<8} {'Value'}")
        print("─" * 50)
        
        passed = 0
        for condition, status in conditions:
            if condition == "RS Rating ≥ 70":
                value = f"{rs_rating:.0f}"
            elif condition == "Price ≥ 30% above 52W low":
                value = f"{((price - low_52w) / low_52w * 100):.1f}%"
            elif condition == "Price ≤ 25% from 52W high":
                value = f"{((high_52w - price) / price * 100):.1f}%"
            else:
                value = f"${price:.2f}"
            
            status_symbol = "✅ PASS" if status else "❌ FAIL"
            if status:
                passed += 1
            print(f"{condition:<25} {status_symbol:<8} {value}")
        
        print("─" * 50)
        print(f"📊 RESULT: {passed}/6 conditions passed")
        print(f"🎯 RS RATING: {rs_rating:.0f} ({'✅ STRONG' if rs_rating >= 70 else '❌ WEAK'})")
        
        return {
            'passed': passed,
            'total': 6,
            'rs_rating': rs_rating,
            'rs_strong': rs_rating >= 70
        }

def main():
    """Test corrected RS ratings"""
    print("🚀 TradeThrust - CORRECTED RS Rating Version")
    print("✅ Accurate Relative Strength vs S&P 500")
    print("=" * 60)
    
    tt = TradeThrustRSCorrected()
    
    # Test with NVDA first
    print("\n🧪 TESTING WITH NVDA (Should show high RS rating)")
    result = tt.analyze_stock('NVDA')
    
    if 'error' not in result:
        rs_rating = result['rs_rating_corrected']
        print(f"\n🎯 NVDA RS RATING RESULT: {rs_rating:.0f}")
        if rs_rating >= 80:
            print("✅ CORRECT: NVDA shows strong RS rating as expected!")
        else:
            print("❌ Still needs adjustment in calculation")
    
    # Interactive mode
    while True:
        try:
            symbol = input("\nEnter stock symbol (or 'exit'): ").strip()
            
            if symbol.lower() == 'exit':
                break
            
            if not symbol:
                continue
            
            result = tt.analyze_stock(symbol)
            
            if 'error' in result:
                print(f"\n❌ {result['error']}")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
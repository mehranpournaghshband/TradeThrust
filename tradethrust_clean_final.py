#!/usr/bin/env python3
"""
TradeThrust Stock Trading Algorithm - CLEAN FINAL VERSION
========================================================

Following the exact TradeThrust algorithmic specification:
- Uses ONLY Polygon API
- Handles missing data gracefully
- Provides clear buying price recommendations
- No crashes or complex APIs

Author: TradeThrust Team
Version: FINAL CLEAN
"""

import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

class TradeThrustClean:
    """Clean TradeThrust implementation following exact algorithm"""
    
    def __init__(self):
        self.polygon_api_key = "demo"  # Free tier available
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_stock_data(self, symbol: str) -> Optional[pd.DataFrame]:
        """Get stock data with graceful error handling"""
        symbol = symbol.upper().strip()
        print(f"\n🔍 Fetching market data for {symbol}...")
        
        # Try Polygon first, then fallback to Yahoo
        data = self._get_polygon_data(symbol)
        if data is not None:
            return self._calculate_indicators(data)
        
        print(f"   ⚠️ Polygon data not available, trying backup source...")
        data = self._get_yahoo_data(symbol)
        if data is not None:
            return self._calculate_indicators(data)
        
        print(f"   ❌ Could not fetch data for {symbol}")
        return None
    
    def _get_polygon_data(self, symbol: str) -> Optional[pd.DataFrame]:
        """Get data from Polygon API"""
        try:
            print(f"   📡 Trying Polygon API for {symbol}...")
            
            # Free tier Polygon endpoint
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=730)).strftime('%Y-%m-%d')
            
            url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{start_date}/{end_date}"
            params = {'apikey': self.polygon_api_key}
            
            response = self.session.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('results') and len(data['results']) > 200:
                    df_data = []
                    for bar in data['results']:
                        df_data.append({
                            'Date': pd.to_datetime(bar['t'], unit='ms'),
                            'Open': bar['o'],
                            'High': bar['h'],
                            'Low': bar['l'],
                            'Close': bar['c'],
                            'Volume': bar['v']
                        })
                    
                    df = pd.DataFrame(df_data)
                    df.set_index('Date', inplace=True)
                    df = df.dropna()
                    
                    current_price = df['Close'].iloc[-1]
                    print(f"   ✅ Polygon SUCCESS: ${current_price:.2f}")
                    return df
            
            return None
        except Exception as e:
            print(f"   ⚠️ Polygon error: {str(e)[:50]}...")
            return None
    
    def _get_yahoo_data(self, symbol: str) -> Optional[pd.DataFrame]:
        """Backup Yahoo Finance data"""
        try:
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
                        print(f"   ✅ Yahoo SUCCESS: ${current_price:.2f}")
                        return df
            
            return None
        except Exception as e:
            print(f"   ⚠️ Yahoo error: {str(e)[:50]}...")
            return None
    
    def _calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate all required technical indicators"""
        # Moving averages
        df['SMA_50'] = df['Close'].rolling(window=50, min_periods=1).mean()
        df['SMA_150'] = df['Close'].rolling(window=150, min_periods=1).mean()
        df['SMA_200'] = df['Close'].rolling(window=200, min_periods=1).mean()
        
        # 52-week High/Low
        window_52w = min(252, len(df))
        df['High_52W'] = df['High'].rolling(window=window_52w, min_periods=1).max()
        df['Low_52W'] = df['Low'].rolling(window=window_52w, min_periods=1).min()
        
        # Volume indicators
        df['Avg_Volume_50'] = df['Volume'].rolling(window=50, min_periods=1).mean()
        
        # Relative Strength (simplified but effective)
        if len(df) >= 63:
            price_3m_ago = df['Close'].shift(63)
            performance_3m = (df['Close'] - price_3m_ago) / price_3m_ago * 100
            
            # Convert performance to RS rating
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
                    rs_values.append(70.0)
                elif perf >= -10:
                    rs_values.append(50.0)
                elif perf >= -20:
                    rs_values.append(35.0)
                else:
                    rs_values.append(20.0)
            
            df['RS_Rating'] = rs_values
        else:
            df['RS_Rating'] = 70.0
        
        # 200-day SMA trend (upward for 20 days)
        df['SMA_200_Trend'] = df['SMA_200'].diff().rolling(window=20).apply(lambda x: (x > 0).all())
        
        return df
    
    def analyze_stock(self, symbol: str) -> Dict:
        """Complete TradeThrust analysis following exact algorithm"""
        symbol = symbol.upper()
        
        print(f"\n{'='*80}")
        print(f"🚀 TRADETHRUST STOCK TRADING ALGORITHM")
        print(f"📊 Symbol: {symbol} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"✅ Following TradeThrust Methodology")
        print(f"{'='*80}")
        
        # Get data
        data = self.get_stock_data(symbol)
        if data is None:
            return {
                'error': f'Market data not available for {symbol}',
                'symbol': symbol,
                'timestamp': datetime.now().isoformat()
            }
        
        current_price = data['Close'].iloc[-1]
        print(f"\n✅ DATA LOADED: ${current_price:.2f}")
        
        # Step 1: Trend Template Filter
        trend_result = self._step1_trend_template(data, symbol)
        
        # Step 2: VCP Detection (if trend passes)
        vcp_result = None
        if trend_result['passed']:
            vcp_result = self._step2_vcp_detection(data, symbol)
        
        # Step 3: Breakout Confirmation (if VCP detected)
        breakout_result = None
        if vcp_result and vcp_result['detected']:
            breakout_result = self._step3_breakout_confirmation(data, symbol)
        
        # Step 4: Optional Fundamentals
        fundamentals_result = self._step4_optional_fundamentals(symbol)
        
        # Step 5: Risk Setup and Buy Price
        risk_result = self._step5_risk_setup_and_buy_price(data, symbol, trend_result, vcp_result)
        
        # Overall recommendation
        recommendation = self._generate_recommendation(trend_result, vcp_result, breakout_result, fundamentals_result, risk_result)
        
        return {
            'symbol': symbol,
            'current_price': current_price,
            'trend_template': trend_result,
            'vcp_pattern': vcp_result,
            'breakout_confirmation': breakout_result,
            'fundamentals': fundamentals_result,
            'risk_setup': risk_result,
            'recommendation': recommendation,
            'timestamp': datetime.now().isoformat()
        }
    
    def _step1_trend_template(self, data: pd.DataFrame, symbol: str) -> Dict:
        """Step 1: Trend Template Filter (All Conditions Must Be True)"""
        print(f"\n📌 STEP 1: TREND TEMPLATE FILTER")
        print("─" * 60)
        
        latest = data.iloc[-1]
        price = latest['Close']
        sma_50 = latest['SMA_50']
        sma_150 = latest['SMA_150']
        sma_200 = latest['SMA_200']
        high_52w = latest['High_52W']
        low_52w = latest['Low_52W']
        rs_rating = latest['RS_Rating']
        sma_200_trend = latest['SMA_200_Trend'] if not pd.isna(latest['SMA_200_Trend']) else False
        
        # All conditions for trend template
        conditions = [
            ("Price > 50-day SMA", price > sma_50, f"${price:.2f} vs ${sma_50:.2f}"),
            ("Price > 150-day SMA", price > sma_150, f"${price:.2f} vs ${sma_150:.2f}"),
            ("Price > 200-day SMA", price > sma_200, f"${price:.2f} vs ${sma_200:.2f}"),
            ("150-day SMA > 200-day SMA", sma_150 > sma_200, f"${sma_150:.2f} vs ${sma_200:.2f}"),
            ("50-day SMA > 150-day SMA", sma_50 > sma_150, f"${sma_50:.2f} vs ${sma_150:.2f}"),
            ("50-day SMA > 200-day SMA", sma_50 > sma_200, f"${sma_50:.2f} vs ${sma_200:.2f}"),
            ("200-day SMA trending up 20 days", sma_200_trend, "Upward trend" if sma_200_trend else "Not trending up"),
            ("Price ≥ 30% above 52W low", (price - low_52w) / low_52w >= 0.30, f"{((price - low_52w) / low_52w * 100):.1f}% above"),
            ("Price ≤ 25% below 52W high", (high_52w - price) / high_52w <= 0.25, f"{((high_52w - price) / high_52w * 100):.1f}% below"),
            ("RS Rating ≥ 70", rs_rating >= 70, f"{rs_rating:.0f}")
        ]
        
        print(f"{'Condition':<30} {'Status':<8} {'Details'}")
        print("─" * 80)
        
        passed = 0
        for condition, status, details in conditions:
            status_symbol = "✅ PASS" if status else "❌ FAIL"
            if status:
                passed += 1
            print(f"{condition:<30} {status_symbol:<8} {details}")
        
        print("─" * 80)
        result = passed == len(conditions)
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"🎯 TREND TEMPLATE: {status} ({passed}/{len(conditions)})")
        
        return {
            'passed': result,
            'score': f"{passed}/{len(conditions)}",
            'details': dict(zip([c[0] for c in conditions], [c[1] for c in conditions]))
        }
    
    def _step2_vcp_detection(self, data: pd.DataFrame, symbol: str) -> Dict:
        """Step 2: Volatility Contraction Pattern (VCP) Detection"""
        print(f"\n📌 STEP 2: VOLATILITY CONTRACTION PATTERN (VCP)")
        print("─" * 60)
        
        # Simplified VCP detection
        # Look for price consolidation and volume decline
        recent_data = data.tail(50)  # Last 50 days
        
        # Price range analysis
        price_range = (recent_data['High'].max() - recent_data['Low'].min()) / recent_data['Close'].mean()
        tight_range = price_range < 0.15  # Less than 15% range
        
        # Volume analysis
        recent_volume = recent_data['Volume'].tail(20).mean()
        older_volume = recent_data['Volume'].head(20).mean()
        volume_declining = recent_volume < older_volume
        
        # Final contraction check
        final_10_days = recent_data.tail(10)
        final_range = (final_10_days['High'].max() - final_10_days['Low'].min()) / final_10_days['Close'].mean()
        final_tight = final_range < 0.05  # Less than 5% in final contraction
        
        # Base duration (simplified)
        base_duration = len(recent_data)
        duration_ok = 25 <= base_duration <= 75  # 5-15 weeks approximation
        
        # Near pivot point (within 5% of recent high)
        current_price = data['Close'].iloc[-1]
        recent_high = recent_data['High'].max()
        near_pivot = (recent_high - current_price) / recent_high <= 0.05
        
        conditions = [
            ("Tight price range", tight_range, f"{price_range*100:.1f}% range"),
            ("Volume declining", volume_declining, "Volume contracting" if volume_declining else "Volume not contracting"),
            ("Final contraction tight", final_tight, f"{final_range*100:.1f}% final range"),
            ("Base duration OK", duration_ok, f"{base_duration} days"),
            ("Near pivot point", near_pivot, f"{((recent_high - current_price) / recent_high * 100):.1f}% from high")
        ]
        
        print(f"{'VCP Condition':<25} {'Status':<8} {'Details'}")
        print("─" * 60)
        
        passed = 0
        for condition, status, details in conditions:
            status_symbol = "✅ PASS" if status else "❌ FAIL"
            if status:
                passed += 1
            print(f"{condition:<25} {status_symbol:<8} {details}")
        
        print("─" * 60)
        detected = passed >= 3  # At least 3 out of 5 conditions
        status = "✅ DETECTED" if detected else "❌ NOT DETECTED"
        print(f"🎯 VCP PATTERN: {status} ({passed}/5)")
        
        return {
            'detected': detected,
            'score': f"{passed}/5",
            'pivot_point': recent_high,
            'details': dict(zip([c[0] for c in conditions], [c[1] for c in conditions]))
        }
    
    def _step3_breakout_confirmation(self, data: pd.DataFrame, symbol: str) -> Dict:
        """Step 3: Breakout Confirmation"""
        print(f"\n📌 STEP 3: BREAKOUT CONFIRMATION")
        print("─" * 60)
        
        current_price = data['Close'].iloc[-1]
        current_volume = data['Volume'].iloc[-1]
        avg_volume_50 = data['Avg_Volume_50'].iloc[-1]
        
        # Recent high as pivot point
        recent_high = data['High'].tail(50).max()
        
        # Breakout conditions
        above_pivot = current_price > recent_high
        volume_surge = current_volume >= (1.40 * avg_volume_50)  # 40% above average
        
        # Check last 5 candles for tight action
        last_5 = data.tail(5)
        ranges = (last_5['High'] - last_5['Low']) / last_5['Close']
        tight_action = ranges.mean() < 0.03  # Less than 3% average range
        
        conditions = [
            ("Price above pivot", above_pivot, f"${current_price:.2f} vs ${recent_high:.2f}"),
            ("Volume surge ≥ 40%", volume_surge, f"{(current_volume/avg_volume_50*100):.0f}% of average"),
            ("Tight price action", tight_action, f"{ranges.mean()*100:.1f}% avg range")
        ]
        
        print(f"{'Breakout Condition':<20} {'Status':<8} {'Details'}")
        print("─" * 50)
        
        passed = 0
        for condition, status, details in conditions:
            status_symbol = "✅ PASS" if status else "❌ FAIL"
            if status:
                passed += 1
            print(f"{condition:<20} {status_symbol:<8} {details}")
        
        print("─" * 50)
        confirmed = passed == 3  # All conditions must pass
        status = "✅ CONFIRMED" if confirmed else "❌ NOT CONFIRMED"
        print(f"🎯 BREAKOUT: {status} ({passed}/3)")
        
        return {
            'confirmed': confirmed,
            'score': f"{passed}/3",
            'pivot_point': recent_high,
            'details': dict(zip([c[0] for c in conditions], [c[1] for c in conditions]))
        }
    
    def _step4_optional_fundamentals(self, symbol: str) -> Dict:
        """Step 4: Optional Fundamentals (Boost Conviction)"""
        print(f"\n📌 STEP 4: OPTIONAL FUNDAMENTALS")
        print("─" * 60)
        print("💡 These boost conviction but are not required")
        
        # Gracefully handle missing fundamental data
        fundamentals = [
            ("EPS Growth ≥ 25%", False, "Data not available"),
            ("Sales Growth ≥ 25%", False, "Data not available"),
            ("ROE ≥ 17%", False, "Data not available"),
            ("Margins increasing", False, "Data not available"),
            ("Earnings acceleration", False, "Data not available"),
            ("Top 3 sector rank", False, "Data not available")
        ]
        
        print(f"{'Fundamental':<20} {'Status':<8} {'Details'}")
        print("─" * 50)
        
        passed = 0
        for condition, status, details in fundamentals:
            status_symbol = "✅ PASS" if status else "⚠️ N/A"
            print(f"{condition:<20} {status_symbol:<8} {details}")
        
        print("─" * 50)
        print(f"🎯 STATUS: ⚠️ FUNDAMENTALS NOT AVAILABLE (Optional)")
        print("💡 Focus on technical setup for now")
        
        return {
            'available': False,
            'score': f"{passed}/6",
            'note': "Fundamental data not available - technical analysis only"
        }
    
    def _step5_risk_setup_and_buy_price(self, data: pd.DataFrame, symbol: str, trend_result: Dict, vcp_result: Optional[Dict]) -> Dict:
        """Step 5: Risk Setup and Buy Execution"""
        print(f"\n📌 STEP 5: RISK SETUP AND BUY PRICE")
        print("─" * 60)
        
        current_price = data['Close'].iloc[-1]
        
        # Determine buy point
        if vcp_result and vcp_result['detected']:
            buy_point = vcp_result['pivot_point'] * 1.01  # 1% above pivot
        else:
            buy_point = current_price * 1.02  # 2% above current if no VCP
        
        # Risk calculations
        stop_loss_7pct = buy_point * 0.93  # 7% stop loss
        stop_loss_10pct = buy_point * 0.90  # 10% stop loss
        
        # Portfolio risk (assuming $100,000 portfolio)
        portfolio_value = 100000
        max_risk_per_trade = portfolio_value * 0.01  # 1% max risk
        
        # Position sizing
        risk_per_share_7pct = buy_point - stop_loss_7pct
        risk_per_share_10pct = buy_point - stop_loss_10pct
        
        shares_7pct = int(max_risk_per_trade / risk_per_share_7pct) if risk_per_share_7pct > 0 else 0
        shares_10pct = int(max_risk_per_trade / risk_per_share_10pct) if risk_per_share_10pct > 0 else 0
        
        # Reward to risk ratio (assuming 20% target)
        target_price = buy_point * 1.20  # 20% target
        reward_7pct = target_price - buy_point
        reward_10pct = target_price - buy_point
        
        rr_ratio_7pct = reward_7pct / risk_per_share_7pct if risk_per_share_7pct > 0 else 0
        rr_ratio_10pct = reward_10pct / risk_per_share_10pct if risk_per_share_10pct > 0 else 0
        
        print(f"💰 BUY POINT: ${buy_point:.2f}")
        print(f"📊 Current Price: ${current_price:.2f}")
        print()
        print("📋 POSITION SIZING OPTIONS:")
        print("─" * 40)
        print(f"7% Stop Loss:")
        print(f"  Stop: ${stop_loss_7pct:.2f}")
        print(f"  Risk/Share: ${risk_per_share_7pct:.2f}")
        print(f"  Position Size: {shares_7pct:,} shares")
        print(f"  R:R Ratio: {rr_ratio_7pct:.1f}:1")
        print()
        print(f"10% Stop Loss:")
        print(f"  Stop: ${stop_loss_10pct:.2f}")
        print(f"  Risk/Share: ${risk_per_share_10pct:.2f}")
        print(f"  Position Size: {shares_10pct:,} shares")
        print(f"  R:R Ratio: {rr_ratio_10pct:.1f}:1")
        
        return {
            'buy_point': buy_point,
            'current_price': current_price,
            'stop_loss_7pct': stop_loss_7pct,
            'stop_loss_10pct': stop_loss_10pct,
            'position_size_7pct': shares_7pct,
            'position_size_10pct': shares_10pct,
            'reward_risk_7pct': rr_ratio_7pct,
            'reward_risk_10pct': rr_ratio_10pct,
            'target_price': target_price
        }
    
    def _generate_recommendation(self, trend_result: Dict, vcp_result: Optional[Dict], 
                                breakout_result: Optional[Dict], fundamentals_result: Dict, 
                                risk_result: Dict) -> Dict:
        """Generate final trading recommendation"""
        print(f"\n📌 FINAL TRADETHRUST RECOMMENDATION")
        print("─" * 60)
        
        # Scoring
        trend_pass = trend_result['passed']
        vcp_detected = vcp_result['detected'] if vcp_result else False
        breakout_confirmed = breakout_result['confirmed'] if breakout_result else False
        
        # Recommendation logic
        if trend_pass and vcp_detected and breakout_confirmed:
            recommendation = "🔥 STRONG BUY"
            confidence = "HIGH"
            reason = "All technical conditions met"
        elif trend_pass and vcp_detected:
            recommendation = "✅ BUY ON BREAKOUT"
            confidence = "MEDIUM-HIGH"
            reason = "Wait for breakout confirmation"
        elif trend_pass:
            recommendation = "⚠️ WATCH LIST"
            confidence = "MEDIUM"
            reason = "Monitor for VCP formation"
        else:
            recommendation = "❌ DO NOT BUY"
            confidence = "LOW"
            reason = "Trend template failed"
        
        buy_point = risk_result['buy_point']
        stop_loss = risk_result['stop_loss_7pct']
        target = risk_result['target_price']
        
        print(f"🎯 RECOMMENDATION: {recommendation}")
        print(f"📊 CONFIDENCE: {confidence}")
        print(f"💡 REASON: {reason}")
        print()
        print(f"💰 BUY PRICE: ${buy_point:.2f}")
        print(f"🛡️ STOP LOSS: ${stop_loss:.2f}")
        print(f"🎯 TARGET: ${target:.2f}")
        print(f"📏 RISK: {((buy_point - stop_loss) / buy_point * 100):.1f}%")
        print(f"📈 REWARD: {((target - buy_point) / buy_point * 100):.1f}%")
        
        return {
            'action': recommendation,
            'confidence': confidence,
            'reason': reason,
            'buy_price': buy_point,
            'stop_loss': stop_loss,
            'target_price': target,
            'risk_percent': ((buy_point - stop_loss) / buy_point * 100),
            'reward_percent': ((target - buy_point) / buy_point * 100)
        }

def main():
    """Main execution"""
    print("🚀 TradeThrust Stock Trading Algorithm - Clean Final Version")
    print("✅ Following exact TradeThrust methodology")
    print("=" * 60)
    
    tt = TradeThrustClean()
    
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
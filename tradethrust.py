#!/usr/bin/env python3
"""
TradeThrust - Professional Stock Trading System
==============================================

Advanced stock analysis and trading system based on Mark Minervini's proven methodology.
Provides buy/sell signals, alerts, and portfolio management for serious traders.

Features:
- Complete Minervini Trend Template analysis
- VCP (Volatility Contraction Pattern) detection
- Real-time buy/sell alerts
- Risk management tools
- Portfolio tracking
- AWS-ready architecture

Author: TradeThrust Team
Version: 1.0.0
"""

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import json
import os
import warnings
import time
from typing import Dict, List, Tuple, Optional
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart

warnings.filterwarnings('ignore')

class TradeThrust:
    """
    Main TradeThrust trading system implementing TradeThrust's methodology
    """
    
    def __init__(self, config_file: str = "tradethrust_config.json"):
        self.config_file = config_file
        self.config = self._load_config()
        self.watchlist = []
        self.alerts = []
        self.portfolio = {}
        self.analysis_cache = {}
        
    def _load_config(self) -> Dict:
        """Load or create configuration file"""
        default_config = {
            "risk_per_trade": 0.01,  # 1% of portfolio
            "max_positions": 10,
            "email_alerts": False,
            "email_config": {
                "smtp_server": "",
                "smtp_port": 587,
                "email": "",
                "password": ""
            },
            "alert_settings": {
                "breakout_alerts": True,
                "breakdown_alerts": True,
                "profit_target_alerts": True
            }
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                return default_config
        else:
            with open(self.config_file, 'w') as f:
                json.dump(default_config, f, indent=4)
            return default_config
    
    def save_config(self):
        """Save current configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)
    
    def fetch_stock_data(self, symbol: str, period: str = "2y") -> Optional[pd.DataFrame]:
        """Fetch comprehensive stock data with all required indicators"""
        try:
            ticker = yf.Ticker(symbol.upper())
            data = ticker.history(period=period)
            
            if data.empty:
                return None
            
            # Calculate all technical indicators
            data = self._calculate_all_indicators(data)
            return data
            
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None
    
    def _calculate_all_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate all technical indicators needed for TradeThrust analysis"""
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
        
        # Price volatility and ranges
        df['Daily_Range'] = df['High'] - df['Low']
        df['Avg_Range_20'] = df['Daily_Range'].rolling(window=20).mean()
        
        # Relative Strength calculation (simplified)
        df['RS_Rating'] = self._calculate_relative_strength(df)
        
        # Support and resistance levels
        df['Support'] = df['Low'].rolling(window=20).min()
        df['Resistance'] = df['High'].rolling(window=20).max()
        
        return df
    
    def _calculate_relative_strength(self, data: pd.DataFrame) -> pd.Series:
        """Calculate simplified relative strength rating"""
        # This is a simplified version - in production, you'd compare against S&P 500
        price_change_13w = data['Close'].pct_change(periods=65)  # 13 weeks
        price_change_26w = data['Close'].pct_change(periods=130)  # 26 weeks
        price_change_52w = data['Close'].pct_change(periods=252)  # 52 weeks
        
        # Weighted average of different timeframes
        rs_score = (price_change_13w * 0.4 + price_change_26w * 0.3 + price_change_52w * 0.3)
        
        # Convert to 1-100 scale (simplified)
        rs_rating = ((rs_score.rank(pct=True)) * 100).fillna(50)
        
        return rs_rating
    
    def check_tradethrust_trend_template(self, data: pd.DataFrame) -> Dict:
        """
        Complete TradeThrust Trend Template analysis
        Returns detailed results for each criterion
        """
        if data is None or len(data) < 252:
            return {'error': 'Insufficient data for analysis'}
        
        latest = data.iloc[-1]
        recent_200 = data.tail(30)  # Last 30 days for 200-day SMA trend
        
        results = {}
        
        # 1. Price above all key moving averages
        price = latest['Close']
        sma_50 = latest['SMA_50']
        sma_150 = latest['SMA_150']
        sma_200 = latest['SMA_200']
        
        results['price_above_smas'] = {
            'pass': price > sma_50 and price > sma_150 and price > sma_200,
            'score': sum([price > sma_50, price > sma_150, price > sma_200]),
            'details': {
                'current_price': price,
                'sma_50': sma_50,
                'sma_150': sma_150,
                'sma_200': sma_200,
                'above_50': price > sma_50,
                'above_150': price > sma_150,
                'above_200': price > sma_200
            }
        }
        
        # 2. 150-day SMA above 200-day SMA
        results['sma_150_above_200'] = {
            'pass': sma_150 > sma_200,
            'details': {
                'sma_150': sma_150,
                'sma_200': sma_200,
                'difference': sma_150 - sma_200
            }
        }
        
        # 3. 50-day SMA above both 150 and 200-day SMAs
        results['sma_50_above_longer'] = {
            'pass': sma_50 > sma_150 and sma_50 > sma_200,
            'details': {
                'sma_50': sma_50,
                'above_150': sma_50 > sma_150,
                'above_200': sma_50 > sma_200
            }
        }
        
        # 4. Price above 50-day SMA
        results['price_above_50sma'] = {
            'pass': price > sma_50,
            'details': {
                'price': price,
                'sma_50': sma_50,
                'percentage_above': ((price - sma_50) / sma_50) * 100
            }
        }
        
        # 5. 200-day SMA trending up for at least 1 month
        sma_200_trend = recent_200['SMA_200'].iloc[-1] > recent_200['SMA_200'].iloc[0]
        results['sma_200_trending_up'] = {
            'pass': sma_200_trend,
            'details': {
                'current_200sma': recent_200['SMA_200'].iloc[-1],
                'month_ago_200sma': recent_200['SMA_200'].iloc[0],
                'trend_direction': 'up' if sma_200_trend else 'down'
            }
        }
        
        # 6. Price at least 30% above 52-week low
        week_52_low = latest['52W_Low']
        pct_above_low = ((price - week_52_low) / week_52_low) * 100
        results['above_52w_low'] = {
            'pass': pct_above_low >= 30,
            'details': {
                'current_price': price,
                'week_52_low': week_52_low,
                'percentage_above': pct_above_low
            }
        }
        
        # 7. Price within 25% of 52-week high
        week_52_high = latest['52W_High']
        pct_from_high = ((week_52_high - price) / week_52_high) * 100
        results['near_52w_high'] = {
            'pass': pct_from_high <= 25,
            'details': {
                'current_price': price,
                'week_52_high': week_52_high,
                'percentage_from_high': pct_from_high
            }
        }
        
        # 8. Relative Strength Rating >= 70
        rs_rating = latest['RS_Rating']
        results['relative_strength'] = {
            'pass': rs_rating >= 70,
            'details': {
                'rs_rating': rs_rating,
                'target': 70
            }
        }
        
        return results
    
    def detect_vcp_pattern(self, data: pd.DataFrame, weeks_back: int = 15) -> Dict:
        """
        Detect Volatility Contraction Pattern (VCP) according to TradeThrust
        """
        if data is None or len(data) < weeks_back * 5:
            return {'vcp_detected': False, 'error': 'Insufficient data'}
        
        # Analyze recent weeks
        analysis_period = data.tail(weeks_back * 5)  # Approximate 5 trading days per week
        
        # Find contractions (pullbacks)
        contractions = self._find_price_contractions(analysis_period)
        
        # Analyze contraction characteristics
        vcp_analysis = self._analyze_vcp_characteristics(contractions, analysis_period)
        
        return vcp_analysis
    
    def _find_price_contractions(self, data: pd.DataFrame) -> List[Dict]:
        """Find price contractions/pullbacks in the data"""
        contractions = []
        
        # Find swing highs and lows
        highs = []
        lows = []
        
        for i in range(5, len(data) - 5):
            # Swing high detection
            if all(data.iloc[i]['High'] >= data.iloc[j]['High'] for j in range(i-5, i+6) if j != i):
                highs.append((i, data.iloc[i]['High'], data.index[i]))
            
            # Swing low detection  
            if all(data.iloc[i]['Low'] <= data.iloc[j]['Low'] for j in range(i-5, i+6) if j != i):
                lows.append((i, data.iloc[i]['Low'], data.index[i]))
        
        # Match highs with subsequent lows to identify contractions
        for i, (high_idx, high_price, high_date) in enumerate(highs):
            subsequent_lows = [low for low in lows if low[0] > high_idx]
            
            if subsequent_lows:
                low_idx, low_price, low_date = min(subsequent_lows, key=lambda x: x[1])
                contraction_pct = ((high_price - low_price) / high_price) * 100
                
                # Calculate volume characteristics during pullback
                pullback_data = data.iloc[high_idx:low_idx+1]
                avg_volume = pullback_data['Volume'].mean()
                base_volume = data.iloc[max(0, high_idx-20):high_idx]['Volume'].mean()
                
                contractions.append({
                    'high_idx': high_idx,
                    'low_idx': low_idx,
                    'high_price': high_price,
                    'low_price': low_price,
                    'high_date': high_date,
                    'low_date': low_date,
                    'contraction_pct': contraction_pct,
                    'duration_days': (low_date - high_date).days,
                    'volume_ratio': avg_volume / base_volume if base_volume > 0 else 1,
                    'avg_volume_during': avg_volume
                })
        
        return sorted(contractions, key=lambda x: x['high_date'])
    
    def _analyze_vcp_characteristics(self, contractions: List[Dict], data: pd.DataFrame) -> Dict:
        """Analyze VCP pattern characteristics"""
        if len(contractions) < 2:
            return {
                'vcp_detected': False,
                'reason': f'Only {len(contractions)} contractions found, need at least 2',
                'contractions_found': len(contractions)
            }
        
        # Check if contractions are getting progressively smaller
        contractions_decreasing = True
        for i in range(1, len(contractions)):
            if contractions[i]['contraction_pct'] >= contractions[i-1]['contraction_pct']:
                contractions_decreasing = False
                break
        
        # Check volume behavior (should decline during pullbacks)
        volume_declining = True
        volume_details = []
        
        for contraction in contractions:
            volume_ratio = contraction['volume_ratio']
            volume_details.append(f"{contraction['contraction_pct']:.1f}% pullback, volume ratio: {volume_ratio:.2f}")
            if volume_ratio > 0.8:  # Volume too high during pullback
                volume_declining = False
        
        # Check for tight action in final contraction
        if contractions:
            final_contraction = contractions[-1]
            tight_action = final_contraction['contraction_pct'] < 15  # Less than 15% pullback
        else:
            tight_action = False
        
        # Check base duration (should be 5-15 weeks ideally)
        if contractions:
            first_high = contractions[0]['high_date']
            last_low = contractions[-1]['low_date']
            base_duration_weeks = (last_low - first_high).days / 7
            good_duration = 5 <= base_duration_weeks <= 15
        else:
            base_duration_weeks = 0
            good_duration = False
        
        # Overall VCP score
        vcp_criteria = [
            contractions_decreasing,
            volume_declining,
            tight_action,
            good_duration,
            len(contractions) >= 2
        ]
        
        vcp_score = sum(vcp_criteria)
        vcp_detected = vcp_score >= 3  # At least 3 out of 5 criteria
        
        return {
            'vcp_detected': vcp_detected,
            'vcp_score': f"{vcp_score}/5",
            'contractions_count': len(contractions),
            'contractions_decreasing': contractions_decreasing,
            'volume_declining': volume_declining,
            'tight_final_action': tight_action,
            'good_base_duration': good_duration,
            'base_duration_weeks': base_duration_weeks,
            'contractions_detail': [
                f"Pullback {i+1}: -{c['contraction_pct']:.1f}% over {c['duration_days']} days"
                for i, c in enumerate(contractions)
            ],
            'volume_detail': volume_details
        }
    
    def check_breakout_entry_signal(self, data: pd.DataFrame) -> Dict:
        """Check for TradeThrust-style breakout entry signals"""
        if data is None or len(data) < 50:
            return {'breakout_signal': False, 'error': 'Insufficient data'}
        
        latest = data.iloc[-1]
        recent_data = data.tail(50)
        
        # Find resistance level (recent highs)
        resistance_period = recent_data.tail(20)
        resistance_level = resistance_period['High'].max()
        
        # Volume analysis
        avg_volume_50 = recent_data['Volume'].mean()
        current_volume = latest['Volume']
        volume_surge = current_volume > avg_volume_50 * 1.4  # 40% above average
        
        # Price breakout check
        current_price = latest['Close']
        price_breakout = current_price > resistance_level * 1.002  # Small buffer for noise
        
        # Check for clean action (no wide-spread bars recently)
        recent_5_days = data.tail(5)
        daily_ranges = recent_5_days['Daily_Range']
        avg_range = daily_ranges.mean()
        clean_action = all(daily_ranges <= avg_range * 1.5)  # No excessively wide bars
        
        # Proximity to resistance
        distance_from_resistance = ((current_price - resistance_level) / resistance_level) * 100
        close_to_resistance = abs(distance_from_resistance) <= 3  # Within 3% of resistance
        
        return {
            'breakout_signal': price_breakout and volume_surge,
            'price_breakout': price_breakout,
            'volume_surge': volume_surge,
            'clean_action': clean_action,
            'close_to_resistance': close_to_resistance,
            'details': {
                'current_price': current_price,
                'resistance_level': resistance_level,
                'current_volume': current_volume,
                'avg_volume_50': avg_volume_50,
                'volume_surge_pct': ((current_volume - avg_volume_50) / avg_volume_50) * 100,
                'distance_from_resistance_pct': distance_from_resistance
            }
        }
    
    def analyze_stock_complete(self, symbol: str) -> Dict:
        """Complete stock analysis using TradeThrust methodology"""
        print(f"\n🚀 TRADETHRUST ANALYSIS: {symbol.upper()}")
        print("=" * 60)
        
        # Fetch data
        data = self.fetch_stock_data(symbol)
        if data is None:
            return {'error': f'Could not fetch data for {symbol}'}
        
        symbol = symbol.upper()
        latest_price = data.iloc[-1]['Close']
        
        # Phase 1: Trend Template Analysis
        print("\n📊 PHASE 1: MINERVINI TREND TEMPLATE")
        print("-" * 40)
        
        trend_results = self.check_minervini_trend_template(data)
        phase1_score = 0
        phase1_total = 8
        
        criteria_names = {
            'price_above_smas': 'Price Above All SMAs (50, 150, 200)',
            'sma_150_above_200': '150-day SMA Above 200-day SMA',
            'sma_50_above_longer': '50-day SMA Above 150 & 200',
            'price_above_50sma': 'Price Above 50-day SMA',
            'sma_200_trending_up': '200-day SMA Trending Up (1 month)',
            'above_52w_low': 'Price ≥30% Above 52-week Low',
            'near_52w_high': 'Price ≤25% From 52-week High',
            'relative_strength': 'Relative Strength ≥70'
        }
        
        for criterion, name in criteria_names.items():
            if criterion in trend_results:
                result = trend_results[criterion]
                status = "✅ PASS" if result['pass'] else "❌ FAIL"
                print(f"{status} {name}")
                
                if criterion == 'price_above_smas':
                    details = result['details']
                    print(f"    Price: ${details['current_price']:.2f} | 50SMA: ${details['sma_50']:.2f} | 150SMA: ${details['sma_150']:.2f} | 200SMA: ${details['sma_200']:.2f}")
                elif criterion == 'above_52w_low':
                    details = result['details']
                    print(f"    52W Low: ${details['week_52_low']:.2f} | Current: {details['percentage_above']:.1f}% above")
                elif criterion == 'near_52w_high':
                    details = result['details']
                    print(f"    52W High: ${details['week_52_high']:.2f} | Current: {details['percentage_from_high']:.1f}% below")
                elif criterion == 'relative_strength':
                    details = result['details']
                    print(f"    RS Rating: {details['rs_rating']:.1f} (Target: ≥70)")
                
                if result['pass']:
                    phase1_score += 1
        
        phase1_pass = phase1_score >= 6  # Allow 2 failures out of 8
        print(f"\n📊 Phase 1 Score: {phase1_score}/{phase1_total} {'✅ STRONG TREND' if phase1_pass else '❌ WEAK TREND'}")
        
        # Phase 2: VCP Pattern Analysis
        print("\n📈 PHASE 2: VCP BASE FORMATION")
        print("-" * 35)
        
        vcp_results = self.detect_vcp_pattern(data)
        if 'error' not in vcp_results:
            vcp_detected = vcp_results['vcp_detected']
            status = "✅ DETECTED" if vcp_detected else "❌ NOT FOUND"
            print(f"{status} VCP Pattern")
            print(f"    Score: {vcp_results['vcp_score']}")
            print(f"    Contractions: {vcp_results['contractions_count']}")
            print(f"    Base Duration: {vcp_results['base_duration_weeks']:.1f} weeks")
            
            if vcp_results['contractions_detail']:
                print("    Pullback Analysis:")
                for detail in vcp_results['contractions_detail']:
                    print(f"      • {detail}")
        else:
            vcp_detected = False
            print("❌ VCP Analysis Failed - Insufficient Data")
        
        # Phase 3: Entry Signal Analysis
        print("\n🎯 PHASE 3: ENTRY SIGNAL CHECK")
        print("-" * 35)
        
        breakout_results = self.check_breakout_entry_signal(data)
        if 'error' not in breakout_results:
            entry_signal = breakout_results['breakout_signal']
            status = "✅ BUY SIGNAL" if entry_signal else "❌ NO SIGNAL"
            print(f"{status} Breakout Entry")
            
            details = breakout_results['details']
            print(f"    Current Price: ${details['current_price']:.2f}")
            print(f"    Resistance Level: ${details['resistance_level']:.2f}")
            print(f"    Volume Surge: {details['volume_surge_pct']:.1f}% above average")
            print(f"    Distance from Resistance: {details['distance_from_resistance_pct']:.2f}%")
        else:
            entry_signal = False
            print("❌ Entry Signal Analysis Failed")
        
        # Risk Management Calculations
        print("\n💰 RISK MANAGEMENT")
        print("-" * 25)
        
        # Calculate stop loss levels
        recent_support = data.tail(20)['Low'].min()
        stop_loss_support = recent_support * 0.98  # 2% below support
        stop_loss_percentage = max(0.07, 0.10)  # 7-10% max risk
        stop_loss_price = latest_price * (1 - stop_loss_percentage)
        
        # Use the higher of the two stop levels (more conservative)
        recommended_stop = max(stop_loss_support, stop_loss_price)
        risk_percent = ((latest_price - recommended_stop) / latest_price) * 100
        
        print(f"Current Price: ${latest_price:.2f}")
        print(f"Recent Support: ${recent_support:.2f}")
        print(f"Recommended Stop Loss: ${recommended_stop:.2f}")
        print(f"Risk per Share: {risk_percent:.1f}%")
        
        # Position sizing based on risk
        portfolio_risk = self.config['risk_per_trade'] * 100  # Convert to percentage
        print(f"Portfolio Risk Target: {portfolio_risk:.1f}%")
        
        # Final Recommendation
        print("\n" + "=" * 60)
        
        # Overall scoring
        overall_score = 0
        if phase1_pass: overall_score += 3
        if vcp_detected: overall_score += 2
        if entry_signal: overall_score += 2
        
        if overall_score >= 5 and entry_signal:
            recommendation = "🟢 STRONG BUY"
            action = "BUY NOW"
            print(f"🎯 RECOMMENDATION: {recommendation}")
            print("✅ This stock meets Minervini's strict criteria!")
            print("✅ Strong trend + VCP base + breakout signal = High probability setup")
        elif overall_score >= 3 and phase1_pass:
            recommendation = "🟡 WATCH LIST"
            action = "MONITOR"
            print(f"⚠️  RECOMMENDATION: {recommendation}")
            print("📊 Good trend structure but wait for better entry signal")
            print("🔍 Add to watchlist and monitor for breakout")
        else:
            recommendation = "🔴 AVOID"
            action = "HOLD/AVOID"
            print(f"❌ RECOMMENDATION: {recommendation}")
            print("🚫 Does not meet Minervini's criteria")
            print("⏳ Wait for better setup or look for other opportunities")
        
        # Create alerts if appropriate
        if entry_signal and phase1_pass:
            self._create_alert(symbol, 'BUY_SIGNAL', latest_price, f"Strong buy signal detected for {symbol}")
        elif phase1_pass and not entry_signal:
            self._create_alert(symbol, 'WATCH', latest_price, f"Good setup for {symbol}, watching for breakout")
        
        return {
            'symbol': symbol,
            'timestamp': datetime.now().isoformat(),
            'recommendation': recommendation,
            'action': action,
            'overall_score': f"{overall_score}/7",
            'phase1_score': f"{phase1_score}/{phase1_total}",
            'phase1_pass': phase1_pass,
            'vcp_detected': vcp_detected,
            'entry_signal': entry_signal,
            'current_price': latest_price,
            'stop_loss': recommended_stop,
            'risk_percent': risk_percent,
            'resistance_level': breakout_results.get('details', {}).get('resistance_level', 0),
            'support_level': recent_support,
            'analysis_details': {
                'trend_template': trend_results,
                'vcp_analysis': vcp_results,
                'breakout_analysis': breakout_results
            }
        }
    
    def _create_alert(self, symbol: str, alert_type: str, price: float, message: str):
        """Create a new alert"""
        alert = {
            'symbol': symbol,
            'type': alert_type,
            'price': price,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'active': True
        }
        self.alerts.append(alert)
        print(f"\n🔔 ALERT CREATED: {message}")
    
    def add_to_watchlist(self, symbol: str):
        """Add stock to watchlist"""
        symbol = symbol.upper()
        if symbol not in self.watchlist:
            self.watchlist.append(symbol)
            print(f"✅ {symbol} added to watchlist")
            self.save_watchlist()
        else:
            print(f"ℹ️  {symbol} already in watchlist")
    
    def remove_from_watchlist(self, symbol: str):
        """Remove stock from watchlist"""
        symbol = symbol.upper()
        if symbol in self.watchlist:
            self.watchlist.remove(symbol)
            print(f"✅ {symbol} removed from watchlist")
            self.save_watchlist()
        else:
            print(f"ℹ️  {symbol} not in watchlist")
    
    def save_watchlist(self):
        """Save watchlist to file"""
        try:
            with open('tradethrust_watchlist.json', 'w') as f:
                json.dump(self.watchlist, f)
        except Exception as e:
            print(f"Error saving watchlist: {e}")
    
    def load_watchlist(self):
        """Load watchlist from file"""
        try:
            if os.path.exists('tradethrust_watchlist.json'):
                with open('tradethrust_watchlist.json', 'r') as f:
                    self.watchlist = json.load(f)
        except Exception as e:
            print(f"Error loading watchlist: {e}")
    
    def scan_watchlist(self):
        """Scan entire watchlist for trading opportunities"""
        if not self.watchlist:
            print("📋 Watchlist is empty. Add stocks with add_to_watchlist(symbol)")
            return
        
        print(f"\n🔍 SCANNING WATCHLIST ({len(self.watchlist)} stocks)")
        print("=" * 60)
        
        opportunities = []
        watch_later = []
        avoid_list = []
        
        for symbol in self.watchlist:
            print(f"\nAnalyzing {symbol}...")
            try:
                result = self.analyze_stock_complete(symbol)
                
                if result['action'] == 'BUY NOW':
                    opportunities.append(result)
                elif result['action'] == 'MONITOR':
                    watch_later.append(result)
                else:
                    avoid_list.append(result)
                    
            except Exception as e:
                print(f"Error analyzing {symbol}: {e}")
        
        # Summary Report
        print(f"\n🎯 WATCHLIST SCAN SUMMARY")
        print("=" * 40)
        
        if opportunities:
            print(f"\n🟢 BUY OPPORTUNITIES ({len(opportunities)}):")
            for opp in opportunities:
                print(f"  • {opp['symbol']}: ${opp['current_price']:.2f} - {opp['recommendation']}")
        
        if watch_later:
            print(f"\n🟡 MONITOR CLOSELY ({len(watch_later)}):")
            for watch in watch_later:
                print(f"  • {watch['symbol']}: ${watch['current_price']:.2f} - Good setup, wait for entry")
        
        if avoid_list:
            print(f"\n🔴 AVOID FOR NOW ({len(avoid_list)}):")
            for avoid in avoid_list:
                print(f"  • {avoid['symbol']}: ${avoid['current_price']:.2f} - Poor setup")
        
        return {
            'opportunities': opportunities,
            'watch_list': watch_later,
            'avoid_list': avoid_list
        }
    
    def create_chart(self, symbol: str, save_path: Optional[str] = None):
        """Create comprehensive trading chart with all indicators"""
        data = self.fetch_stock_data(symbol)
        if data is None:
            print(f"Cannot create chart for {symbol} - no data available")
            return
        
        # Use recent 6 months for clarity
        chart_data = data.tail(120)
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12), 
                                       gridspec_kw={'height_ratios': [3, 1]})
        
        # Price and moving averages
        ax1.plot(chart_data.index, chart_data['Close'], label='Price', linewidth=2.5, color='black')
        ax1.plot(chart_data.index, chart_data['SMA_50'], label='50 SMA', alpha=0.8, color='blue', linewidth=1.5)
        ax1.plot(chart_data.index, chart_data['SMA_150'], label='150 SMA', alpha=0.8, color='orange', linewidth=1.5)
        ax1.plot(chart_data.index, chart_data['SMA_200'], label='200 SMA', alpha=0.8, color='red', linewidth=1.5)
        ax1.plot(chart_data.index, chart_data['EMA_10'], label='10 EMA', alpha=0.7, color='green', linestyle='--')
        ax1.plot(chart_data.index, chart_data['EMA_21'], label='21 EMA', alpha=0.7, color='purple', linestyle='--')
        
        # Support and resistance levels
        latest = chart_data.iloc[-1]
        ax1.axhline(y=latest['52W_High'], color='green', linestyle=':', alpha=0.6, label='52W High', linewidth=2)
        ax1.axhline(y=latest['52W_Low'], color='red', linestyle=':', alpha=0.6, label='52W Low', linewidth=2)
        
        # Recent resistance level
        resistance = chart_data.tail(20)['High'].max()
        ax1.axhline(y=resistance, color='purple', linestyle='-', alpha=0.7, label='Recent Resistance', linewidth=2)
        
        ax1.set_title(f'{symbol.upper()} - TradeThrust Analysis Chart', fontsize=18, fontweight='bold')
        ax1.set_ylabel('Price ($)', fontsize=14)
        ax1.legend(loc='upper left', fontsize=10)
        ax1.grid(True, alpha=0.3)
        
        # Volume with alerts
        colors = ['red' if vol > chart_data['Avg_Volume_20'].iloc[i] * 1.5 else 'lightblue' 
                 for i, vol in enumerate(chart_data['Volume'])]
        ax2.bar(chart_data.index, chart_data['Volume'], alpha=0.7, color=colors)
        ax2.plot(chart_data.index, chart_data['Avg_Volume_20'], color='red', linewidth=2, label='20-day Avg Volume')
        ax2.set_ylabel('Volume', fontsize=14)
        ax2.set_xlabel('Date', fontsize=14)
        ax2.legend(fontsize=10)
        ax2.grid(True, alpha=0.3)
        
        # Format dates
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        
        # Save chart
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Chart saved to {save_path}")
        else:
            chart_path = f'{symbol.upper()}_tradethrust_chart.png'
            plt.savefig(chart_path, dpi=300, bbox_inches='tight')
            print(f"Chart saved to {chart_path}")
        
        plt.show()
    
    def export_analysis_report(self, symbol: str, analysis_result: Dict):
        """Export detailed analysis report to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"TradeThrust_Report_{symbol}_{timestamp}.txt"
        
        with open(filename, 'w') as f:
            f.write("TRADETHRUST PROFESSIONAL ANALYSIS REPORT\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Symbol: {analysis_result['symbol']}\n")
            f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Current Price: ${analysis_result['current_price']:.2f}\n")
            f.write(f"Recommendation: {analysis_result['recommendation']}\n")
            f.write(f"Action: {analysis_result['action']}\n")
            f.write(f"Overall Score: {analysis_result['overall_score']}\n\n")
            
            f.write("RISK MANAGEMENT\n")
            f.write("-" * 20 + "\n")
            f.write(f"Recommended Stop Loss: ${analysis_result['stop_loss']:.2f}\n")
            f.write(f"Risk per Share: {analysis_result['risk_percent']:.1f}%\n")
            f.write(f"Support Level: ${analysis_result['support_level']:.2f}\n")
            f.write(f"Resistance Level: ${analysis_result['resistance_level']:.2f}\n\n")
            
            f.write("DETAILED ANALYSIS\n")
            f.write("-" * 20 + "\n")
            f.write(f"Phase 1 (Trend): {analysis_result['phase1_score']} - {'PASS' if analysis_result['phase1_pass'] else 'FAIL'}\n")
            f.write(f"VCP Pattern: {'DETECTED' if analysis_result['vcp_detected'] else 'NOT FOUND'}\n")
            f.write(f"Entry Signal: {'PRESENT' if analysis_result['entry_signal'] else 'ABSENT'}\n\n")
            
            f.write("TRADING PLAN\n")
            f.write("-" * 15 + "\n")
            if analysis_result['action'] == 'BUY NOW':
                f.write("1. Buy at current market price or on slight pullback\n")
                f.write(f"2. Set stop loss at ${analysis_result['stop_loss']:.2f}\n")
                f.write("3. Target first profit at 20-25% gain\n")
                f.write("4. Trail stop higher as stock advances\n")
            elif analysis_result['action'] == 'MONITOR':
                f.write("1. Add to watchlist for daily monitoring\n")
                f.write("2. Wait for volume breakout above resistance\n")
                f.write("3. Be ready to buy on confirmed breakout\n")
            else:
                f.write("1. Avoid this stock for now\n")
                f.write("2. Wait for better technical setup\n")
                f.write("3. Re-evaluate in 2-4 weeks\n")
        
        print(f"📄 Detailed report saved to {filename}")
        return filename

def main():
    """Main TradeThrust application interface"""
    print("🚀 Welcome to TradeThrust - Professional Trading System")
    print("Based on TradeThrust's proven methodology")
    print("=" * 60)
    
    # Initialize TradeThrust
    tt = TradeThrust()
    tt.load_watchlist()
    
    while True:
        print("\n📋 TRADETHRUST MENU")
        print("-" * 25)
        print("1. 📊 Analyze Single Stock")
        print("2. 📈 Add to Watchlist")
        print("3. 🔍 Scan Watchlist")
        print("4. 📋 View Watchlist")
        print("5. 🗑️  Remove from Watchlist")
        print("6. 📊 Create Chart")
        print("7. ⚙️  Settings")
        print("8. 🚪 Exit")
        
        choice = input("\nSelect option (1-8): ").strip()
        
        if choice == '1':
            symbol = input("Enter stock symbol: ").strip().upper()
            if symbol:
                try:
                    result = tt.analyze_stock_complete(symbol)
                    if 'error' not in result:
                        # Ask if user wants to save report
                        save_report = input(f"\nSave detailed report for {symbol}? (y/n): ").strip().lower()
                        if save_report == 'y':
                            tt.export_analysis_report(symbol, result)
                    else:
                        print(f"Error: {result['error']}")
                except Exception as e:
                    print(f"Error analyzing {symbol}: {e}")
        
        elif choice == '2':
            symbol = input("Enter stock symbol to add: ").strip().upper()
            if symbol:
                tt.add_to_watchlist(symbol)
        
        elif choice == '3':
            tt.scan_watchlist()
        
        elif choice == '4':
            if tt.watchlist:
                print(f"\n📋 Current Watchlist ({len(tt.watchlist)} stocks):")
                for i, symbol in enumerate(tt.watchlist, 1):
                    print(f"  {i}. {symbol}")
            else:
                print("\n📋 Watchlist is empty")
        
        elif choice == '5':
            if tt.watchlist:
                print(f"\nCurrent watchlist: {', '.join(tt.watchlist)}")
                symbol = input("Enter symbol to remove: ").strip().upper()
                if symbol:
                    tt.remove_from_watchlist(symbol)
            else:
                print("Watchlist is empty")
        
        elif choice == '6':
            symbol = input("Enter stock symbol for chart: ").strip().upper()
            if symbol:
                try:
                    tt.create_chart(symbol)
                except Exception as e:
                    print(f"Error creating chart for {symbol}: {e}")
        
        elif choice == '7':
            print(f"\n⚙️  Current Settings:")
            print(f"Risk per trade: {tt.config['risk_per_trade']*100:.1f}%")
            print(f"Max positions: {tt.config['max_positions']}")
            print("Settings modification will be available in future version")
        
        elif choice == '8':
            print("Thank you for using TradeThrust! 🚀")
            print("Trade safely and follow your risk management rules!")
            break
        
        else:
            print("Invalid option. Please select 1-8.")

if __name__ == "__main__":
    main()
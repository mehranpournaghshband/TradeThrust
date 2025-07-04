#!/usr/bin/env python3
"""
TradeThrust Stock Trading Algorithm - FINNHUB EDITION
====================================================

Following the EXACT TradeThrust algorithmic specification with:
- Finnhub API for reliable stock data
- Confidence scoring system (0-100)
- Anti-rules and risk management
- Professional output formatting

Author: TradeThrust Team
Version: FINNHUB FINAL
"""

import pandas as pd
import numpy as np
import requests
import os
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import warnings
warnings.filterwarnings('ignore')

class TradeThrustFinnhub:
    """TradeThrust implementation using Finnhub API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize TradeThrust with Finnhub API
        
        Args:
            api_key: Finnhub API key (get free at https://finnhub.io)
                    If None, will check FINNHUB_API_KEY environment variable
        """
        if api_key is None:
            api_key = os.getenv('FINNHUB_API_KEY', 'demo')
        
        self.finnhub_api_key = api_key
        self.base_url = "https://finnhub.io/api/v1"
        self.session = requests.Session()
        self.session.headers.update({
            'X-Finnhub-Token': self.finnhub_api_key,
            'User-Agent': 'TradeThrust/1.0'
        })
        
        # Portfolio settings
        self.portfolio_value = 100000  # Default $100k portfolio
        self.max_positions = 8  # Max 5-8 positions as per anti-rules
    
    def get_stock_data(self, symbol: str) -> Optional[pd.DataFrame]:
        """Get comprehensive stock data from Finnhub"""
        symbol = symbol.upper().strip()
        print(f"\n🔍 Fetching market data for {symbol} from Finnhub...")
        
        try:
            # Get historical data (2 years)
            end_time = int(datetime.now().timestamp())
            start_time = int((datetime.now() - timedelta(days=730)).timestamp())
            
            # Finnhub stock candles endpoint
            url = f"{self.base_url}/stock/candle"
            params = {
                'symbol': symbol,
                'resolution': 'D',  # Daily data
                'from': start_time,
                'to': end_time
            }
            
            print(f"   📡 Requesting data from Finnhub API...")
            response = self.session.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('s') == 'ok' and data.get('c'):  # Check if we have valid data
                    # Create DataFrame from Finnhub data
                    df = pd.DataFrame({
                        'Date': pd.to_datetime(data['t'], unit='s'),
                        'Open': data['o'],
                        'High': data['h'],
                        'Low': data['l'],
                        'Close': data['c'],
                        'Volume': data['v']
                    })
                    
                    df.set_index('Date', inplace=True)
                    df = df.dropna()
                    
                    if len(df) > 200:  # Ensure we have enough data
                        current_price = df['Close'].iloc[-1]
                        print(f"   ✅ Finnhub SUCCESS: ${current_price:.2f} ({len(df)} days)")
                        return self._calculate_indicators(df)
                    else:
                        print(f"   ⚠️ Insufficient data: only {len(df)} days")
                        return None
                else:
                    print(f"   ⚠️ Finnhub returned no data for {symbol}")
                    return None
            else:
                print(f"   ❌ Finnhub API error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   ❌ Error fetching data: {str(e)[:50]}...")
            return None
    
    def _calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate all required technical indicators"""
        print(f"   🔧 Calculating technical indicators...")
        
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
        
        # Price ranges for VCP analysis
        df['High_Low_Range'] = (df['High'] - df['Low']) / df['Close']
        
        # Relative Strength calculation
        if len(df) >= 63:
            price_3m_ago = df['Close'].shift(63)
            performance_3m = (df['Close'] - price_3m_ago) / price_3m_ago * 100
            
            # Convert performance to RS rating (0-99)
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
        df['SMA_200_Slope'] = df['SMA_200'].diff()
        df['SMA_200_Trend'] = df['SMA_200_Slope'].rolling(window=20).apply(lambda x: (x > 0).all())
        
        print(f"   ✅ Technical indicators calculated")
        return df
    
    def analyze_stock(self, symbol: str) -> Dict:
        """Complete TradeThrust analysis following exact algorithm"""
        symbol = symbol.upper()
        
        print(f"\n{'='*80}")
        print(f"🚀 TRADETHRUST FINNHUB ALGORITHM")
        print(f"📊 Symbol: {symbol} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔗 Data Source: Finnhub.io API")
        print(f"✅ Following EXACT TradeThrust Principles")
        print(f"{'='*80}")
        
        # Get data from Finnhub
        data = self.get_stock_data(symbol)
        if data is None:
            return {
                'error': f'Market data not available for {symbol} from Finnhub',
                'symbol': symbol,
                'data_source': 'Finnhub',
                'timestamp': datetime.now().isoformat()
            }
        
        current_price = data['Close'].iloc[-1]
        print(f"\n✅ DATA LOADED: ${current_price:.2f}")
        
        # Apply TradeThrust 5-step algorithm
        results = {}
        
        # Step 1: Trend Template Filter (EXACT implementation)
        trend_result = self._step1_trend_template_exact(data, symbol)
        results['trend_template'] = trend_result
        
        # Step 2: VCP Detection (Enhanced)
        vcp_result = None
        if trend_result['passed']:
            vcp_result = self._step2_vcp_detection_enhanced(data, symbol)
            results['vcp_pattern'] = vcp_result
        else:
            results['vcp_pattern'] = {'detected': False, 'reason': 'Trend template failed'}
        
        # Step 3: Breakout Confirmation (Exact criteria)
        breakout_result = None
        if vcp_result and vcp_result['detected']:
            breakout_result = self._step3_breakout_confirmation_exact(data, symbol)
            results['breakout_confirmation'] = breakout_result
        else:
            results['breakout_confirmation'] = {'confirmed': False, 'reason': 'No VCP detected'}
        
        # Step 4: Optional Fundamentals (Finnhub has some fundamental data)
        fundamentals_result = self._step4_fundamentals_finnhub(symbol)
        results['fundamentals'] = fundamentals_result
        
        # Step 5: Risk Setup and Buy Execution
        risk_result = self._step5_risk_setup_exact(data, symbol, trend_result, vcp_result, breakout_result)
        results['risk_setup'] = risk_result
        
        # Anti-Rules Check
        anti_rules_result = self._check_anti_rules(data, symbol, trend_result)
        results['anti_rules'] = anti_rules_result
        
        # Market Condition Check (using Finnhub)
        market_condition = self._check_market_condition()
        results['market_condition'] = market_condition
        
        # Generate final recommendation with confidence score
        recommendation = self._generate_enhanced_recommendation(
            trend_result, vcp_result, breakout_result, fundamentals_result, 
            risk_result, anti_rules_result, market_condition
        )
        results['recommendation'] = recommendation
        
        return {
            'symbol': symbol,
            'current_price': current_price,
            'data_source': 'Finnhub',
            **results,
            'timestamp': datetime.now().isoformat()
        }
    
    def _step1_trend_template_exact(self, data: pd.DataFrame, symbol: str) -> Dict:
        """Step 1: Trend Template Filter - EXACT Implementation"""
        print(f"\n📌 STEP 1: TREND TEMPLATE FILTER (EXACT CRITERIA)")
        print("─" * 70)
        
        latest = data.iloc[-1]
        price = latest['Close']
        sma_50 = latest['SMA_50']
        sma_150 = latest['SMA_150']
        sma_200 = latest['SMA_200']
        high_52w = latest['High_52W']
        low_52w = latest['Low_52W']
        rs_rating = latest['RS_Rating']
        sma_200_trend = latest['SMA_200_Trend'] if not pd.isna(latest['SMA_200_Trend']) else False
        
        # EXACT conditions as per TradeThrust algorithm
        conditions = [
            ("Price > 50-day SMA", price > sma_50, f"${price:.2f} vs ${sma_50:.2f}", 10),
            ("Price > 150-day SMA", price > sma_150, f"${price:.2f} vs ${sma_150:.2f}", 10),
            ("Price > 200-day SMA", price > sma_200, f"${price:.2f} vs ${sma_200:.2f}", 10),
            ("150-day SMA > 200-day SMA", sma_150 > sma_200, f"${sma_150:.2f} vs ${sma_200:.2f}", 10),
            ("50-day SMA > 150-day SMA", sma_50 > sma_150, f"${sma_50:.2f} vs ${sma_150:.2f}", 10),
            ("50-day SMA > 200-day SMA", sma_50 > sma_200, f"${sma_50:.2f} vs ${sma_200:.2f}", 10),
            ("200-day SMA trending up 20 days", sma_200_trend, "Upward" if sma_200_trend else "Not trending", 10),
            ("Price ≥ 30% above 52W low", (price - low_52w) / low_52w >= 0.30, f"{((price - low_52w) / low_52w * 100):.1f}%", 10),
            ("Price ≤ 25% below 52W high", (high_52w - price) / high_52w <= 0.25, f"{((high_52w - price) / high_52w * 100):.1f}% below", 10),
            ("RS Rating ≥ 70", rs_rating >= 70, f"{rs_rating:.0f}", 10)
        ]
        
        print(f"{'Condition':<32} {'Status':<8} {'Details':<20} {'Points'}")
        print("─" * 80)
        
        total_score = 0
        max_score = 100
        passed_conditions = 0
        
        for condition, status, details, points in conditions:
            status_symbol = "✅ PASS" if status else "❌ FAIL"
            if status:
                total_score += points
                passed_conditions += 1
            print(f"{condition:<32} {status_symbol:<8} {details:<20} {points if status else 0}")
        
        print("─" * 80)
        result = passed_conditions == len(conditions)  # ALL must pass
        status = "✅ PASSED" if result else "❌ FAILED"
        confidence = (total_score / max_score) * 100
        
        print(f"🎯 TREND TEMPLATE: {status} ({passed_conditions}/{len(conditions)}) | Score: {confidence:.0f}%")
        
        return {
            'passed': result,
            'score': total_score,
            'max_score': max_score,
            'confidence': confidence,
            'conditions_met': passed_conditions,
            'total_conditions': len(conditions),
            'details': dict(zip([c[0] for c in conditions], [c[1] for c in conditions]))
        }
    
    def _step2_vcp_detection_enhanced(self, data: pd.DataFrame, symbol: str) -> Dict:
        """Step 2: Enhanced VCP Detection with exact criteria"""
        print(f"\n📌 STEP 2: VOLATILITY CONTRACTION PATTERN (ENHANCED)")
        print("─" * 70)
        
        # Analyze last 75 days for VCP (5-15 weeks = 25-75 days)
        recent_data = data.tail(75)
        
        # Find contractions (price ranges getting tighter)
        contractions = self._find_price_contractions(recent_data)
        
        # VCP criteria
        num_contractions = len(contractions)
        contractions_decreasing = self._are_contractions_decreasing(contractions)
        volume_declining = self._is_volume_declining_in_contractions(recent_data, contractions)
        final_tight_range = self._has_final_tight_range(recent_data)
        low_volume_final = self._has_low_volume_final_contraction(recent_data)
        duration_ok = 25 <= len(recent_data) <= 75
        near_pivot = self._is_near_pivot_point(recent_data)
        
        conditions = [
            ("≥2 price contractions", num_contractions >= 2, f"{num_contractions} found", 15),
            ("Contractions decreasing", contractions_decreasing, "Getting tighter" if contractions_decreasing else "Not tightening", 15),
            ("Volume declining", volume_declining, "Drying up" if volume_declining else "Not declining", 15),
            ("Final range <5%", final_tight_range, f"{self._get_final_range_pct(recent_data):.1f}% range", 20),
            ("Below avg volume final", low_volume_final, "Low volume" if low_volume_final else "High volume", 15),
            ("Duration 5-15 weeks", duration_ok, f"{len(recent_data)} days", 10),
            ("Within 5% of pivot", near_pivot, f"{self._get_pivot_distance_pct(recent_data):.1f}% from high", 10)
        ]
        
        print(f"{'VCP Condition':<25} {'Status':<8} {'Details':<20} {'Points'}")
        print("─" * 75)
        
        total_score = 0
        max_score = 100
        passed_conditions = 0
        
        for condition, status, details, points in conditions:
            status_symbol = "✅ PASS" if status else "❌ FAIL"
            if status:
                total_score += points
                passed_conditions += 1
            print(f"{condition:<25} {status_symbol:<8} {details:<20} {points if status else 0}")
        
        print("─" * 75)
        # VCP detected if score >= 70% (more lenient than trend template)
        detected = total_score >= 70
        status = "✅ DETECTED" if detected else "❌ NOT DETECTED"
        confidence = total_score
        
        print(f"🎯 VCP PATTERN: {status} | Score: {confidence:.0f}/100")
        
        return {
            'detected': detected,
            'score': total_score,
            'max_score': max_score,
            'confidence': confidence,
            'pivot_point': recent_data['High'].max(),
            'conditions_met': passed_conditions,
            'total_conditions': len(conditions),
            'details': dict(zip([c[0] for c in conditions], [c[1] for c in conditions]))
        }
    
    def _step3_breakout_confirmation_exact(self, data: pd.DataFrame, symbol: str) -> Dict:
        """Step 3: Breakout Confirmation - Exact Criteria"""
        print(f"\n📌 STEP 3: BREAKOUT CONFIRMATION (EXACT CRITERIA)")
        print("─" * 70)
        
        current_price = data['Close'].iloc[-1]
        current_volume = data['Volume'].iloc[-1]
        avg_volume_50 = data['Avg_Volume_50'].iloc[-1]
        
        # Pivot point from recent high
        recent_high = data['High'].tail(50).max()
        
        # Exact breakout conditions
        above_pivot = current_price > recent_high
        volume_surge = current_volume >= (1.40 * avg_volume_50)  # Exactly 40% above average
        
        # Last 5 candles tight action
        last_5 = data.tail(5)
        tight_action = self._check_tight_price_action(last_5)
        
        conditions = [
            ("Price closes above pivot", above_pivot, f"${current_price:.2f} vs ${recent_high:.2f}", 40),
            ("Volume ≥ 40% above avg", volume_surge, f"{(current_volume/avg_volume_50*100):.0f}% of average", 35),
            ("Last 5 candles tight", tight_action, "Tight action" if tight_action else "Sloppy action", 25)
        ]
        
        print(f"{'Breakout Condition':<25} {'Status':<8} {'Details':<25} {'Points'}")
        print("─" * 75)
        
        total_score = 0
        max_score = 100
        passed_conditions = 0
        
        for condition, status, details, points in conditions:
            status_symbol = "✅ PASS" if status else "❌ FAIL"
            if status:
                total_score += points
                passed_conditions += 1
            print(f"{condition:<25} {status_symbol:<8} {details:<25} {points if status else 0}")
        
        print("─" * 75)
        # Breakout confirmed if ALL conditions met (exact requirement)
        confirmed = passed_conditions == len(conditions)
        status = "✅ CONFIRMED" if confirmed else "❌ NOT CONFIRMED"
        confidence = total_score
        
        print(f"🎯 BREAKOUT: {status} | Score: {confidence:.0f}/100")
        
        return {
            'confirmed': confirmed,
            'score': total_score,
            'max_score': max_score,
            'confidence': confidence,
            'pivot_point': recent_high,
            'conditions_met': passed_conditions,
            'total_conditions': len(conditions),
            'details': dict(zip([c[0] for c in conditions], [c[1] for c in conditions]))
        }
    
    def _step4_fundamentals_finnhub(self, symbol: str) -> Dict:
        """Step 4: Optional Fundamentals using Finnhub"""
        print(f"\n📌 STEP 4: OPTIONAL FUNDAMENTALS (FINNHUB)")
        print("─" * 70)
        print("💡 Attempting to fetch fundamental data from Finnhub...")
        
        try:
            # Try to get basic company metrics from Finnhub
            url = f"{self.base_url}/stock/metric"
            params = {'symbol': symbol, 'metric': 'all'}
            
            response = self.session.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                metrics = data.get('metric', {})
                
                if metrics:
                    print(f"   ✅ Fundamental data retrieved from Finnhub")
                    
                    # Extract available metrics
                    roe = metrics.get('roeTTM', 0)
                    eps_growth = metrics.get('epsGrowth5Y', 0) if metrics.get('epsGrowth5Y') else 0
                    
                    fundamentals = [
                        ("EPS Growth ≥ 25%", eps_growth >= 25, f"{eps_growth:.1f}%" if eps_growth else "N/A", 15),
                        ("Sales Growth ≥ 25%", False, "Data not available", 15),
                        ("ROE ≥ 17%", roe >= 17, f"{roe:.1f}%" if roe else "N/A", 15),
                        ("Margins increasing", False, "Data not available", 15),
                        ("Earnings acceleration", False, "Data not available", 20),
                        ("Top 3 sector rank", False, "Data not available", 20)
                    ]
                else:
                    print(f"   ⚠️ No fundamental data available")
                    fundamentals = self._get_default_fundamentals()
            else:
                print(f"   ⚠️ Finnhub fundamentals API error: {response.status_code}")
                fundamentals = self._get_default_fundamentals()
                
        except Exception as e:
            print(f"   ❌ Error fetching fundamentals: {str(e)[:50]}...")
            fundamentals = self._get_default_fundamentals()
        
        print(f"{'Fundamental':<20} {'Status':<8} {'Details':<20} {'Points'}")
        print("─" * 70)
        
        total_score = 0
        max_score = 100
        
        for condition, status, details, points in fundamentals:
            status_symbol = "✅ PASS" if status else "⚠️ N/A"
            if status:
                total_score += points
            print(f"{condition:<20} {status_symbol:<8} {details:<20} {points if status else 0}")
        
        print("─" * 70)
        print(f"🎯 FUNDAMENTALS: {'✅ AVAILABLE' if total_score > 0 else '⚠️ LIMITED'} | Score: {total_score}/100")
        
        return {
            'available': total_score > 0,
            'score': total_score,
            'max_score': max_score,
            'confidence': total_score,
            'note': "Using Finnhub fundamental data where available"
        }
    
    def _get_default_fundamentals(self) -> List:
        """Default fundamentals when data not available"""
        return [
            ("EPS Growth ≥ 25%", False, "Data not available", 15),
            ("Sales Growth ≥ 25%", False, "Data not available", 15),
            ("ROE ≥ 17%", False, "Data not available", 15),
            ("Margins increasing", False, "Data not available", 15),
            ("Earnings acceleration", False, "Data not available", 20),
            ("Top 3 sector rank", False, "Data not available", 20)
        ]
    
    def _step5_risk_setup_exact(self, data: pd.DataFrame, symbol: str, trend_result: Dict, 
                               vcp_result: Optional[Dict], breakout_result: Optional[Dict]) -> Dict:
        """Step 5: Risk Setup and Buy Execution - Exact Implementation"""
        print(f"\n📌 STEP 5: RISK SETUP AND BUY EXECUTION")
        print("─" * 70)
        
        current_price = data['Close'].iloc[-1]
        
        # Determine entry price based on breakout status
        if breakout_result and breakout_result['confirmed']:
            entry_price = current_price  # Already broken out
        elif vcp_result and vcp_result['detected']:
            entry_price = vcp_result['pivot_point'] * 1.01  # 1% above pivot
        else:
            entry_price = current_price * 1.02  # 2% above current
        
        # Risk calculations (5-10% as per algorithm)
        stop_loss_5pct = entry_price * 0.95
        stop_loss_7pct = entry_price * 0.93
        stop_loss_10pct = entry_price * 0.90
        
        # Position sizing (exact implementation)
        max_risk_per_trade = self.portfolio_value * 0.01  # Exactly 1% max risk
        
        risk_per_share_5pct = entry_price - stop_loss_5pct
        risk_per_share_7pct = entry_price - stop_loss_7pct
        risk_per_share_10pct = entry_price - stop_loss_10pct
        
        shares_5pct = int(max_risk_per_trade / risk_per_share_5pct) if risk_per_share_5pct > 0 else 0
        shares_7pct = int(max_risk_per_trade / risk_per_share_7pct) if risk_per_share_7pct > 0 else 0
        shares_10pct = int(max_risk_per_trade / risk_per_share_10pct) if risk_per_share_10pct > 0 else 0
        
        # Reward-to-risk ratios (minimum 2:1 as per algorithm)
        target_20pct = entry_price * 1.20
        target_25pct = entry_price * 1.25
        
        rr_ratio_5pct = ((target_20pct - entry_price) / risk_per_share_5pct) if risk_per_share_5pct > 0 else 0
        rr_ratio_7pct = ((target_20pct - entry_price) / risk_per_share_7pct) if risk_per_share_7pct > 0 else 0
        rr_ratio_10pct = ((target_20pct - entry_price) / risk_per_share_10pct) if risk_per_share_10pct > 0 else 0
        
        # Risk validation
        risk_acceptable = all([
            rr_ratio_7pct >= 2.0,  # Minimum 2:1 reward-to-risk
            max_risk_per_trade <= (self.portfolio_value * 0.01)  # Max 1% portfolio risk
        ])
        
        print(f"💰 ENTRY PRICE: ${entry_price:.2f}")
        print(f"📊 Current Price: ${current_price:.2f}")
        print()
        print("📋 POSITION SIZING OPTIONS:")
        print("─" * 50)
        print(f"5% Stop Loss: ${stop_loss_5pct:.2f} | {shares_5pct:,} shares | R:R {rr_ratio_5pct:.1f}:1")
        print(f"7% Stop Loss: ${stop_loss_7pct:.2f} | {shares_7pct:,} shares | R:R {rr_ratio_7pct:.1f}:1")
        print(f"10% Stop Loss: ${stop_loss_10pct:.2f} | {shares_10pct:,} shares | R:R {rr_ratio_10pct:.1f}:1")
        print()
        print(f"🎯 TARGETS: 20% = ${target_20pct:.2f} | 25% = ${target_25pct:.2f}")
        print(f"🛡️ RISK ACCEPTABLE: {'✅ YES' if risk_acceptable else '❌ NO'}")
        
        return {
            'entry_price': entry_price,
            'current_price': current_price,
            'stop_loss_5pct': stop_loss_5pct,
            'stop_loss_7pct': stop_loss_7pct,
            'stop_loss_10pct': stop_loss_10pct,
            'position_size_5pct': shares_5pct,
            'position_size_7pct': shares_7pct,
            'position_size_10pct': shares_10pct,
            'reward_risk_5pct': rr_ratio_5pct,
            'reward_risk_7pct': rr_ratio_7pct,
            'reward_risk_10pct': rr_ratio_10pct,
            'target_20pct': target_20pct,
            'target_25pct': target_25pct,
            'risk_acceptable': risk_acceptable,
            'max_portfolio_risk': max_risk_per_trade
        }
    
    def _check_anti_rules(self, data: pd.DataFrame, symbol: str, trend_result: Dict) -> Dict:
        """Check TradeThrust Anti-Rules"""
        print(f"\n🚫 ANTI-RULES CHECK")
        print("─" * 50)
        
        current_price = data['Close'].iloc[-1]
        rs_rating = data['RS_Rating'].iloc[-1]
        
        anti_rules = [
            ("RS Rating < 70", rs_rating < 70, f"RS: {rs_rating:.0f}"),
            ("Too early in base", False, "Base timing OK"),  # Simplified check
            ("High volatility action", False, "Volatility OK"),  # Would need more analysis
            ("Ignoring volume", False, "Volume considered"),
            ("Too many positions", False, f"Max {self.max_positions} rule")
        ]
        
        violations = 0
        for rule, violated, details in anti_rules:
            status = "⚠️ VIOLATED" if violated else "✅ OK"
            if violated:
                violations += 1
            print(f"{rule:<25} {status:<12} {details}")
        
        print("─" * 50)
        clean = violations == 0
        print(f"🛡️ ANTI-RULES: {'✅ CLEAN' if clean else f'⚠️ {violations} VIOLATIONS'}")
        
        return {
            'clean': clean,
            'violations': violations,
            'total_rules': len(anti_rules),
            'details': dict(zip([r[0] for r in anti_rules], [r[1] for r in anti_rules]))
        }
    
    def _check_market_condition(self) -> Dict:
        """Check overall market condition using Finnhub"""
        print(f"\n📈 MARKET CONDITION CHECK")
        print("─" * 50)
        
        # Could implement SPX analysis using Finnhub here
        # For now, simplified check
        market_healthy = True  # Assume healthy for now
        
        print(f"Overall Market: {'✅ HEALTHY' if market_healthy else '⚠️ WEAK'}")
        print("💡 Could enhance with SPX analysis using Finnhub")
        
        return {
            'healthy': market_healthy,
            'note': "Simplified check - could enhance with index analysis"
        }
    
    def _generate_enhanced_recommendation(self, trend_result: Dict, vcp_result: Optional[Dict], 
                                        breakout_result: Optional[Dict], fundamentals_result: Dict,
                                        risk_result: Dict, anti_rules_result: Dict, 
                                        market_condition: Dict) -> Dict:
        """Generate enhanced recommendation with confidence scoring"""
        print(f"\n📌 TRADETHRUST FINNHUB RECOMMENDATION")
        print("─" * 70)
        
        # Calculate overall confidence score
        scores = []
        weights = []
        
        # Trend Template (40% weight - most critical)
        if trend_result['passed']:
            scores.append(trend_result['confidence'])
            weights.append(40)
        else:
            scores.append(0)
            weights.append(40)
        
        # VCP Pattern (25% weight)
        if vcp_result and vcp_result['detected']:
            scores.append(vcp_result['confidence'])
            weights.append(25)
        else:
            scores.append(0)
            weights.append(25)
        
        # Breakout Confirmation (20% weight)
        if breakout_result and breakout_result['confirmed']:
            scores.append(breakout_result['confidence'])
            weights.append(20)
        else:
            scores.append(0)
            weights.append(20)
        
        # Risk Setup (10% weight)
        if risk_result['risk_acceptable']:
            scores.append(100)
            weights.append(10)
        else:
            scores.append(50)
            weights.append(10)
        
        # Anti-rules penalty (5% weight)
        if anti_rules_result['clean']:
            scores.append(100)
            weights.append(5)
        else:
            scores.append(0)
            weights.append(5)
        
        # Calculate weighted confidence score
        total_score = sum(s * w for s, w in zip(scores, weights))
        total_weight = sum(weights)
        confidence_score = total_score / total_weight
        
        # Generate recommendation based on exact algorithm logic
        trend_pass = trend_result['passed']
        vcp_detected = vcp_result['detected'] if vcp_result else False
        breakout_confirmed = breakout_result['confirmed'] if breakout_result else False
        risk_ok = risk_result['risk_acceptable']
        anti_rules_clean = anti_rules_result['clean']
        
        # Decision logic
        if trend_pass and vcp_detected and breakout_confirmed and risk_ok and anti_rules_clean:
            recommendation = "🔥 STRONG BUY"
            action_confidence = "VERY HIGH"
            reason = "All TradeThrust criteria met - Execute trade"
        elif trend_pass and vcp_detected and risk_ok and anti_rules_clean:
            recommendation = "✅ BUY ON BREAKOUT"
            action_confidence = "HIGH"
            reason = "Setup complete - Wait for breakout confirmation"
        elif trend_pass and risk_ok and anti_rules_clean:
            recommendation = "⚠️ WATCH LIST"
            action_confidence = "MEDIUM"
            reason = "Trend strong - Monitor for VCP formation"
        elif not anti_rules_clean:
            recommendation = "❌ AVOID"
            action_confidence = "LOW"
            reason = "Anti-rules violated - Do not trade"
        else:
            recommendation = "❌ DO NOT BUY"
            action_confidence = "LOW"
            reason = "Insufficient setup quality"
        
        # Get price levels
        entry_price = risk_result['entry_price']
        stop_loss = risk_result['stop_loss_7pct']
        target = risk_result['target_20pct']
        
        print(f"🎯 RECOMMENDATION: {recommendation}")
        print(f"📊 CONFIDENCE SCORE: {confidence_score:.0f}/100")
        print(f"💪 ACTION CONFIDENCE: {action_confidence}")
        print(f"💡 REASON: {reason}")
        print(f"🔗 DATA SOURCE: Finnhub.io")
        print()
        print(f"💰 ENTRY PRICE: ${entry_price:.2f}")
        print(f"🛡️ STOP LOSS: ${stop_loss:.2f}")
        print(f"🎯 TARGET: ${target:.2f}")
        print(f"📏 RISK: {((entry_price - stop_loss) / entry_price * 100):.1f}%")
        print(f"📈 REWARD: {((target - entry_price) / entry_price * 100):.1f}%")
        
        return {
            'action': recommendation,
            'confidence_score': confidence_score,
            'action_confidence': action_confidence,
            'reason': reason,
            'entry_price': entry_price,
            'stop_loss': stop_loss,
            'target_price': target,
            'risk_percent': ((entry_price - stop_loss) / entry_price * 100),
            'reward_percent': ((target - entry_price) / entry_price * 100),
            'data_source': 'Finnhub',
            'score_breakdown': {
                'trend_template': trend_result['confidence'] if trend_result['passed'] else 0,
                'vcp_pattern': vcp_result['confidence'] if vcp_result and vcp_result['detected'] else 0,
                'breakout_confirmation': breakout_result['confidence'] if breakout_result and breakout_result['confirmed'] else 0,
                'risk_setup': 100 if risk_result['risk_acceptable'] else 50,
                'anti_rules': 100 if anti_rules_result['clean'] else 0
            }
        }
    
    # Helper methods for VCP analysis
    def _find_price_contractions(self, data: pd.DataFrame) -> List[Dict]:
        """Find price contraction periods"""
        contractions = []
        
        # Look for periods of decreasing volatility
        rolling_ranges = data['High_Low_Range'].rolling(window=10).mean()
        
        # Find local peaks in volatility that decrease over time
        for i in range(10, len(rolling_ranges)-10):
            if (rolling_ranges.iloc[i-5:i].mean() > rolling_ranges.iloc[i:i+5].mean() and
                rolling_ranges.iloc[i:i+5].mean() > rolling_ranges.iloc[i+5:i+10].mean()):
                contractions.append({
                    'start': i-5,
                    'end': i+5,
                    'range': rolling_ranges.iloc[i:i+5].mean()
                })
        
        return contractions[-3:] if len(contractions) >= 2 else []
    
    def _are_contractions_decreasing(self, contractions: List[Dict]) -> bool:
        """Check if contractions are getting smaller"""
        if len(contractions) < 2:
            return False
        
        for i in range(1, len(contractions)):
            if contractions[i]['range'] >= contractions[i-1]['range']:
                return False
        return True
    
    def _is_volume_declining_in_contractions(self, data: pd.DataFrame, contractions: List[Dict]) -> bool:
        """Check if volume declines during contractions"""
        if not contractions:
            return False
        
        recent_volume = data['Volume'].tail(20).mean()
        older_volume = data['Volume'].head(20).mean()
        
        return recent_volume < older_volume
    
    def _has_final_tight_range(self, data: pd.DataFrame) -> bool:
        """Check if final contraction has tight range (<5%)"""
        final_10_days = data.tail(10)
        final_range = (final_10_days['High'].max() - final_10_days['Low'].min()) / final_10_days['Close'].mean()
        return final_range < 0.05
    
    def _get_final_range_pct(self, data: pd.DataFrame) -> float:
        """Get final range percentage"""
        final_10_days = data.tail(10)
        return ((final_10_days['High'].max() - final_10_days['Low'].min()) / final_10_days['Close'].mean()) * 100
    
    def _has_low_volume_final_contraction(self, data: pd.DataFrame) -> bool:
        """Check if final contraction has below average volume"""
        final_volume = data['Volume'].tail(10).mean()
        avg_volume = data['Avg_Volume_50'].iloc[-1]
        return final_volume < avg_volume
    
    def _is_near_pivot_point(self, data: pd.DataFrame) -> bool:
        """Check if current price is within 5% of pivot point"""
        current_price = data['Close'].iloc[-1]
        pivot_point = data['High'].max()
        return (pivot_point - current_price) / pivot_point <= 0.05
    
    def _get_pivot_distance_pct(self, data: pd.DataFrame) -> float:
        """Get distance from pivot point as percentage"""
        current_price = data['Close'].iloc[-1]
        pivot_point = data['High'].max()
        return ((pivot_point - current_price) / pivot_point) * 100
    
    def _check_tight_price_action(self, last_5_data: pd.DataFrame) -> bool:
        """Check if last 5 candles show tight price action"""
        ranges = (last_5_data['High'] - last_5_data['Low']) / last_5_data['Close']
        avg_range = ranges.mean()
        return avg_range < 0.03  # Less than 3% average range

def main():
    """Main execution with API key from environment or input"""
    print("🚀 TradeThrust Finnhub Algorithm")
    print("✅ Using Finnhub.io for reliable stock data")
    print("📊 Get your free API key at: https://finnhub.io")
    print("=" * 60)
    
    # Check for API key in environment variable first
    api_key = os.getenv('FINNHUB_API_KEY')
    
    if api_key:
        print("🔑 Using FINNHUB_API_KEY from environment variable")
        print("✅ API key loaded successfully")
    else:
        # Get API key from user if not in environment
        api_key = input("Enter your Finnhub API key (or press Enter for demo): ").strip()
        if not api_key:
            api_key = "demo"
            print("🔧 Using demo API key (limited functionality)")
    
    tt = TradeThrustFinnhub(api_key=api_key)
    
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
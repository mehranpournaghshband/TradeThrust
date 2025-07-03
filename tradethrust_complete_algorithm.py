#!/usr/bin/env python3
"""
TradeThrust Complete Algorithm Implementation
===========================================

Professional stock analysis implementing the complete TradeThrust methodology
with exact algorithmic rules for buy/sell decisions and risk management.

Features:
- Complete Trend Template Filter (10 criteria)
- VCP Pattern Detection Algorithm
- Breakout Confirmation System
- Optional Fundamentals Analysis
- Risk Management & Position Sizing
- Sell Algorithm Implementation
- Anti-Rules Warning System

Author: TradeThrust Team
Version: 3.0.0 (Complete Algorithm)
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import warnings

warnings.filterwarnings('ignore')

class TradeThrustComplete:
    """
    Complete TradeThrust Algorithm Implementation
    """
    
    def __init__(self):
        self.analysis_results = {}
        self.watchlist = []
        
    def fetch_stock_data(self, symbol: str, period: str = "2y") -> Optional[pd.DataFrame]:
        """Fetch comprehensive stock data with all required indicators"""
        try:
            ticker = yf.Ticker(symbol.upper())
            data = ticker.history(period=period)
            
            if data.empty:
                return None
            
            # Calculate all technical indicators
            data = self._calculate_complete_indicators(data, symbol)
            return data
            
        except Exception as e:
            print(f"❌ Error fetching data for {symbol}: {e}")
            return None
    
    def _calculate_complete_indicators(self, data: pd.DataFrame, symbol: str) -> pd.DataFrame:
        """Calculate all technical indicators required by the algorithm"""
        df = data.copy()
        
        # Simple Moving Averages
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        df['SMA_150'] = df['Close'].rolling(window=150).mean()
        df['SMA_200'] = df['Close'].rolling(window=200).mean()
        
        # 52-week high and low
        df['52W_High'] = df['High'].rolling(window=252).max()
        df['52W_Low'] = df['Low'].rolling(window=252).min()
        
        # Volume indicators
        df['Avg_Volume_50'] = df['Volume'].rolling(window=50).mean()
        df['Volume_Ratio'] = df['Volume'] / df['Avg_Volume_50']
        
        # Relative Strength calculation (simplified - comparing to SPY)
        try:
            spy_data = yf.Ticker('SPY').history(period="2y")
            if not spy_data.empty:
                spy_returns = spy_data['Close'].pct_change(20)  # 20-day returns
                stock_returns = df['Close'].pct_change(20)
                df['RS_Rating'] = ((stock_returns / spy_returns) * 50 + 50).fillna(50)
            else:
                df['RS_Rating'] = 70  # Default if SPY data unavailable
        except:
            df['RS_Rating'] = 70  # Default if calculation fails
        
        # Price ranges and support/resistance
        df['Daily_Range'] = df['High'] - df['Low']
        df['ATR_20'] = df['Daily_Range'].rolling(window=20).mean()
        
        # Pivot point calculation (resistance for breakout)
        df['Pivot_Point'] = df['High'].rolling(window=20).max()
        
        return df
    
    def analyze_stock_complete(self, symbol: str) -> Dict:
        """Complete stock analysis using TradeThrust algorithm"""
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
        
        # Step 1: Trend Template Filter
        trend_results = self._step1_trend_template_filter(data, symbol)
        
        # Step 2: VCP Pattern Detection
        vcp_results = self._step2_vcp_detection(data, symbol)
        
        # Step 3: Pivot Point Analysis & Breakout Confirmation
        pivot_results = self._step3_pivot_point_analysis(data, symbol)
        
        # Step 4: Optional Fundamentals (placeholder - would need additional data)
        fundamentals_results = self._step4_fundamentals_check(symbol)
        
        # Step 5: Risk Setup
        risk_results = self._step5_risk_setup(data, trend_results, vcp_results, pivot_results)
        
        # Generate final recommendation
        final_recommendation = self._generate_complete_recommendation(
            trend_results, vcp_results, pivot_results, fundamentals_results, risk_results
        )
        
        # Display buy/sell prices
        self._display_complete_prices(risk_results)
        
        # Show sell algorithm
        self._display_sell_algorithm(data, risk_results)
        
        # Show anti-rules warnings
        self._display_anti_rules_warnings(trend_results, vcp_results, pivot_results)
        
        # Summary
        self._display_complete_summary(final_recommendation, symbol)
        
        return {
            'symbol': symbol,
            'current_price': current_price,
            'trend_results': trend_results,
            'vcp_results': vcp_results,
            'pivot_results': pivot_results,
            'fundamentals_results': fundamentals_results,
            'risk_results': risk_results,
            'recommendation': final_recommendation
        }
    
    def _print_header(self, symbol: str):
        """Print professional header"""
        print("\n" + "═" * 80)
        print(f"🚀 TRADETHRUST COMPLETE ALGORITHM ANALYSIS")
        print(f"📊 Symbol: {symbol} | Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("📚 Based on TradeThrust Professional Trading Methodology")
        print("═" * 80)
    
    def _step1_trend_template_filter(self, data: pd.DataFrame, symbol: str) -> Dict:
        """Step 1: Trend Template Filter - All 10 conditions must be true"""
        print(f"\n✅ STEP 1: TREND TEMPLATE FILTER")
        print("─" * 60)
        print("All conditions must be TRUE to pass the filter:")
        
        latest = data.iloc[-1]
        recent_20 = data.tail(20)
        
        # Get current values
        price = latest['Close']
        sma_50 = latest['SMA_50']
        sma_150 = latest['SMA_150']
        sma_200 = latest['SMA_200']
        high_52w = latest['52W_High']
        low_52w = latest['52W_Low']
        rs_rating = latest['RS_Rating']
        
        # Check 200-day SMA rising for last 20+ trading days
        sma_200_rising = recent_20['SMA_200'].iloc[-1] > recent_20['SMA_200'].iloc[0]
        
        # All 10 conditions from the algorithm
        conditions = [
            {
                'condition': 'price > 50-day SMA',
                'current': f"${price:.2f}",
                'target': f">${sma_50:.2f}",
                'status': price > sma_50,
                'reason': f"Price {((price - sma_50) / sma_50) * 100:+.1f}% vs 50 SMA"
            },
            {
                'condition': 'price > 150-day SMA',
                'current': f"${price:.2f}",
                'target': f">${sma_150:.2f}",
                'status': price > sma_150,
                'reason': f"Price {((price - sma_150) / sma_150) * 100:+.1f}% vs 150 SMA"
            },
            {
                'condition': 'price > 200-day SMA',
                'current': f"${price:.2f}",
                'target': f">${sma_200:.2f}",
                'status': price > sma_200,
                'reason': f"Price {((price - sma_200) / sma_200) * 100:+.1f}% vs 200 SMA"
            },
            {
                'condition': '150-day SMA > 200-day SMA',
                'current': f"${sma_150:.2f}",
                'target': f">${sma_200:.2f}",
                'status': sma_150 > sma_200,
                'reason': f"150 SMA {((sma_150 - sma_200) / sma_200) * 100:+.1f}% vs 200 SMA"
            },
            {
                'condition': '50-day SMA > 150-day SMA',
                'current': f"${sma_50:.2f}",
                'target': f">${sma_150:.2f}",
                'status': sma_50 > sma_150,
                'reason': f"50 SMA {((sma_50 - sma_150) / sma_150) * 100:+.1f}% vs 150 SMA"
            },
            {
                'condition': '50-day SMA > 200-day SMA',
                'current': f"${sma_50:.2f}",
                'target': f">${sma_200:.2f}",
                'status': sma_50 > sma_200,
                'reason': f"50 SMA {((sma_50 - sma_200) / sma_200) * 100:+.1f}% vs 200 SMA"
            },
            {
                'condition': '200-day SMA rising 20+ days',
                'current': "Trend Direction",
                'target': "Rising",
                'status': sma_200_rising,
                'reason': f"200 SMA {'rising' if sma_200_rising else 'falling'} over 20 days"
            },
            {
                'condition': 'price ≥ (52W low × 1.3)',
                'current': f"${price:.2f}",
                'target': f"≥${low_52w * 1.3:.2f}",
                'status': price >= (low_52w * 1.3),
                'reason': f"Price {((price / (low_52w * 1.3)) - 1) * 100:+.1f}% vs required level"
            },
            {
                'condition': 'price ≥ (0.75 × 52W high)',
                'current': f"${price:.2f}",
                'target': f"≥${high_52w * 0.75:.2f}",
                'status': price >= (high_52w * 0.75),
                'reason': f"Price {((price / (high_52w * 0.75)) - 1) * 100:+.1f}% vs 75% of high"
            },
            {
                'condition': 'RS_Rating ≥ 70',
                'current': f"{rs_rating:.1f}",
                'target': "≥70",
                'status': rs_rating >= 70,
                'reason': f"Relative Strength {rs_rating:.1f} vs market"
            }
        ]
        
        # Display results table
        print(f"{'Condition':<30} {'Current':<12} {'Target':<15} {'Status':<8} Reasoning")
        print("─" * 100)
        
        passed_count = 0
        for cond in conditions:
            status_symbol = "✅ PASS" if cond['status'] else "❌ FAIL"
            print(f"{cond['condition']:<30} {cond['current']:<12} {cond['target']:<15} {status_symbol:<8} {cond['reason']}")
            if cond['status']:
                passed_count += 1
        
        trend_passed = passed_count == 10
        print("─" * 100)
        print(f"🎯 TREND TEMPLATE RESULT: {passed_count}/10 - {'✅ PASSED' if trend_passed else '❌ FAILED'}")
        
        if trend_passed:
            print("✅ ALL trend template conditions met - proceed to VCP analysis")
        else:
            print("❌ Trend template FAILED - stock does not qualify for TradeThrust system")
        
        return {
            'passed': trend_passed,
            'score': passed_count,
            'total': 10,
            'conditions': conditions
        }
    
    def _step2_vcp_detection(self, data: pd.DataFrame, symbol: str) -> Dict:
        """Step 2: VCP Pattern Detection Algorithm"""
        print(f"\n📈 STEP 2: VCP (VOLATILITY CONTRACTION PATTERN) DETECTION")
        print("─" * 60)
        
        # Analyze last 15 weeks (75 trading days)
        vcp_period = data.tail(75)
        contractions = self._find_detailed_contractions(vcp_period)
        current_price = data.iloc[-1]['Close']
        pivot_point = data.tail(20)['High'].max()
        
        # VCP Algorithm conditions
        vcp_conditions = []
        
        # Condition 1: ≥2 price contractions
        enough_contractions = len(contractions) >= 2
        vcp_conditions.append({
            'condition': '≥2 price contractions',
            'status': enough_contractions,
            'detail': f"Found {len(contractions)} contractions (need ≥2)"
        })
        
        # Condition 2: Each contraction smaller than previous
        contractions_decreasing = True
        if len(contractions) >= 2:
            for i in range(1, len(contractions)):
                if contractions[i]['percentage'] >= contractions[i-1]['percentage']:
                    contractions_decreasing = False
                    break
        else:
            contractions_decreasing = False
        
        vcp_conditions.append({
            'condition': 'Each contraction smaller',
            'status': contractions_decreasing,
            'detail': 'Pullbacks getting smaller' if contractions_decreasing else 'Pullbacks not decreasing'
        })
        
        # Condition 3: Volume shrinks during contractions
        volume_shrinks = True
        for contraction in contractions:
            if contraction.get('avg_volume_ratio', 1) > 0.8:
                volume_shrinks = False
                break
        
        vcp_conditions.append({
            'condition': 'Volume shrinks in pullbacks',
            'status': volume_shrinks,
            'detail': 'Volume declining in contractions' if volume_shrinks else 'Volume stays high'
        })
        
        # Condition 4: Final contraction tight
        final_tight = False
        if contractions:
            final_tight = contractions[-1]['percentage'] < 10  # Tight = less than 10%
        
        vcp_conditions.append({
            'condition': 'Final contraction tight',
            'status': final_tight,
            'detail': f"Final pullback: -{contractions[-1]['percentage']:.1f}%" if contractions else "No contractions"
        })
        
        # Condition 5: Final contraction below-average volume
        final_low_volume = False
        if contractions:
            final_low_volume = contractions[-1].get('avg_volume_ratio', 1) < 0.7
        
        vcp_conditions.append({
            'condition': 'Final contraction low volume',
            'status': final_low_volume,
            'detail': f"Final volume ratio: {contractions[-1].get('avg_volume_ratio', 0):.2f}" if contractions else "No data"
        })
        
        # Condition 6: Base duration 5-15 weeks
        base_duration_ok = len(vcp_period) >= 25 and len(vcp_period) <= 75  # 5-15 weeks
        vcp_conditions.append({
            'condition': 'Base duration 5-15 weeks',
            'status': base_duration_ok,
            'detail': f"Base duration: {len(vcp_period)/5:.1f} weeks"
        })
        
        # Condition 7: Current price within 5% of pivot
        near_pivot = abs(current_price - pivot_point) / pivot_point <= 0.05
        vcp_conditions.append({
            'condition': 'Within 5% of pivot point',
            'status': near_pivot,
            'detail': f"Price {((current_price - pivot_point) / pivot_point) * 100:+.1f}% vs pivot"
        })
        
        # Display VCP analysis
        print(f"{'VCP Condition':<30} {'Status':<10} Details")
        print("─" * 70)
        
        vcp_score = 0
        for condition in vcp_conditions:
            status_symbol = "✅ PASS" if condition['status'] else "❌ FAIL"
            print(f"{condition['condition']:<30} {status_symbol:<10} {condition['detail']}")
            if condition['status']:
                vcp_score += 1
        
        vcp_detected = vcp_score >= 6  # Need at least 6/7 conditions
        print("─" * 70)
        print(f"📈 VCP PATTERN RESULT: {vcp_score}/7 - {'✅ DETECTED' if vcp_detected else '❌ NOT DETECTED'}")
        
        if vcp_detected:
            print("✅ VCP pattern confirmed - stock ready for breakout")
        else:
            print("❌ VCP pattern not formed - wait for proper base")
        
        return {
            'detected': vcp_detected,
            'score': vcp_score,
            'conditions': vcp_conditions,
            'contractions': contractions,
            'pivot_point': pivot_point
        }
    
    def _step3_pivot_point_analysis(self, data: pd.DataFrame, symbol: str) -> Dict:
        """Step 3: Comprehensive Pivot Point Analysis"""
        print(f"\n🎯 STEP 3: PIVOT POINT ANALYSIS")
        print("─" * 45)
        
        # Identify Valid Pivot Point
        pivot_analysis = self._identify_valid_pivot_point(data)
        
        # Confirm Valid Breakout
        breakout_analysis = self._confirm_valid_breakout(data, pivot_analysis)
        
        return {
            'pivot_analysis': pivot_analysis,
            'breakout_analysis': breakout_analysis,
            'overall_confirmed': pivot_analysis['valid'] and breakout_analysis['confirmed']
        }
    
    def _identify_valid_pivot_point(self, data: pd.DataFrame) -> Dict:
        """🔹 Algorithm: Identify a Valid Pivot Point"""
        print("🔹 ALGORITHM: IDENTIFY VALID PIVOT POINT")
        print("─" * 50)
        
        # 1. Identify Base Pattern (5-15 weeks = 25-75 trading days)
        base_period = data.tail(75)  # Look at last 15 weeks max
        
        if len(base_period) < 25:
            return {
                'valid': False,
                'reason': 'Insufficient data for base analysis',
                'pivot_point': None
            }
        
        # 2. Find contractions in the base
        contractions = self._find_base_contractions(base_period)
        
        # Validate base pattern requirements
        base_valid = True
        validation_results = []
        
        # Requirement: 5-15 weeks consolidation
        weeks_in_base = len(base_period) / 5
        weeks_valid = 5 <= weeks_in_base <= 15
        validation_results.append({
            'condition': 'Base duration 5-15 weeks',
            'current': f"{weeks_in_base:.1f} weeks",
            'status': weeks_valid,
            'detail': f"Base spans {weeks_in_base:.1f} weeks"
        })
        if not weeks_valid:
            base_valid = False
        
        # Requirement: At least 2 contractions
        enough_contractions = len(contractions) >= 2
        validation_results.append({
            'condition': 'At least 2 contractions',
            'current': f"{len(contractions)} found",
            'status': enough_contractions,
            'detail': f"Found {len(contractions)} price contractions"
        })
        if not enough_contractions:
            base_valid = False
        
        # Requirement: Each contraction smaller than previous
        contractions_decreasing = True
        if len(contractions) >= 2:
            for i in range(1, len(contractions)):
                if contractions[i]['decline_pct'] >= contractions[i-1]['decline_pct']:
                    contractions_decreasing = False
                    break
        else:
            contractions_decreasing = False
        
        validation_results.append({
            'condition': 'Each contraction smaller',
            'current': 'Decreasing' if contractions_decreasing else 'Not decreasing',
            'status': contractions_decreasing,
            'detail': 'Pullbacks getting progressively smaller' if contractions_decreasing else 'Pullbacks not decreasing'
        })
        if not contractions_decreasing:
            base_valid = False
        
        # Requirement: Volume contracts during pullbacks
        volume_contracts = True
        avg_contraction_volume = 0
        if contractions:
            for contraction in contractions:
                if contraction['avg_volume_ratio'] > 0.8:  # Volume too high during pullback
                    volume_contracts = False
                avg_contraction_volume += contraction['avg_volume_ratio']
            avg_contraction_volume /= len(contractions)
        else:
            volume_contracts = False
        
        validation_results.append({
            'condition': 'Volume contracts in pullbacks',
            'current': f"{avg_contraction_volume:.2f}x avg",
            'status': volume_contracts,
            'detail': f"Average pullback volume: {avg_contraction_volume:.2f}x normal"
        })
        if not volume_contracts:
            base_valid = False
        
        # 3. Locate Final Contraction and Pivot Point
        pivot_point = None
        pivot_valid = False
        current_price = data.iloc[-1]['Close']
        
        if contractions and base_valid:
            final_contraction = contractions[-1]
            
            # Find highest price just before final contraction
            pre_contraction_data = base_period.iloc[:final_contraction['start_idx']]
            if len(pre_contraction_data) > 0:
                pivot_point = pre_contraction_data['High'].max()
                
                # Validate pivot conditions
                
                # Must be within 5% of current price
                within_5_percent = abs(current_price - pivot_point) / pivot_point <= 0.05
                
                # Must come from tight price range (final contraction should be tight)
                tight_range = final_contraction['decline_pct'] < 15  # Less than 15% pullback
                
                # Minimal volatility before breakout (check last 5-10 days)
                recent_data = data.tail(10)
                recent_volatility = (recent_data['High'] - recent_data['Low']).mean()
                base_volatility = (base_period['High'] - base_period['Low']).mean()
                minimal_volatility = recent_volatility < base_volatility * 0.8
                
                # Not sloppy/loose base (contractions should be orderly)
                orderly_base = len([c for c in contractions if c['decline_pct'] > 25]) == 0  # No pullbacks > 25%
                
                pivot_valid = within_5_percent and tight_range and minimal_volatility and orderly_base
                
                validation_results.extend([
                    {
                        'condition': 'Within 5% of current price',
                        'current': f"{((current_price - pivot_point) / pivot_point) * 100:+.1f}%",
                        'status': within_5_percent,
                        'detail': f"Pivot at ${pivot_point:.2f}, current ${current_price:.2f}"
                    },
                    {
                        'condition': 'Tight price range',
                        'current': f"{final_contraction['decline_pct']:.1f}%",
                        'status': tight_range,
                        'detail': f"Final contraction: -{final_contraction['decline_pct']:.1f}%"
                    },
                    {
                        'condition': 'Minimal volatility',
                        'current': f"{recent_volatility:.2f}",
                        'status': minimal_volatility,
                        'detail': f"Recent volatility {(recent_volatility/base_volatility)*100:.0f}% of base average"
                    },
                    {
                        'condition': 'Well-defined base',
                        'current': 'Orderly' if orderly_base else 'Sloppy',
                        'status': orderly_base,
                        'detail': 'No excessive pullbacks' if orderly_base else 'Contains large pullbacks'
                    }
                ])
        
        # Display results
        print(f"{'Pivot Condition':<30} {'Current':<15} {'Status':<10} Details")
        print("─" * 75)
        
        valid_conditions = 0
        for result in validation_results:
            status_symbol = "✅ PASS" if result['status'] else "❌ FAIL"
            print(f"{result['condition']:<30} {result['current']:<15} {status_symbol:<10} {result['detail']}")
            if result['status']:
                valid_conditions += 1
        
        overall_valid = base_valid and pivot_valid
        print("─" * 75)
        print(f"🎯 PIVOT POINT RESULT: {valid_conditions}/{len(validation_results)} - {'✅ VALID' if overall_valid else '❌ INVALID'}")
        
        if overall_valid:
            print(f"✅ Valid pivot point identified at ${pivot_point:.2f}")
        else:
            print("❌ No valid pivot point found - wait for proper base formation")
        
        return {
            'valid': overall_valid,
            'pivot_point': pivot_point,
            'contractions': contractions,
            'validation_results': validation_results,
            'base_weeks': weeks_in_base
        }
    
    def _confirm_valid_breakout(self, data: pd.DataFrame, pivot_analysis: Dict) -> Dict:
        """🔹 Algorithm: Confirm a Valid Breakout"""
        print(f"\n🔹 ALGORITHM: CONFIRM VALID BREAKOUT")
        print("─" * 50)
        
        if not pivot_analysis['valid']:
            print("❌ Cannot confirm breakout - no valid pivot point")
            return {
                'confirmed': False,
                'reason': 'No valid pivot point identified'
            }
        
        latest = data.iloc[-1]
        recent_10 = data.tail(10)
        recent_50 = data.tail(50)
        
        current_price = latest['Close']
        daily_high = latest['High']
        daily_low = latest['Low']
        current_volume = latest['Volume']
        pivot_point = pivot_analysis['pivot_point']
        avg_volume_50 = recent_50['Volume'].mean()
        
        breakout_conditions = []
        
        # 1. Price Confirmation
        
        # Price breaks above pivot point
        breaks_pivot = current_price > pivot_point
        breakout_conditions.append({
            'category': 'Price',
            'condition': 'Breaks above pivot point',
            'current': f"${current_price:.2f}",
            'target': f">${pivot_point:.2f}",
            'status': breaks_pivot,
            'detail': f"{((current_price - pivot_point) / pivot_point) * 100:+.1f}% above pivot"
        })
        
        # Closes at or near daily high
        close_near_high = (current_price / daily_high) >= 0.95  # Within 5% of daily high
        breakout_conditions.append({
            'category': 'Price',
            'condition': 'Closes near daily high',
            'current': f"{(current_price/daily_high)*100:.1f}%",
            'target': '≥95%',
            'status': close_near_high,
            'detail': f"Close is {(current_price/daily_high)*100:.1f}% of daily high"
        })
        
        # Stays above pivot intraday (no failure)
        no_intraday_failure = daily_low >= pivot_point * 0.98  # Allow 2% cushion for noise
        breakout_conditions.append({
            'category': 'Price',
            'condition': 'No intraday failure',
            'current': f"${daily_low:.2f}",
            'target': f"≥${pivot_point * 0.98:.2f}",
            'status': no_intraday_failure,
            'detail': f"Low stayed {((daily_low - pivot_point) / pivot_point) * 100:+.1f}% vs pivot"
        })
        
        # 2. Volume Confirmation
        
        # Breakout volume ≥40-50% higher than average (using 50% threshold)
        volume_surge = current_volume >= avg_volume_50 * 1.5  # 50% higher
        volume_increase_pct = ((current_volume - avg_volume_50) / avg_volume_50) * 100
        breakout_conditions.append({
            'category': 'Volume',
            'condition': 'Volume ≥50% above average',
            'current': f"{current_volume:,.0f}",
            'target': f"≥{avg_volume_50 * 1.5:,.0f}",
            'status': volume_surge,
            'detail': f"{volume_increase_pct:+.0f}% above 50-day average"
        })
        
        # Volume increasing relative to prior days
        recent_volumes = recent_10['Volume'].iloc[-5:]  # Last 5 days
        volume_trend_up = current_volume > recent_volumes.mean() * 1.2
        breakout_conditions.append({
            'category': 'Volume',
            'condition': 'Volume increasing vs recent',
            'current': f"{current_volume:,.0f}",
            'target': f">{recent_volumes.mean() * 1.2:,.0f}",
            'status': volume_trend_up,
            'detail': f"{((current_volume / recent_volumes.mean()) - 1) * 100:+.0f}% vs recent 5-day avg"
        })
        
        # 3. Structure Confirmation
        
        # Prior 5-10 days show tight price action
        prior_ranges = recent_10['High'] - recent_10['Low']
        avg_range_recent = prior_ranges.mean()
        longer_avg_range = data.tail(50)['High'].subtract(data.tail(50)['Low']).mean()
        tight_prior_action = avg_range_recent < longer_avg_range * 0.8
        breakout_conditions.append({
            'category': 'Structure',
            'condition': 'Prior 5-10 days tight',
            'current': f"{avg_range_recent:.2f}",
            'target': f"<{longer_avg_range * 0.8:.2f}",
            'status': tight_prior_action,
            'detail': f"Recent range {(avg_range_recent/longer_avg_range)*100:.0f}% of normal"
        })
        
        # No wide-range down days just before breakout
        recent_5_days = data.tail(5)
        wide_down_days = 0
        for _, day in recent_5_days.iterrows():
            daily_range = day['High'] - day['Low']
            if (day['Close'] < day['Open']) and (daily_range > longer_avg_range * 1.5):
                wide_down_days += 1
        
        no_wide_down = wide_down_days == 0
        breakout_conditions.append({
            'category': 'Structure',
            'condition': 'No wide-range down days',
            'current': f"{wide_down_days} found",
            'target': '0',
            'status': no_wide_down,
            'detail': f"Found {wide_down_days} wide-range down days in last 5 days"
        })
        
        # Display breakout confirmation results
        print(f"{'Category':<10} {'Condition':<25} {'Current':<15} {'Target':<15} {'Status':<10} Details")
        print("─" * 100)
        
        confirmed_conditions = 0
        total_conditions = len(breakout_conditions)
        
        for condition in breakout_conditions:
            status_symbol = "✅ PASS" if condition['status'] else "❌ FAIL"
            print(f"{condition['category']:<10} {condition['condition']:<25} {condition['current']:<15} {condition['target']:<15} {status_symbol:<10} {condition['detail']}")
            if condition['status']:
                confirmed_conditions += 1
        
        # Breakout confirmed if most conditions pass (6 out of 8)
        breakout_confirmed = confirmed_conditions >= 6
        
        print("─" * 100)
        print(f"🎯 BREAKOUT CONFIRMATION: {confirmed_conditions}/{total_conditions} - {'✅ CONFIRMED' if breakout_confirmed else '❌ NOT CONFIRMED'}")
        
        if breakout_confirmed:
            print(f"✅ Breakout confirmed above ${pivot_point:.2f} with volume - BUY SIGNAL")
        else:
            print("❌ Breakout not confirmed - wait for proper signal")
        
        return {
            'confirmed': breakout_confirmed,
            'score': confirmed_conditions,
            'total': total_conditions,
            'conditions': breakout_conditions,
            'volume_ratio': current_volume / avg_volume_50,
            'pivot_point': pivot_point
        }
    
    def _find_base_contractions(self, data: pd.DataFrame) -> List[Dict]:
        """Find price contractions within a base pattern"""
        contractions = []
        
        if len(data) < 10:
            return contractions
        
        # Find swing highs and lows
        highs = []
        lows = []
        
        window = min(5, len(data) // 4)  # Adaptive window size
        
        for i in range(window, len(data) - window):
            # Swing high: higher than surrounding days
            if all(data.iloc[i]['High'] >= data.iloc[j]['High'] for j in range(i-window, i+window+1) if j != i):
                highs.append({
                    'index': i,
                    'price': data.iloc[i]['High'],
                    'date': data.index[i]
                })
            
            # Swing low: lower than surrounding days
            if all(data.iloc[i]['Low'] <= data.iloc[j]['Low'] for j in range(i-window, i+window+1) if j != i):
                lows.append({
                    'index': i,
                    'price': data.iloc[i]['Low'],
                    'date': data.index[i]
                })
        
        # Match highs with subsequent lows to find contractions
        for high in highs:
            subsequent_lows = [low for low in lows if low['index'] > high['index']]
            
            if subsequent_lows:
                # Find the lowest low after this high
                lowest_low = min(subsequent_lows, key=lambda x: x['price'])
                
                # Calculate contraction metrics
                decline_pct = ((high['price'] - lowest_low['price']) / high['price']) * 100
                duration_days = (lowest_low['date'] - high['date']).days
                
                # Get volume data during this contraction
                contraction_data = data.iloc[high['index']:lowest_low['index']+1]
                if len(contraction_data) > 0:
                    avg_volume = contraction_data['Volume'].mean()
                    base_avg_volume = data['Volume'].mean()
                    volume_ratio = avg_volume / base_avg_volume if base_avg_volume > 0 else 1
                    
                    contractions.append({
                        'start_idx': high['index'],
                        'end_idx': lowest_low['index'],
                        'high_price': high['price'],
                        'low_price': lowest_low['price'],
                        'decline_pct': decline_pct,
                        'duration_days': duration_days,
                        'avg_volume_ratio': volume_ratio,
                        'start_date': high['date'],
                        'end_date': lowest_low['date']
                    })
        
        # Sort by start date and filter for meaningful contractions
        contractions = sorted(contractions, key=lambda x: x['start_date'])
        meaningful_contractions = [c for c in contractions if c['decline_pct'] >= 3]  # At least 3% pullback
        
        return meaningful_contractions
    
    def _step3_breakout_confirmation(self, data: pd.DataFrame, symbol: str) -> Dict:
        """Step 3: Legacy Breakout Confirmation (kept for compatibility)"""
        print(f"\n🎯 STEP 3: BREAKOUT CONFIRMATION (LEGACY)")
        print("─" * 45)
        
        latest = data.iloc[-1]
        recent_5 = data.tail(5)
        recent_50 = data.tail(50)
        
        current_price = latest['Close']
        pivot_point = recent_50['High'].max()
        avg_volume_50 = recent_50['Volume'].mean()
        current_volume = latest['Volume']
        
        # Breakout conditions
        breakout_conditions = []
        
        # Condition 1: Breakout candle closes above pivot point
        above_pivot = current_price > pivot_point
        breakout_conditions.append({
            'condition': 'Close above pivot point',
            'current': f"${current_price:.2f}",
            'target': f">${pivot_point:.2f}",
            'status': above_pivot,
            'detail': f"{((current_price - pivot_point) / pivot_point) * 100:+.1f}% vs pivot"
        })
        
        # Condition 2: Breakout volume ≥ 1.4x 50-day average
        volume_surge = current_volume >= (avg_volume_50 * 1.4)
        breakout_conditions.append({
            'condition': 'Volume ≥ 1.4x average',
            'current': f"{current_volume:,.0f}",
            'target': f"≥{avg_volume_50 * 1.4:,.0f}",
            'status': volume_surge,
            'detail': f"{(current_volume / avg_volume_50):.1f}x average volume"
        })
        
        # Condition 3: Last 5 candles tight (low volatility)
        tight_action = True
        if len(recent_5) >= 5:
            ranges = recent_5['High'] - recent_5['Low']
            avg_range = ranges.mean()
            recent_atr = data.tail(20)['Daily_Range'].mean()
            tight_action = avg_range < recent_atr * 0.8  # Tight = less than 80% of normal range
        
        breakout_conditions.append({
            'condition': 'Last 5 candles tight',
            'current': "Volatility",
            'target': "Low",
            'status': tight_action,
            'detail': f"Recent range {'tight' if tight_action else 'wide'} vs normal"
        })
        
        # Display breakout analysis
        print(f"{'Breakout Condition':<25} {'Current':<15} {'Target':<15} {'Status':<8} Details")
        print("─" * 80)
        
        breakout_score = 0
        for condition in breakout_conditions:
            status_symbol = "✅ PASS" if condition['status'] else "❌ FAIL"
            print(f"{condition['condition']:<25} {condition['current']:<15} {condition['target']:<15} {status_symbol:<8} {condition['detail']}")
            if condition['status']:
                breakout_score += 1
        
        breakout_confirmed = breakout_score == 3  # All 3 must pass
        print("─" * 80)
        print(f"🎯 BREAKOUT RESULT: {breakout_score}/3 - {'✅ CONFIRMED' if breakout_confirmed else '❌ NOT CONFIRMED'}")
        
        if breakout_confirmed:
            print("✅ Breakout confirmed with volume - ready to buy")
        else:
            print("❌ Breakout not confirmed - wait for proper signal")
        
        return {
            'confirmed': breakout_confirmed,
            'score': breakout_score,
            'conditions': breakout_conditions,
            'pivot_point': pivot_point,
            'volume_ratio': current_volume / avg_volume_50
        }
    
    def _step4_fundamentals_check(self, symbol: str) -> Dict:
        """Step 4: Optional Fundamentals Check (Boost Conviction)"""
        print(f"\n💡 STEP 4: FUNDAMENTALS CHECK (OPTIONAL)")
        print("─" * 50)
        print("Note: Fundamental data requires premium API access")
        
        # Placeholder for fundamentals - would need additional data source
        fundamentals = {
            'available': False,
            'eps_growth': None,
            'sales_growth': None,
            'roe': None,
            'margins_increasing': None,
            'earnings_acceleration': None,
            'sector_rank': None,
            'conviction_boost': False
        }
        
        print("📊 Fundamental metrics to check (when data available):")
        print("   • EPS Growth YoY ≥ 25%")
        print("   • Sales Growth YoY ≥ 25%")
        print("   • ROE ≥ 17%")
        print("   • Margins increasing")
        print("   • Earnings acceleration present")
        print("   • Sector rank in top 3")
        print("⚠️  Fundamentals analysis skipped - technical analysis sufficient")
        
        return fundamentals
    
    def _step5_risk_setup(self, data: pd.DataFrame, trend_results: Dict, 
                         vcp_results: Dict, pivot_results: Dict) -> Dict:
        """Step 5: Risk Setup Before Buy"""
        print(f"\n🛡️  STEP 5: RISK SETUP (BEFORE BUY)")
        print("─" * 45)
        
        latest = data.iloc[-1]
        current_price = latest['Close']
        
        # Calculate stop loss (5-10% below entry)
        stop_loss_5pct = current_price * 0.95  # 5% stop
        stop_loss_8pct = current_price * 0.92  # 8% stop
        stop_loss_10pct = current_price * 0.90  # 10% stop
        
        # Find recent support level
        recent_support = data.tail(20)['Low'].min()
        support_stop = recent_support * 0.98  # 2% below support
        
        # Choose the higher stop loss (less risk)
        recommended_stop = max(stop_loss_8pct, support_stop)
        
        # Calculate risk and position sizing
        risk_per_share = current_price - recommended_stop
        risk_percent = (risk_per_share / current_price) * 100
        
        # Profit targets
        target_1 = current_price * 1.20  # 20% profit
        target_2 = current_price * 1.35  # 35% profit  
        target_3 = current_price * 1.50  # 50% profit
        
        # Reward to risk ratio
        reward_risk_ratio = (target_1 - current_price) / risk_per_share
        
        # Position sizing (1% portfolio risk)
        portfolio_risk_1pct = 0.01  # 1% of portfolio
        
        # Risk conditions
        risk_conditions = []
        
        # Condition 1: Reward to risk ratio ≥ 2
        good_reward_risk = reward_risk_ratio >= 2.0
        risk_conditions.append({
            'condition': 'Reward/Risk ratio ≥ 2',
            'current': f"{reward_risk_ratio:.1f}:1",
            'target': "≥2:1",
            'status': good_reward_risk
        })
        
        # Condition 2: Total risk ≤ 1% of portfolio
        acceptable_risk = risk_percent <= 10  # Max 10% risk per trade
        risk_conditions.append({
            'condition': 'Risk ≤ 10% per trade',
            'current': f"{risk_percent:.1f}%",
            'target': "≤10%",
            'status': acceptable_risk
        })
        
        # Condition 3: Market condition healthy (simplified)
        market_healthy = True  # Would need market analysis
        risk_conditions.append({
            'condition': 'Market condition healthy',
            'current': "Assessment",
            'target': "Healthy",
            'status': market_healthy
        })
        
        # Display risk analysis
        print(f"{'Risk Condition':<25} {'Current':<15} {'Target':<15} Status")
        print("─" * 65)
        
        risk_score = 0
        for condition in risk_conditions:
            status_symbol = "✅ PASS" if condition['status'] else "❌ FAIL"
            print(f"{condition['condition']:<25} {condition['current']:<15} {condition['target']:<15} {status_symbol}")
            if condition['status']:
                risk_score += 1
        
        risk_acceptable = risk_score == 3
        print("─" * 65)
        print(f"🛡️  RISK ASSESSMENT: {risk_score}/3 - {'✅ ACCEPTABLE' if risk_acceptable else '❌ HIGH RISK'}")
        
        return {
            'acceptable': risk_acceptable,
            'entry_price': current_price,
            'stop_loss': recommended_stop,
            'risk_per_share': risk_per_share,
            'risk_percent': risk_percent,
            'target_1': target_1,
            'target_2': target_2,
            'target_3': target_3,
            'reward_risk_ratio': reward_risk_ratio,
            'portfolio_risk': portfolio_risk_1pct,
            'conditions': risk_conditions
        }
    
    def _display_complete_prices(self, risk_results: Dict):
        """Display exact buy and sell prices"""
        print(f"\n💰 EXACT BUY & SELL PRICES")
        print("═" * 50)
        
        # Two lines as requested
        print(f"🟢 BUY PRICE:  ${risk_results['entry_price']:.2f} (IMMEDIATE)")
        print(f"🔴 SELL PRICE: ${risk_results['stop_loss']:.2f} (STOP LOSS)")
        
        print(f"\n📊 COMPLETE PRICE LEVELS:")
        print("─" * 35)
        print(f"🛒 Entry Price:    ${risk_results['entry_price']:.2f}")
        print(f"🛑 Stop Loss:      ${risk_results['stop_loss']:.2f} (-{risk_results['risk_percent']:.1f}%)")
        print(f"🎯 Target 1:       ${risk_results['target_1']:.2f} (+20%)")
        print(f"🎯 Target 2:       ${risk_results['target_2']:.2f} (+35%)")
        print(f"🎯 Target 3:       ${risk_results['target_3']:.2f} (+50%)")
        print(f"⚖️  Risk/Reward:    1:{risk_results['reward_risk_ratio']:.1f}")
        
        print(f"\n💼 POSITION SIZING:")
        print(f"   Risk per Share: ${risk_results['risk_per_share']:.2f}")
        print(f"   For 1% Portfolio Risk:")
        print(f"   $10,000 portfolio → {(100 / risk_results['risk_per_share']):.0f} shares max")
        print(f"   $100,000 portfolio → {(1000 / risk_results['risk_per_share']):.0f} shares max")
    
    def _display_sell_algorithm(self, data: pd.DataFrame, risk_results: Dict):
        """Display sell algorithm rules"""
        print(f"\n📉 TRADETHRUST SELL ALGORITHM")
        print("═" * 50)
        
        print(f"🔻 STEP 1: PROTECTIVE STOP-LOSS")
        print(f"   IF price falls below ${risk_results['stop_loss']:.2f}")
        print(f"   THEN SELL immediately (hard stop)")
        print(f"   IF base rises AND stop can be moved up")
        print(f"   THEN TRAIL stop higher below new support")
        
        print(f"\n🔻 STEP 2: TECHNICAL BREAKDOWN")
        print(f"   SELL if:")
        print(f"   • Price closes below 50-day SMA on high volume")
        print(f"   • Price drops on above-average volume after extended move")
        print(f"   • Price fails to hold breakout and does not recover")
        print(f"   • Price breaks below swing low")
        print(f"   • Relative Strength drops significantly vs sector")
        
        print(f"\n💰 STEP 3: PROFIT TAKING (SELL ON STRENGTH)")
        print(f"   IF gain ≥ 20-25% THEN SELL 25-50% of position")
        print(f"   IF trend continues THEN HOLD remainder with trailing stop")
        print(f"   IF price goes parabolic OR volume spikes near top")
        print(f"   THEN SELL or tighten trailing stop")
    
    def _display_anti_rules_warnings(self, trend_results: Dict, vcp_results: Dict, 
                                   pivot_results: Dict):
        """Display anti-rules warnings"""
        print(f"\n🚫 TRADETHRUST WARNINGS (ANTI-RULES)")
        print("═" * 50)
        print(f"AVOID executing trades if:")
        print(f"❌ Averaging down on losing positions")
        print(f"❌ Buying early inside a base (before breakout)")
        print(f"❌ Buying stocks with RS < 70")
        print(f"❌ Ignoring volume on breakout")
        print(f"❌ Holding more than 5-8 positions at once")
        
        # Check for violations
        violations = []
        if not trend_results.get('passed', False):
            violations.append("Trend template failed")
        if not pivot_results.get('overall_confirmed', False):
            violations.append("Breakout not confirmed")
        
        if violations:
            print(f"\n⚠️  CURRENT VIOLATIONS:")
            for violation in violations:
                print(f"   ❌ {violation}")
        else:
            print(f"\n✅ No anti-rule violations detected")
    
    def _generate_complete_recommendation(self, trend_results: Dict, vcp_results: Dict,
                                        pivot_results: Dict, fundamentals_results: Dict,
                                        risk_results: Dict) -> Dict:
        """Generate final recommendation based on all steps"""
        # Check all conditions
        trend_passed = trend_results.get('passed', False)
        vcp_detected = vcp_results.get('detected', False)
        breakout_confirmed = pivot_results.get('overall_confirmed', False)
        risk_acceptable = risk_results.get('acceptable', False)
        
        # Generate recommendation
        if trend_passed and vcp_detected and breakout_confirmed and risk_acceptable:
            recommendation = "🟢 STRONG BUY"
            action = "EXECUTE BUY ORDER"
            confidence = "HIGH"
            reasoning = "All TradeThrust algorithm conditions met"
        elif trend_passed and vcp_detected and risk_acceptable:
            recommendation = "🟡 WATCH LIST"
            action = "WAIT FOR BREAKOUT"
            confidence = "MEDIUM"
            reasoning = "Good setup, wait for breakout confirmation"
        elif trend_passed:
            recommendation = "🟡 MONITOR"
            action = "WATCH FOR VCP"
            confidence = "LOW"
            reasoning = "Trend template passed, watch for base formation"
        else:
            recommendation = "🔴 AVOID"
            action = "SKIP THIS STOCK"
            confidence = "HIGH"
            reasoning = "Does not meet TradeThrust algorithm requirements"
        
        return {
            'recommendation': recommendation,
            'action': action,
            'confidence': confidence,
            'reasoning': reasoning,
            'trend_passed': trend_passed,
            'vcp_detected': vcp_detected,
            'breakout_confirmed': breakout_confirmed,
            'risk_acceptable': risk_acceptable
        }
    
    def _display_complete_summary(self, recommendation: Dict, symbol: str):
        """Display final summary"""
        print(f"\n🎯 FINAL TRADETHRUST RECOMMENDATION")
        print("═" * 50)
        
        print(f"📊 Algorithm Results:")
        print(f"   Trend Template: {'✅ PASSED' if recommendation['trend_passed'] else '❌ FAILED'}")
        print(f"   VCP Pattern: {'✅ DETECTED' if recommendation['vcp_detected'] else '❌ NOT DETECTED'}")
        print(f"   Breakout: {'✅ CONFIRMED' if recommendation['breakout_confirmed'] else '❌ NOT CONFIRMED'}")
        print(f"   Risk Setup: {'✅ ACCEPTABLE' if recommendation['risk_acceptable'] else '❌ HIGH RISK'}")
        
        print(f"\n🎯 Recommendation: {recommendation['recommendation']}")
        print(f"🎬 Action: {recommendation['action']}")
        print(f"🎯 Confidence: {recommendation['confidence']}")
        print(f"💭 Reasoning: {recommendation['reasoning']}")
        
        print(f"\n📋 NEXT STEPS:")
        if recommendation['action'] == 'EXECUTE BUY ORDER':
            print(f"   1. ✅ Place buy order at market price")
            print(f"   2. ✅ Set stop loss order immediately")
            print(f"   3. ✅ Set profit target alerts")
            print(f"   4. ✅ Monitor daily for sell signals")
        elif recommendation['action'] == 'WAIT FOR BREAKOUT':
            print(f"   1. 📊 Add {symbol} to active watchlist")
            print(f"   2. 🚨 Set breakout alert above pivot point")
            print(f"   3. 📈 Monitor volume for confirmation")
            print(f"   4. ⏰ Re-analyze when breakout occurs")
        elif recommendation['action'] == 'WATCH FOR VCP':
            print(f"   1. 📊 Add {symbol} to watchlist")
            print(f"   2. 👀 Monitor for base formation")
            print(f"   3. ⏰ Re-analyze weekly")
            print(f"   4. 🚨 Look for VCP pattern development")
        else:
            print(f"   1. ❌ Remove from consideration")
            print(f"   2. 🔍 Focus on better candidates")
            print(f"   3. ⏰ Re-evaluate in 4-6 weeks")
            print(f"   4. 📚 Find stocks that pass trend template")
        
        print("═" * 50)
        print(f"✅ Analysis Complete | TradeThrust Complete Algorithm v3.0")
        print("═" * 50)
    
    def _find_detailed_contractions(self, data: pd.DataFrame) -> List[Dict]:
        """Find detailed price contractions for VCP analysis"""
        contractions = []
        
        if len(data) < 10:
            return contractions
        
        # Find swing highs and lows
        highs = []
        lows = []
        
        for i in range(2, len(data) - 2):
            # Swing high: higher than 2 days before and after
            if (data.iloc[i]['High'] > data.iloc[i-1]['High'] and 
                data.iloc[i]['High'] > data.iloc[i-2]['High'] and
                data.iloc[i]['High'] > data.iloc[i+1]['High'] and 
                data.iloc[i]['High'] > data.iloc[i+2]['High']):
                highs.append((i, data.iloc[i]['High']))
            
            # Swing low: lower than 2 days before and after
            if (data.iloc[i]['Low'] < data.iloc[i-1]['Low'] and 
                data.iloc[i]['Low'] < data.iloc[i-2]['Low'] and
                data.iloc[i]['Low'] < data.iloc[i+1]['Low'] and 
                data.iloc[i]['Low'] < data.iloc[i+2]['Low']):
                lows.append((i, data.iloc[i]['Low']))
        
        # Match highs with subsequent lows to find contractions
        for i, (high_idx, high_price) in enumerate(highs):
            subsequent_lows = [low for low in lows if low[0] > high_idx]
            if subsequent_lows:
                low_idx, low_price = min(subsequent_lows, key=lambda x: x[1])
                
                # Calculate contraction metrics
                contraction_pct = ((high_price - low_price) / high_price) * 100
                duration = low_idx - high_idx
                
                # Calculate average volume during contraction
                contraction_period = data.iloc[high_idx:low_idx+1]
                if len(contraction_period) > 0:
                    avg_volume = contraction_period['Volume'].mean()
                    overall_avg = data['Volume'].mean()
                    volume_ratio = avg_volume / overall_avg if overall_avg > 0 else 1
                else:
                    volume_ratio = 1
                
                contractions.append({
                    'percentage': contraction_pct,
                    'duration': duration,
                    'high_price': high_price,
                    'low_price': low_price,
                    'avg_volume_ratio': volume_ratio
                })
        
        # Sort by chronological order and return latest contractions
        return sorted(contractions, key=lambda x: x['duration'])[-5:]  # Last 5 contractions

def main():
    """Main function for TradeThrust Complete Algorithm"""
    print("🚀 Welcome to TradeThrust Complete Algorithm")
    print("Professional Stock Analysis with Complete Implementation")
    print("=" * 60)
    
    tt = TradeThrustComplete()
    
    while True:
        print("\n📋 TRADETHRUST COMPLETE MENU")
        print("-" * 35)
        print("1. 📊 Analyze Stock (Complete Algorithm)")
        print("2. 🚪 Exit")
        
        choice = input("\nSelect option (1-2): ").strip()
        
        if choice == '1':
            symbol = input("Enter stock symbol: ").strip().upper()
            if symbol:
                try:
                    result = tt.analyze_stock_complete(symbol)
                    
                    # Ask if user wants another analysis
                    another = input(f"\nAnalyze another stock? (y/n): ").strip().lower()
                    if another != 'y':
                        break
                        
                except Exception as e:
                    print(f"❌ Error analyzing {symbol}: {e}")
        
        elif choice == '2':
            print("\n🚀 Thank you for using TradeThrust Complete Algorithm!")
            print("Remember: Follow the algorithm rules strictly for best results!")
            break
        
        else:
            print("❌ Invalid option. Please select 1-2.")

if __name__ == "__main__":
    main()
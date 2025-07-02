# Mehran Stock Analysis Program - TradeStock Repository

## Complete Educational Stock Analysis Tool

This repository contains a comprehensive Python program that implements **Mehran's Stock Buying Checklist** - a systematic approach to stock analysis based on proven technical indicators and risk management principles.

## 🎯 What This Program Does

The Mehran Stock Analyzer helps you make informed stock buying decisions by implementing a **3-phase systematic approach**:

### Phase 1: Trend Template (Foundation)
- ✅ Price above 50, 150, and 200-day moving averages
- ✅ Moving averages in proper uptrend order (50 > 150 > 200)
- ✅ Stock price at least 30% above 52-week low
- ✅ Stock price within 25% of 52-week high  
- ✅ Price above 10 and 21-day exponential moving averages

### Phase 2: VCP Base Formation (Volatility Contraction Pattern)
- ✅ Progressive pullback contractions (each smaller than the last)
- ✅ Volume dry-up during corrections
- ✅ Price range tightening (coiling effect)

### Phase 3: Entry Trigger
- ✅ Breakout above recent resistance
- ✅ Volume surge (50%+ above average)

## 📁 Program Files

### Core Analysis Engine
- **`mehran_stock_analyzer.py`** - Main analysis program (476 lines)
  - Complete implementation of Mehran's buying criteria
  - Comprehensive technical indicator calculations
  - Risk management with stop-loss suggestions
  - Professional chart generation with all indicators
  - Command-line interface for single stock analysis

### Interactive Demo & Learning
- **`demo_mehran_analyzer.py`** - Interactive demo version (204 lines)
  - Educational walkthrough of Mehran's system
  - Interactive multi-stock analysis
  - Batch analysis of popular stocks
  - Learning mode with detailed explanations

### Setup & Dependencies
- **`setup.py`** - Automated installation and testing (105 lines)
- **`requirements.txt`** - Python package dependencies
- **`README.md`** - Complete documentation and usage guide

## 🚀 Quick Start

### Option 1: Automated Setup
```bash
python setup.py
```
This will:
- Install all required packages
- Test the installation
- Run a demo analysis on AAPL
- Generate sample charts

### Option 2: Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Analyze a stock
python mehran_stock_analyzer.py AAPL

# Run interactive demo
python demo_mehran_analyzer.py
```

## 📊 Example Usage

### Single Stock Analysis
```bash
python mehran_stock_analyzer.py TSLA
```

### Interactive Demo
```bash
python demo_mehran_analyzer.py
```

### Batch Analysis
```bash
python demo_mehran_analyzer.py batch
```

### Educational Mode
```bash
python demo_mehran_analyzer.py education
```

## 📈 Sample Output

```
🔍 MEHRAN STOCK ANALYSIS: AAPL
============================================================

📊 PHASE 1: TREND TEMPLATE
------------------------------
❌ FAIL Price Above Smas
    Price: $211.12 | 50SMA: $210.85 | 150SMA: $210.72 | 200SMA: $206.39
✅ PASS Sma Stacking
    50SMA > 150SMA: True | 150SMA > 200SMA: True
❌ FAIL Above 52w Low
    52W Low: $164.08 | Current: 28.7% above low (need ≥30%)
✅ PASS Near 52w High
    52W High: $237.23 | Current: 11.0% below high (need ≤25%)
❌ FAIL Above Emas
    Price: $211.12 | 10EMA: $212.89 | 21EMA: $212.67

Phase 1 Score: 2/5 ❌ FAIL

⚠️  RECOMMENDATION: 🔴 DO NOT BUY
This stock does not meet sufficient criteria. Wait for better setup.

💰 RISK MANAGEMENT
--------------------
Current Price: $211.12
Suggested Stop Loss: $191.17 (9.4% risk)
```

## 🎓 Educational Features

### Learning Modes
1. **Interactive Analysis** - Step-by-step stock evaluation
2. **Batch Testing** - Compare multiple stocks simultaneously  
3. **Educational Walkthrough** - Learn the system principles
4. **Visual Charts** - See all indicators on professional charts

### Key Learning Points
- **Selectivity is Good** - The system is designed to be picky
- **Risk Management** - Always calculate stop-losses before buying
- **Patience Pays** - Wait for all criteria to align
- **Evidence Over Hope** - Use data, not emotions

## 📋 Program Features

### Technical Analysis
- ✅ Multiple moving averages (SMA 50/150/200, EMA 10/21)
- ✅ 52-week high/low analysis
- ✅ Volume analysis and surge detection
- ✅ VCP pattern recognition
- ✅ Breakout confirmation signals
- ✅ Support/resistance identification

### Risk Management
- ✅ Automatic stop-loss calculation
- ✅ Risk percentage assessment
- ✅ Position sizing guidance
- ✅ Entry timing optimization

### Visualization
- ✅ Professional chart generation
- ✅ All indicators plotted
- ✅ Volume analysis overlay
- ✅ 52-week high/low reference lines
- ✅ Export to PNG format

### User Experience
- ✅ Clear pass/fail criteria
- ✅ Detailed explanations for each test
- ✅ Educational insights
- ✅ Multiple usage modes
- ✅ Command-line and interactive interfaces

## 🎯 Perfect For

### Individual Investors
- Learn systematic stock analysis
- Remove emotion from decisions
- Build disciplined trading habits
- Understand institutional-grade criteria

### Educators & Students
- Teach technical analysis concepts
- Demonstrate risk management
- Practice with real market data
- Understand market psychology

### Trading Groups
- Standardize analysis criteria
- Share consistent methodology
- Compare stock opportunities
- Educational discussions

## 🔧 Technical Requirements

- **Python 3.7+**
- **Dependencies**: yfinance, pandas, numpy, matplotlib
- **Data Source**: Yahoo Finance (free, real-time)
- **Output**: Terminal analysis + PNG charts + text reports

## 📚 Educational Value

This program teaches:
1. **Systematic Approach** - How professionals analyze stocks
2. **Risk Management** - Position sizing and stop-losses
3. **Technical Analysis** - Moving averages, volume, patterns
4. **Market Psychology** - Why certain setups work
5. **Discipline** - Waiting for quality opportunities

## 🎯 Success Metrics

A typical analysis session might show:
- **Analyzed**: 10 stocks
- **Buy Candidates**: 1-2 stocks (10-20% rate)
- **This selectivity is GOOD** - protects capital

The system is designed to be highly selective, which is exactly what protects your capital in real trading.

## 📞 Support & Learning

The program includes:
- Detailed error messages
- Educational explanations for each criterion
- Visual charts for better understanding
- Interactive modes for hands-on learning
- Batch analysis for broader market perspective

---

**Remember**: This tool is for educational purposes. Always do your own research and consider consulting with financial professionals for investment decisions.

The goal is to learn systematic, disciplined approaches to stock analysis that can improve your understanding of market dynamics and risk management.
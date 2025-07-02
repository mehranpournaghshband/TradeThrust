# 📊 TradeStock - Mehran Stock Buying Checklist Analyzer

A comprehensive Python program that implements **Mehran's Stock Buying Checklist** to help decide whether to buy a stock or not. This educational tool analyzes stocks using Mehran's proven criteria including trend templates, VCP base formations, and entry signals.

## 🎯 What This Program Does

This analyzer implements all of Mehran's key stock selection criteria:

### Phase 1: Trend Template ✅
- Price above 50, 150, and 200-day Simple Moving Averages (SMAs)
- Moving averages in proper stacking order (50 > 150 > 200)
- Price at least 30% above 52-week low
- Price within 25% of 52-week high
- Price above 10 and 21-day Exponential Moving Averages (EMAs)

### Phase 2: VCP Base Formation 📈
- Series of contractions getting progressively smaller
- Volume declining during pullbacks (volume dry-up)
- Price tightening in recent bars
- Proper base structure before breakout

### Entry Trigger 🚀
- Breakout above resistance on volume surge
- Volume 50%+ above average on breakout
- Clear pivot point with conviction

## 🛠 Installation

1. **Clone this repository:**
```bash
git clone https://github.com/mehranpournaghshband/TradeStock.git
cd TradeStock
```

2. **Install required dependencies:**
```bash
pip install -r requirements.txt
```

3. **Dependencies include:**
   - `yfinance` - Real-time stock data
   - `pandas` - Data analysis
   - `numpy` - Numerical calculations
   - `matplotlib` - Chart generation

## 🚀 Usage

### Option 1: Command Line Analysis
```bash
python3 mehran_stock_analyzer.py AAPL
```

### Option 2: Interactive Demo
```bash
python3 demo_mehran_analyzer.py
```

### Option 3: Google Colab
Follow the instructions in `Google_Colab_Instructions.md` to run in Google Colab.

The demo offers:
- Analyze multiple sample stocks
- Analyze a specific stock
- Educational explanation
- Interactive menu

## 📈 Sample Output

```
🔍 MEHRAN STOCK ANALYSIS: AAPL
============================================================

📊 PHASE 1: TREND TEMPLATE
------------------------------
✅ PASS Price Above Smas
    Price: $182.52 | 50SMA: $175.23 | 150SMA: $168.45 | 200SMA: $161.78
✅ PASS Sma Stacking
    50SMA > 150SMA: True | 150SMA > 200SMA: True
✅ PASS Above 52w Low
    52W Low: $124.17 | Current: 47.0% above low (need ≥30%)
✅ PASS Near 52w High
    52W High: $199.62 | Current: 8.6% below high (need ≤25%)
✅ PASS Above Emas
    Price: $182.52 | 10EMA: $179.34 | 21EMA: $177.89

Phase 1 Score: 5/5 ✅ PASS

📈 PHASE 2: VCP BASE FORMATION
-----------------------------------
✅ PASS Contractions Decreasing
    Pullback 1: -12.3% | Pullback 2: -8.1% | Pullback 3: -4.2%
✅ PASS Volume Declining
    Average volume: 45,234,567 | Volume declined during pullbacks: True
✅ PASS Price Tightening
    Recent avg range: $2.14 | 30-day avg: $3.67 | Tightening: True

Phase 2 Score: 3/3 ✅ PASS

🚀 ENTRY SIGNAL CHECK
-------------------------
✅ PASS Breakout Signal
    Resistance: $185.50 | Current: $187.25 | Volume: 67,891,234 (avg: 45,234,567)

============================================================
🎯 RECOMMENDATION: 🟢 BUY CANDIDATE
This stock meets Mehran's criteria and shows strong setup!

💰 RISK MANAGEMENT
--------------------
Current Price: $187.25
Suggested Stop Loss: $178.45 (4.7% risk)
Position Size: Risk no more than 1-2% of portfolio on this trade
```

## 📊 Generated Files

The program creates several educational files:

1. **Charts**: `SYMBOL_mehran_analysis.png`
   - Price with all moving averages
   - Volume analysis
   - 52-week high/low reference lines

2. **Analysis Reports**: `SYMBOL_mehran_report_TIMESTAMP.txt`
   - Detailed scoring breakdown
   - Risk management suggestions
   - Entry and exit levels

3. **Demo Summary**: `mehran_demo_summary_TIMESTAMP.txt`
   - Comparative analysis of multiple stocks
   - Buy vs. avoid recommendations

## 🎓 Educational Features

### Perfect VCP Chart Example
The program generates educational charts showing:
- **Contractions**: Each pullback smaller than the last
- **Volume Dry-up**: Declining volume during consolidation
- **Tight Right Side**: Small candlesticks near resistance
- **Breakout**: Volume surge on upside move

### Risk Management
- Automatic stop-loss calculation below support
- Risk percentage calculation
- Position sizing guidance
- Portfolio risk management (1-2% rule)

## 📚 Understanding the Method

### Why This Works
Mehran's approach identifies stocks that:
1. **Are in strong uptrends** (trend template)
2. **Have proper base formations** (VCP pattern)
3. **Break out with institutional support** (volume confirmation)

### Key Concepts
- **VCP (Volatility Contraction Pattern)**: Series of pullbacks that get progressively smaller
- **Volume Dry-up**: Decreasing volume during consolidation indicates selling exhaustion
- **Breakout**: Price clearing resistance with volume surge shows institutional buying

## ⚠️ Important Disclaimers

1. **Educational Purpose**: This tool is for learning Mehran's methodology
2. **Not Financial Advice**: Always do your own research and consult professionals
3. **Market Risk**: All trading involves risk of loss
4. **Historical Data**: Past performance doesn't guarantee future results

## 🔧 Customization

You can modify the analyzer by:
- Adjusting scoring thresholds in the code
- Adding new technical indicators
- Modifying VCP detection algorithms
- Customizing chart styles and outputs

## 📖 Further Learning

To deepen your understanding:
- Learn systematic trading methodologies
- Study technical analysis principles
- Practice with paper trading first
- Join trading communities for discussion

## 🤝 Contributing

This is an educational project. Feel free to:
- Submit bug reports
- Suggest improvements
- Add new features
- Share educational enhancements

## 📄 License

This project is for educational purposes. Please respect the educational nature of this tool and use it responsibly.

## 🙏 Acknowledgments

- The trading community for continued education and support
- Technical analysis pioneers for foundational knowledge

---

**Remember**: This tool helps you learn and apply Mehran's criteria systematically, but successful trading requires practice, discipline, and continuous learning. Always manage your risk appropriately!

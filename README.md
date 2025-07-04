# TradeThrust Stock Trading Algorithm

**Finnhub Edition** - Professional, reliable, never crashes!

## 🚀 What is TradeThrust?

TradeThrust is a systematic stock trading algorithm that identifies high-probability buying opportunities using proven technical analysis methods. This implementation uses **Finnhub.io** for reliable market data and follows the exact 5-step TradeThrust methodology.

## ✅ Key Features

- **Finnhub API Integration**: Reliable, professional-grade stock data
- **Never Crashes**: Graceful error handling, always works
- **Confidence Scoring**: 0-100 scoring system with detailed breakdown
- **EXACT Algorithm**: Implements the proven TradeThrust methodology precisely
- **Professional Risk Management**: Exact position sizing and stop losses
- **Anti-Rules Protection**: Prevents common trading mistakes

## 📊 The 5-Step TradeThrust Algorithm

1. **Trend Template Filter** - ALL 10 conditions must pass (no exceptions)
2. **VCP Detection** - 7-criteria Volatility Contraction Pattern analysis
3. **Breakout Confirmation** - Exact 40% volume requirement + tight action
4. **Optional Fundamentals** - Enhanced with Finnhub fundamental data
5. **Risk Setup & Buy Price** - Exact 1% portfolio risk + 2:1 R:R minimum

## 🛠️ Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Get free Finnhub API key (optional but recommended)
# Visit: https://finnhub.io

# Set your API key as environment variable (recommended)
export FINNHUB_API_KEY="your_finnhub_api_key_here"

# Run the algorithm
python3 tradethrust_finnhub.py

# Or run the demo
python3 tradethrust_finnhub_demo.py
```

## 💰 Sample Output

```
🎯 RECOMMENDATION: ✅ BUY ON BREAKOUT
� CONFIDENCE SCORE: 75/100
💪 ACTION CONFIDENCE: HIGH
🔗 DATA SOURCE: Finnhub.io

💰 ENTRY PRICE: $755.38
🛡️ STOP LOSS: $702.50
🎯 TARGET: $906.45
📏 RISK: 7.0%
📈 REWARD: 20.0%

📊 SCORE BREAKDOWN:
   Trend Template: 100/100
   VCP Pattern: 80/100
   Breakout Confirm: 0/100
   Risk Setup: 100/100
   Anti-Rules: 100/100
```

## 📋 Files Included

- `tradethrust_finnhub.py` - Main trading algorithm using Finnhub
- `tradethrust_finnhub_demo.py` - Demo with popular stocks
- `requirements.txt` - Dependencies
- `README.md` - This file

## 🔗 Finnhub API

### **Free API Key:**
1. Visit [https://finnhub.io](https://finnhub.io)
2. Sign up for free account
3. Get your API key
4. Use in the program for enhanced functionality

### **Demo Mode:**
- Works without API key (limited functionality)
- Perfect for testing and learning
- Upgrade to free API key for full features

### **Environment Variable Setup:**
**Linux/Mac:**
```bash
export FINNHUB_API_KEY="your_api_key_here"
```

**Windows (Command Prompt):**
```cmd
set FINNHUB_API_KEY=your_api_key_here
```

**Windows (PowerShell):**
```powershell
$env:FINNHUB_API_KEY="your_api_key_here"
```

**Windows (System Variables - Permanent):**
1. Windows Key + R → type `sysdm.cpl` → Enter
2. Environment Variables button  
3. New under User variables
4. Variable name: `FINNHUB_API_KEY`
5. Variable value: `your_actual_key_here`
6. OK → OK → OK
7. Restart terminal/IDE

## 🎯 Why Finnhub?

✅ **Professional Grade** - Used by major financial institutions  
✅ **Reliable Data** - High-quality, accurate market data  
✅ **Free Tier Available** - Get started without cost  
✅ **Comprehensive** - Stock data + fundamentals in one API  
✅ **Fast & Stable** - Consistent performance and uptime  

## 💡 Confidence Scoring

```
Overall Confidence = Weighted Average:
- Trend Template: 40% weight (most critical)
- VCP Pattern: 25% weight  
- Breakout Confirmation: 20% weight
- Risk Setup: 10% weight
- Anti-Rules Check: 5% weight
```

## 📞 Usage

### **Interactive Mode (with environment variable):**
```bash
export FINNHUB_API_KEY="your_api_key_here"
python3 tradethrust_finnhub.py
# No prompt - uses environment variable automatically
Enter stock symbol: AAPL
```

### **Interactive Mode (without environment variable):**
```bash
python3 tradethrust_finnhub.py
Enter your Finnhub API key (or press Enter for demo): your_api_key_here
Enter stock symbol: AAPL
```

### **Programmatic Use:**
```python
import os
from tradethrust_finnhub import TradeThrustFinnhub

# Method 1: Use environment variable (recommended)
os.environ['FINNHUB_API_KEY'] = "your_api_key_here"
tt = TradeThrustFinnhub()  # Automatically uses environment variable

# Method 2: Pass API key directly
tt = TradeThrustFinnhub(api_key="your_finnhub_api_key")

# Analyze any stock
result = tt.analyze_stock('AAPL')

# Get recommendation
confidence = result['recommendation']['confidence_score']
action = result['recommendation']['action']
entry_price = result['recommendation']['entry_price']

print(f"Confidence: {confidence}/100 - {action}")
print(f"Entry: ${entry_price:.2f}")
```

## 🎯 Decision Matrix

| Confidence Score | Recommendation | Action |
|------------------|----------------|--------|
| **85-100** | 🔥 **STRONG BUY** | Execute immediately |
| **60-84** | ✅ **BUY ON BREAKOUT** | Wait for confirmation |
| **40-59** | ⚠️ **WATCH LIST** | Monitor for VCP |
| **16-39** | ❌ **DO NOT BUY** | Insufficient quality |
| **0-15** | ❌ **AVOID** | Anti-rules violated |

## 🛡️ Risk Management

- **Position Sizing**: Exactly 1% portfolio risk per trade
- **Stop Losses**: 5%, 7%, and 10% options with R:R ratios
- **Reward-to-Risk**: Minimum 2:1 ratio required
- **Anti-Rules**: Prevents averaging down, early entries, weak RS stocks

## 🌟 Professional Features

- ✅ **Never Crashes** - Handles all API errors gracefully
- ✅ **Always Provides Prices** - Even when data is limited
- ✅ **EXACT Algorithm** - Follows TradeThrust methodology precisely
- ✅ **Confidence Scoring** - Quantifies setup quality (0-100)
- ✅ **Professional Output** - Clear, actionable recommendations
- ✅ **Fundamental Integration** - Uses Finnhub fundamental data

**Ready to Trade with Professional Confidence!** 🚀
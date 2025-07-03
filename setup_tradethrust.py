#!/usr/bin/env python3
"""
TradeThrust Setup and Demo Script
=================================

This script sets up TradeThrust and demonstrates its capabilities.
Run this to get started with TradeThrust quickly and see examples.

Usage:
    python setup_tradethrust.py

Features:
- Automatic dependency installation
- Environment detection (Colab, Jupyter, Local)
- Demo analysis with popular stocks
- Quick setup verification
"""

import subprocess
import sys
import os
import platform
from datetime import datetime

def print_header():
    """Print TradeThrust header"""
    print("🚀" + "=" * 60 + "🚀")
    print("               TRADETHRUST SETUP & DEMO")
    print("        Professional Stock Trading System")
    print("      Based on TradeThrust's Methodology")
    print("🚀" + "=" * 60 + "🚀")
    print()

def detect_environment():
    """Detect the current environment"""
    print("🔍 Detecting Environment...")
    
    # Check for Google Colab
    try:
        import google.colab
        print("✅ Environment: Google Colab")
        return "colab"
    except ImportError:
        pass
    
    # Check for Jupyter
    try:
        from IPython import get_ipython
        if get_ipython() is not None:
            print("✅ Environment: Jupyter Notebook")
            return "jupyter"
    except ImportError:
        pass
    
    # Default to local
    print("✅ Environment: Local Python")
    return "local"

def install_dependencies():
    """Install required packages"""
    print("\n📦 Installing Dependencies...")
    
    # Core packages required for TradeThrust
    packages = [
        'yfinance>=0.2.12',
        'pandas>=1.5.0',
        'numpy>=1.21.0',
        'matplotlib>=3.5.0'
    ]
    
    # Optional packages for enhanced features
    optional_packages = [
        'seaborn>=0.11.0',
        'plotly>=5.0.0',
        'streamlit>=1.28.0',
        'ipywidgets>=8.0.0'
    ]
    
    print("Installing core packages...")
    for package in packages:
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                package, "--quiet", "--upgrade"
            ])
            print(f"  ✅ {package.split('>=')[0]}")
        except subprocess.CalledProcessError:
            print(f"  ❌ Failed to install {package}")
            return False
    
    print("\nInstalling optional packages...")
    for package in optional_packages:
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                package, "--quiet", "--upgrade"
            ])
            print(f"  ✅ {package.split('>=')[0]}")
        except subprocess.CalledProcessError:
            print(f"  ⚠️  Optional package {package} failed to install")
    
    return True

def verify_installation():
    """Verify that all packages are working"""
    print("\n🔧 Verifying Installation...")
    
    tests = [
        ("yfinance", "import yfinance; yfinance.Ticker('AAPL')"),
        ("pandas", "import pandas as pd; pd.DataFrame()"),
        ("numpy", "import numpy as np; np.array([1,2,3])"),
        ("matplotlib", "import matplotlib.pyplot as plt")
    ]
    
    for name, test_code in tests:
        try:
            exec(test_code)
            print(f"  ✅ {name}")
        except Exception as e:
            print(f"  ❌ {name}: {e}")
            return False
    
    print("✅ All core packages verified!")
    return True

def create_demo_analysis():
    """Create and run demo analysis"""
    print("\n🎬 Running TradeThrust Demo...")
    
    # Import the simplified TradeThrustColab class
    demo_code = '''
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

class TradeThrustDemo:
    """Simplified demo version of TradeThrust"""
    
    def __init__(self):
        print("🚀 TradeThrust Demo - Ready for Analysis!")
    
    def analyze_stock(self, symbol):
        """Quick stock analysis"""
        try:
            # Fetch data
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1y")
            
            if data.empty:
                return f"❌ No data for {symbol}"
            
            # Calculate indicators
            data['SMA_50'] = data['Close'].rolling(50).mean()
            data['SMA_150'] = data['Close'].rolling(150).mean()
            data['SMA_200'] = data['Close'].rolling(200).mean()
            data['52W_High'] = data['High'].rolling(252).max()
            data['52W_Low'] = data['Low'].rolling(252).min()
            data['Avg_Volume'] = data['Volume'].rolling(20).mean()
            
            latest = data.iloc[-1]
            price = latest['Close']
            
            # TradeThrust criteria check
            criteria = {
                'price_above_smas': price > latest['SMA_50'] and price > latest['SMA_150'] and price > latest['SMA_200'],
                'sma_stacking': latest['SMA_50'] > latest['SMA_150'] > latest['SMA_200'],
                'above_52w_low': ((price - latest['52W_Low']) / latest['52W_Low']) * 100 >= 30,
                'near_52w_high': ((latest['52W_High'] - price) / latest['52W_High']) * 100 <= 25,
            }
            
            score = sum(criteria.values())
            volume_surge = latest['Volume'] > latest['Avg_Volume'] * 1.5
            
            # Recommendation
            if score >= 3 and volume_surge:
                recommendation = "🟢 STRONG BUY"
            elif score >= 2:
                recommendation = "🟡 WATCH"
            else:
                recommendation = "🔴 AVOID"
            
            return {
                'symbol': symbol,
                'price': price,
                'recommendation': recommendation,
                'score': f"{score}/4",
                'volume_surge': volume_surge
            }
            
        except Exception as e:
            return f"❌ Error analyzing {symbol}: {e}"

# Run demo
demo = TradeThrustDemo()

# Demo stocks
demo_stocks = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA']

print("\\n📊 DEMO ANALYSIS RESULTS:")
print("=" * 50)

for stock in demo_stocks:
    result = demo.analyze_stock(stock)
    if isinstance(result, dict):
        volume_text = "📈 High Volume" if result['volume_surge'] else "📊 Normal Volume"
        print(f"{result['recommendation']} {result['symbol']}: ${result['price']:.2f} | Score: {result['score']} | {volume_text}")
    else:
        print(result)
'''
    
    exec(demo_code)

def show_usage_examples():
    """Show usage examples"""
    print("\n" + "=" * 60)
    print("🎓 TRADETHRUST USAGE EXAMPLES")
    print("=" * 60)
    
    examples = [
        ("📊 Analyze Single Stock", '''
from tradethrust_colab import TradeThrustColab

tt = TradeThrustColab()
result = tt.analyze_stock('AAPL')
'''),
        
        ("📋 Build Watchlist", '''
# Add stocks to watchlist
stocks = ['AAPL', 'MSFT', 'GOOGL', 'TSLA']
for stock in stocks:
    tt.add_to_watchlist(stock)

# Scan for opportunities
tt.scan_watchlist()
'''),
        
        ("🔍 Quick Screen", '''
# Screen multiple stocks
tech_stocks = ['AAPL', 'MSFT', 'GOOGL', 'META', 'NVDA']
tt.quick_screen(tech_stocks)
'''),
        
        ("📊 Web Interface", '''
# Run web interface (requires streamlit)
streamlit run tradethrust_web.py
'''),
        
        ("💻 Desktop Application", '''
# Run full desktop application
python tradethrust.py
''')
    ]
    
    for title, code in examples:
        print(f"\n{title}:")
        print("-" * len(title))
        print(code)

def show_file_structure():
    """Show the TradeThrust file structure"""
    print("\n📁 TRADETHRUST FILE STRUCTURE:")
    print("=" * 40)
    
    files = [
        ("tradethrust.py", "Main desktop application with full features"),
        ("tradethrust_colab.py", "Google Colab optimized version"),
        ("tradethrust_web.py", "Streamlit web interface"),
        ("TradeThrust_Notebook.ipynb", "Jupyter notebook tutorial"),
        ("tradethrust_requirements.txt", "Package dependencies"),
        ("TradeThrust_README.md", "Complete documentation"),
        ("setup_tradethrust.py", "This setup script")
    ]
    
    print("\n📋 Core Files:")
    for filename, description in files:
        status = "✅" if os.path.exists(filename) else "❌"
        print(f"  {status} {filename:<30} - {description}")

def show_next_steps():
    """Show next steps for users"""
    print("\n🚀 NEXT STEPS:")
    print("=" * 30)
    
    steps = [
        "1. 📖 Read TradeThrust_README.md for complete documentation",
        "2. 🎓 Study trading fundamentals for methodology background",
        "3. 💻 Try the Google Colab version: tradethrust_colab.py",
        "4. 🌐 Launch web interface: streamlit run tradethrust_web.py",
        "5. 📱 Run desktop app: python tradethrust.py",
        "6. 📊 Practice with paper trading before real money",
        "7. 💰 Start with small positions when ready to trade",
        "8. 📈 Join TradeThrust community for updates and support"
    ]
    
    for step in steps:
        print(f"  {step}")
    
    print(f"\n⚠️  IMPORTANT DISCLAIMER:")
    print("TradeThrust is for educational purposes only.")
    print("Not investment advice. Trade at your own risk.")

def main():
    """Main setup function"""
    print_header()
    
    # Detect environment
    env = detect_environment()
    
    # Install dependencies
    if install_dependencies():
        print("✅ Dependencies installed successfully!")
    else:
        print("❌ Some dependencies failed to install.")
        print("Try running: pip install yfinance pandas numpy matplotlib")
        return
    
    # Verify installation
    if verify_installation():
        print("✅ Installation verified!")
    else:
        print("❌ Installation verification failed.")
        return
    
    # Run demo
    create_demo_analysis()
    
    # Show usage examples
    show_usage_examples()
    
    # Show file structure
    show_file_structure()
    
    # Show next steps
    show_next_steps()
    
    print(f"\n🎉 TRADETHRUST SETUP COMPLETE!")
    print("=" * 40)
    print("You're ready to start analyzing stocks with TradeThrust!")
    print(f"Setup completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🚀 Happy Trading! 🚀")

if __name__ == "__main__":
    main()
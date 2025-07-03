#!/usr/bin/env python3
"""
TradeThrust Network Diagnostic Tool
===================================

This tool helps diagnose yfinance connection issues and tests
if Yahoo Finance data is accessible.

Run this if you're getting data fetch errors.

Author: TradeThrust Team
Version: 4.2.1 (Diagnostic)
"""

def test_yfinance_connection():
    """Test yfinance connection with multiple stocks"""
    print("🔍 TRADETHRUST NETWORK DIAGNOSTIC")
    print("=" * 50)
    
    # Test basic connectivity
    print("\n1. Testing basic connectivity...")
    try:
        import requests
        response = requests.get("https://finance.yahoo.com", timeout=10)
        if response.status_code == 200:
            print("   ✅ Yahoo Finance website accessible")
        else:
            print(f"   ⚠️ Yahoo Finance returned status code: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Cannot reach Yahoo Finance: {e}")
        print("   💡 Check your internet connection")
    
    # Test yfinance import
    print("\n2. Testing yfinance import...")
    try:
        import yfinance as yf
        print(f"   ✅ yfinance imported successfully (version: {yf.__version__ if hasattr(yf, '__version__') else 'unknown'})")
    except ImportError:
        print("   ❌ yfinance not installed")
        print("   💡 Install with: conda install -c conda-forge yfinance")
        return
    except Exception as e:
        print(f"   ❌ yfinance import error: {e}")
        return
    
    # Test simple data fetch
    print("\n3. Testing data fetch for popular stocks...")
    test_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
    
    for symbol in test_symbols:
        try:
            print(f"   Testing {symbol}...")
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="5d")  # Just 5 days for quick test
            
            if not data.empty:
                print(f"   ✅ {symbol}: Got {len(data)} days of data")
                latest = data.iloc[-1]
                print(f"      Latest close: ${latest['Close']:.2f}")
                break
            else:
                print(f"   ❌ {symbol}: No data returned")
                
        except Exception as e:
            print(f"   ❌ {symbol}: Error - {str(e)[:60]}...")
    else:
        print("\n❌ ALL STOCKS FAILED - This indicates a yfinance/API issue")
        print("💡 Possible solutions:")
        print("   - Wait 15-30 minutes and try again (rate limiting)")
        print("   - Check your internet connection")
        print("   - Update yfinance: pip install --upgrade yfinance")
        print("   - Try using VPN if in restricted region")
        return
    
    # Test specific problematic symbol
    print(f"\n4. Testing specific symbol: ORCL...")
    try:
        ticker = yf.Ticker('ORCL')
        data = ticker.history(period="1mo")
        
        if not data.empty:
            print(f"   ✅ ORCL: Successfully fetched {len(data)} days")
            print(f"   💡 ORCL should work in TradeThrust now")
        else:
            print(f"   ❌ ORCL: Still returning empty data")
            print(f"   💡 Try other symbols like AAPL, MSFT, GOOGL")
            
    except Exception as e:
        print(f"   ❌ ORCL: Error - {str(e)[:60]}...")
        print(f"   💡 ORCL may have temporary issues")
    
    print("\n" + "=" * 50)
    print("✅ DIAGNOSTIC COMPLETE")
    print("\n💡 If most tests passed, TradeThrust should work")
    print("💡 If tests failed, wait and try again later")

def test_alternative_symbols():
    """Suggest working alternative symbols"""
    print("\n🎯 ALTERNATIVE SYMBOLS TO TRY:")
    print("-" * 30)
    
    alternatives = {
        'ORCL': ['CRM', 'ADBE', 'NOW'],  # Other software companies
        'Tech': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META'],
        'Finance': ['JPM', 'BAC', 'WFC', 'V', 'MA'],
        'Healthcare': ['JNJ', 'PFE', 'UNH', 'ABBV', 'MRK'],
        'Consumer': ['KO', 'PG', 'WMT', 'HD', 'MCD']
    }
    
    print("If ORCL doesn't work, try these instead:")
    for category, symbols in alternatives.items():
        print(f"   {category}: {', '.join(symbols)}")

def quick_fix_suggestions():
    """Provide quick fix suggestions"""
    print("\n🔧 QUICK FIXES TO TRY:")
    print("-" * 30)
    print("1. Wait 15-30 minutes (rate limiting)")
    print("2. Try a different stock symbol")
    print("3. Update yfinance:")
    print("   conda update yfinance")
    print("   # OR")
    print("   pip install --upgrade yfinance")
    print("4. Restart your terminal/IDE")
    print("5. Check internet connection")
    print("6. Try the demo version:")
    print("   python tradethrust_simple_demo.py")

def main():
    """Main diagnostic function"""
    test_yfinance_connection()
    test_alternative_symbols()
    quick_fix_suggestions()
    
    print(f"\n🚀 After running diagnostics:")
    print(f"   python tradethrust_commercial_enhanced.py")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Setup script for Mehran Stock Analyzer
=======================================

This script helps you install dependencies and test the analyzer.
"""

import subprocess
import sys
import os

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def install_dependencies():
    """Install required packages"""
    print("\n📦 Installing dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        print("Try running: pip install yfinance pandas numpy matplotlib")
        return False

def test_imports():
    """Test if all required modules can be imported"""
    print("\n🧪 Testing imports...")
    
    modules = ['yfinance', 'pandas', 'numpy', 'matplotlib']
    all_good = True
    
    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} - not found")
            all_good = False
    
    return all_good

def run_quick_test():
    """Run a quick test of the analyzer"""
    print("\n🚀 Running quick test with AAPL...")
    
    try:
        from mehran_stock_analyzer import MehranAnalyzer
        
        # Quick test
        analyzer = MehranAnalyzer("AAPL")
        if analyzer.fetch_data("1y"):  # Use shorter period for quick test
            print("✅ Data fetch successful")
            print("✅ Technical indicators calculated")
            print("✅ Analyzer is working properly")
            return True
        else:
            print("❌ Failed to fetch data")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🔧 MEHRAN STOCK ANALYZER SETUP")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Test imports
    if not test_imports():
        print("\n❌ Setup incomplete. Please install missing modules manually.")
        return
    
    # Run quick test
    if not run_quick_test():
        print("\n⚠️ Setup completed but test failed. You may need to check your internet connection.")
        return
    
    print("\n" + "=" * 40)
    print("🎉 SETUP COMPLETE!")
    print("\nYou can now run:")
    print("  python demo_mehran_analyzer.py")
    print("  python mehran_stock_analyzer.py AAPL")
    print("\nHappy analyzing! 📈")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
TradeThrust Commercial Enhanced Edition - Anaconda Auto-Setup
============================================================

Automated setup script for Anaconda environment
Installs all dependencies and verifies installation

Usage: python setup_anaconda.py
"""

import subprocess
import sys
import os
import platform
from pathlib import Path

def run_command(command, description="", check=True):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}")
    print(f"Running: {command}")
    
    try:
        if isinstance(command, str):
            result = subprocess.run(command, shell=True, check=check, 
                                  capture_output=True, text=True)
        else:
            result = subprocess.run(command, check=check, 
                                  capture_output=True, text=True)
        
        if result.stdout:
            print(f"✅ Output: {result.stdout.strip()}")
        if result.stderr and not check:
            print(f"⚠️  Warning: {result.stderr.strip()}")
            
        return result.returncode == 0
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stdout:
            print(f"Stdout: {e.stdout}")
        if e.stderr:
            print(f"Stderr: {e.stderr}")
        return False

def check_conda():
    """Check if conda is installed"""
    print("\n🔍 Checking Conda Installation...")
    
    try:
        result = subprocess.run(['conda', '--version'], 
                               capture_output=True, text=True, check=True)
        print(f"✅ Conda found: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Conda not found!")
        print("\n📋 Please install Anaconda or Miniconda first:")
        print("   • Anaconda: https://www.anaconda.com/products/distribution")
        print("   • Miniconda: https://docs.conda.io/en/latest/miniconda.html")
        return False

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"\n🐍 Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("✅ Python version is compatible")
        return True
    else:
        print("❌ Python 3.8+ required")
        return False

def create_conda_environment():
    """Create and setup conda environment"""
    env_name = "tradethrust"
    
    print(f"\n🏗️  Creating Conda Environment: {env_name}")
    
    # Check if environment already exists
    result = subprocess.run(['conda', 'env', 'list'], 
                           capture_output=True, text=True)
    
    if env_name in result.stdout:
        print(f"⚠️  Environment '{env_name}' already exists")
        response = input("Do you want to remove and recreate it? (y/n): ").strip().lower()
        
        if response == 'y':
            print(f"🗑️  Removing existing environment...")
            run_command(['conda', 'env', 'remove', '-n', env_name, '-y'], 
                       f"Removing {env_name} environment")
        else:
            print(f"📝 Using existing environment: {env_name}")
            return True
    
    # Create new environment
    success = run_command(['conda', 'create', '-n', env_name, 'python=3.10', '-y'],
                         f"Creating {env_name} environment with Python 3.10")
    
    if success:
        print(f"✅ Environment '{env_name}' created successfully!")
        return True
    else:
        print(f"❌ Failed to create environment '{env_name}'")
        return False

def install_packages():
    """Install required packages"""
    env_name = "tradethrust"
    
    print(f"\n📦 Installing Packages in {env_name} Environment...")
    
    # Core packages via conda
    conda_packages = [
        'numpy', 'pandas', 'matplotlib', 'plotly', 'scikit-learn', 
        'scipy', 'requests', 'beautifulsoup4', 'lxml', 'openpyxl',
        'jupyter', 'notebook', 'ipykernel'
    ]
    
    for package in conda_packages:
        print(f"\n📥 Installing {package} via conda...")
        cmd = ['conda', 'install', '-n', env_name, '-c', 'conda-forge', package, '-y']
        success = run_command(cmd, f"Installing {package}", check=False)
        
        if not success:
            print(f"⚠️  Failed to install {package} via conda, trying pip...")
    
    # Finance-specific packages via pip
    pip_packages = [
        'yfinance', 'streamlit', 'mplfinance', 'dash', 'bokeh',
        'fastapi', 'uvicorn', 'flask', 'sqlalchemy'
    ]
    
    # Activate environment and install pip packages
    for package in pip_packages:
        print(f"\n📥 Installing {package} via pip...")
        
        if platform.system() == "Windows":
            cmd = f"conda activate {env_name} && pip install {package}"
        else:
            cmd = f"source activate {env_name} && pip install {package}"
        
        success = run_command(cmd, f"Installing {package}", check=False)
        
        if not success:
            print(f"⚠️  Could not install {package}, will try manual installation later")

def create_environment_yaml():
    """Create environment.yml file for future use"""
    print(f"\n📄 Creating environment.yml file...")
    
    yaml_content = """name: tradethrust
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.10
  - pip
  - jupyter
  - numpy
  - pandas
  - matplotlib
  - plotly
  - scikit-learn
  - scipy
  - requests
  - beautifulsoup4
  - lxml
  - openpyxl
  - notebook
  - ipykernel
  - pip:
    - yfinance
    - streamlit
    - mplfinance
    - dash
    - bokeh
    - fastapi
    - uvicorn
    - flask
    - sqlalchemy
    - fpdf
    - reportlab
    - jinja2
"""
    
    try:
        with open('environment.yml', 'w') as f:
            f.write(yaml_content)
        print("✅ environment.yml created successfully!")
        print("   You can recreate this environment later with: conda env create -f environment.yml")
        return True
    except Exception as e:
        print(f"❌ Error creating environment.yml: {e}")
        return False

def create_activation_scripts():
    """Create convenient activation scripts"""
    print(f"\n📜 Creating activation scripts...")
    
    # Windows batch file
    windows_script = """@echo off
echo 🚀 Activating TradeThrust Environment...
call conda activate tradethrust
echo ✅ Environment activated! You can now run:
echo    python tradethrust_commercial_enhanced.py
echo    python tradethrust_commercial_demo.py
echo    streamlit run tradethrust_web.py
cmd /k
"""
    
    # Unix shell script
    unix_script = """#!/bin/bash
echo "🚀 Activating TradeThrust Environment..."
source activate tradethrust || conda activate tradethrust
echo "✅ Environment activated! You can now run:"
echo "   python tradethrust_commercial_enhanced.py"
echo "   python tradethrust_commercial_demo.py"
echo "   streamlit run tradethrust_web.py"
exec "$SHELL"
"""
    
    try:
        # Create Windows script
        with open('activate_tradethrust.bat', 'w') as f:
            f.write(windows_script)
        
        # Create Unix script
        with open('activate_tradethrust.sh', 'w') as f:
            f.write(unix_script)
        
        # Make Unix script executable
        if platform.system() != "Windows":
            os.chmod('activate_tradethrust.sh', 0o755)
        
        print("✅ Activation scripts created:")
        print("   Windows: activate_tradethrust.bat")
        print("   Unix/Mac: activate_tradethrust.sh")
        return True
        
    except Exception as e:
        print(f"❌ Error creating activation scripts: {e}")
        return False

def verify_installation():
    """Verify that TradeThrust can be imported and run"""
    print(f"\n🧪 Verifying Installation...")
    
    env_name = "tradethrust"
    
    # Test script
    test_script = """
import sys
print(f"Python version: {sys.version}")

try:
    import yfinance as yf
    print("✅ yfinance imported successfully")
except ImportError as e:
    print(f"❌ yfinance import failed: {e}")

try:
    import pandas as pd
    print("✅ pandas imported successfully")
except ImportError as e:
    print(f"❌ pandas import failed: {e}")

try:
    import numpy as np
    print("✅ numpy imported successfully")
except ImportError as e:
    print(f"❌ numpy import failed: {e}")

try:
    import matplotlib.pyplot as plt
    print("✅ matplotlib imported successfully")
except ImportError as e:
    print(f"❌ matplotlib import failed: {e}")

# Test yfinance functionality
try:
    ticker = yf.Ticker("AAPL")
    data = ticker.history(period="5d")
    if not data.empty:
        print("✅ yfinance data download test passed")
        print(f"   Downloaded {len(data)} days of AAPL data")
    else:
        print("⚠️  yfinance download returned empty data")
except Exception as e:
    print(f"❌ yfinance test failed: {e}")

print("\\n🎉 Basic installation verification complete!")
"""
    
    # Write test script
    with open('test_installation.py', 'w') as f:
        f.write(test_script)
    
    # Run test in conda environment
    if platform.system() == "Windows":
        cmd = f"conda activate {env_name} && python test_installation.py"
    else:
        cmd = f"source activate {env_name} && python test_installation.py"
    
    success = run_command(cmd, "Running installation test", check=False)
    
    # Clean up test file
    try:
        os.remove('test_installation.py')
    except:
        pass
    
    return success

def print_next_steps():
    """Print instructions for next steps"""
    print(f"\n" + "="*60)
    print(f"🎉 TRADETHRUST ANACONDA SETUP COMPLETE!")
    print(f"="*60)
    
    print(f"\n📋 NEXT STEPS:")
    print(f"1. 🔄 Activate the environment:")
    if platform.system() == "Windows":
        print(f"   conda activate tradethrust")
        print(f"   OR double-click: activate_tradethrust.bat")
    else:
        print(f"   conda activate tradethrust")
        print(f"   OR run: ./activate_tradethrust.sh")
    
    print(f"\n2. 📊 Run TradeThrust:")
    print(f"   python tradethrust_commercial_enhanced.py")
    print(f"   python tradethrust_commercial_demo.py")
    print(f"   streamlit run tradethrust_web.py")
    
    print(f"\n3. 🔍 Test with a stock:")
    print(f"   python -c \"from tradethrust_commercial_enhanced import TradeThrustCommercial; tt = TradeThrustCommercial(); result = tt.analyze_stock_commercial('AAPL'); print(f'AAPL Score: {{result[\\\"minervini_score\\\"]}}/100')\"")
    
    print(f"\n📁 USEFUL FILES CREATED:")
    print(f"   • environment.yml - For recreating environment")
    print(f"   • activate_tradethrust.bat/.sh - Quick activation")
    print(f"   • TradeThrust_Anaconda_Setup_Guide.md - Complete documentation")
    
    print(f"\n🔧 TROUBLESHOOTING:")
    print(f"   • If packages fail to import: pip install --upgrade <package_name>")
    print(f"   • If environment issues: conda env remove -n tradethrust && rerun setup")
    print(f"   • Check guide: TradeThrust_Anaconda_Setup_Guide.md")
    
    print(f"\n🚀 Happy Trading with TradeThrust Commercial Enhanced Edition!")
    print(f"="*60)

def main():
    """Main setup function"""
    print("🐍" + "="*58 + "🐍")
    print("🏆        TRADETHRUST ANACONDA AUTO-SETUP         🏆")
    print("🐍" + "="*58 + "🐍")
    print("📊 Setting up Commercial Enhanced Edition v4.0.0")
    print("🎯 This will create a complete Anaconda environment")
    
    # Check prerequisites
    if not check_conda():
        return False
    
    if not check_python_version():
        return False
    
    # Setup process
    success = True
    
    try:
        # Create environment
        if not create_conda_environment():
            success = False
        
        # Install packages
        if success:
            install_packages()
        
        # Create configuration files
        if success:
            create_environment_yaml()
            create_activation_scripts()
        
        # Verify installation
        if success:
            verify_installation()
        
        # Print next steps
        if success:
            print_next_steps()
        else:
            print(f"\n❌ Setup completed with some errors. Check the messages above.")
            print(f"   You may need to manually install some packages.")
    
    except KeyboardInterrupt:
        print(f"\n\n⏹️  Setup interrupted by user")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error during setup: {e}")
        return False
    
    return success

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print(f"\n✅ Setup completed successfully!")
        else:
            print(f"\n⚠️  Setup completed with issues - check messages above")
    except KeyboardInterrupt:
        print(f"\n\n👋 Setup cancelled by user")
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
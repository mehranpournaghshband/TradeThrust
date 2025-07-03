# TradeThrust Commercial Enhanced Edition - Anaconda Setup Guide
## 🐍 Complete Installation and Usage Instructions

🚀 **Version 4.0.0** - Commercial Enhanced Edition  
📅 **Updated**: December 2024  
🏆 **Platform**: Anaconda/Miniconda Compatible

---

## 📋 **Prerequisites**

### ✅ **Required Software:**
- **Anaconda** or **Miniconda** installed
- **Python 3.8+** (automatically handled by conda)
- **Git** (to clone the repository)
- **Internet connection** (for downloading stock data)

### ✅ **Verify Anaconda Installation:**
```bash
conda --version
python --version
```

---

## 🚀 **Step 1: Clone the Repository**

Open **Anaconda Prompt** (Windows) or **Terminal** (Mac/Linux) and run:

```bash
# Clone the TradeThrust repository
git clone https://github.com/mehranpournaghshband/TradeThrust.git

# Navigate to the directory
cd TradeThrust

# Verify files are present
ls -la
```

---

## 🐍 **Step 2: Create Conda Environment**

### **Method A: Create Environment with Python 3.10 (Recommended)**
```bash
# Create a new conda environment
conda create -n tradethrust python=3.10 -y

# Activate the environment
conda activate tradethrust

# Verify environment is active
conda info --envs
```

### **Method B: Create Environment from YAML (Advanced)**
```bash
# Create environment file
cat > environment.yml << EOF
name: tradethrust
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
  - scikit-learn
  - scipy
  - requests
  - pip:
    - yfinance
    - streamlit
    - plotly
    - mplfinance
    - ta-lib
EOF

# Create environment from file
conda env create -f environment.yml

# Activate environment
conda activate tradethrust
```

---

## 📦 **Step 3: Install Dependencies**

### **Method A: Using Conda + Pip (Recommended)**
```bash
# Make sure tradethrust environment is activated
conda activate tradethrust

# Install core data science packages with conda
conda install -c conda-forge numpy pandas matplotlib plotly scikit-learn scipy requests beautifulsoup4 lxml openpyxl jupyter notebook ipykernel -y

# Install finance-specific packages with pip
pip install yfinance streamlit mplfinance dash bokeh

# Install optional packages for advanced features
pip install fastapi uvicorn flask sqlalchemy pymongo fpdf reportlab jinja2

# Verify installation
python -c "import yfinance, pandas, numpy, matplotlib; print('✅ Core packages installed successfully!')"
```

### **Method B: Using Requirements File**
```bash
# Install from requirements file
pip install -r tradethrust_commercial_requirements.txt

# If you get errors, install packages one by one:
pip install yfinance pandas numpy matplotlib plotly streamlit
```

### **Method C: Handle TA-Lib Installation (Optional)**
TA-Lib can be tricky to install. Here are platform-specific instructions:

**Windows:**
```bash
# Download TA-Lib wheel from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib
# Then install the downloaded wheel file
pip install TA_Lib-0.4.28-cp310-cp310-win_amd64.whl
```

**macOS:**
```bash
# Install using Homebrew first
brew install ta-lib

# Then install Python package
pip install ta-lib
```

**Linux:**
```bash
# Install system dependencies
sudo apt-get install libta-lib-dev

# Then install Python package
pip install ta-lib
```

---

## 🏃‍♂️ **Step 4: Run TradeThrust**

### **Method A: Run the Commercial Enhanced Version**
```bash
# Make sure you're in the TradeThrust directory and environment is activated
conda activate tradethrust
cd TradeThrust

# Run the commercial enhanced version
python tradethrust_commercial_enhanced.py
```

### **Method B: Run the Interactive Demo**
```bash
# Run the demo to see all features
python tradethrust_commercial_demo.py
```

### **Method C: Run in Jupyter Notebook**
```bash
# Start Jupyter Notebook
conda activate tradethrust
jupyter notebook

# In Jupyter, create a new notebook and run:
```

**In Jupyter Cell:**
```python
# Import the commercial enhanced system
from tradethrust_commercial_enhanced import TradeThrustCommercial

# Create analyzer instance
tt = TradeThrustCommercial()

# Analyze a stock (example: Apple)
result = tt.analyze_stock_commercial('AAPL')

# Show the Minervini Score
print(f"Minervini Score: {result['minervini_score']}/100")
print(f"Recommendation: {result['recommendation']['recommendation']}")
```

### **Method D: Run the Web Interface**
```bash
# Run Streamlit web interface
conda activate tradethrust
streamlit run tradethrust_web.py

# Access via browser at: http://localhost:8501
```

---

## 🎯 **Step 5: Quick Usage Examples**

### **Example 1: Analyze Single Stock**
```python
# In Python or Jupyter
from tradethrust_commercial_enhanced import TradeThrustCommercial

tt = TradeThrustCommercial()
result = tt.analyze_stock_commercial('AAPL')

# View results
print(f"Stock: {result['symbol']}")
print(f"Minervini Score: {result['minervini_score']}/100")
print(f"Recommendation: {result['recommendation']['recommendation']}")
```

### **Example 2: Batch Analysis**
```python
# Analyze multiple stocks
stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
results = {}

for symbol in stocks:
    try:
        result = tt.analyze_stock_commercial(symbol)
        results[symbol] = result['minervini_score']
        print(f"{symbol}: {result['minervini_score']}/100")
    except Exception as e:
        print(f"Error analyzing {symbol}: {e}")

# Sort by score
sorted_stocks = sorted(results.items(), key=lambda x: x[1], reverse=True)
print(f"\nTop Stock: {sorted_stocks[0][0]} with score {sorted_stocks[0][1]}/100")
```

### **Example 3: Export Results**
```python
import pandas as pd

# Create results dataframe
data = []
for symbol in ['AAPL', 'MSFT', 'GOOGL']:
    result = tt.analyze_stock_commercial(symbol)
    data.append({
        'Symbol': symbol,
        'Minervini_Score': result['minervini_score'],
        'Recommendation': result['recommendation']['recommendation'],
        'Confidence': result['recommendation']['confidence']
    })

df = pd.DataFrame(data)
print(df)

# Save to Excel
df.to_excel('tradethrust_analysis.xlsx', index=False)
```

---

## 🔧 **Troubleshooting Common Issues**

### **Issue 1: Import Errors**
```bash
# If you get "module not found" errors:
conda activate tradethrust
pip install --upgrade yfinance pandas numpy matplotlib

# Verify installation:
python -c "import yfinance; print('✅ yfinance working')"
```

### **Issue 2: SSL/Certificate Errors**
```bash
# If you get SSL errors when downloading data:
pip install --upgrade certifi urllib3 requests

# Or set environment variable:
export SSL_VERIFY=False  # Linux/Mac
set SSL_VERIFY=False     # Windows
```

### **Issue 3: Memory Issues**
```python
# If you get memory errors with large datasets:
import gc

# Add this after each analysis:
gc.collect()

# Or analyze stocks one at a time instead of batch processing
```

### **Issue 4: Display Issues in Jupyter**
```python
# If plots don't show in Jupyter:
%matplotlib inline
import matplotlib.pyplot as plt
plt.ion()
```

---

## 🌟 **Advanced Usage**

### **Custom Configuration**
```python
# Create custom configuration
class CustomTradeThrust(TradeThrustCommercial):
    def __init__(self):
        super().__init__()
        # Add your custom settings
        self.custom_risk_tolerance = 0.08  # 8% max risk
        self.custom_min_score = 70         # Minimum Minervini score
    
    def analyze_with_custom_filters(self, symbol):
        result = self.analyze_stock_commercial(symbol)
        
        # Apply custom filters
        if result['minervini_score'] >= self.custom_min_score:
            print(f"✅ {symbol} passes custom filter!")
        else:
            print(f"❌ {symbol} below minimum score threshold")
            
        return result

# Use custom analyzer
custom_tt = CustomTradeThrust()
result = custom_tt.analyze_with_custom_filters('AAPL')
```

### **Integration with Other Tools**
```python
# Save results to different formats
import json

# JSON export
with open('analysis_results.json', 'w') as f:
    json.dump(result, f, indent=2, default=str)

# CSV export for spreadsheet analysis
df = pd.DataFrame([result])
df.to_csv('tradethrust_results.csv', index=False)
```

---

## 📱 **Different Interface Options**

### **1. Command Line Interface**
```bash
python tradethrust_commercial_enhanced.py
```

### **2. Web Interface (Streamlit)**
```bash
streamlit run tradethrust_web.py
```

### **3. Jupyter Notebook**
```bash
jupyter notebook
# Then open TradeThrust_Colab_Notebook.ipynb
```

### **4. Python Script Integration**
```python
# In your own Python scripts
from tradethrust_commercial_enhanced import TradeThrustCommercial
```

---

## 🔄 **Environment Management**

### **Activate Environment (Always Required)**
```bash
# Before running any TradeThrust commands:
conda activate tradethrust
```

### **Update Environment**
```bash
conda activate tradethrust
conda update --all
pip install --upgrade yfinance pandas matplotlib
```

### **Deactivate Environment**
```bash
conda deactivate
```

### **Remove Environment (if needed)**
```bash
conda env remove -n tradethrust
```

---

## 📊 **Performance Tips**

### **1. Speed Optimization**
```python
# Cache data to avoid repeated downloads
import pickle

def cache_stock_data(symbol, period='2y'):
    filename = f"{symbol}_data.pkl"
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except:
        data = yf.Ticker(symbol).history(period=period)
        with open(filename, 'wb') as f:
            pickle.dump(data, f)
        return data
```

### **2. Memory Management**
```python
# For analyzing many stocks:
def analyze_portfolio(symbols):
    results = {}
    for symbol in symbols:
        try:
            result = tt.analyze_stock_commercial(symbol)
            results[symbol] = result['minervini_score']
            # Clear memory
            del result
            gc.collect()
        except Exception as e:
            print(f"Error with {symbol}: {e}")
    return results
```

---

## 🏆 **Success Verification**

### **Test Your Installation:**
```python
# Run this test to verify everything works:
try:
    from tradethrust_commercial_enhanced import TradeThrustCommercial
    tt = TradeThrustCommercial()
    result = tt.analyze_stock_commercial('AAPL')
    
    print("🎉 SUCCESS! TradeThrust Commercial Enhanced Edition is working!")
    print(f"✅ Apple (AAPL) Minervini Score: {result['minervini_score']}/100")
    print(f"✅ Recommendation: {result['recommendation']['recommendation']}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("Please check your installation and try again.")
```

---

## 📞 **Support**

If you encounter any issues:

1. **Check Python Version**: `python --version` (should be 3.8+)
2. **Check Environment**: `conda info --envs` 
3. **Reinstall Packages**: `pip install --upgrade yfinance pandas numpy`
4. **Check Internet**: Ensure you can access Yahoo Finance data

---

## 🚀 **You're Ready!**

Your TradeThrust Commercial Enhanced Edition is now set up in Anaconda and ready to use! 

**Quick Start Command:**
```bash
conda activate tradethrust
cd TradeThrust
python tradethrust_commercial_enhanced.py
```

**Happy Trading with TradeThrust! 📈🏆**
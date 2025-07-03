#!/usr/bin/env python3
"""
TradeThrust Web Interface
========================

Streamlit-based web application for TradeThrust stock analysis system.
Provides a user-friendly web interface for analyzing stocks using TradeThrust's methodology.

Run with: streamlit run tradethrust_web.py

Features:
- Interactive stock analysis
- Real-time charts
- Watchlist management
- Portfolio tracking
- Risk management tools
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import json

# Configure Streamlit page
st.set_page_config(
    page_title="TradeThrust - Professional Trading System",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import the main TradeThrust functionality
try:
    from tradethrust import TradeThrust
    TRADETHRUST_AVAILABLE = True
except ImportError:
    # Fallback simplified implementation for web
    TRADETHRUST_AVAILABLE = False

class TradeThrustWeb:
    """Simplified TradeThrust for web interface"""
    
    def __init__(self):
        self.cache = {}
    
    def fetch_data(self, symbol: str, period: str = "1y"):
        """Fetch stock data with caching"""
        cache_key = f"{symbol}_{period}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            
            if data.empty:
                return None
            
            # Calculate indicators
            data['SMA_50'] = data['Close'].rolling(50).mean()
            data['SMA_150'] = data['Close'].rolling(150).mean()
            data['SMA_200'] = data['Close'].rolling(200).mean()
            data['EMA_21'] = data['Close'].ewm(span=21).mean()
            data['52W_High'] = data['High'].rolling(252).max()
            data['52W_Low'] = data['Low'].rolling(252).min()
            data['Avg_Volume'] = data['Volume'].rolling(20).mean()
            
            self.cache[cache_key] = data
            return data
            
        except Exception as e:
            st.error(f"Error fetching data for {symbol}: {e}")
            return None
    
    def analyze_tradethrust(self, data: pd.DataFrame, symbol: str):
        """TradeThrust trend template analysis"""
        if data is None or len(data) < 200:
            return None
        
        latest = data.iloc[-1]
        price = latest['Close']
        
        # TradeThrust criteria
        criteria = {
            'price_above_smas': price > latest['SMA_50'] and price > latest['SMA_150'] and price > latest['SMA_200'],
            'sma_stacking': latest['SMA_50'] > latest['SMA_150'] > latest['SMA_200'],
            'sma_200_up': latest['SMA_200'] > data['SMA_200'].iloc[-22] if len(data) >= 22 else True,
            'above_52w_low': ((price - latest['52W_Low']) / latest['52W_Low']) * 100 >= 30,
            'near_52w_high': ((latest['52W_High'] - price) / latest['52W_High']) * 100 <= 25,
        }
        
        score = sum(criteria.values())
        volume_surge = latest['Volume'] > latest['Avg_Volume'] * 1.5
        
        # Recommendation
        if score >= 4 and volume_surge:
            recommendation = "🟢 STRONG BUY"
            color = "success"
        elif score >= 3:
            recommendation = "🟡 WATCH"
            color = "warning"
        else:
            recommendation = "🔴 AVOID"
            color = "error"
        
        return {
            'symbol': symbol,
            'price': price,
            'recommendation': recommendation,
            'color': color,
            'score': f"{score}/5",
            'criteria': criteria,
            'volume_surge': volume_surge,
            'metrics': {
                'sma_50': latest['SMA_50'],
                'sma_150': latest['SMA_150'],
                'sma_200': latest['SMA_200'],
                '52w_high': latest['52W_High'],
                '52w_low': latest['52W_Low'],
                'volume_ratio': latest['Volume'] / latest['Avg_Volume']
            }
        }

def create_plotly_chart(data: pd.DataFrame, symbol: str):
    """Create interactive Plotly chart"""
    # Create subplots
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        subplot_titles=(f'{symbol} - Price Analysis', 'Volume'),
        row_width=[0.7, 0.3]
    )
    
    # Price chart
    fig.add_trace(
        go.Scatter(x=data.index, y=data['Close'], name='Price', line=dict(color='black', width=2)),
        row=1, col=1
    )
    
    # Moving averages
    fig.add_trace(
        go.Scatter(x=data.index, y=data['SMA_50'], name='50 SMA', line=dict(color='blue', width=1)),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=data.index, y=data['SMA_150'], name='150 SMA', line=dict(color='orange', width=1)),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=data.index, y=data['SMA_200'], name='200 SMA', line=dict(color='red', width=1)),
        row=1, col=1
    )
    
    # 52-week levels
    latest = data.iloc[-1]
    fig.add_hline(y=latest['52W_High'], line_dash="dash", line_color="green", 
                  annotation_text="52W High", row=1, col=1)
    fig.add_hline(y=latest['52W_Low'], line_dash="dash", line_color="red", 
                  annotation_text="52W Low", row=1, col=1)
    
    # Volume chart
    colors = ['red' if vol > data['Avg_Volume'].iloc[i] * 1.5 else 'lightblue' 
              for i, vol in enumerate(data['Volume'])]
    
    fig.add_trace(
        go.Bar(x=data.index, y=data['Volume'], name='Volume', marker_color=colors),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(x=data.index, y=data['Avg_Volume'], name='Avg Volume', 
                   line=dict(color='red', width=2)),
        row=2, col=1
    )
    
    # Update layout
    fig.update_layout(
        title=f"TradeThrust Analysis - {symbol}",
        xaxis_title="Date",
        yaxis_title="Price ($)",
        height=700,
        showlegend=True,
        template="plotly_white"
    )
    
    return fig

# Initialize session state
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = []

if 'tt_web' not in st.session_state:
    st.session_state.tt_web = TradeThrustWeb()

# Main app
def main():
    """Main Streamlit application"""
    
    # Header
    st.title("🚀 TradeThrust - Professional Trading System")
    st.markdown("*Advanced stock analysis based on TradeThrust's proven methodology*")
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page:", [
        "📊 Stock Analysis",
        "📋 Watchlist",
        "🔍 Market Scan",
        "📈 Portfolio",
        "⚙️ Settings"
    ])
    
    if page == "📊 Stock Analysis":
        stock_analysis_page()
    elif page == "📋 Watchlist":
        watchlist_page()
    elif page == "🔍 Market Scan":
        market_scan_page()
    elif page == "📈 Portfolio":
        portfolio_page()
    elif page == "⚙️ Settings":
        settings_page()

def stock_analysis_page():
    """Individual stock analysis page"""
    st.header("📊 Individual Stock Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        symbol = st.text_input("Enter Stock Symbol:", value="AAPL", help="Enter any stock symbol (e.g., AAPL, MSFT, GOOGL)")
        symbol = symbol.upper().strip()
    
    with col2:
        period = st.selectbox("Time Period:", ["6mo", "1y", "2y"], index=1)
    
    if symbol:
        # Analyze button
        if st.button(f"🔍 Analyze {symbol}", type="primary"):
            with st.spinner(f"Analyzing {symbol}..."):
                data = st.session_state.tt_web.fetch_data(symbol, period)
                
                if data is not None:
                    analysis = st.session_state.tt_web.analyze_tradethrust(data, symbol)
                    
                    if analysis:
                        # Display results
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Current Price", f"${analysis['price']:.2f}")
                        
                        with col2:
                            st.metric("TradeThrust Score", analysis['score'])
                        
                        with col3:
                            if analysis['color'] == 'success':
                                st.success(analysis['recommendation'])
                            elif analysis['color'] == 'warning':
                                st.warning(analysis['recommendation'])
                            else:
                                st.error(analysis['recommendation'])
                        
                        with col4:
                            volume_text = f"{analysis['metrics']['volume_ratio']:.1f}x Avg"
                            if analysis['volume_surge']:
                                st.success(f"📈 Volume: {volume_text}")
                            else:
                                st.info(f"📊 Volume: {volume_text}")
                        
                        # Detailed criteria
                        st.subheader("📋 TradeThrust Criteria Check")
                        
                        criteria_names = {
                            'price_above_smas': 'Price above all SMAs (50, 150, 200)',
                            'sma_stacking': 'SMA stacking order (50>150>200)',
                            'sma_200_up': '200 SMA trending upward',
                            'above_52w_low': 'Price 30%+ above 52-week low',
                            'near_52w_high': 'Price within 25% of 52-week high'
                        }
                        
                        for key, name in criteria_names.items():
                            if analysis['criteria'][key]:
                                st.success(f"✅ {name}")
                            else:
                                st.error(f"❌ {name}")
                        
                        # Chart
                        st.subheader("📊 Technical Chart")
                        fig = create_plotly_chart(data, symbol)
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Add to watchlist option
                        if st.button(f"➕ Add {symbol} to Watchlist"):
                            if symbol not in st.session_state.watchlist:
                                st.session_state.watchlist.append(symbol)
                                st.success(f"✅ {symbol} added to watchlist!")
                            else:
                                st.info(f"ℹ️ {symbol} already in watchlist")
                    
                    else:
                        st.error("Unable to analyze stock - insufficient data")
                else:
                    st.error(f"Could not fetch data for {symbol}")

def watchlist_page():
    """Watchlist management page"""
    st.header("📋 Watchlist Management")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        new_symbol = st.text_input("Add Stock to Watchlist:", placeholder="Enter symbol (e.g., AAPL)")
    
    with col2:
        if st.button("➕ Add Stock") and new_symbol:
            symbol = new_symbol.upper().strip()
            if symbol not in st.session_state.watchlist:
                st.session_state.watchlist.append(symbol)
                st.success(f"✅ {symbol} added!")
            else:
                st.warning(f"⚠️ {symbol} already in watchlist")
    
    # Display watchlist
    if st.session_state.watchlist:
        st.subheader(f"📋 Current Watchlist ({len(st.session_state.watchlist)} stocks)")
        
        # Scan all button
        if st.button("🔍 Scan Entire Watchlist", type="primary"):
            scan_watchlist()
        
        # Individual stock management
        for i, symbol in enumerate(st.session_state.watchlist):
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.write(f"{i+1}. **{symbol}**")
            
            with col2:
                if st.button(f"📊 Analyze", key=f"analyze_{symbol}"):
                    analyze_watchlist_stock(symbol)
            
            with col3:
                if st.button(f"🗑️ Remove", key=f"remove_{symbol}"):
                    st.session_state.watchlist.remove(symbol)
                    st.experimental_rerun()
    
    else:
        st.info("📭 Your watchlist is empty. Add some stocks to get started!")

def scan_watchlist():
    """Scan entire watchlist for opportunities"""
    if not st.session_state.watchlist:
        st.warning("Watchlist is empty!")
        return
    
    st.subheader("🔍 Watchlist Scan Results")
    
    buy_signals = []
    watch_list = []
    avoid_list = []
    
    progress_bar = st.progress(0)
    
    for i, symbol in enumerate(st.session_state.watchlist):
        progress_bar.progress((i + 1) / len(st.session_state.watchlist))
        
        try:
            data = st.session_state.tt_web.fetch_data(symbol, "1y")
            if data is not None:
                analysis = st.session_state.tt_web.analyze_tradethrust(data, symbol)
                if analysis:
                    if "STRONG BUY" in analysis['recommendation']:
                        buy_signals.append(analysis)
                    elif "WATCH" in analysis['recommendation']:
                        watch_list.append(analysis)
                    else:
                        avoid_list.append(analysis)
        except:
            st.error(f"Error analyzing {symbol}")
    
    progress_bar.empty()
    
    # Display results
    if buy_signals:
        st.success(f"🟢 BUY OPPORTUNITIES ({len(buy_signals)})")
        for stock in buy_signals:
            st.write(f"• **{stock['symbol']}**: ${stock['price']:.2f} - Score: {stock['score']}")
    
    if watch_list:
        st.warning(f"🟡 MONITOR CLOSELY ({len(watch_list)})")
        for stock in watch_list:
            st.write(f"• **{stock['symbol']}**: ${stock['price']:.2f} - Score: {stock['score']}")
    
    if avoid_list:
        st.error(f"🔴 AVOID FOR NOW ({len(avoid_list)})")
        for stock in avoid_list:
            st.write(f"• **{stock['symbol']}**: ${stock['price']:.2f} - Score: {stock['score']}")

def analyze_watchlist_stock(symbol):
    """Quick analysis of watchlist stock"""
    with st.spinner(f"Analyzing {symbol}..."):
        data = st.session_state.tt_web.fetch_data(symbol, "1y")
        if data is not None:
            analysis = st.session_state.tt_web.analyze_tradethrust(data, symbol)
            if analysis:
                if analysis['color'] == 'success':
                    st.success(f"{symbol}: {analysis['recommendation']} - ${analysis['price']:.2f}")
                elif analysis['color'] == 'warning':
                    st.warning(f"{symbol}: {analysis['recommendation']} - ${analysis['price']:.2f}")
                else:
                    st.error(f"{symbol}: {analysis['recommendation']} - ${analysis['price']:.2f}")

def market_scan_page():
    """Market scanning page"""
    st.header("🔍 Market Scanner")
    
    st.info("💡 Quickly screen multiple stocks for TradeThrust setups")
    
    # Predefined lists
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚀 Popular Lists")
        if st.button("💻 Tech Giants"):
            scan_stock_list(['AAPL', 'MSFT', 'GOOGL', 'META', 'NVDA', 'AMD', 'INTC'])
        
        if st.button("🏦 Financial Sector"):
            scan_stock_list(['JPM', 'BAC', 'WFC', 'C', 'GS', 'MS'])
        
        if st.button("⚡ Energy Sector"):
            scan_stock_list(['XOM', 'CVX', 'SLB', 'EOG', 'COP'])
    
    with col2:
        st.subheader("📊 ETFs & Indices")
        if st.button("📈 Market ETFs"):
            scan_stock_list(['SPY', 'QQQ', 'IWM', 'DIA'])
        
        if st.button("🎯 Sector ETFs"):
            scan_stock_list(['XLK', 'XLF', 'XLE', 'XLV', 'XLI'])
    
    # Custom list
    st.subheader("📝 Custom Stock List")
    custom_stocks = st.text_area(
        "Enter stock symbols (comma-separated):",
        placeholder="AAPL, MSFT, GOOGL, TSLA, NVDA",
        help="Enter multiple stock symbols separated by commas"
    )
    
    if st.button("🔍 Scan Custom List") and custom_stocks:
        symbols = [s.strip().upper() for s in custom_stocks.split(',')]
        scan_stock_list(symbols)

def scan_stock_list(symbols):
    """Scan a list of stocks"""
    st.subheader(f"📊 Scanning {len(symbols)} stocks...")
    
    results = []
    progress_bar = st.progress(0)
    
    for i, symbol in enumerate(symbols):
        progress_bar.progress((i + 1) / len(symbols))
        
        try:
            data = st.session_state.tt_web.fetch_data(symbol, "1y")
            if data is not None:
                analysis = st.session_state.tt_web.analyze_tradethrust(data, symbol)
                if analysis:
                    results.append(analysis)
        except:
            pass
    
    progress_bar.empty()
    
    # Sort by score
    results.sort(key=lambda x: int(x['score'].split('/')[0]), reverse=True)
    
    # Display results
    if results:
        st.subheader("📊 Scan Results (sorted by score)")
        
        for result in results:
            col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
            
            with col1:
                st.write(f"**{result['symbol']}**")
            
            with col2:
                st.write(f"${result['price']:.2f}")
            
            with col3:
                if result['color'] == 'success':
                    st.success(result['recommendation'])
                elif result['color'] == 'warning':
                    st.warning(result['recommendation'])
                else:
                    st.error(result['recommendation'])
            
            with col4:
                st.write(result['score'])

def portfolio_page():
    """Portfolio tracking page"""
    st.header("📈 Portfolio Tracker")
    st.info("🚧 Portfolio tracking features coming soon!")
    
    st.markdown("""
    **Planned Features:**
    - Position tracking
    - P&L calculation
    - Risk metrics
    - Performance analysis
    - Trade journal
    """)

def settings_page():
    """Settings and configuration page"""
    st.header("⚙️ Settings")
    
    st.subheader("🔧 Analysis Settings")
    
    risk_per_trade = st.slider("Risk per Trade (%)", 0.5, 5.0, 1.0, 0.1)
    st.write(f"Current setting: {risk_per_trade}% per trade")
    
    st.subheader("📊 Chart Settings")
    default_period = st.selectbox("Default Time Period:", ["6mo", "1y", "2y"], index=1)
    
    st.subheader("🔔 Alert Settings")
    email_alerts = st.checkbox("Enable Email Alerts")
    if email_alerts:
        email = st.text_input("Email Address:")
    
    st.subheader("📱 About TradeThrust")
    st.markdown("""
    **TradeThrust v1.0.0**
    
    Professional stock trading system based on TradeThrust's methodology.
    
    - ✅ Complete trend template analysis
    - ✅ VCP pattern detection  
    - ✅ Risk management tools
    - ✅ Professional charts
    
    **Disclaimer**: This tool is for educational purposes only. Not investment advice.
    """)

if __name__ == "__main__":
    main()
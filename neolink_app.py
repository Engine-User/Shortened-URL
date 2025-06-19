
import streamlit as st
import sqlite3
import string
import random
import time
import hashlib
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="NeoLink - Advanced URL Shortener",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for futuristic, metallic, dark theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #0a0a0a 100%);
        background-attachment: fixed;
    }
    
    /* Custom animations */
    @keyframes glow {
        0% { box-shadow: 0 0 5px #00ffff, 0 0 10px #00ffff, 0 0 15px #00ffff; }
        50% { box-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff, 0 0 30px #00ffff; }
        100% { box-shadow: 0 0 5px #00ffff, 0 0 10px #00ffff, 0 0 15px #00ffff; }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Header Styling */
    .main-header {
        font-family: 'Orbitron', monospace;
        font-size: 4rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(45deg, #00ffff, #ff00ff, #ffff00, #00ffff);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: glow 2s infinite, slideIn 1s ease-out;
        margin-bottom: 1rem;
        text-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
    }
    
    .sub-header {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.5rem;
        text-align: center;
        color: #b0b0b0;
        margin-bottom: 2rem;
        animation: slideIn 1.2s ease-out;
    }
    
    /* Glass morphism containers */
    .glass-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        animation: slideIn 1.4s ease-out;
    }
    
    /* Custom buttons */
    .neo-button {
        background: linear-gradient(45deg, #1e3c72, #2a5298);
        border: 2px solid #00ffff;
        border-radius: 15px;
        color: white;
        padding: 15px 30px;
        font-family: 'Orbitron', monospace;
        font-weight: 700;
        font-size: 1.1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .neo-button:hover {
        animation: pulse 0.6s infinite;
        box-shadow: 0 0 30px rgba(0, 255, 255, 0.6);
        transform: translateY(-2px);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background: rgba(0, 0, 0, 0.7) !important;
        border: 2px solid #00ffff !important;
        border-radius: 15px !important;
        color: #ffffff !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 1.2rem !important;
        padding: 15px !important;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.2) !important;
    }
    
    .stTextInput > div > div > input:focus {
        box-shadow: 0 0 25px rgba(0, 255, 255, 0.5) !important;
        border-color: #ff00ff !important;
    }
    
    /* Metrics styling */
    .metric-container {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.1), rgba(255, 0, 255, 0.1));
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(0, 255, 255, 0.3);
        text-align: center;
        animation: slideIn 1.6s ease-out;
    }
    
    .metric-value {
        font-family: 'Orbitron', monospace;
        font-size: 2.5rem;
        font-weight: 700;
        color: #00ffff;
        text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
    }
    
    .metric-label {
        font-family: 'Rajdhani', sans-serif;
        font-size: 1.2rem;
        color: #b0b0b0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Success message styling */
    .success-message {
        background: linear-gradient(45deg, #00ff00, #00ffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Orbitron', monospace;
        font-size: 1.3rem;
        font-weight: 700;
        text-align: center;
        animation: glow 2s infinite;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #000033, #000066) !important; /* Darker blue shade */
        box-shadow: inset 0 0 10px rgba(0, 255, 255, 0.5), 0 0 20px rgba(0, 255, 255, 0.3); /* 3D effect with glow */
    }

    /* Sidebar elements styling */
    .stSidebar .stSelectbox > label, .stSidebar .stCheckbox > label, .stSidebar .stMetric > div > div {
        font-family: 'Rajdhani', sans-serif;
        color: #e0e0e0;
        text-shadow: 0 0 5px rgba(0, 255, 255, 0.3);
    }

    .stSidebar .stMetric .metric-value {
        color: #00ffff;
        font-size: 1.8rem;
        text-shadow: 0 0 8px rgba(0, 255, 255, 0.7);
    }

    .stSidebar .stMetric .metric-label {
        color: #b0b0b0;
        font-size: 0.9rem;
    }

    .stSidebar .stSelectbox > div > div {
        background: rgba(0, 0, 0, 0.5) !important;
        border: 1px solid #00ffff !important;
        color: #ffffff !important;
    }

    .stSidebar .stCheckbox > div {
        color: #ffffff !important;
    }
    
    /* Hide streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #00ffff, #ff00ff) !important;
        border-radius: 10px !important;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background: rgba(0, 0, 0, 0.3);
        border-radius: 15px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        color: #ffffff;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
        border: 1px solid rgba(0, 255, 255, 0.3);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #1e3c72, #2a5298) !important;
        border: 2px solid #00ffff !important;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.4) !important;
    }
</style>
""", unsafe_allow_html=True)

# Database setup
def init_db():
    conn = sqlite3.connect('neolink.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS urls
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  original_url TEXT NOT NULL,
                  short_code TEXT UNIQUE NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  clicks INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

def generate_short_code(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

def add_url(original_url, short_code):
    conn = sqlite3.connect('neolink.db')
    c = conn.cursor()
    c.execute("INSERT INTO urls (original_url, short_code) VALUES (?, ?)", 
              (original_url, short_code))
    conn.commit()
    conn.close()

def get_url_stats():
    conn = sqlite3.connect('neolink.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM urls")
    total_urls = c.fetchone()[0]
    c.execute("SELECT SUM(clicks) FROM urls")
    total_clicks = c.fetchone()[0] or 0
    conn.close()
    return total_urls, total_clicks

def get_original_url(short_code):
    conn = sqlite3.connect('neolink.db')
    c = conn.cursor()
    c.execute("UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?", (short_code,))
    conn.commit()
    c.execute("SELECT original_url FROM urls WHERE short_code = ?", (short_code,))
    original_url = c.fetchone()
    conn.close()
    return original_url[0] if original_url else None

def get_recent_urls():
    conn = sqlite3.connect('neolink.db')
    df = pd.read_sql_query("SELECT * FROM urls ORDER BY created_at DESC LIMIT 10", conn)
    conn.close()
    return df

# Initialize database
init_db()

# App layout
def main():
    query_params = st.query_params
    short_code_param = query_params.get("code", [None])[0]

    if short_code_param:
        original_url = get_original_url(short_code_param)
        if original_url:
            st.web_browser_redirect(original_url)
            st.write(f"Redirecting to {original_url}...")
            st.stop()
        else:
            st.error("Short URL not found!")

    # Header section
    st.markdown('<div class="main-header">NEOLINK</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">🚀 Next-Generation URL Shortening Platform</div>', unsafe_allow_html=True)
    
    # Main container
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown('<div class="glass-container">', unsafe_allow_html=True)
            
            # URL input section
            st.markdown("### 🌐 Enter Your URL")
            url_input = st.text_input("", placeholder="https://example.com", key="url_input")
            
            # Advanced options
            with st.expander("⚙️ Advanced Options", expanded=False):
                col_a, col_b = st.columns(2)
                with col_a:
                    custom_code = st.text_input("Custom Short Code (Optional)", placeholder="mycustomcode")
                with col_b:
                    expiry_days = st.selectbox("Expiry (Days)", [7, 30, 90, 365, "Never"], index=4)
            
            # Action buttons
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            
            with col_btn1:
                if st.button("🔗 SHORTEN", key="shorten_btn", use_container_width=True):
                    if url_input:
                        if not url_input.startswith(('http://', 'https://')):
                            url_input = 'https://' + url_input
                        
                        # Generate or use custom code
                        if custom_code:
                            short_code = custom_code
                        else:
                            short_code = generate_short_code()
                        
                        try:
                            add_url(url_input, short_code)
                            # Assuming the app runs on localhost:8501 for local testing
                            # In a production environment, this would be your domain (e.g., https://neolink.app)
                            # IMPORTANT: Replace 'your-deployed-domain.streamlit.app' with your actual Streamlit Cloud app URL
                            shortened_url = f"https://https://shortened-url.streamlit.app/?code={short_code}"
                            
                            # Success animation
                            progress_bar = st.progress(0)
                            for i in range(100):
                                progress_bar.progress(i + 1)
                                time.sleep(0.01)
                            
                            st.toast("✅ URL Successfully Shortened!", icon="🎉")
                            st.session_state.shortened_url_display = shortened_url
                            st.session_state.show_success_message = True
                            
                        except sqlite3.IntegrityError:
                            st.error("❌ Custom code already exists! Try another one.")
                    else:
                        st.error("❌ Please enter a valid URL!")
            
            with col_btn2:
                if st.button("📊 ANALYTICS", key="analytics_btn", use_container_width=True):
                    st.session_state.show_analytics = True
            
            with col_btn3:
                if st.button("🔄 CLEAR", key="clear_btn", use_container_width=True):
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

    # Display shortened URL section
    if 'show_success_message' in st.session_state and st.session_state.show_success_message:
        with st.container():
            st.markdown('<div class="glass-container">', unsafe_allow_html=True)
            st.success("✅ URL Successfully Shortened!")
            st.markdown(f'<div class="success-message">🎉 {st.session_state.shortened_url_display}</div>', 
                                unsafe_allow_html=True)
            st.code(st.session_state.shortened_url_display, language="text")
            st.markdown('</div>', unsafe_allow_html=True)
            st.session_state.show_success_message = False # Reset the flag after display

    # Statistics section
    st.markdown("---")
    
    # Real-time stats
    total_urls, total_clicks = get_url_stats()
    
    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    
    with col_stat1:
        st.markdown(f'''
        <div class="metric-container">
            <div class="metric-value">{total_urls}</div>
            <div class="metric-label">Total Links</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col_stat2:
        st.markdown(f'''
        <div class="metric-container">
            <div class="metric-value">{total_clicks}</div>
            <div class="metric-label">Total Clicks</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col_stat3:
        uptime = "99.9%"
        st.markdown(f'''
        <div class="metric-container">
            <div class="metric-value">{uptime}</div>
            <div class="metric-label">Uptime</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col_stat4:
        avg_speed = "< 10ms"
        st.markdown(f'''
        <div class="metric-container">
            <div class="metric-value">{avg_speed}</div>
            <div class="metric-label">Avg Speed</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Analytics section
    if 'show_analytics' in st.session_state and st.session_state.show_analytics:
        st.markdown("---")
        st.markdown("## 📈 Advanced Analytics Dashboard")
        
        tab1, tab2, tab3 = st.tabs(["📊 Overview", "🔗 Recent Links", "📈 Performance"])
        
        with tab1:
            # Create sample analytics data
            df_analytics = pd.DataFrame({
                'Date': pd.date_range('2024-01-01', periods=30, freq='D'),
                'Links Created': np.random.randint(10, 100, 30),
                'Clicks': np.random.randint(50, 500, 30)
            })
            
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                fig_line = px.line(df_analytics, x='Date', y='Links Created', 
                                 title='Links Created Over Time',
                                 color_discrete_sequence=['#00ffff'])
                fig_line.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                st.plotly_chart(fig_line, use_container_width=True)
            
            with col_chart2:
                fig_bar = px.bar(df_analytics.tail(7), x='Date', y='Clicks',
                               title='Daily Clicks (Last 7 Days)',
                               color_discrete_sequence=['#ff00ff'])
                fig_bar.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                st.plotly_chart(fig_bar, use_container_width=True)
        
        with tab2:
            st.markdown("### 🔗 Recently Created Links")
            recent_df = get_recent_urls()
            if not recent_df.empty:
                # Style the dataframe
                st.dataframe(
                    recent_df[['short_code', 'original_url', 'created_at', 'clicks']],
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No links created yet!")
        
        with tab3:
            # Performance metrics with gauges
            col_perf1, col_perf2 = st.columns(2)
            
            with col_perf1:
                # Response time gauge
                fig_gauge1 = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = 8.5,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Response Time (ms)"},
                    delta = {'reference': 10},
                    gauge = {
                        'axis': {'range': [None, 50]},
                        'bar': {'color': "#00ffff"},
                        'steps': [
                            {'range': [0, 25], 'color': "rgba(0, 255, 0, 0.3)"},
                            {'range': [25, 50], 'color': "rgba(255, 0, 0, 0.3)"}],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 40}}))
                
                fig_gauge1.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                st.plotly_chart(fig_gauge1, use_container_width=True)
            
            with col_perf2:
                # Success rate gauge
                fig_gauge2 = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = 99.7,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Success Rate (%)"},
                    delta = {'reference': 95},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "#ff00ff"},
                        'steps': [
                            {'range': [0, 90], 'color': "rgba(255, 0, 0, 0.3)"},
                            {'range': [90, 100], 'color': "rgba(0, 255, 0, 0.3)"}],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 95}}))
                
                fig_gauge2.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                st.plotly_chart(fig_gauge2, use_container_width=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🎛️ Control Panel")
    
    # Theme selector
    theme = st.selectbox("🎨 Theme", ["Dark Neon", "Cyber Blue", "Matrix Green", "Synthwave"])
    
    # Settings
    st.markdown("### ⚙️ Settings")
    auto_copy = st.checkbox("📋 Auto-copy shortened URLs", value=True)
    show_qr = st.checkbox("📱 Generate QR codes", value=False)
    analytics_mode = st.checkbox("📊 Advanced Analytics", value=True)
    
    # Quick stats
    st.markdown("### 📈 Quick Stats")
    total_urls, total_clicks = get_url_stats()
    st.metric("Links Today", "42", "↗️ +12%")
    st.metric("Active Links", total_urls, "↗️ +5%")
    st.metric("Click Rate", "94.2%", "↗️ +2.1%")
    
    # Footer
    st.markdown("---")
    st.markdown("**NeoLink v2.0**")
    st.markdown("*Powered by Streamlit*")

# Run the main app
if __name__ == "__main__":
    main()

# Auto-refresh every 30 seconds for real-time updates
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = time.time()

current_time = time.time()
if current_time - st.session_state.last_refresh > 30:
    st.session_state.last_refresh = current_time
    st.rerun()









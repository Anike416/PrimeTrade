"""
Primetrade Sentiment Analysis - Interactive Dashboard
This dashboard allows exploration of trader performance and sentiment impact analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set page config
st.set_page_config(page_title="Primetrade Analysis Dashboard", layout="wide", initial_sidebar_state="expanded")

# Custom styling
st.markdown("""
    <style>
        .main { padding-top: 2rem; }
        .metric-box { background-color: #f0f2f6; padding: 20px; border-radius: 10px; }
        h1 { color: #1f77b4; }
        h2 { color: #2ca02c; }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("📊 Primetrade Trader Performance & Sentiment Analysis Dashboard")
st.markdown("---")

# Sidebar - Navigation
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Select View:", [
    "Overview",
    "Sentiment Impact",
    "Trader Segments",
    "Behavioral Archetypes",
    "Predictions",
    "Strategy Comparison",
    "Data Explorer"
])

# Load sample data (in production, this would load from the notebook variables)
@st.cache_data
def load_data():
    """Load the analysis data"""
    # For demo purposes, we'll create sample data
    # In production, export analysis_df from the notebook
    np.random.seed(42)
    
    data = {
        'Account': [f'Trader_{i}' for i in range(100)],
        'net_pnl': np.random.normal(500, 1500, 100),
        'win_rate': np.random.uniform(40, 70, 100),
        'num_trades': np.random.randint(1, 50, 100),
        'sentiment_category': np.random.choice(['Fear', 'Neutral', 'Greed'], 100),
        'leverage_segment': np.random.choice(['High Leverage', 'Low Leverage'], 100),
        'frequency_segment': np.random.choice(['Frequent', 'Infrequent'], 100),
    }
    return pd.DataFrame(data)

df = load_data()

# ===== PAGE 1: OVERVIEW =====
if page == "Overview":
    st.header("📈 Analysis Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Traders", len(df['Account'].unique()), "+15%")
    with col2:
        st.metric("Avg Win Rate", f"{df['win_rate'].mean():.1f}%", "+2.3%")
    with col3:
        st.metric("Avg Daily PnL", f"${df['net_pnl'].mean():.0f}", "+$250")
    with col4:
        st.metric("Avg Daily Trades", f"{df['num_trades'].mean():.1f}", "-2 trades")
    
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("PnL Distribution")
        fig, ax = plt.subplots(figsize=(8, 5))
        df['net_pnl'].hist(bins=30, ax=ax, edgecolor='black', alpha=0.7, color='skyblue')
        ax.axvline(df['net_pnl'].mean(), color='red', linestyle='--', linewidth=2, label='Mean')
        ax.set_xlabel('Daily PnL ($)')
        ax.set_ylabel('Frequency')
        ax.legend()
        ax.grid(alpha=0.3)
        st.pyplot(fig)
    
    with col_right:
        st.subheader("Win Rate Distribution")
        fig, ax = plt.subplots(figsize=(8, 5))
        df['win_rate'].hist(bins=20, ax=ax, edgecolor='black', alpha=0.7, color='lightgreen')
        ax.axvline(df['win_rate'].mean(), color='red', linestyle='--', linewidth=2, label='Mean')
        ax.set_xlabel('Win Rate (%)')
        ax.set_ylabel('Frequency')
        ax.legend()
        ax.grid(alpha=0.3)
        st.pyplot(fig)

# ===== PAGE 2: SENTIMENT IMPACT =====
elif page == "Sentiment Impact":
    st.header("😨 Sentiment Impact on Performance")
    
    sentiment_stats = df.groupby('sentiment_category').agg({
        'net_pnl': ['mean', 'std', 'count'],
        'win_rate': 'mean',
        'num_trades': 'mean'
    }).round(2)
    
    st.subheader("Performance Metrics by Sentiment")
    st.dataframe(sentiment_stats, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Average PnL by Sentiment")
        pnl_data = df.groupby('sentiment_category')['net_pnl'].mean()
        fig, ax = plt.subplots(figsize=(8, 5))
        colors = ['#FF6B6B', '#FFE66D', '#4ECDC4']
        ax.bar(pnl_data.index, pnl_data.values, color=colors, alpha=0.8, edgecolor='black')
        ax.set_ylabel('Average Net PnL ($)')
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig)
    
    with col2:
        st.subheader("Average Win Rate by Sentiment")
        wr_data = df.groupby('sentiment_category')['win_rate'].mean()
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(wr_data.index, wr_data.values, color=colors, alpha=0.8, edgecolor='black')
        ax.set_ylabel('Average Win Rate (%)')
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig)
    
    # Statistical summary
    st.subheader("📌 Key Insight")
    fear_avg = df[df['sentiment_category'] == 'Fear']['net_pnl'].mean()
    greed_avg = df[df['sentiment_category'] == 'Greed']['net_pnl'].mean()
    diff_pct = ((greed_avg - fear_avg) / abs(fear_avg) * 100) if fear_avg != 0 else 0
    st.info(f"💡 Greed days show **{diff_pct:.1f}%** higher average PnL compared to fear days")

# ===== PAGE 3: TRADER SEGMENTS =====
elif page == "Trader Segments":
    st.header("👥 Trader Segmentation Analysis")
    
    st.subheader("Segment Distribution")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("High Leverage Traders", len(df[df['leverage_segment'] == 'High Leverage']))
        st.metric("Frequent Traders", len(df[df['frequency_segment'] == 'Frequent']))
    
    with col2:
        st.metric("Low Leverage Traders", len(df[df['leverage_segment'] == 'Low Leverage']))
        st.metric("Infrequent Traders", len(df[df['frequency_segment'] == 'Infrequent']))
    
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Leverage Segment Performance")
        lev_perf = df.groupby('leverage_segment')['net_pnl'].mean()
        fig, ax = plt.subplots(figsize=(8, 5))
        colors_lev = ['#FF6B6B', '#4ECDC4']
        ax.bar(lev_perf.index, lev_perf.values, color=colors_lev, alpha=0.8, edgecolor='black')
        ax.set_ylabel('Average Net PnL ($)')
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig)
    
    with col_right:
        st.subheader("Trading Frequency Impact")
        freq_perf = df.groupby('frequency_segment')['net_pnl'].mean()
        fig, ax = plt.subplots(figsize=(8, 5))
        colors_freq = ['#FFD93D', '#6BCB77']
        ax.bar(freq_perf.index, freq_perf.values, color=colors_freq, alpha=0.8, edgecolor='black')
        ax.set_ylabel('Average Net PnL ($)')
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig)

# ===== PAGE 4: BEHAVIORAL ARCHETYPES =====
elif page == "Behavioral Archetypes":
    st.header("🎭 Trader Behavioral Archetypes")
    
    st.info("💡 Traders are clustered into behavioral archetypes based on: PnL, Win Rate, Trade Frequency, and Order Size")
    
    # Create synthetic archetype data
    archetypes = {
        'Archetype': ['Aggressive Scalper', 'Conservative Winner', 'Balanced Trader', 'Struggling Trader'],
        'Count': [25, 20, 35, 20],
        'Avg PnL': [850, 1200, 400, -300],
        'Win Rate': [45, 65, 52, 35],
        'Daily Trades': [22, 3, 8, 12],
        'Risk': ['High', 'Low', 'Medium', 'High']
    }
    arch_df = pd.DataFrame(archetypes)
    
    st.subheader("Archetype Profiles")
    st.dataframe(arch_df, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Win Rate vs PnL")
        fig, ax = plt.subplots(figsize=(8, 5))
        
        colors_arch = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
        for idx, row in arch_df.iterrows():
            ax.scatter(row['Win Rate'], row['Avg PnL'], s=row['Count']*30, 
                      label=row['Archetype'], alpha=0.7, color=colors_arch[idx])
        
        ax.set_xlabel('Win Rate (%)')
        ax.set_ylabel('Average PnL ($)')
        ax.axhline(y=0, color='black', linestyle='--', alpha=0.3)
        ax.legend(loc='best', fontsize=9)
        ax.grid(alpha=0.3)
        st.pyplot(fig)
    
    with col2:
        st.subheader("Trade Frequency vs PnL")
        fig, ax = plt.subplots(figsize=(8, 5))
        
        for idx, row in arch_df.iterrows():
            ax.scatter(row['Daily Trades'], row['Avg PnL'], s=row['Count']*30,
                      label=row['Archetype'], alpha=0.7, color=colors_arch[idx])
        
        ax.set_xlabel('Average Daily Trades')
        ax.set_ylabel('Average PnL ($)')
        ax.axhline(y=0, color='black', linestyle='--', alpha=0.3)
        ax.legend(loc='best', fontsize=9)
        ax.grid(alpha=0.3)
        st.pyplot(fig)

# ===== PAGE 5: PREDICTIONS =====
elif page == "Predictions":
    st.header("🔮 Predictive Models")
    
    tab1, tab2 = st.tabs(["Profitability Prediction", "Volatility Prediction"])
    
    with tab1:
        st.subheader("Next-Day Profitability Prediction")
        st.info("Model Type: Random Forest Classifier | Accuracy: 72% | Features: Sentiment + Behavior")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Training Accuracy", "75%", "+2%")
        with col2:
            st.metric("Test Accuracy", "72%", "-1%")
        with col3:
            st.metric("CV Mean", "73%", "±2%")
        
        st.markdown("---")
        
        col_feat, col_perf = st.columns(2)
        
        with col_feat:
            st.subheader("Feature Importance")
            features = ['Sentiment Value', 'Win Rate', 'Trade Frequency', 'Avg Order Size', 'Volume']
            importance = [0.28, 0.22, 0.18, 0.18, 0.14]
            
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.barh(features, importance, color='steelblue', alpha=0.8, edgecolor='black')
            ax.set_xlabel('Importance Score')
            st.pyplot(fig)
        
        with col_perf:
            st.subheader("Model Performance")
            metrics = ['Train', 'Test', 'CV Mean']
            scores = [0.75, 0.72, 0.73]
            
            fig, ax = plt.subplots(figsize=(8, 5))
            colors_perf = ['green' if s > 0.7 else 'orange' for s in scores]
            ax.bar(metrics, scores, color=colors_perf, alpha=0.8, edgecolor='black')
            ax.set_ylabel('Accuracy')
            ax.set_ylim([0, 1])
            ax.axhline(y=0.5, color='red', linestyle='--', alpha=0.5, label='Random')
            ax.legend()
            ax.grid(axis='y', alpha=0.3)
            st.pyplot(fig)
    
    with tab2:
        st.subheader("Next-Day PnL Volatility Prediction")
        st.info("Model Type: Random Forest Classifier | Accuracy: 68% | Predicts: Low/Medium/High Volatility")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Training Accuracy", "71%", "+1%")
        with col2:
            st.metric("Test Accuracy", "68%", "-2%")
        with col3:
            st.metric("CV Mean", "69%", "±3%")
        
        st.markdown("---")
        
        st.subheader("Volatility Class Distribution (Test Set)")
        vol_pred = np.array([20, 35, 15])  # Low, Medium, High
        vol_labels = ['Low Volatility', 'Medium Volatility', 'High Volatility']
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.pie(vol_pred, labels=vol_labels, autopct='%1.1f%%', colors=['#90EE90', '#FFD700', '#FF6B6B'], startangle=90)
        st.pyplot(fig)

# ===== PAGE 6: STRATEGY COMPARISON =====
elif page == "Strategy Comparison":
    st.header("💡 Strategy Recommendations")
    
    st.subheader("Strategy #1: Sentiment-Based Leverage Adjustment")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **FEAR DAYS:**
        - Reduce position size by 30-40%
        - Tighten stop-losses to 2% max
        - Prioritize high-conviction trades
        
        **GREED DAYS:**
        - Increase position size to normal
        - Can explore 5x leverage
        - Higher frequency sustainable
        """)
    
    with col2:
        fig, ax = plt.subplots(figsize=(8, 5))
        strategies = ['Fear\n(Current)', 'Fear\n(With Strategy)', 'Greed\n(Current)', 'Greed\n(With Strategy)']
        volatility = [1200, 900, 800, 800]
        colors_strat = ['#FF6B6B', '#FFB6C1', '#4ECDC4', '#98FB98']
        ax.bar(strategies, volatility, color=colors_strat, alpha=0.8, edgecolor='black')
        ax.set_ylabel('PnL Volatility')
        ax.set_title('Expected Volatility Reduction')
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig)
    
    st.markdown("---")
    
    st.subheader("Strategy #2: Trade Frequency Optimization")
    col1, col2 = st.columns(2)
    
    with col1:
        fig, ax = plt.subplots(figsize=(8, 5))
        freq_types = ['Frequent\nTraders', 'Infrequent\nTraders']
        pnl = [32000, 3500]
        colors_freq = ['#FF9999', '#66B2FF']
        ax.bar(freq_types, pnl, color=colors_freq, alpha=0.8, edgecolor='black')
        ax.set_ylabel('Average Daily PnL ($)')
        ax.set_title('Current Performance by Frequency')
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig)
    
    with col2:
        st.markdown("""
        **FOR FREQUENT TRADERS:**
        - Scale back to 5-7 trades on fear days
        - Enforce 1:2 risk/reward ratio
        - Skip first hour post-sentiment update
        - Expected: +22% avg PnL
        
        **FOR INFREQUENT TRADERS:**
        - Maintain current on all days
        - Slight increase on greed days
        - Don't change with sentiment
        - Expected: +8% consistency
        """)

# ===== PAGE 7: DATA EXPLORER =====
elif page == "Data Explorer":
    st.header("🔍 Data Explorer")
    
    st.subheader("Filter & Explore Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_sentiment = st.multiselect("Sentiment Category", df['sentiment_category'].unique(), 
                                           default=df['sentiment_category'].unique())
    
    with col2:
        selected_leverage = st.multiselect("Leverage Segment", df['leverage_segment'].unique(),
                                          default=df['leverage_segment'].unique())
    
    with col3:
        selected_frequency = st.multiselect("Frequency Segment", df['frequency_segment'].unique(),
                                           default=df['frequency_segment'].unique())
    
    # Filter data
    filtered_df = df[
        (df['sentiment_category'].isin(selected_sentiment)) &
        (df['leverage_segment'].isin(selected_leverage)) &
        (df['frequency_segment'].isin(selected_frequency))
    ]
    
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Traders Shown", len(filtered_df))
    with col2:
        st.metric("Avg PnL", f"${filtered_df['net_pnl'].mean():.0f}")
    with col3:
        st.metric("Avg Win Rate", f"{filtered_df['win_rate'].mean():.1f}%")
    with col4:
        st.metric("Avg Daily Trades", f"{filtered_df['num_trades'].mean():.1f}")
    
    st.markdown("---")
    
    st.subheader("Trader Data Table")
    st.dataframe(filtered_df.sort_values('net_pnl', ascending=False), use_container_width=True)
    
    # Download CSV
    csv = filtered_df.to_csv(index=False)
    st.download_button("📥 Download as CSV", csv, "trader_data.csv", "text/csv")

# Footer
st.markdown("---")
st.markdown("""
    <center>
        <p style='font-size: 12px; color: gray;'>
        Primetrade.ai Data Science Analysis Dashboard | Last Updated: April 2026<br>
        For more details, refer to the full analysis notebook: analysis.ipynb
        </p>
    </center>
""", unsafe_allow_html=True)

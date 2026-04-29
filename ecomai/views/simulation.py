# ================================================================
# PAGE — What-If Simulation
# ================================================================
"""Scenario modeling for pricing, discount, and marketing changes."""

import pandas as pd
import streamlit as st
import plotly.graph_objects as go

from ecomai.utils.charts import themed_chart


def page_simulation(df):
    """
    Render the What-If Simulation page.

    Parameters
    ----------
    df : pd.DataFrame
        Filtered transaction data.
    """
    st.markdown('<div class="main-header">⚡ What-If Scenario Simulation</div>', unsafe_allow_html=True)
    st.markdown('*Dynamically model the impact of pricing, discounts & marketing changes*')
    st.divider()

    base = df['revenue'].sum()
    ca, cb = st.columns([1, 2])
    
    with ca:
        st.markdown("### 🎛️ Levers")
        price_chg  = st.slider("💲 Price Change (%)",       -30, 50,  0)
        disc_chg   = st.slider("🏷️ Discount Change (%)",    -20, 20,  0)
        mkt_budget = st.slider("📣 Marketing Budget (₹L)",    0, 100, 10)
        mkt_roi    = st.slider("📈 Marketing ROI Multiplier", 1.0, 6.0, 2.5, 0.1)
        conv_chg   = st.slider("🛒 Conversion Rate (%)",     -20, 40,  0)
        ret_chg    = st.slider("🔁 Customer Retention (%)",  -10, 20,  0)

        # Basic financial model
        Dp = base * price_chg / 100
        Dd = -base * disc_chg / 100 * 0.55  # Assumes elasticity dampening
        Dm = (mkt_budget * 100_000) * (mkt_roi - 1)
        Dc = base * conv_chg / 100
        Dr = base * ret_chg / 100
        
        new_rev = base + Dp + Dd + Dm + Dc + Dr
        pct = (new_rev - base) / base * 100 if base > 0 else 0

    with cb:
        st.markdown("### 📊 Impact")
        m1, m2, m3 = st.columns(3)
        m1.metric("Baseline Revenue",  f"₹{base:,.0f}")
        m2.metric("Projected Revenue", f"₹{new_rev:,.0f}", f"{pct:+.1f}%")
        m3.metric("Net Change",        f"₹{new_rev-base:+,.0f}")

        # Waterfall chart
        fig = go.Figure(go.Waterfall(
            orientation='v',
            measure=['absolute', 'relative', 'relative', 'relative', 'relative', 'relative'],
            x=['Baseline', 'Price', 'Discount', 'Marketing', 'Conversion', 'Retention'],
            y=[base, Dp, Dd, Dm, Dc, Dr],
            connector={"line": {"color": "#94a3b8"}},
            increasing={"marker": {"color": "#22c55e"}},
            decreasing={"marker": {"color": "#ef4444"}},
            totals={"marker": {"color": "#667eea"}}
        ))
        fig.update_layout(title="Revenue Waterfall", yaxis_title="Revenue (₹)", showlegend=False)
        themed_chart(fig, use_container_width=True)

        # Impact breakdown table
        fdf = pd.DataFrame({
            'Factor': ['Price', 'Discount', 'Marketing', 'Conversion', 'Retention'],
            'Δ Revenue (₹)': [Dp, Dd, Dm, Dc, Dr],
            'Δ Revenue (%)': [x / base * 100 if base > 0 else 0 for x in [Dp, Dd, Dm, Dc, Dr]]
        }).round(2)
        st.dataframe(fdf, use_container_width=True)

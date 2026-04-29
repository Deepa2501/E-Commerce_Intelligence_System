# ================================================================
# PAGE — Home / Overview
# ================================================================
"""Main landing page displaying top-level metrics and health."""

import streamlit as st
import plotly.express as px

from ecomai.utils.charts import themed_chart
from ecomai.insights.alerts import smart_alerts


def page_home(df, rfm, r2):
    """
    Render the Home dashboard page.

    Parameters
    ----------
    df : pd.DataFrame
        Filtered transaction data.
    rfm : pd.DataFrame
        Customer segments data.
    r2 : float
        R-squared score of the sales prediction model.
    """
    st.markdown('<div class="main-header">🛍️ E-Commerce Intelligence System</div>',
                unsafe_allow_html=True)
    st.markdown('*AI-powered analytics · predictions · recommendations · simulations*')
    st.divider()

    # Top-level metrics
    tot_rev = df['revenue'].sum()
    orders = df['order_id'].nunique()
    custs = df['customer_id'].nunique()
    aov = df['revenue'].mean()
    prods = df['product_name'].nunique()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("💰 Total Revenue", f"₹{tot_rev:,.0f}")
    c2.metric("📦 Total Orders", f"{orders:,}")
    c3.metric("👤 Customers", f"{custs:,}")
    c4.metric("🛒 Avg Order Value", f"₹{aov:,.0f}")
    c5.metric("🏷️ Products", f"{prods}")
    st.divider()

    # Revenue Over Time & Category Share
    ca, cb = st.columns(2)
    with ca:
        st.markdown('<div class="sec-header">📈 Revenue Over Time</div>', unsafe_allow_html=True)
        tr = df.groupby(df['date'].dt.to_period('M'))['revenue'].sum().reset_index()
        tr['date'] = tr['date'].astype(str)
        fig = px.area(
            tr, x='date', y='revenue', 
            color_discrete_sequence=['#667eea'],
            labels={'revenue': 'Revenue (₹)', 'date': 'Month'}
        )
        fig.update_layout(showlegend=False, margin=dict(t=5, b=5))
        themed_chart(fig, use_container_width=True)

    with cb:
        st.markdown('<div class="sec-header">🏷️ Category Revenue Share</div>', unsafe_allow_html=True)
        cr = df.groupby('category')['revenue'].sum().reset_index()
        fig2 = px.pie(
            cr, values='revenue', names='category',
            color_discrete_sequence=px.colors.qualitative.Set3, hole=0.42
        )
        fig2.update_layout(margin=dict(t=5, b=5))
        themed_chart(fig2, use_container_width=True)

    # Model Health & Live Alerts
    cc, cd = st.columns([1, 2])
    with cc:
        st.markdown('<div class="sec-header">🤖 Model Health</div>', unsafe_allow_html=True)
        st.metric("Sales Model R²", f"{r2:.3f}", delta="Gradient Boosting")
        hv_count = len(rfm[rfm['segment_label'] == 'High-Value'])
        st.metric("High-Value Customers", hv_count)

    with cd:
        st.markdown('<div class="sec-header">🚨 Live Alerts</div>', unsafe_allow_html=True)
        # Display top 4 alerts
        for icon, atype, msg in smart_alerts(df)[:4]:
            if atype == 'WARNING':
                st.warning(f"{icon} {msg}")
            elif atype == 'POSITIVE':
                st.success(f"{icon} {msg}")
            else:
                st.info(f"{icon} {msg}")

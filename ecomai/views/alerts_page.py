# ================================================================
# PAGE — Smart Alerts
# ================================================================
"""Display real-time business alerts and product performance."""

import streamlit as st

from ecomai.insights.alerts import smart_alerts


def page_alerts(df):
    """
    Render the Smart Alerts page.

    Parameters
    ----------
    df : pd.DataFrame
        Filtered transaction data.
    """
    st.markdown('<div class="main-header">🚨 Smart Alerts</div>', unsafe_allow_html=True)
    st.markdown('*Real-time rule-based + data-driven business intelligence*')
    st.divider()

    alerts = smart_alerts(df)
    warns = [a for a in alerts if a[1] == 'WARNING']
    poss  = [a for a in alerts if a[1] == 'POSITIVE']
    infos = [a for a in alerts if a[1] == 'INFO']

    c1, c2, c3 = st.columns(3)
    c1.metric("🔴 Warnings", len(warns))
    c2.metric("🟢 Positive Signals", len(poss))
    c3.metric("🔵 Informational", len(infos))
    st.divider()

    # Display Alert Categories
    if warns:
        st.subheader("⚠️ Warnings")
        for icon, _, msg in warns: 
            st.error(f"{icon}  {msg}")
            
    if poss:
        st.subheader("✅ Positive Signals")
        for icon, _, msg in poss: 
            st.success(f"{icon}  {msg}")
            
    if infos:
        st.subheader("ℹ️ Informational")
        for icon, _, msg in infos: 
            st.info(f"{icon}  {msg}")

    st.divider()
    
    # Product Performance Breakdown
    st.subheader("📦 Product Performance Table")

    # Build aggregation dict dynamically based on available columns
    agg_dict = {
        'Revenue': ('revenue', 'sum'),
        'Orders': ('order_id', 'count'),
    }
    if 'price' in df.columns and df['price'].nunique() > 1:
        agg_dict['Avg_Price'] = ('price', 'mean')
    if 'quantity' in df.columns:
        agg_dict['Total_Units'] = ('quantity', 'sum')
    if 'discount' in df.columns and df['discount'].nunique() > 2:
        agg_dict['Avg_Discount'] = ('discount', 'mean')
    if 'gross_profit' in df.columns:
        agg_dict['Gross_Profit'] = ('gross_profit', 'sum')

    pp = df.groupby('product_name').agg(**agg_dict).reset_index().sort_values(
        'Revenue', ascending=False
    ).round(1)
    
    if len(pp) > 0:
        q10, q90 = pp['Revenue'].quantile(0.10), pp['Revenue'].quantile(0.90)
        pp['Status'] = pp['Revenue'].apply(
            lambda v: '🟢 High' if v >= q90 else ('🔴 Low' if v <= q10 else '🟡 Mid')
        )
        st.dataframe(pp, use_container_width=True)
    else:
        st.info("No product data available.")

# ================================================================
# PAGE — Customer Segments
# ================================================================
"""Customer segmentation analytics via K-Means clustering."""

import streamlit as st
import plotly.express as px

from ecomai.utils.charts import themed_chart
from ecomai.config import SEGMENT_COLORS


def page_segments(rfm):
    """
    Render the Customer Segments page.

    Parameters
    ----------
    rfm : pd.DataFrame
        Customer RFM data with cluster labels.
    """
    st.markdown('<div class="main-header">👥 Customer Segmentation</div>', unsafe_allow_html=True)
    st.markdown('*K-Means (k=3) clustering on RFM — Recency · Frequency · Monetary*')
    st.divider()

    # Top-level metrics
    vc = rfm['segment_label'].value_counts()
    c1, c2, c3 = st.columns(3)
    c1.metric("🏆 High-Value",   vc.get('High-Value', 0))
    c2.metric("📊 Medium-Value", vc.get('Medium-Value', 0))
    c3.metric("📉 Low-Value",    vc.get('Low-Value', 0))
    st.divider()

    # 2D Visualisations
    ca, cb = st.columns(2)
    with ca:
        sp = rfm['segment_label'].value_counts().reset_index()
        sp.columns = ['Segment', 'Count']
        fig = px.pie(
            sp, values='Count', names='Segment', hole=0.42,
            color='Segment', color_discrete_map=SEGMENT_COLORS, 
            title="Segment Distribution"
        )
        themed_chart(fig, use_container_width=True)
        
    with cb:
        fig2 = px.scatter(
            rfm, x='frequency', y='monetary', color='segment_label',
            size='monetary', color_discrete_map=SEGMENT_COLORS,
            hover_data=['customer_id', 'recency'],
            title="Frequency vs Spend",
            labels={'monetary': 'Total Spend (₹)', 'frequency': 'Orders'}
        )
        themed_chart(fig2, use_container_width=True)

    # Segment Summary Table
    st.subheader("📋 Segment Summary")
    ss = rfm.groupby('segment_label').agg(
        Customers=('customer_id', 'count'),
        Avg_Recency=('recency', 'mean'),
        Avg_Frequency=('frequency', 'mean'),
        Avg_Spend=('monetary', 'mean'),
        Total_Revenue=('monetary', 'sum'),
    ).round(1).reset_index()
    ss.columns = [
        'Segment', 'Customers', 'Avg Recency (days)', 'Avg Frequency',
        'Avg Spend (₹)', 'Total Revenue (₹)'
    ]
    st.dataframe(ss, use_container_width=True)

    # 3D Visualisation
    st.subheader("🌐 3D RFM Scatter")
    fig3 = px.scatter_3d(
        rfm, x='recency', y='frequency', z='monetary',
        color='segment_label', color_discrete_map=SEGMENT_COLORS, opacity=0.65,
        labels={'monetary': 'Spend (₹)', 'frequency': 'Frequency', 'recency': 'Recency (days)'},
        title="3D RFM Cluster View"
    )
    themed_chart(fig3, use_container_width=True)

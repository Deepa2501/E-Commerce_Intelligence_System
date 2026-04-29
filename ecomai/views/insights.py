# ================================================================
# PAGE — Business Insights
# ================================================================
"""Actionable insights, recommendations, and data export features."""

import pandas as pd
import streamlit as st
import plotly.express as px

from ecomai.utils.charts import themed_chart
from ecomai.insights.recommendations import business_recommendations


def page_insights(df, rfm, r2, mae):
    """
    Render the Business Insights page.

    Parameters
    ----------
    df : pd.DataFrame
        Filtered transaction data.
    rfm : pd.DataFrame
        Customer segments data.
    r2 : float
        Sales model R-squared score.
    mae : float
        Sales model Mean Absolute Error.
    """
    st.markdown('<div class="main-header">💡 Business Recommendation Engine</div>',
                unsafe_allow_html=True)
    st.markdown('*Rule-based + data-driven actionable playbook*')
    st.divider()

    # Priority Action Plan
    recs = business_recommendations(df, rfm)
    st.subheader("🎯 Priority Action Plan")
    if recs:
        for rec in recs:
            st.markdown(f"""
            <div class="rec-card">
                <strong>{rec['priority']}</strong> &nbsp;|&nbsp; {rec['action']}
                <br><small>📌 Impact: <em>{rec['impact']}</em></small>
            </div>""", unsafe_allow_html=True)
    else:
        st.info("No priority actions identified based on current data.")

    st.divider()
    ca, cb = st.columns(2)
    
    with ca:
        st.subheader("🏆 Category Ranking & Strategy")
        cr = df.groupby('category')['revenue'].sum().sort_values(ascending=False).reset_index()
        cr.columns = ['Category', 'Revenue (₹)']
        
        # Simple strategy logic
        cr['Strategy'] = [
            '📈 Scale Up' if i < 2 else ('🔄 Maintain' if i < 4 else '⚠️ Review')
            for i in range(len(cr))
        ]

        # Add margin column if gross_profit exists
        if 'gross_profit' in df.columns:
            margin_by_cat = df.groupby('category').apply(
                lambda g: g['gross_profit'].sum() / max(g['revenue'].sum(), 1) * 100
            ).round(1)
            cr['Margin (%)'] = cr['Category'].map(margin_by_cat)

        st.dataframe(cr, use_container_width=True)
        
    with cb:
        # Discount Efficiency chart (only if meaningful discount data)
        has_discount = 'discount' in df.columns and df['discount'].nunique() > 2
        if has_discount:
            st.subheader("🏷️ Discount Efficiency")
            de = df.groupby('discount').apply(
                lambda g: g['revenue'].sum() / max(g['order_id'].nunique(), 1)
            ).reset_index()
            de.columns = ['Discount (%)', 'Revenue per Order']
            
            fig = px.scatter(
                de, x='Discount (%)', y='Revenue per Order',
                size='Revenue per Order', color='Revenue per Order',
                color_continuous_scale='RdYlGn',
                title="Discount Level vs Revenue per Order"
            )
            themed_chart(fig, use_container_width=True)
        elif 'gross_profit' in df.columns:
            # Fallback: Profit Margin by Category
            st.subheader("💰 Profit Margin by Category")
            gp = df.groupby('category').agg(
                revenue=('revenue', 'sum'),
                profit=('gross_profit', 'sum')
            ).reset_index()
            gp['margin_pct'] = (gp['profit'] / gp['revenue'].clip(lower=1) * 100).round(1)
            
            fig = px.bar(
                gp, x='category', y='margin_pct', color='margin_pct',
                color_continuous_scale='RdYlGn',
                title="Gross Profit Margin by Category",
                labels={'margin_pct': 'Margin (%)', 'category': ''}
            )
            themed_chart(fig, use_container_width=True)
        else:
            st.subheader("📊 Revenue by Category")
            cr2 = df.groupby('category')['revenue'].sum().reset_index()
            fig = px.pie(
                cr2, values='revenue', names='category', hole=0.4,
                title="Revenue Share by Category",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            themed_chart(fig, use_container_width=True)

    st.divider()
    
    # Data Export section
    st.subheader("📥 Export")
    c1, c2 = st.columns(2)
    with c1:
        st.download_button(
            "⬇️ Filtered Data (CSV)", 
            df.to_csv(index=False),
            "ecom_data.csv", 
            "text/csv", 
            use_container_width=True
        )
    with c2:
        summary = pd.DataFrame({
            'Metric': [
                'Total Revenue', 'Total Orders', 'Customers',
                'Avg Order Value', 'Model R²', 'MAE'
            ],
            'Value': [
                f"₹{df['revenue'].sum():,.0f}", df['order_id'].nunique(),
                df['customer_id'].nunique(), f"₹{df['revenue'].mean():,.0f}" if len(df) else "0",
                f"{r2:.4f}", f"₹{mae:,.0f}"
            ]
        })
        st.download_button(
            "⬇️ Summary Report (CSV)", 
            summary.to_csv(index=False),
            "summary_report.csv", 
            "text/csv", 
            use_container_width=True
        )

# ================================================================
# PAGE — Dashboard & EDA
# ================================================================
"""Exploratory Data Analysis dashboard with multiple visualisations."""

import streamlit as st
import plotly.express as px

from ecomai.utils.charts import themed_chart


def page_eda(df):
    """
    Render the Dashboard & EDA page.

    Parameters
    ----------
    df : pd.DataFrame
        Filtered transaction data.
    """
    st.markdown('<div class="main-header">📊 Dashboard & EDA</div>', unsafe_allow_html=True)
    st.divider()

    t1, t2, t3, t4 = st.tabs(["📈 Sales Trends", "🏆 Products", "🗺️ Regions", "👤 Customers"])

    # Tab 1: Sales Trends
    with t1:
        c1, c2 = st.columns(2)
        with c1:
            mrev = df.groupby([df['date'].dt.to_period('M'), 'category'])['revenue'].sum().reset_index()
            mrev['date'] = mrev['date'].astype(str)
            fig = px.line(
                mrev, x='date', y='revenue', color='category',
                title="Monthly Revenue by Category",
                color_discrete_sequence=px.colors.qualitative.Set2,
                labels={'revenue': 'Revenue (₹)'}
            )
            themed_chart(fig, use_container_width=True)
            
        with c2:
            qr = df.groupby(['year', 'quarter'])['revenue'].sum().reset_index()
            qr['period'] = qr['year'].astype(str) + '-Q' + qr['quarter'].astype(str)
            fig2 = px.bar(
                qr, x='period', y='revenue', color='quarter',
                title="Quarterly Revenue",
                color_discrete_sequence=px.colors.qualitative.Pastel,
                labels={'revenue': 'Revenue (₹)'}
            )
            themed_chart(fig2, use_container_width=True)

        dow = df.groupby('day_of_week')['revenue'].mean().reset_index()
        dow['day'] = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        fig3 = px.bar(
            dow, x='day', y='revenue', color='revenue',
            color_continuous_scale='Viridis', title="Avg Revenue by Day of Week",
            labels={'revenue': 'Avg Revenue (₹)'}
        )
        themed_chart(fig3, use_container_width=True)

    # Tab 2: Products
    with t2:
        c1, c2 = st.columns(2)
        with c1:
            tp = df.groupby('product_name')['revenue'].sum().nlargest(10).reset_index()
            fig = px.bar(
                tp, x='revenue', y='product_name', orientation='h',
                color='revenue', color_continuous_scale='Blues',
                title="Top 10 Products by Revenue",
                labels={'revenue': 'Revenue (₹)', 'product_name': ''}
            )
            fig.update_layout(yaxis={'categoryorder': 'total ascending'})
            themed_chart(fig, use_container_width=True)
            
        with c2:
            # Discount vs Revenue scatter (only if discount data is meaningful)
            has_discount = 'discount' in df.columns and df['discount'].nunique() > 1
            if has_discount:
                cd_df = df.groupby('category').agg(
                    avg_discount=('discount', 'mean'), 
                    total_revenue=('revenue', 'sum')
                ).reset_index()
                fig2 = px.scatter(
                    cd_df, x='avg_discount', y='total_revenue',
                    size='total_revenue', color='category', text='category',
                    title="Category: Discount vs Revenue",
                    labels={'avg_discount': 'Avg Discount (%)', 'total_revenue': 'Revenue (₹)'},
                    color_discrete_sequence=px.colors.qualitative.Bold
                )
                fig2.update_traces(textposition='top center')
                themed_chart(fig2, use_container_width=True)
            else:
                # Fallback: Category revenue breakdown
                cr = df.groupby('category')['revenue'].sum().reset_index()
                fig2 = px.bar(
                    cr, x='category', y='revenue', color='category',
                    title="Revenue by Category",
                    color_discrete_sequence=px.colors.qualitative.Bold,
                    labels={'revenue': 'Revenue (₹)', 'category': ''}
                )
                themed_chart(fig2, use_container_width=True)

        # Price distribution (only if price column exists with variance)
        if 'price' in df.columns and df['price'].nunique() > 1:
            fig3 = px.box(
                df, x='category', y='price', color='category',
                title="Price Distribution by Category",
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            themed_chart(fig3, use_container_width=True)
        else:
            # Fallback: Units sold by category
            ubc = df.groupby('category')['quantity'].sum().reset_index()
            fig3 = px.bar(
                ubc, x='category', y='quantity', color='category',
                title="Units Sold by Category",
                color_discrete_sequence=px.colors.qualitative.Pastel,
                labels={'quantity': 'Total Units', 'category': ''}
            )
            themed_chart(fig3, use_container_width=True)

    # Tab 3: Regions
    with t3:
        if 'region' in df.columns:
            c1, c2 = st.columns(2)
            with c1:
                rr = df.groupby('region')['revenue'].sum().reset_index()
                fig = px.bar(
                    rr, x='region', y='revenue', color='region',
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    title="Revenue by Region", labels={'revenue': 'Revenue (₹)'}
                )
                themed_chart(fig, use_container_width=True)
                
            with c2:
                heat = df.groupby(['region', 'category'])['revenue'].sum().unstack(fill_value=0)
                fig2 = px.imshow(
                    heat, color_continuous_scale='YlOrRd',
                    title="Region x Category Revenue Heatmap",
                    labels=dict(color='Revenue (₹)'), aspect='auto'
                )
                themed_chart(fig2, use_container_width=True)
        else:
            st.info("No region data available in the current dataset.")

    # Tab 4: Customers
    with t4:
        cf = df.groupby('customer_id')['order_id'].count().reset_index()
        cf.columns = ['customer_id', 'orders']
        
        c1, c2 = st.columns(2)
        with c1:
            fig = px.histogram(
                cf, x='orders', nbins=25,
                color_discrete_sequence=['#667eea'],
                title="Customer Purchase Frequency",
                labels={'orders': 'Number of Orders'}
            )
            themed_chart(fig, use_container_width=True)
            
        with c2:
            tc = df.groupby('customer_id')['revenue'].sum().nlargest(15).reset_index()
            fig2 = px.bar(
                tc, x='customer_id', y='revenue',
                color='revenue', color_continuous_scale='Teal',
                title="Top 15 Customers by Revenue",
                labels={'revenue': 'Revenue (₹)', 'customer_id': 'Customer ID'}
            )
            themed_chart(fig2, use_container_width=True)

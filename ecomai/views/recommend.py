# ================================================================
# PAGE — Recommendations
# ================================================================
"""Product recommendation engine interface via collaborative filtering."""

import streamlit as st
import plotly.express as px

from ecomai.utils.charts import themed_chart
from ecomai.models.recommender import recommend


def page_recommendations(df, prod_sim):
    """
    Render the Recommendations page.

    Parameters
    ----------
    df : pd.DataFrame
        Filtered transaction data.
    prod_sim : pd.DataFrame
        Product cosine similarity matrix.
    """
    st.markdown('<div class="main-header">🎯 Recommendation Engine</div>', unsafe_allow_html=True)
    st.markdown('*Collaborative filtering via cosine similarity on purchase-count matrix*')
    st.divider()

    all_prods = sorted(df['product_name'].unique())
    ca, cb = st.columns([2, 1])
    sel_prod = ca.selectbox("🔍 Select Product", all_prods)
    n_recs = cb.slider("# Recommendations", 3, 10, 5)

    if st.button("🎯 Get Recommendations", type="primary"):
        recs = recommend(sel_prod, prod_sim, n_recs)
        
        if recs:
            st.success(f"**Customers who bought '{sel_prod}' also frequently bought:**")
            cols = st.columns(min(len(recs), 3))
            
            for i, r in enumerate(recs):
                rd = df[df['product_name'] == r]
                with cols[i % 3]:
                    # Build product card with available data
                    avg_p = rd['price'].mean() if (len(rd) and 'price' in rd.columns) else 0
                    cat_ = rd['category'].iloc[0] if len(rd) else 'N/A'
                    ords = rd['order_id'].nunique()
                    sim_s = round(prod_sim.loc[sel_prod, r] * 100, 1) if r in prod_sim.columns else 0
                    
                    # Price line only if meaningful
                    price_line = f"<p>💰 ₹{avg_p:,.0f}</p>" if avg_p > 0 else ""
                    
                    st.markdown(f"""
                    <div class="prod-card">
                        <h4>🏷️ {r}</h4>
                        <p>📂 {cat_}</p>
                        {price_line}
                        <p>📦 {ords} orders</p>
                        <p>🔗 Similarity: {sim_s}%</p>
                    </div>""", unsafe_allow_html=True)
        else:
            st.warning("No similar products found.")

    st.divider()
    
    # Heatmap of top co-purchased products
    st.subheader("📊 Product Similarity Matrix — Top 15")
    top15 = df.groupby('product_name')['quantity'].sum().nlargest(15).index
    subset = prod_sim.loc[
        prod_sim.index.intersection(top15),
        prod_sim.columns.intersection(top15)
    ]
    
    if not subset.empty:
        fig = px.imshow(
            subset, color_continuous_scale='RdYlGn',
            title="Co-purchase Similarity Heatmap", aspect='auto'
        )
        fig.update_layout(height=520)
        themed_chart(fig, use_container_width=True)
    else:
        st.info("Not enough product data to build similarity heatmap.")

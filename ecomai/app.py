# ================================================================
# 🛍️ E-COMMERCE INTELLIGENCE SYSTEM — ENTRY POINT
# ================================================================
"""Main Streamlit application entry point."""

import streamlit as st
import sys
import os

# Add parent directory to path to allow absolute imports from 'ecomai'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# Internal imports
from ecomai.config import NAV_PAGES
from ecomai.utils.theme import apply_streamlit_theme, inject_css, render_theme_toggle
from ecomai.data.generator import generate_sample_data
from ecomai.data.loader import load_and_clean
from ecomai.models.sales_model import build_sales_model
from ecomai.models.segmentation import build_rfm_segments
from ecomai.models.recommender import build_recommender

# Views
from ecomai.views.home import page_home
from ecomai.views.eda import page_eda
from ecomai.views.prediction import page_prediction
from ecomai.views.segments import page_segments
from ecomai.views.recommend import page_recommendations
from ecomai.views.simulation import page_simulation
from ecomai.views.alerts_page import page_alerts
from ecomai.views.insights import page_insights

# ----------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------
st.set_page_config(
    page_title="EcomAI Intelligence",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main application loop."""
    # Apply theme and styling
    apply_streamlit_theme()
    inject_css()
    render_theme_toggle()

    # Sidebar setup
    with st.sidebar:
        st.markdown("## 🛍️ EcomAI Intelligence")
        st.markdown("*Industry-grade analytics system*")
        st.divider()

        page = st.selectbox("📌 Navigate", NAV_PAGES)

        st.divider()
        st.markdown("### 📁 Data Source")
        uploaded = st.file_uploader("Upload your CSV", type=['csv'])

        if uploaded:
            df_raw = load_and_clean(uploaded)
            st.success(f"✅ Loaded {len(df_raw):,} rows")
        else:
            df_raw = generate_sample_data()
            st.info("📦 Using 6,000-row synthetic dataset")

        st.divider()
        st.markdown("### 🔍 Global Filters")
        years = sorted(df_raw['year'].unique())
        sel_yrs = st.multiselect("Year", years, default=years)
        
        cats_all = sorted(df_raw['category'].unique())
        sel_cats = st.multiselect("Category", cats_all, default=cats_all)
        
        regs_all = sorted(df_raw['region'].unique()) if 'region' in df_raw.columns else []
        sel_regs = st.multiselect("Region", regs_all, default=regs_all) if regs_all else regs_all

    # Apply global filters
    df = df_raw[df_raw['year'].isin(sel_yrs) & df_raw['category'].isin(sel_cats)]
    if sel_regs and 'region' in df.columns:
        df = df[df['region'].isin(sel_regs)]

    # Handle empty data
    if df.empty:
        st.warning("⚠️ No data matches selected filters.")
        return

    # Build models for the current filtered view
    model, le, mae, r2, monthly_df = build_sales_model(df)
    rfm, _, _                      = build_rfm_segments(df)
    prod_sim, _                    = build_recommender(df)

    # Route to selected page
    if   page == "🏠 Home":               page_home(df, rfm, r2)
    elif page == "📊 Dashboard & EDA":    page_eda(df)
    elif page == "🔮 Sales Prediction":   page_prediction(df, model, le, mae, r2, monthly_df)
    elif page == "👥 Customer Segments":  page_segments(rfm)
    elif page == "🎯 Recommendations":    page_recommendations(df, prod_sim)
    elif page == "⚡ What-If Simulation": page_simulation(df)
    elif page == "🚨 Smart Alerts":       page_alerts(df)
    elif page == "💡 Business Insights":  page_insights(df, rfm, r2, mae)


if __name__ == "__main__":
    main()

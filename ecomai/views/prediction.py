# ================================================================
# PAGE — Sales Prediction
# ================================================================
"""Predictive analytics and ML model performance dashboard."""

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from ecomai.utils.charts import themed_chart


def page_prediction(df, model, le, mae, r2, monthly_df):
    """
    Render the Sales Prediction page.

    Parameters
    ----------
    df : pd.DataFrame
        Filtered transaction data.
    model : GradientBoostingRegressor
        Trained sales prediction model.
    le : LabelEncoder
        Encoder used for product categories.
    mae : float
        Mean Absolute Error of the model.
    r2 : float
        R-squared score of the model.
    monthly_df : pd.DataFrame
        Historical aggregated monthly data.
    """
    st.markdown('<div class="main-header">🔮 Sales Prediction</div>', unsafe_allow_html=True)
    st.markdown('*Gradient Boosting Regressor trained on 3 years of monthly category sales*')
    st.divider()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Algorithm", "Gradient Boosting")
    c2.metric("R² Score", f"{r2:.4f}")
    c3.metric("MAE", f"₹{mae:,.0f}")
    c4.metric("Training Set", "80% historical data")
    st.divider()

    # Future Forecast Tool
    st.subheader("🔭 Forecast Future Revenue")
    cats = sorted(df['category'].unique())
    a, b, c_ = st.columns(3)
    yr = a.selectbox("Year", [2024, 2025, 2026], index=1)
    mo = b.selectbox("Month", range(1, 13), index=5,
                     format_func=lambda m: pd.Timestamp(2000, m, 1).strftime('%B'))
    cat = c_.selectbox("Category", cats)

    if st.button("🔮 Predict", type="primary"):
        enc = le.transform([cat])[0]
        pred = model.predict(pd.DataFrame(
            [[yr, mo, enc]],
            columns=['year', 'month', 'category_enc']
        ))[0]
        
        st.success(f"### 💰 Predicted Revenue for {cat} — "
                   f"{pd.Timestamp(yr, mo, 1).strftime('%B %Y')}: ₹{pred:,.0f}")

        # Show full year forecast
        rows = []
        for m in range(1, 13):
            inp = pd.DataFrame([[yr, m, enc]], columns=['year', 'month', 'category_enc'])
            rows.append({
                'Month': pd.Timestamp(yr, m, 1).strftime('%b'),
                'Predicted Revenue': model.predict(inp)[0]
            })
            
        fdf = pd.DataFrame(rows)
        fig = px.bar(
            fdf, x='Month', y='Predicted Revenue',
            color='Predicted Revenue', color_continuous_scale='Viridis',
            title=f"Full-Year Forecast — {cat} ({yr})",
            labels={'Predicted Revenue': 'Revenue (₹)'}
        )
        themed_chart(fig, use_container_width=True)

    st.divider()
    
    # Historical Actual vs Predicted
    st.subheader("📊 Actual vs Predicted (Historical)")
    sel = st.selectbox("Category", cats, key='avp')
    
    hist = monthly_df[monthly_df['category'] == sel].copy().sort_values(['year', 'month'])
    hist['period'] = hist['year'].astype(str) + '-' + hist['month'].astype(str).str.zfill(2)
    hist['predicted'] = model.predict(hist[['year', 'month', 'category_enc']])

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=hist['period'], y=hist['revenue'],
        name='Actual', line=dict(color='#667eea', width=2.5)
    ))
    fig2.add_trace(go.Scatter(
        x=hist['period'], y=hist['predicted'],
        name='Predicted', line=dict(color='#f093fb', width=2, dash='dash')
    ))
    fig2.update_layout(
        title=f"Actual vs Predicted — {sel}",
        xaxis_title="Period", yaxis_title="Revenue (₹)"
    )
    themed_chart(fig2, use_container_width=True)

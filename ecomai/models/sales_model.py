# ================================================================
# MODEL — Gradient Boosting Sales Forecaster
# ================================================================
"""
Trains a Gradient Boosting Regressor on monthly category-level revenue
and returns the model along with evaluation metrics.
"""

import pandas as pd
import streamlit as st
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

from ecomai.config import RANDOM_SEED


@st.cache_data
def build_sales_model(df: pd.DataFrame):
    """
    Train a Gradient Boosting model on monthly aggregated revenue.

    Parameters
    ----------
    df : pd.DataFrame
        Full transaction dataset with year, month, category, revenue.

    Returns
    -------
    tuple
        (model, label_encoder, mae, r2_score, monthly_df)
    """
    monthly = df.groupby(['year', 'month', 'category'])['revenue'].sum().reset_index()
    le = LabelEncoder()
    monthly['category_enc'] = le.fit_transform(monthly['category'])

    X = monthly[['year', 'month', 'category_enc']]
    y = monthly['revenue']
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_SEED
    )

    mdl = GradientBoostingRegressor(
        n_estimators=200, learning_rate=0.08,
        max_depth=4, random_state=RANDOM_SEED
    )
    mdl.fit(X_tr, y_tr)
    y_pred = mdl.predict(X_te)

    return mdl, le, mean_absolute_error(y_te, y_pred), r2_score(y_te, y_pred), monthly

# ================================================================
# MODEL — K-Means RFM Customer Segmentation
# ================================================================
"""
Segments customers into High / Medium / Low value tiers using
K-Means clustering on Recency-Frequency-Monetary features.
"""

import pandas as pd
import streamlit as st
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

from ecomai.config import RANDOM_SEED


@st.cache_data
def build_rfm_segments(df: pd.DataFrame):
    """
    Build RFM segments using K-Means (k=3).

    Parameters
    ----------
    df : pd.DataFrame
        Full transaction dataset.

    Returns
    -------
    tuple
        (rfm_dataframe, kmeans_model, scaler)
    """
    ref = df['date'].max()
    rfm = df.groupby('customer_id').agg(
        recency  =('date',     lambda x: (ref - x.max()).days),
        frequency=('order_id', 'count'),
        monetary =('revenue',  'sum'),
    ).reset_index()

    sc = StandardScaler()
    rfm_s = sc.fit_transform(rfm[['recency', 'frequency', 'monetary']])

    km = KMeans(n_clusters=3, n_init=15, random_state=RANDOM_SEED)
    rfm['segment'] = km.fit_predict(rfm_s)

    # Label segments by average monetary value
    rank = rfm.groupby('segment')['monetary'].mean().sort_values(ascending=False).index
    lmap = {rank[0]: 'High-Value', rank[1]: 'Medium-Value', rank[2]: 'Low-Value'}
    rfm['segment_label'] = rfm['segment'].map(lmap)

    return rfm, km, sc

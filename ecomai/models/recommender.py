# ================================================================
# MODEL — Collaborative Filtering Recommender
# ================================================================
"""
Product recommendation engine using cosine similarity
on a customer × product purchase-count matrix.
"""

import pandas as pd
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity


@st.cache_data
def build_recommender(df: pd.DataFrame):
    """
    Build a product similarity matrix from purchase history.

    Parameters
    ----------
    df : pd.DataFrame
        Full transaction dataset.

    Returns
    -------
    tuple
        (similarity_matrix, customer_product_matrix)
    """
    mat = (df.groupby(['customer_id', 'product_name'])['quantity']
             .sum().unstack(fill_value=0))
    sim = pd.DataFrame(
        cosine_similarity(mat.T),
        index=mat.columns, columns=mat.columns
    )
    return sim, mat


def recommend(product: str, sim: pd.DataFrame, n: int = 5) -> list:
    """
    Return the top-n most similar products.

    Parameters
    ----------
    product : str
        Seed product name.
    sim : pd.DataFrame
        Product similarity matrix.
    n : int
        Number of recommendations.

    Returns
    -------
    list[str]
        Recommended product names.
    """
    if product not in sim.index:
        return []
    return sim[product].sort_values(ascending=False).iloc[1:n + 1].index.tolist()

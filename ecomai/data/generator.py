# ================================================================
# DATA — Synthetic Data Generator
# ================================================================
"""
Generates realistic synthetic e-commerce data with seasonal patterns.
Replace with a real CSV loader in production.
"""

import numpy as np
import pandas as pd
import streamlit as st

from ecomai.config import CATALOGUE, PRICE_MAP, DEFAULT_SAMPLE_SIZE, RANDOM_SEED


@st.cache_data
def generate_sample_data(n: int = DEFAULT_SAMPLE_SIZE) -> pd.DataFrame:
    """
    Create a synthetic e-commerce dataset with seasonal revenue patterns.

    Parameters
    ----------
    n : int
        Number of order rows to generate.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns: order_id, customer_id, product_name,
        category, price, quantity, discount, region, date, revenue,
        month, year, quarter, day_of_week, week_of_year.
    """
    np.random.seed(RANDOM_SEED)

    cats, prods, prices = [], [], []
    for _ in range(n):
        c = np.random.choice(list(CATALOGUE))
        p = np.random.choice(CATALOGUE[c])
        pr = round(np.random.uniform(*PRICE_MAP[c]), 2)
        cats.append(c)
        prods.append(p)
        prices.append(pr)

    dates = sorted(np.random.choice(
        pd.date_range('2022-01-01', '2024-12-31', periods=n), n, replace=False))

    df = pd.DataFrame({
        'order_id':     range(10001, 10001 + n),
        'customer_id':  np.random.randint(1000, 1800, n),
        'product_name': prods,
        'category':     cats,
        'price':        prices,
        'quantity':     np.random.choice([1, 2, 3, 4, 5], n,
                                         p=[.50, .25, .14, .07, .04]),
        'discount':     np.random.choice([0, 5, 10, 15, 20, 25, 30], n,
                                         p=[.38, .15, .15, .12, .10, .05, .05]),
        'region':       np.random.choice(
                            ['North', 'South', 'East', 'West', 'Central'], n,
                            p=[.25, .20, .20, .20, .15]),
        'date':         pd.to_datetime(dates),
    })

    # Derived columns
    df['revenue']      = df['price'] * df['quantity'] * (1 - df['discount'] / 100)
    df['month']        = df['date'].dt.month
    df['year']         = df['date'].dt.year
    df['quarter']      = df['date'].dt.quarter
    df['day_of_week']  = df['date'].dt.dayofweek
    df['week_of_year'] = df['date'].dt.isocalendar().week.astype(int)

    # Seasonal adjustment (peaks in summer)
    seasonal = 1 + 0.35 * np.sin(2 * np.pi * (df['month'] - 3) / 12)
    df['revenue'] *= seasonal
    return df

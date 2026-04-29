# ================================================================
# DATA — CSV Loader & Cleaner
# ================================================================
"""Upload handler for user-provided CSV files.

Supports both the internal synthetic schema and real-world datasets
with columns like Order ID, Sales, Units, Division, etc.
"""

import numpy as np
import pandas as pd
import streamlit as st

# ----------------------------------------------------------------
# Column mapping: Real Dataset → Internal Schema
# ----------------------------------------------------------------
COLUMN_MAP = {
    'Order ID':        'order_id',
    'Order Date':      'date',
    'Ship Date':       'ship_date',
    'Ship Mode':       'ship_mode',
    'Customer':        'customer_id',
    'Customer Name':   'customer_id',
    'Customer ID':     'customer_id',
    'Country/Region':  'country',
    'Country':         'country',
    'City':            'city',
    'State/Province':  'state',
    'State':           'state',
    'Postal Code':     'postal_code',
    'Division':        'category',
    'Category':        'category',
    'Sub-Category':    'sub_category',
    'Region':          'region',
    'Product ID':      'product_id',
    'Product Name':    'product_name',
    'Sales':           'revenue',
    'Units':           'quantity',
    'Quantity':        'quantity',
    'Gross Profit':    'gross_profit',
    'Cost':            'cost',
    'Discount':        'discount',
    'Profit':          'gross_profit',
    'Row ID':          'row_id',
}


@st.cache_data
def load_and_clean(uploaded) -> pd.DataFrame:
    """
    Load a user-uploaded CSV and normalise it to the internal schema.

    Handles two scenarios:
    1. Internal schema (synthetic data) — columns already named correctly.
    2. Real-world schema — columns like 'Order Date', 'Sales', 'Division', etc.

    Automatically renames columns, derives missing temporal features,
    and computes revenue / price / discount when possible.

    Parameters
    ----------
    uploaded : UploadedFile
        Streamlit file-uploader object.

    Returns
    -------
    pd.DataFrame
        Cleaned DataFrame ready for analysis.
    """
    df = pd.read_csv(uploaded)

    # ---- Step 1: Rename columns to internal schema ----
    rename = {}
    for orig_col in df.columns:
        cleaned = orig_col.strip()
        if cleaned in COLUMN_MAP:
            rename[orig_col] = COLUMN_MAP[cleaned]
    if rename:
        df = df.rename(columns=rename)

    # ---- Step 2: Drop fully empty rows ----
    df.dropna(how='all', inplace=True)

    # ---- Step 3: Parse date ----
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df.dropna(subset=['date'], inplace=True)

    # ---- Step 4: Derive temporal columns ----
    if 'date' in df.columns:
        for col, fn in [
            ('month',        lambda d: d.dt.month),
            ('year',         lambda d: d.dt.year),
            ('quarter',      lambda d: d.dt.quarter),
            ('day_of_week',  lambda d: d.dt.dayofweek),
            ('week_of_year', lambda d: d.dt.isocalendar().week.astype(int)),
        ]:
            if col not in df.columns:
                df[col] = fn(df['date'])

    # ---- Step 5: Derive revenue if missing ----
    if 'revenue' not in df.columns:
        if 'price' in df.columns and 'quantity' in df.columns:
            disc = df['discount'] if 'discount' in df.columns else 0
            df['revenue'] = df['price'] * df['quantity'] * (1 - disc / 100)
        elif 'cost' in df.columns and 'gross_profit' in df.columns:
            df['revenue'] = df['cost'] + df['gross_profit']

    # ---- Step 6: Derive price if missing ----
    if 'price' not in df.columns and 'revenue' in df.columns and 'quantity' in df.columns:
        df['price'] = np.where(df['quantity'] > 0, df['revenue'] / df['quantity'], 0)

    # ---- Step 7: Derive discount if missing ----
    if 'discount' not in df.columns:
        if 'cost' in df.columns and 'revenue' in df.columns and 'quantity' in df.columns:
            # Effective discount: difference between unit cost and unit revenue
            unit_cost = np.where(df['quantity'] > 0, df['cost'] / df['quantity'], 0)
            unit_rev  = np.where(df['quantity'] > 0, df['revenue'] / df['quantity'], 0)
            # If cost > revenue, there's effectively a discount applied
            df['discount'] = np.where(
                unit_cost > 0,
                np.clip(((unit_cost - unit_rev) / unit_cost) * 100, 0, 100),
                0
            ).round(1)
        else:
            df['discount'] = 0

    # ---- Step 8: Ensure order_id exists ----
    if 'order_id' not in df.columns:
        df['order_id'] = range(10001, 10001 + len(df))

    # ---- Step 9: Ensure customer_id exists ----
    if 'customer_id' not in df.columns:
        df['customer_id'] = 'Unknown'

    # ---- Step 10: Ensure category exists ----
    if 'category' not in df.columns:
        df['category'] = 'General'

    # ---- Step 11: Ensure product_name exists ----
    if 'product_name' not in df.columns:
        if 'product_id' in df.columns:
            df['product_name'] = df['product_id']
        else:
            df['product_name'] = 'Product'

    # ---- Step 12: Drop helper column ----
    if 'row_id' in df.columns:
        df.drop(columns=['row_id'], inplace=True)

    return df

# ================================================================
# INSIGHTS — Business Recommendations
# ================================================================
"""
Data-driven actionable playbook generating strategic recommendations
based on overall sales and customer segments.
"""

import pandas as pd


def business_recommendations(df: pd.DataFrame, rfm: pd.DataFrame) -> list:
    """
    Generate strategic business recommendations.

    Parameters
    ----------
    df : pd.DataFrame
        Full transaction dataset.
    rfm : pd.DataFrame
        Customer segmentation dataset (RFM).

    Returns
    -------
    list of dicts
        Format: [{'priority': str, 'action': str, 'impact': str}, ...]
    """
    recs = []
    
    # 1. High-Value Customer Retention
    hv = rfm[rfm['segment_label'] == 'High-Value']
    if len(hv) > 0:
        recs.append({
            'priority': '🔥 Critical',
            'action': f'Activate loyalty programme for {len(hv)} High-Value customers',
            'impact': 'Revenue retention & LTV uplift'
        })

    # 2. Top Category Marketing
    top_cat = df.groupby('category')['revenue'].sum().idxmax()
    recs.append({
        'priority': '📈 High',
        'action': f'Increase marketing spend on "{top_cat}" — your #1 revenue category',
        'impact': 'Top-line growth'
    })

    # 3. Margin Protection for Star Products (conditional on discount data)
    has_discount = 'discount' in df.columns and df['discount'].nunique() > 2
    if has_discount:
        low_disc = df[df['discount'] <= df['discount'].quantile(0.25)].groupby('product_name')['revenue'].sum()
        if len(low_disc) > 0:
            star = low_disc.idxmax()
            recs.append({
                'priority': '💰 High',
                'action': f'"{star}" sells well at low discount — protect margin, avoid deep discounting',
                'impact': 'Margin protection'
            })
    else:
        # Fallback: identify top product by revenue
        top_prod = df.groupby('product_name')['revenue'].sum().idxmax()
        recs.append({
            'priority': '💰 High',
            'action': f'"{top_prod}" is your top seller — ensure consistent stock & visibility',
            'impact': 'Revenue protection'
        })

    # 4. One-time Buyer Re-engagement
    one_timers = rfm[rfm['frequency'] == 1]
    if len(one_timers) > 0:
        recs.append({
            'priority': '📧 Medium',
            'action': f'Re-engage {len(one_timers)} one-time buyers via email/SMS retargeting',
            'impact': 'Customer retention'
        })

    # 5. Weekend vs Weekday Sales
    if 'day_of_week' in df.columns:
        weekend = df[df['day_of_week'] >= 5]['revenue'].sum()
        weekday = df[df['day_of_week'] < 5]['revenue'].sum()
        if weekday > 0 and weekend / weekday < 0.35:
            recs.append({
                'priority': '📅 Medium',
                'action': 'Launch weekend flash sales — weekend revenue is below weekdays',
                'impact': 'Revenue uplift +10-15%'
            })

    # 6. Low Volume Category / Bundle Opportunity
    low_stock_cat = df.groupby('category')['quantity'].mean().idxmin()
    recs.append({
        'priority': '📦 Low',
        'action': f'Review stock levels for "{low_stock_cat}" — lowest avg units per order',
        'impact': 'Conversion optimisation'
    })

    # 7. Gross Profit Opportunity (if gross_profit data exists)
    if 'gross_profit' in df.columns:
        cat_margin = df.groupby('category').apply(
            lambda g: g['gross_profit'].sum() / max(g['revenue'].sum(), 1) * 100
        )
        low_margin_cat = cat_margin.idxmin()
        recs.append({
            'priority': '⚠️ Medium',
            'action': f'"{low_margin_cat}" has the lowest profit margin ({cat_margin.min():.1f}%) — review pricing',
            'impact': 'Margin improvement'
        })

    return recs

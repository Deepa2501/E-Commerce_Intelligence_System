# ================================================================
# INSIGHTS — Smart Alerts
# ================================================================
"""
Rule-based generation of business alerts (warnings, positives, info)
based on real-time data analysis.
"""

import pandas as pd


def smart_alerts(df: pd.DataFrame) -> list:
    """
    Generate business alerts from the current dataset.

    Parameters
    ----------
    df : pd.DataFrame
        Full transaction dataset.

    Returns
    -------
    list of tuples
        Format: [(icon, type, message), ...]
        e.g., [('🔴', 'WARNING', 'Sales fell 12% QoQ')]
    """
    alerts = []
    cut = df['date'].max()

    # 1. Quarter-over-Quarter Revenue Momentum
    r3 = df[df['date'] >= cut - pd.DateOffset(months=3)]['revenue'].sum()
    p3 = df[(df['date'] >= cut - pd.DateOffset(months=6)) &
            (df['date'] < cut - pd.DateOffset(months=3))]['revenue'].sum()
    if p3 > 0:
        ch = (r3 - p3) / p3 * 100
        if ch < -10:
            alerts.append(('🔴', 'WARNING', f'Sales fell {abs(ch):.1f}% QoQ — investigate root cause'))
        elif ch > 15:
            alerts.append(('🟢', 'POSITIVE', f'Sales grew {ch:.1f}% QoQ — strong momentum'))

    # 2. Product Performance Extremes
    prod_rev = df.groupby('product_name')['revenue'].sum()
    low = prod_rev[prod_rev < prod_rev.quantile(0.10)].index.tolist()
    high = prod_rev[prod_rev > prod_rev.quantile(0.90)].index.tolist()

    if low:
        alerts.append(('🟡', 'WARNING',
                       f'Underperforming products: {", ".join(low[:3])} — consider promotions or delisting'))
    if high:
        alerts.append(('🟢', 'POSITIVE',
                       f'Star products: {", ".join(high[:3])} — increase stock & visibility'))

    # 3. Lowest Category
    low_cat = df.groupby('category')['revenue'].sum().idxmin()
    alerts.append(('🔵', 'INFO',
                   f'"{low_cat}" has lowest revenue — launch category-specific promotions'))

    # 4. Discount Efficiency (only if meaningful discount data exists)
    has_discount = 'discount' in df.columns and df['discount'].nunique() > 2
    if has_discount:
        eff = df.groupby('discount').apply(
            lambda g: g['revenue'].sum() / max(g['order_id'].nunique(), 1)
        ).reset_index()
        eff.columns = ['discount', 'rev_per_order']
        
        if len(eff) > 3:
            no_disc = eff.loc[eff['discount'] == eff['discount'].min(), 'rev_per_order']
            hi_disc = eff.loc[eff['discount'] == eff['discount'].max(), 'rev_per_order']
            if len(no_disc) and len(hi_disc) and no_disc.values[0] > hi_disc.values[0]:
                alerts.append(('🟡', 'WARNING',
                               'High discounts are reducing revenue per order — reassess discount strategy'))

    # 5. Gross Profit Margin Alert (if gross_profit data exists)
    if 'gross_profit' in df.columns and 'revenue' in df.columns:
        total_rev = df['revenue'].sum()
        total_gp = df['gross_profit'].sum()
        if total_rev > 0:
            margin = total_gp / total_rev * 100
            if margin < 15:
                alerts.append(('🔴', 'WARNING',
                               f'Overall gross margin is low at {margin:.1f}% — review pricing strategy'))
            elif margin > 40:
                alerts.append(('🟢', 'POSITIVE',
                               f'Healthy gross margin of {margin:.1f}% — strong pricing power'))

    # 6. Shipping Mode Insight (if ship_mode data exists)
    if 'ship_mode' in df.columns:
        mode_rev = df.groupby('ship_mode')['revenue'].sum()
        top_mode = mode_rev.idxmax()
        alerts.append(('🔵', 'INFO',
                       f'"{top_mode}" is the most popular shipping mode by revenue'))

    return alerts

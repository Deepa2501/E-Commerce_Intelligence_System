# ================================================================
# UTILS — Chart Wrappers
# ================================================================
"""
Helper functions for rendering Plotly charts with theme awareness.
"""

import streamlit as st
from .theme import is_dark_mode


def get_plotly_template() -> str:
    """Return the appropriate Plotly template based on the current theme."""
    return 'plotly_dark' if is_dark_mode() else 'plotly_white'


def themed_chart(fig, **kwargs):
    """
    Wrapper for st.plotly_chart that auto-applies the dark/light template
    and handles background transparency for seamless integration.

    Parameters
    ----------
    fig : plotly.graph_objects.Figure
        The Plotly figure to render.
    **kwargs : dict
        Additional arguments passed to st.plotly_chart (e.g., use_container_width).
    """
    tmpl = get_plotly_template()
    fig.update_layout(template=tmpl)
    
    if is_dark_mode():
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#e2e8f0'
        )
        
    st.plotly_chart(fig, **kwargs)

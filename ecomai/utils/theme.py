# ================================================================
# UTILS — Theme & Styling
# ================================================================
"""
Handles Streamlit dark/light mode switching, CSS injection,
and dynamic theme toggling.
"""

import streamlit as st
import os


def is_dark_mode() -> bool:
    """Check if dark mode is currently active in session state."""
    return st.session_state.get('dark_mode', False)


def apply_streamlit_theme():
    """
    Set Streamlit's internal theme config for native components 
    (like dataframes/glide-data-grid) based on current theme state.
    """
    if is_dark_mode():
        st._config.set_option('theme.backgroundColor', '#0f1117')
        st._config.set_option('theme.secondaryBackgroundColor', '#1a1d29')
        st._config.set_option('theme.textColor', '#e2e8f0')
        st._config.set_option('theme.primaryColor', '#667eea')
    else:
        st._config.set_option('theme.backgroundColor', '#ffffff')
        st._config.set_option('theme.secondaryBackgroundColor', '#f8fafc')
        st._config.set_option('theme.textColor', '#1f2937')
        st._config.set_option('theme.primaryColor', '#667eea')


def render_theme_toggle():
    """Render a dark/light mode toggle button in the top-right corner."""
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
        
    dark = is_dark_mode()
    label = '☀️ Light' if dark else '🌙 Dark'
    
    cols = st.columns([6, 1])
    with cols[1]:
        if st.button(label, key='theme_toggle'):
            st.session_state.dark_mode = not dark
            st.rerun()


def inject_css():
    """
    Inject global CSS styles based on the current theme.
    Loads dark mode CSS from assets if active.
    """
    dark = is_dark_mode()
    
    # Dynamic variables based on theme
    if dark:
        bg = '#0f1117'
        card_bg = '#1a1d29'
        border = '#2d3348'
        text = '#e2e8f0'
        sec_text = '#cbd5e1'
        rec_bg = '#1a2e1a'
        rec_border = '#2d5a2d'
    else:
        bg = '#ffffff'
        card_bg = '#f8fafc'
        border = '#e2e8f0'
        text = '#374151'
        sec_text = '#374151'
        rec_bg = '#f0fdf4'
        rec_border = '#86efac'

    # Base CSS
    base_css = f"""
    <style>
    .main-header {{
        font-size: 2.1rem; font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
    }}
    .sec-header {{
        font-size: 1.15rem; font-weight: 700; color: {sec_text};
        border-left: 4px solid #667eea; padding-left: 10px;
        margin: 1.4rem 0 0.8rem 0;
    }}
    div[data-testid="metric-container"] {{
        background: {card_bg}; border: 1px solid {border};
        border-radius: 12px; padding: 0.6rem 1rem;
    }}
    .rec-card {{
        background: {rec_bg}; border: 1px solid {rec_border};
        border-radius: 10px; padding: 0.9rem 1.2rem; margin: 0.4rem 0;
        color: {text};
    }}
    .prod-card {{
        background: {card_bg}; border: 1px solid {border};
        border-radius: 10px; padding: 1rem; margin: 0.5rem 0;
        text-align: center; color: {text};
    }}
    </style>
    """
    st.markdown(base_css, unsafe_allow_html=True)

    # Dark mode specific overrides
    if dark:
        css_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'dark_mode.css')
        try:
            with open(css_path, 'r') as f:
                dark_css = f.read()
            st.markdown(f"<style>{dark_css}</style>", unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"Could not load dark mode CSS: {e}")

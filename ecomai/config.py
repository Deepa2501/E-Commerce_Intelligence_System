# ================================================================
# CONFIGURATION & CONSTANTS
# ================================================================
"""
Centralised configuration for the EcomAI Intelligence System.
All magic numbers, catalogue data, and colour palettes live here.
"""

# ---- Product Catalogue ----
CATALOGUE = {
    'Electronics':   ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Smartwatch'],
    'Clothing':      ['T-Shirt', 'Jeans', 'Dress', 'Jacket', 'Sneakers'],
    'Home & Kitchen':['Blender', 'Cookware Set', 'Coffee Maker', 'Vacuum', 'Air Fryer'],
    'Books':         ['Fiction Novel', 'Self-Help Book', 'Textbook', 'Biography', 'Cookbook'],
    'Sports':        ['Yoga Mat', 'Dumbbells', 'Running Shoes', 'Bicycle', 'Tennis Racket'],
}

PRICE_MAP = {
    'Electronics': (8000, 90000),
    'Clothing': (400, 5000),
    'Home & Kitchen': (1000, 18000),
    'Books': (150, 1500),
    'Sports': (800, 22000),
}

# ---- Segment Color Map ----
SEGMENT_COLORS = {
    'High-Value':   '#22c55e',
    'Medium-Value': '#f59e0b',
    'Low-Value':    '#ef4444',
}

# ---- Theme Palette ----
BRAND_PRIMARY   = '#667eea'
BRAND_SECONDARY = '#764ba2'

LIGHT_THEME = {
    'bg':         '#ffffff',
    'card_bg':    '#f8fafc',
    'border':     '#e2e8f0',
    'text':       '#374151',
    'sec_text':   '#374151',
    'rec_bg':     '#f0fdf4',
    'rec_border': '#86efac',
    'secondary_bg': '#f8fafc',
}

DARK_THEME = {
    'bg':         '#0f1117',
    'card_bg':    '#1a1d29',
    'border':     '#2d3348',
    'text':       '#e2e8f0',
    'sec_text':   '#cbd5e1',
    'rec_bg':     '#1a2e1a',
    'rec_border': '#2d5a2d',
    'secondary_bg': '#1a1d29',
}

# ---- Navigation Pages ----
NAV_PAGES = [
    "🏠 Home",
    "📊 Dashboard & EDA",
    "🔮 Sales Prediction",
    "👥 Customer Segments",
    "🎯 Recommendations",
    "⚡ What-If Simulation",
    "🚨 Smart Alerts",
    "💡 Business Insights",
]

# ---- Data Defaults ----
DEFAULT_SAMPLE_SIZE = 6000
RANDOM_SEED = 42

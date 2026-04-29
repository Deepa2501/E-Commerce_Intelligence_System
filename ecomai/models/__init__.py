"""Machine learning models for sales, segmentation, and recommendations."""
from .sales_model import build_sales_model
from .segmentation import build_rfm_segments
from .recommender import build_recommender, recommend

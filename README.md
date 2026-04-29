# 🛍️ E-Commerce Intelligence System
**Live Dashboard:**[View Application Here](https://ecomintelligence.streamlit.app/)
> An industry-grade AI-powered analytics dashboard built with  
> **Python · Streamlit · scikit-learn · Plotly**

---

## ✨ Features

| Module | What it does |
|---|---|
| 🏠 **Home** | KPI cards, revenue trend, category share, live alerts |
| 📊 **EDA Dashboard** | Sales trends, top products, region heatmaps, customer behaviour |
| 🔮 **Sales Prediction** | Gradient Boosting · 12-month forecast · Actual vs Predicted chart |
| 👥 **Customer Segments** | K-Means RFM · High / Medium / Low value · 3D scatter |
| 🎯 **Recommendations** | Collaborative filtering · Co-purchase similarity matrix |
| ⚡ **What-If Simulation** | Price · Discount · Marketing · Conversion · Retention levers + waterfall |
| 🚨 **Smart Alerts** | QoQ trend · Product health · Discount cannibalisation detection |
| 💡 **Business Insights** | Priority action plan · Discount efficiency · CSV export |

---

## 🚀 Quick Start

```bash
# 1 — Clone the repo
git clone https://github.com/yourname/ecom-intelligence.git
cd ecom-intelligence

# 2 — Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3 — Install dependencies
pip install -r requirements.txt

# 4 — Run the app
streamlit run app/main.py
# Opens at http://localhost:8501
```

---

## 📁 Project Structure

```
ecom_intelligence/
    ├── .streamlit/
    │   └── config.toml          # Streamlit-specific UI/server settings
    ├── ecomai/
    │   ├── __pycache__/         # Compiled Python bytecode
    │   ├── assets/              # Static files (images, logos, custom CSS)
    │   ├── data/                # Dataset storage (CSV, SQL, etc.)
    │   ├── insights/            # Logic for analytics and data processing
    │   ├── models/              # Trained ML models and weights
    │   ├── utils/               # Shared helper functions and decorators
    │   ├── views/               # UI components or multi-page layouts
    │   ├── __init__.py          # Marks ecomai as a Python package
    │   ├── app.py               # Main application entry point
    │   └── config.py            # Application-wide constants/env variables
    ├── reports/
    │   ├── executive_summary.md # High-level project summary
    │   └── research_paper.md    # Technical documentation/whitepaper
    ├── .gitignore               # Version control exclusion rules
    ├── README.md                # Project overview and setup guide
    └── requirements.txt         # Project dependencies and libraries 
```

---

## 📂 Custom CSV Schema

Your CSV must contain these columns:

| Column | Type | Example |
|---|---|---|
| order_id | int | 10001 |
| customer_id | int | 1023 |
| product_name | str | Laptop |
| category | str | Electronics |
| price | float | 45999.00 |
| quantity | int | 2 |
| discount | float | 10 |
| region | str | North |
| date | date | 2023-06-15 |

> Revenue, month, year, quarter, and day_of_week are **auto-derived**.

---

## 🧠 ML Architecture

- **Sales Prediction** — `GradientBoostingRegressor` (200 trees, lr=0.08) on monthly category-level aggregates. Achieves R² ≈ 0.92 on synthetic data.
- **Customer Segmentation** — `KMeans(k=3)` on StandardScaler-normalised RFM features. Clusters auto-labelled by average monetary rank.
- **Recommendation Engine** — Cosine similarity on a customer × product purchase-count matrix. Returns top-N co-purchased products.

---

## 🛠️ Tech Stack

| Layer | Library |
|---|---|
| UI | Streamlit 1.32+ |
| Data | pandas, numpy |
| ML | scikit-learn |
| Viz | Plotly Express / Graph Objects |
| Packaging | pip / venv |

---

## 📄 License

MIT License

Copyright (c) 2024 EcomAI Intelligence

Permission is hereby granted, free of charge, to any person obtaining a copy...

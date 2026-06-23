# Brazilian E-Commerce EDA — Olist Dataset

> **Descripción en español:** Análisis exploratorio completo del dataset público de Olist, el mayor marketplace de Brasil. Se analizan ~100K órdenes (2016–2018) para extraer insights sobre tendencias de ventas, comportamiento temporal de compras, performance por categoría, logística y satisfacción del cliente. El objetivo es demostrar capacidad de análisis end-to-end con storytelling orientado a stakeholders de negocio.

---

## Business Context & Objective

Olist connects small Brazilian retailers to major e-commerce platforms (Mercado Livre, Amazon Brazil, etc.). This dataset covers the full order lifecycle — from purchase to review — across 9 relational tables.

**Objective:** Surface the 5–7 most actionable business insights from the data, using professional-quality visualisations and structured storytelling, as if presenting to a non-technical business audience.

---

## Dataset Description

Source: [Olist Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) — Kaggle

| File | Rows (approx.) | Description |
|---|---:|---|
| `olist_orders_dataset.csv` | 99,441 | Master order table — status, timestamps, customer ID |
| `olist_order_items_dataset.csv` | 112,650 | One row per item per order — price, freight, seller, product |
| `olist_products_dataset.csv` | 32,951 | Product catalogue — category, dimensions, weight |
| `product_category_name_translation.csv` | 71 | Portuguese → English category name mapping |
| `olist_customers_dataset.csv` | 99,441 | Customer city and state (anonymised) |
| `olist_order_reviews_dataset.csv` | 100,000 | Post-delivery review score (1–5) and comments |
| `olist_order_payments_dataset.csv` | 103,886 | Payment method, installments, and value |
| `olist_sellers_dataset.csv` | 3,095 | Seller city and state |
| `olist_geolocation_dataset.csv` | 1,000,163 | Zip code prefix → lat/lon mapping |

---

## Key Findings

### 1 · Revenue grew ~135% YoY (2017 → 2018)
The 3-month moving average confirms a structural upward trend — not seasonal noise. Q4 (Nov–Dec) shows a consistent spike tied to Black Friday and Christmas.

![Sales Trend](outputs/figures/01_sales_trend.png)

---

### 2 · Customers shop during office hours, mostly on weekdays
The peak buying window is **Tuesday–Thursday, 11 AM–2 PM**. Weekend activity drops significantly, especially Sunday mornings.

![Time Heatmap](outputs/figures/03_time_heatmap.png)

---

### 3 · Health & Beauty and Electronics dominate revenue
The treemap reveals high-revenue categories with varying ticket sizes. Several high-revenue categories also show below-median review scores — a loyalty risk.

![Category Treemap](outputs/figures/02_treemap_categories.png)

---

### 4 · Delivery time is the #1 driver of 1-star reviews — not price
Spearman correlation between delivery days and review score is stronger than any price-related variable. On-time delivery is the most powerful lever for customer satisfaction.

![Delivery Distribution](outputs/figures/04_delivery_histogram.png)

---

### 5 · Northern states have the worst logistics performance and lowest NPS
Northern and Northeastern states show both the longest median delivery times and the lowest review scores — a compound problem that geographic logistics investment would solve.

![Review by State](outputs/figures/06_review_by_state.png)

---

## Tech Stack

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.2-150458?style=flat&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.9-11557c?style=flat)
![Seaborn](https://img.shields.io/badge/Seaborn-0.13-4c72b0?style=flat)
![Plotly](https://img.shields.io/badge/Plotly-5.22-3F4F75?style=flat&logo=plotly&logoColor=white)
![Scipy](https://img.shields.io/badge/SciPy-1.13-8CAAE6?style=flat&logo=scipy&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=flat&logo=jupyter&logoColor=white)

---

## How to Reproduce

```bash
# 1. Clone the repository
git clone <repo-url>
cd sales-eda-portfolio

# 2. Download the dataset from Kaggle
#    https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
#    Extract all CSVs into: data/raw/

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the notebook
jupyter notebook notebooks/sales_eda.ipynb
```

> **Note:** The `data/raw/` folder is excluded from version control (see `.gitignore`). You must download the dataset manually from Kaggle.

---

## Key Skills Demonstrated

| Skill | Where Applied |
|---|---|
| **Data wrangling** | 9-table relational merge, datetime parsing, derived metrics |
| **Exploratory Data Analysis** | Missing value analysis, outlier detection (IQR), distribution profiling |
| **Statistical thinking** | Pearson & Spearman correlation, moving averages, quartile binning |
| **Data visualisation** | Matplotlib, Seaborn, Plotly (treemap, choropleth, violin, heatmap) |
| **Business storytelling** | Each section framed as a business question with an actionable conclusion |
| **Code quality** | Modular src/ architecture, reusable viz utilities, clean notebook structure |
| **Python best practices** | Type hints, docstrings, separation of concerns (loader / utils / notebook) |

---

## Project Structure

```
sales-eda-portfolio/
├── data/
│   └── raw/                    ← CSVs here (not committed)
├── notebooks/
│   └── sales_eda.ipynb         ← Main analysis notebook
├── src/
│   ├── data_loader.py          ← Loads and merges all 9 CSVs
│   └── viz_utils.py            ← Shared styling and chart helpers
├── outputs/
│   └── figures/                ← Exported charts (not committed)
├── requirements.txt
├── .gitignore
└── README.md
```

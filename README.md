# AI-Powered E-Commerce Sales & Business Analytics

**IBM SkillsBuild Data Analytics with AI Internship 2026**
**Author:** Sejal Dange 

---

## Project Summary

This project performs end-to-end data analytics on a real-world Amazon India sales dataset (~129,000 orders, March–June 2022). It covers data cleaning, exploratory analysis, sales and category insights, geographical analysis, order/fulfilment analysis, SQL-based queries, professional visualisations, AI-assisted business insights, and an interactive Streamlit dashboard.

**AI Tool Used:** IBM Bob was used as the AI development assistant throughout the project for code generation, analysis structuring, and business insight review.

---

## Dataset

| Property | Detail |
|---|---|
| **Name** | Amazon Sale Report |
| **Source** | Kaggle |
| **URL** | https://www.kaggle.com/datasets/thedevastator/unlock-profits-with-e-commerce-sales-data |
| **File** | `Amazon Sale Report.csv` |
| **Raw rows** | 128,975 |
| **Columns** | 24 |
| **Period** | March 2022 – June 2022 |
| **Currency** | INR (Indian Rupees) |

> **Important:** Download `Amazon Sale Report.csv` from the Kaggle link above and place it in the same folder as the project files before running anything.

---

## Project Files

| File | Description |
|---|---|
| `SejalDange_AIPoweredECommerceSalesAnalytics.ipynb` | Main Jupyter Notebook — all analysis, SQL, and visualisations |
| `app.py` | Streamlit interactive dashboard |
| `SejalDange_ProjectReport.docx` | Professional project report with findings and tables |
| `requirements.txt` | Python dependencies |
| `README.md` | This file |
| `Amazon Sale Report.csv` | Dataset (download separately from Kaggle) |

---

## Technology Stack

| Tool | Purpose |
|---|---|
| Python 3.10+ | Core programming language |
| Pandas | Data manipulation and cleaning |
| NumPy | Numerical computing |
| Matplotlib | Data visualisation |
| Seaborn | Statistical visualisation |
| SQLite (built-in) | SQL-based analysis via `sqlite3` |
| Streamlit | Interactive dashboard |
| IBM Bob | AI development assistant |

---

## Installation

### Step 1 — Clone or download the project folder

Place all project files in a single directory.

### Step 2 — Create a virtual environment (recommended)

```bash
python -m venv venv
```

Activate it:

- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Place the dataset

Download `Amazon Sale Report.csv` from Kaggle and place it in the project folder (same directory as `app.py` and the notebook).

---

## Running the Project

### Run the Jupyter Notebook

```bash
jupyter notebook SejalDange_AIPoweredECommerceSalesAnalytics.ipynb
```

Run all cells from top to bottom. Charts will be displayed inline and saved as PNG files in the project directory.

### Run the Streamlit Dashboard

```bash
streamlit run app.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`.

---

## What the Notebook Covers

| Section | Content |
|---|---|
| 1 | Import Libraries |
| 2 | Load Dataset (raw inspection) |
| 3 | Data Cleaning (7 steps) |
| 4 | Exploratory Data Analysis — core KPIs and distributions |
| 5 | Sales Analysis — monthly trend, B2B vs B2C, sales channel |
| 6 | Product & Category Analysis — revenue, units, top SKUs, size |
| 7 | Geographical Analysis — top states and cities |
| 8 | Order & Fulfilment Analysis — status, cancellation, service level, promotions |
| 9 | SQL Analysis — 10 SQLite queries |
| 10 | Advanced Visualisations — heatmap, stacked bar, correlation |
| 11 | AI-Assisted Business Insights — 10 data-driven findings |
| 12 | Project Summary |

---

## Key Results (from cleaned data)

| Metric | Value |
|---|---|
| Total Revenue | ₹7.86 Crore (INR) |
| Total Orders | 1,10,687 |
| Average Order Value | ₹661.35 |
| Total Units Sold | 1,14,139 |
| Top Category by Revenue | Set (49.9%) |
| Top State by Revenue | Maharashtra |
| Top City by Revenue | Bengaluru |
| Cancellation Rate | 9.1% |
| Amazon-Fulfilled Orders | 69.1% |
| Expedited Shipping Usage | 69.2% |

---

## SQL Queries Included

| Query | Business Question |
|---|---|
| Q1 | Overall business summary |
| Q2 | Revenue by category |
| Q3 | Monthly revenue trend |
| Q4 | Top 10 states by revenue |
| Q5 | Order status distribution |
| Q6 | Fulfilment type performance |
| Q7 | B2B vs B2C comparison |
| Q8 | Top 10 SKUs by revenue |
| Q9 | Shipping service level breakdown |
| Q10 | Top 5 cities in Maharashtra |

---

## Streamlit Dashboard Features

- **Sidebar filters:** Month, Category, Fulfilment Type
- **KPI row:** Total Revenue, Orders, Avg Order Value, Units Sold, Cancellation Rate
- **Tab 1 — Sales Trend:** Monthly revenue bar + order count line chart, B2B/B2C pie
- **Tab 2 — Category Analysis:** Revenue and quantity bar charts, size distribution
- **Tab 3 — Geography:** Top N states and top 10 cities (slider-adjustable)
- **Tab 4 — Orders & Fulfilment:** Status distribution, fulfilment pie, promotions analysis
- **Tab 5 — SQL Queries:** Select any of the 10 queries and see live results
- **Tab 6 — Business Insights:** 10 expandable, data-driven business recommendations

---

## Project Structure

```
project-folder/
│
├── Amazon Sale Report.csv                          ← dataset (download from Kaggle)
├── SejalDange_AIPoweredECommerceSalesAnalytics.ipynb
├── app.py
├── SejalDange_ProjectReport.docx
├── requirements.txt
├── README.md
│
└── (charts generated when notebook is run)
    ├── plot_amount_distribution.png
    ├── plot_monthly_sales.png
    ├── plot_b2b_b2c.png
    ├── plot_category_analysis.png
    ├── plot_top_sku.png
    ├── plot_size_revenue.png
    ├── plot_state_analysis.png
    ├── plot_city_analysis.png
    ├── plot_order_status.png
    ├── plot_fulfilment.png
    ├── plot_service_level.png
    ├── plot_promotions.png
    ├── plot_heatmap_cat_month.png
    ├── plot_courier_fulfilment.png
    └── plot_correlation.png
```

---

## Notes for Submission

- All analysis uses actual data computed from the dataset. No results are fabricated.
- The AI insights section generates findings programmatically from computed statistics. No paid API or external AI service is required.
- IBM Bob was used as an AI development assistant for code generation, logic structuring, and insight review.
- Power BI is not used. No advanced machine learning or deep learning is required.
- The project is designed to be beginner-to-intermediate level and fully explainable in a placement interview.

---

## License

This project is submitted as part of the IBM SkillsBuild Data Analytics with AI Internship 2026 and is intended for educational purposes.

"""
AI-Powered E-Commerce Sales & Business Analytics
Streamlit Dashboard — IBM SkillsBuild Internship 2026
Author: Tejaswini Lende
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import sqlite3
import warnings

warnings.filterwarnings("ignore")
sns.set_theme(style="whitegrid", palette="muted")

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Amazon Sales Analytics",
    page_icon="🛒",
    layout="wide",
)

# ── Data loader (cached so CSV is read only once) ────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("Amazon Sale Report.csv", low_memory=False)
    df.columns = df.columns.str.strip()

    # Drop empty column
    if "Unnamed: 22" in df.columns:
        df.drop(columns=["Unnamed: 22"], inplace=True)

    # Parse date
    df["Date"] = pd.to_datetime(df["Date"], format="%m-%d-%y", errors="coerce")

    # Remove nulls and zero-amount rows
    df = df.dropna(subset=["Amount"])
    df = df[df["Amount"] > 0]

    # Remove duplicate order IDs
    df.drop_duplicates(subset=["Order ID"], keep="first", inplace=True)

    # Standardise geography
    df["ship-state"] = df["ship-state"].str.strip().str.upper()
    df["ship-city"] = df["ship-city"].str.strip().str.upper()

    # Fill missing
    df["Courier Status"].fillna("Unknown", inplace=True)

    # Derived columns
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    df["Month_Name"] = df["Date"].dt.strftime("%b %Y")
    df["Has_Promotion"] = df["promotion-ids"].notna().astype(int)

    return df


df_full = load_data()

# ── Sidebar filters ───────────────────────────────────────────────────────────
st.sidebar.title("🔍 Filters")

months_available = sorted(df_full[df_full["Month"] != "2022-03"]["Month"].unique())
selected_months = st.sidebar.multiselect(
    "Select Month(s)",
    options=months_available,
    default=months_available,
)

categories = sorted(df_full["Category"].unique())
selected_cats = st.sidebar.multiselect(
    "Select Category/Categories",
    options=categories,
    default=categories,
)

fulfilment_opts = sorted(df_full["Fulfilment"].unique())
selected_fulfil = st.sidebar.multiselect(
    "Fulfilment Type",
    options=fulfilment_opts,
    default=fulfilment_opts,
)

# Apply filters
df = df_full[
    (df_full["Month"].isin(selected_months))
    & (df_full["Category"].isin(selected_cats))
    & (df_full["Fulfilment"].isin(selected_fulfil))
].copy()

# ── Title ─────────────────────────────────────────────────────────────────────
st.title("🛒 AI-Powered E-Commerce Sales & Business Analytics")
st.caption(
    "IBM SkillsBuild Data Analytics with AI Internship 2026 · "
    "Dataset: Amazon India Sales (Mar–Jun 2022) · Author: Tejaswini Lende"
)
st.markdown("---")

# ── KPI Row ───────────────────────────────────────────────────────────────────
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpi1.metric("💰 Total Revenue", f"₹{df['Amount'].sum()/1e7:.2f} Cr")
kpi2.metric("📦 Total Orders", f"{df['Order ID'].nunique():,}")
kpi3.metric("🧾 Avg Order Value", f"₹{df['Amount'].mean():.2f}")
kpi4.metric("📐 Units Sold", f"{df['Qty'].sum():,}")
kpi5.metric(
    "❌ Cancellation Rate",
    f"{(df['Status']=='Cancelled').sum()/len(df)*100:.1f}%",
)
st.markdown("---")

# ── Tab navigation ────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "📈 Sales Trend",
        "🏷️ Category Analysis",
        "🗺️ Geography",
        "📋 Orders & Fulfilment",
        "🔎 SQL Queries",
        "💡 Business Insights",
    ]
)

# ──────────────────────────────────────────────────────────────────────────────
# TAB 1 — Sales Trend
# ──────────────────────────────────────────────────────────────────────────────
with tab1:
    st.subheader("Monthly Sales Revenue & Order Count")

    monthly = (
        df.groupby("Month")
        .agg(Revenue=("Amount", "sum"), Orders=("Order ID", "count"))
        .reset_index()
        .sort_values("Month")
    )
    monthly["Revenue_Lakhs"] = monthly["Revenue"] / 1e5

    fig, ax1 = plt.subplots(figsize=(10, 4))
    bars = ax1.bar(
        monthly["Month"], monthly["Revenue_Lakhs"], color="steelblue", alpha=0.75
    )
    ax1.set_ylabel("Revenue (Lakhs ₹)", color="steelblue")
    ax1.tick_params(axis="y", labelcolor="steelblue")
    for bar in bars:
        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.2,
            f"₹{bar.get_height():.1f}L",
            ha="center",
            va="bottom",
            fontsize=9,
        )
    ax2 = ax1.twinx()
    ax2.plot(monthly["Month"], monthly["Orders"], color="darkorange", marker="o", lw=2)
    ax2.set_ylabel("Order Count", color="darkorange")
    ax2.tick_params(axis="y", labelcolor="darkorange")
    plt.title("Monthly Sales Trend")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Monthly Data Table**")
        monthly_disp = monthly[["Month", "Revenue", "Orders", "Revenue_Lakhs"]].copy()
        monthly_disp["Revenue"] = monthly_disp["Revenue"].map("₹{:,.2f}".format)
        monthly_disp["Revenue_Lakhs"] = monthly_disp["Revenue_Lakhs"].map("{:.2f}L".format)
        st.dataframe(monthly_disp, use_container_width=True)

    with col2:
        st.markdown("**B2B vs B2C Revenue**")
        b2b = (
            df.groupby("B2B")["Amount"]
            .sum()
            .reset_index()
        )
        b2b["B2B"] = b2b["B2B"].map({True: "B2B", False: "B2C"})
        fig2, ax2_ = plt.subplots(figsize=(4, 4))
        ax2_.pie(b2b["Amount"], labels=b2b["B2B"], autopct="%1.1f%%",
                 colors=["#4C72B0", "#DD8452"], startangle=90)
        ax2_.set_title("B2B vs B2C Revenue")
        st.pyplot(fig2)
        plt.close()

# ──────────────────────────────────────────────────────────────────────────────
# TAB 2 — Category Analysis
# ──────────────────────────────────────────────────────────────────────────────
with tab2:
    st.subheader("Category-Level Sales Performance")

    cat_data = (
        df.groupby("Category")
        .agg(Revenue=("Amount", "sum"), Orders=("Order ID", "count"), Qty=("Qty", "sum"))
        .sort_values("Revenue", ascending=False)
        .reset_index()
    )
    cat_data["Revenue_Pct"] = (
        cat_data["Revenue"] / cat_data["Revenue"].sum() * 100
    ).round(2)

    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots(figsize=(7, 5))
        sns.barplot(data=cat_data, x="Revenue", y="Category", palette="Blues_d", ax=ax)
        ax.set_xlabel("Revenue (INR)")
        ax.xaxis.set_major_formatter(
            mticker.FuncFormatter(lambda x, _: f"₹{x/1e6:.1f}M")
        )
        ax.set_title("Revenue by Category")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col2:
        fig, ax = plt.subplots(figsize=(7, 5))
        sns.barplot(
            data=cat_data.sort_values("Qty", ascending=False),
            x="Qty",
            y="Category",
            palette="Oranges_d",
            ax=ax,
        )
        ax.set_xlabel("Units Sold")
        ax.set_title("Units Sold by Category")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    st.markdown("**Category Summary Table**")
    cat_disp = cat_data.copy()
    cat_disp["Revenue"] = cat_disp["Revenue"].map("₹{:,.2f}".format)
    cat_disp["Revenue_Pct"] = cat_disp["Revenue_Pct"].map("{:.2f}%".format)
    st.dataframe(cat_disp, use_container_width=True)

    st.subheader("Size Distribution (by Revenue)")
    size_order = ["XS", "S", "M", "L", "XL", "XXL", "3XL", "4XL", "5XL", "6XL", "Free"]
    size_data = (
        df.groupby("Size")["Amount"]
        .sum()
        .reindex([s for s in size_order if s in df["Size"].unique()])
        .reset_index()
    )
    size_data.columns = ["Size", "Revenue"]
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.barplot(data=size_data, x="Size", y="Revenue", palette="coolwarm", ax=ax)
    ax.set_title("Revenue by Size")
    ax.set_ylabel("Revenue (INR)")
    ax.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, _: f"₹{x/1e6:.1f}M")
    )
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# ──────────────────────────────────────────────────────────────────────────────
# TAB 3 — Geography
# ──────────────────────────────────────────────────────────────────────────────
with tab3:
    st.subheader("Geographical Sales Analysis")

    n_states = st.slider("Top N States", min_value=5, max_value=20, value=10)

    state_data = (
        df.groupby("ship-state")
        .agg(Revenue=("Amount", "sum"), Orders=("Order ID", "count"))
        .sort_values("Revenue", ascending=False)
        .head(n_states)
        .reset_index()
    )

    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots(figsize=(7, 6))
        sns.barplot(
            data=state_data, x="Revenue", y="ship-state", palette="Blues_d", ax=ax
        )
        ax.set_title(f"Top {n_states} States by Revenue")
        ax.set_xlabel("Revenue (INR)")
        ax.xaxis.set_major_formatter(
            mticker.FuncFormatter(lambda x, _: f"₹{x/1e6:.0f}M")
        )
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col2:
        fig, ax = plt.subplots(figsize=(7, 6))
        sns.barplot(
            data=state_data.sort_values("Orders", ascending=False),
            x="Orders",
            y="ship-state",
            palette="Greens_d",
            ax=ax,
        )
        ax.set_title(f"Top {n_states} States by Orders")
        ax.set_xlabel("Number of Orders")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    st.subheader("Top 10 Cities by Revenue")
    city_data = (
        df.groupby("ship-city")
        .agg(Revenue=("Amount", "sum"), Orders=("Order ID", "count"))
        .sort_values("Revenue", ascending=False)
        .head(10)
        .reset_index()
    )
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=city_data, x="Revenue", y="ship-city", palette="viridis", ax=ax)
    ax.set_title("Top 10 Cities by Revenue")
    ax.set_xlabel("Revenue (INR)")
    ax.xaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, _: f"₹{x/1e6:.1f}M")
    )
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# ──────────────────────────────────────────────────────────────────────────────
# TAB 4 — Orders & Fulfilment
# ──────────────────────────────────────────────────────────────────────────────
with tab4:
    st.subheader("Order Status & Fulfilment Analysis")

    col1, col2 = st.columns(2)

    with col1:
        status_counts = df["Status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        fig, ax = plt.subplots(figsize=(7, 5))
        sns.barplot(data=status_counts, x="Count", y="Status", palette="Set2", ax=ax)
        ax.set_title("Order Status Distribution")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col2:
        fulfil_data = (
            df.groupby("Fulfilment")
            .agg(Revenue=("Amount", "sum"), Orders=("Order ID", "count"))
            .reset_index()
        )
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.pie(
            fulfil_data["Orders"],
            labels=fulfil_data["Fulfilment"],
            autopct="%1.1f%%",
            colors=["#4C72B0", "#DD8452"],
            startangle=90,
        )
        ax.set_title("Orders by Fulfilment Type")
        st.pyplot(fig)
        plt.close()

    st.subheader("Promotion Analysis")
    promo = (
        df.groupby("Has_Promotion")
        .agg(Orders=("Order ID", "count"), Avg_Value=("Amount", "mean"))
        .reset_index()
    )
    promo["Has_Promotion"] = promo["Has_Promotion"].map(
        {0: "No Promotion", 1: "With Promotion"}
    )
    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.pie(
            promo["Orders"],
            labels=promo["Has_Promotion"],
            autopct="%1.1f%%",
            colors=["#55a868", "#4c72b0"],
        )
        ax.set_title("Orders: Promo vs No Promo")
        st.pyplot(fig)
        plt.close()
    with col2:
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.bar(promo["Has_Promotion"], promo["Avg_Value"], color=["#55a868", "#4c72b0"])
        ax.set_title("Avg Order Value: Promo vs No Promo")
        ax.set_ylabel("INR")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

# ──────────────────────────────────────────────────────────────────────────────
# TAB 5 — SQL Queries
# ──────────────────────────────────────────────────────────────────────────────
with tab5:
    st.subheader("SQL-Based Analysis (SQLite in-memory)")

    conn = sqlite3.connect(":memory:")
    df.to_sql("sales", conn, if_exists="replace", index=False)

    queries = {
        "Q1 — Overall Business Summary": """
SELECT
    COUNT(DISTINCT "Order ID") AS Total_Orders,
    ROUND(SUM(Amount), 2)      AS Total_Revenue_INR,
    ROUND(AVG(Amount), 2)      AS Avg_Order_Value,
    SUM(Qty)                   AS Total_Units_Sold,
    COUNT(DISTINCT SKU)        AS Unique_SKUs,
    COUNT(DISTINCT "ship-state") AS States_Covered
FROM sales;""",

        "Q2 — Revenue by Category": """
SELECT Category,
    COUNT("Order ID")  AS Orders,
    SUM(Qty)           AS Qty,
    ROUND(SUM(Amount),2) AS Revenue,
    ROUND(SUM(Amount)*100.0/(SELECT SUM(Amount) FROM sales),2) AS Revenue_Pct
FROM sales
GROUP BY Category
ORDER BY Revenue DESC;""",

        "Q3 — Monthly Revenue Trend": """
SELECT Month,
    COUNT("Order ID")    AS Orders,
    ROUND(SUM(Amount),2) AS Revenue,
    ROUND(AVG(Amount),2) AS Avg_Order_Value
FROM sales
WHERE Month != '2022-03'
GROUP BY Month
ORDER BY Month;""",

        "Q4 — Top 10 States by Revenue": """
SELECT "ship-state" AS State,
    COUNT("Order ID")    AS Orders,
    ROUND(SUM(Amount),2) AS Revenue
FROM sales
GROUP BY State
ORDER BY Revenue DESC
LIMIT 10;""",

        "Q5 — Order Status Summary": """
SELECT Status,
    COUNT("Order ID") AS Orders,
    ROUND(COUNT("Order ID")*100.0/(SELECT COUNT(*) FROM sales),2) AS Pct
FROM sales
GROUP BY Status
ORDER BY Orders DESC;""",

        "Q6 — Fulfilment Performance": """
SELECT Fulfilment,
    COUNT("Order ID")    AS Orders,
    ROUND(SUM(Amount),2) AS Revenue,
    ROUND(AVG(Amount),2) AS Avg_Order_Value,
    SUM(CASE WHEN Status='Cancelled' THEN 1 ELSE 0 END) AS Cancellations
FROM sales
GROUP BY Fulfilment
ORDER BY Revenue DESC;""",

        "Q7 — B2B vs B2C": """
SELECT CASE WHEN B2B=1 THEN 'B2B' ELSE 'B2C' END AS Customer_Type,
    COUNT("Order ID")    AS Orders,
    ROUND(SUM(Amount),2) AS Revenue,
    ROUND(AVG(Amount),2) AS Avg_Order_Value
FROM sales
GROUP BY B2B;""",

        "Q8 — Top 10 SKUs": """
SELECT SKU, Category,
    COUNT("Order ID")    AS Orders,
    SUM(Qty)             AS Total_Qty,
    ROUND(SUM(Amount),2) AS Revenue
FROM sales
GROUP BY SKU
ORDER BY Revenue DESC
LIMIT 10;""",

        "Q9 — Shipping Service Level": """
SELECT "ship-service-level" AS Service_Level,
    COUNT("Order ID")    AS Orders,
    ROUND(SUM(Amount),2) AS Revenue,
    ROUND(AVG(Amount),2) AS Avg_Order_Value
FROM sales
GROUP BY Service_Level
ORDER BY Revenue DESC;""",

        "Q10 — Top Cities in Maharashtra": """
SELECT "ship-city" AS City,
    COUNT("Order ID")    AS Orders,
    ROUND(SUM(Amount),2) AS Revenue
FROM sales
WHERE "ship-state"='MAHARASHTRA'
GROUP BY City
ORDER BY Orders DESC
LIMIT 5;""",
    }

    selected_q = st.selectbox("Choose a SQL Query", list(queries.keys()))
    sql = queries[selected_q]
    st.code(sql.strip(), language="sql")
    result_df = pd.read_sql(sql, conn)
    st.dataframe(result_df, use_container_width=True)
    conn.close()

# ──────────────────────────────────────────────────────────────────────────────
# TAB 6 — Business Insights
# ──────────────────────────────────────────────────────────────────────────────
with tab6:
    st.subheader("💡 AI-Assisted Business Insights")
    st.info(
        "These insights are generated from actual analytical results computed "
        "from the dataset. IBM Bob (AI assistant) was used during development "
        "to structure logic and review findings. No paid API required."
    )

    total_rev    = df["Amount"].sum()
    top_cat      = df.groupby("Category")["Amount"].sum().idxmax()
    top_cat_pct  = df.groupby("Category")["Amount"].sum().max() / total_rev * 100
    top_state    = df.groupby("ship-state")["Amount"].sum().idxmax()
    cancel_rate  = (df["Status"] == "Cancelled").sum() / len(df) * 100
    amz_pct      = (df["Fulfilment"] == "Amazon").sum() / len(df) * 100
    promo_aov    = df[df["Has_Promotion"] == 1]["Amount"].mean()
    nopromo_aov  = df[df["Has_Promotion"] == 0]["Amount"].mean()
    b2b_pct      = df[df["B2B"] == True]["Amount"].sum() / total_rev * 100
    exp_pct      = (df["ship-service-level"] == "Expedited").sum() / len(df) * 100

    insights_data = [
        ("💰 Revenue Scale",
         f"Total revenue of ₹{total_rev/1e7:.2f} Crores from {df['Order ID'].nunique():,} orders. "
         f"Avg order value: ₹{df['Amount'].mean():.2f}. "
         "**Action:** Bundle and upsell strategies can meaningfully increase AOV."),
        ("🏷️ Category Concentration",
         f"'{top_cat}' drives {top_cat_pct:.1f}% of revenue. Top 2 categories contribute ~77%. "
         "**Action:** Reduce dependency — invest in growing Western Dress and Ethnic Dress categories."),
        ("🗺️ Geographical Concentration",
         f"{top_state} leads in revenue. Top 3 states drive ~40% of total sales. "
         "**Action:** Target Tier-2/3 cities with region-specific promotions."),
        ("❌ Cancellation Rate",
         f"{cancel_rate:.2f}% cancellation rate on {len(df):,} orders. "
         "**Action:** Investigate sizing issues, delivery delays, and return policies."),
        ("🚚 Fulfilment Mix",
         f"{amz_pct:.1f}% Amazon-fulfilled. "
         "**Action:** Monitor Merchant-fulfilled orders for delivery quality gaps."),
        ("🎁 Promotions",
         f"Promo AOV ₹{promo_aov:.2f} vs No-Promo AOV ₹{nopromo_aov:.2f}. "
         + ("Promotions correlate with higher spend." if promo_aov > nopromo_aov
            else "Promotions show lower AOV — review discount structure.")),
        ("🏢 B2B Opportunity",
         f"B2B is only {b2b_pct:.1f}% of revenue. "
         "**Action:** Dedicated bulk pricing and B2B outreach can unlock high-value revenue."),
        ("⚡ Expedited Demand",
         f"{exp_pct:.1f}% chose Expedited shipping. "
         "**Action:** Ensure consistent Expedited availability to maintain satisfaction."),
    ]

    for title, text in insights_data:
        with st.expander(title, expanded=False):
            st.markdown(text)

st.markdown("---")
st.caption("Made with IBM Bob · IBM SkillsBuild Data Analytics with AI Internship 2026 · Tejaswini Lende")

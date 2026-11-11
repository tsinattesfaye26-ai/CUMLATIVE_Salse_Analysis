"""
Sales analysis, Oct 01 - Oct 16, 2026
16 questions in 5 parts. Each question saves its result in its own table (q1_..., q2_...)
so the visualization / app.py can import it:  from analysis import q1_product_group

Run from the project root:  python analysis/analysis.py
"""

# ============================================================
# SETUP
# ============================================================
import pandas as pd

df = pd.read_csv("data/processed/CUMLATIVE_SALES_CLEAN.csv")
df["date"] = pd.to_datetime(df["date"], format="%b %d,%Y")
df = df.rename(columns={"total_incl_vat": "total"})

# one table per product group (used by several questions)
ups = df[df["category"] == "UPS"]
wf = df[df["category"] == "WF"]
em = df[df["category"] == "EM"]


# ============================================================
# PART 1: OVERALL PERFORMANCE
# ============================================================

# Q1. What is the total sales performance by product group?
q1_product_group = df.groupby("category")["total"].sum().sort_values(ascending=False).reset_index()
q1_product_group["share_pct"] = (q1_product_group["total"] / df["total"].sum() * 100).round(2)

# Q2. What is the sales performance of each salesperson?
q2_salesperson = df.groupby("sales_person")["total"].sum().sort_values(ascending=False).reset_index()
q2_salesperson["share_pct"] = (q2_salesperson["total"] / df["total"].sum() * 100).round(2)


# ============================================================
# PART 2: PRODUCTS
# ============================================================

# Q3. What are the top 10 products by total sales?
q3_top_products = df.groupby("item")["total"].sum().nlargest(10).reset_index()
q3_top_products["share_pct"] = (q3_top_products["total"] / df["total"].sum() * 100).round(2)

# Q4. What are the top 10 UPS products by total sales?
q4_ups_products = ups.groupby("item")["total"].sum().nlargest(10).reset_index()
q4_ups_products["share_pct"] = (q4_ups_products["total"] / ups["total"].sum() * 100).round(2)

# Q5. What are the top 10 Water Filter products by total sales?
q5_wf_products = wf.groupby("item")["total"].sum().nlargest(10).reset_index()
q5_wf_products["share_pct"] = (q5_wf_products["total"] / wf["total"].sum() * 100).round(2)

# Q6. What are the top 10 Electromechanical products by total sales?
q6_em_products = em.groupby("item")["total"].sum().nlargest(10).reset_index()
q6_em_products["share_pct"] = (q6_em_products["total"] / em["total"].sum() * 100).round(2)


# ============================================================
# PART 3: CUSTOMERS
# ============================================================

# Q7. What are the top 10 customers by total sales across all products?
q7_top_customers = df.groupby("company_name")["total"].sum().nlargest(10).reset_index()
q7_top_customers["share_pct"] = (q7_top_customers["total"] / df["total"].sum() * 100).round(2)

# Q8. What are the top 10 UPS customers by total sales?
q8_ups_customers = ups.groupby("company_name")["total"].sum().nlargest(10).reset_index()
q8_ups_customers["share_pct"] = (q8_ups_customers["total"] / ups["total"].sum() * 100).round(2)

# Q9. What are the top 10 Water Filter customers by total sales?
q9_wf_customers = wf.groupby("company_name")["total"].sum().nlargest(10).reset_index()
q9_wf_customers["share_pct"] = (q9_wf_customers["total"] / wf["total"].sum() * 100).round(2)

# Q10. What are the top 10 Electromechanical customers by total sales?
q10_em_customers = em.groupby("company_name")["total"].sum().nlargest(10).reset_index()
q10_em_customers["share_pct"] = (q10_em_customers["total"] / em["total"].sum() * 100).round(2)


# ============================================================
# PART 4: BUSINESS INSIGHTS
# ============================================================

# Q11. Which products have high sales quantity but relatively low sales value?
q11_qty_vs_value = df.groupby("item").agg(quantity=("quantity", "sum"), total_sales=("total", "sum")).reset_index()
q11_qty_vs_value["quantity_rank"] = q11_qty_vs_value["quantity"].rank(ascending=False, method="min").astype(int)
q11_qty_vs_value["sales_rank"] = q11_qty_vs_value["total_sales"].rank(ascending=False, method="min").astype(int)
q11_qty_vs_value["avg_price_per_unit"] = (q11_qty_vs_value["total_sales"] / q11_qty_vs_value["quantity"]).round(0)
q11_qty_vs_value = q11_qty_vs_value.sort_values("quantity", ascending=False).head(15)

# Q12. How much of the total sales comes from the top 10 customers?
q12_top10_share = pd.DataFrame({
    "top10_sales": [q7_top_customers["total"].sum()],
    "all_sales": [df["total"].sum()],
    "share_pct": [round(q7_top_customers["total"].sum() / df["total"].sum() * 100, 2)],
})

# Q13. Which salesperson performs best within each product group?
q13_by_group = df.groupby(["category", "sales_person"])["total"].sum().reset_index()
q13_by_group["share_of_group_pct"] = (
    q13_by_group["total"] / q13_by_group.groupby("category")["total"].transform("sum") * 100
).round(2)
q13_by_group = q13_by_group.sort_values(["category", "total"], ascending=[True, False])
q13_best_per_group = q13_by_group.groupby("category").head(1).reset_index(drop=True)

# Q14. Which products have the highest average sales per transaction?
q14_avg_per_transaction = df.groupby("item")["total"].agg(
    average_sale="mean", transactions="count", total_sales="sum"
).round(0).sort_values("average_sale", ascending=False).head(10).reset_index()

# Q15. How does sales performance change over time?
q15_daily = df.groupby("date")["total"].sum().reset_index()
q15_daily["cumulative"] = q15_daily["total"].cumsum()


# ============================================================
# PART 5: DAILY SALES
# ============================================================

# Q16. What were the sales on each specific day?
#      One row per day (days with no sales are included with 0).
q16_daily_summary = df.groupby("date").agg(
    total=("total", "sum"),
    transactions=("total", "size"),
    quantity=("quantity", "sum"),
)

_all_days = pd.date_range(
    q16_daily_summary.index.min(),
    q16_daily_summary.index.max(),
    freq="D",
)

q16_daily_summary = (
    q16_daily_summary
    .reindex(_all_days, fill_value=0)
    .rename_axis("date")
    .reset_index()
)

q16_daily_summary["average_sale"] = (
    q16_daily_summary["total"].div(
        q16_daily_summary["transactions"].where(q16_daily_summary["transactions"] > 0)
    )
).fillna(0)

q16_daily_summary["cumulative"] = q16_daily_summary["total"].cumsum()


def get_day_data(selected_day):
    """Return every transaction of one specific day (used by the Daily Sales page)."""
    day = pd.Timestamp(selected_day).normalize()
    return df[df["date"].dt.normalize() == day].copy()


# ============================================================
# SHOW ALL RESULTS (only when you run this file directly)
# ============================================================
if __name__ == "__main__":
    pd.options.display.float_format = "{:,.2f}".format
    pd.options.display.width = 200
    print("Rows:", len(df), "  Total:", round(df["total"].sum(), 2), "\n")
    for name in ["q1_product_group", "q2_salesperson", "q3_top_products", "q4_ups_products",
                 "q5_wf_products", "q6_em_products", "q7_top_customers", "q8_ups_customers",
                 "q9_wf_customers", "q10_em_customers", "q11_qty_vs_value", "q12_top10_share",
                 "q13_by_group", "q13_best_per_group", "q14_avg_per_transaction", "q15_daily",
                 "q16_daily_summary"]:
        print("=====", name)
        print(globals()[name].to_string(index=False), "\n")
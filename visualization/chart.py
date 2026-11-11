"""
Charts for the 15 questions. One function per question: fig_q1() ... fig_q15()
Each function returns a Plotly figure built from the matching table in analysis/analysis.py

Use in app.py:  from visualization.chart import fig_q1
"""
from matplotlib.pylab import eig
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from analysis.analysis import (
    q1_product_group, q2_salesperson,
    q3_top_products, q4_ups_products, q5_wf_products, q6_em_products,
    q7_top_customers, q8_ups_customers, q9_wf_customers, q10_em_customers,
    q11_qty_vs_value, q12_top10_share, q13_by_group,
    q14_avg_per_transaction, q15_daily,
)

BLUE = "#2E5A88"
GROUP_NAMES = {"UPS": "UPS", "WF": "Water Filter", "EM": "Electromechanical"}
MONEY_LABEL = "Total sales (incl. VAT)"


def bar_h(table, x, y, title, hover=None, x_label=MONEY_LABEL):
    """Horizontal bar chart, biggest bar on top (used by most questions)."""
    fig = px.bar(table, x=x, y=y, orientation="h", title=title, hover_data=hover)
    fig.update_traces(marker_color=BLUE, texttemplate="%{x:,.0f}", textposition="outside", cliponaxis=False)
    fig.update_yaxes(autorange="reversed", title=None, automargin=True)
    fig.update_xaxes(title=x_label)
    fig.update_layout(template="plotly_white", height=450, margin=dict(r=90))
    return fig


# ---------------- PART 1: OVERALL PERFORMANCE ----------------

def fig_q1():
    """Q1. Sales by product group -> donut (only 3 groups, so the shares are easy to read)."""
    t = q1_product_group.copy()
    t["category"] = t["category"].map(GROUP_NAMES)
    fig = px.pie(t, names="category", values="total", hole=0.5, title="Sales by product group")
    fig.update_traces(textinfo="label+percent", textposition="outside")
    fig.update_layout(template="plotly_white", height=450, showlegend=False)
    return fig


def fig_q2():
    """Q2. Sales by salesperson -> horizontal bar."""
    return bar_h(q2_salesperson, "total", "sales_person", "Sales by salesperson", hover=["share_pct"])


# ---------------- PART 2: PRODUCTS ----------------

def fig_q3():
    return bar_h(q3_top_products, "total", "item", "Top 10 products by total sales", hover=["share_pct"])


def fig_q4():
    return bar_h(q4_ups_products, "total", "item", "Top 10 UPS products", hover=["share_pct"])


def fig_q5():
    return bar_h(q5_wf_products, "total", "item", "Top 10 Water Filter products", hover=["share_pct"])


def fig_q6():
    return bar_h(q6_em_products, "total", "item", "Top 10 Electromechanical products", hover=["share_pct"])


# ---------------- PART 3: CUSTOMERS ----------------

def fig_q7():
    return bar_h(q7_top_customers, "total", "company_name", "Top 10 customers (all products)", hover=["share_pct"])


def fig_q8():
    return bar_h(q8_ups_customers, "total", "company_name", "Top 10 UPS customers", hover=["share_pct"])


def fig_q9():
    return bar_h(q9_wf_customers, "total", "company_name", "Top 10 Water Filter customers", hover=["share_pct"])


def fig_q10():
    return bar_h(q10_em_customers, "total", "company_name", "Top 10 Electromechanical customers", hover=["share_pct"])


# ---------------- PART 4: BUSINESS INSIGHTS ----------------

def fig_q11():
    """Q11. Units sold vs sales value -> scatter. Bottom-right = many units but low value."""
    fig = px.scatter(
        q11_qty_vs_value, x="quantity", y="total_sales", text="item",
        hover_data=["quantity_rank", "sales_rank", "avg_price_per_unit"],
        title="Units sold vs sales value (top 15 products by units)",
    )
    fig.update_traces(marker=dict(size=12, color=BLUE), textposition="top center")
    fig.update_xaxes(title="Units sold")
    fig.update_yaxes(title=MONEY_LABEL)
    fig.update_layout(template="plotly_white", height=500)
    return fig


def fig_q12():
    """Q12. Share of sales from the top 10 customers -> donut."""
    row = q12_top10_share.iloc[0]
    fig = px.pie(
        names=["Top 10 customers", "All other customers"],
        values=[row["top10_sales"], row["all_sales"] - row["top10_sales"]],
        hole=0.5, title="How much of the sales comes from the top 10 customers",
    )
    fig.update_traces(textinfo="label+percent", textposition="outside")
    fig.update_layout(template="plotly_white", height=450, showlegend=False)
    return fig


def fig_q13():
    """Q13. Salespeople inside each product group -> grouped bar."""
    t = q13_by_group.copy()
    t["category"] = t["category"].map(GROUP_NAMES)
    fig = px.bar(
        t, x="category", y="total", color="sales_person", barmode="group",
        hover_data=["share_of_group_pct"], title="Sales by salesperson inside each product group",
    )
    fig.update_xaxes(title=None)
    fig.update_yaxes(title=MONEY_LABEL)
    fig.update_layout(template="plotly_dark", height=500, legend_title_text="Salesperson")
    return fig


def fig_q14():
    """Q14. Highest average sale per transaction -> horizontal bar (hover shows number of transactions)."""
    return bar_h(
        q14_avg_per_transaction, "average_sale", "item",
        "Top 10 products by average sale per transaction",
        hover=["transactions", "total_sales"], x_label="Average sale per transaction",
    )


def fig_q15():
    """Q15. Sales over time -> daily bars + cumulative line."""
    days = q15_daily["date"].dt.strftime("%b %d")
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
    go.Bar(
        x=days,
        y=q15_daily["total"],
        name="Daily sales",
        marker_color="#4F7CFF",
        marker_line_color="#6F92FF",
        marker_line_width=1,
    ),
    secondary_y=False
)
    fig.add_trace(go.Scatter(x=days, y=q15_daily["cumulative"], name="Cumulative sales",
                             mode="lines+markers", line=dict(color="#E07B39")), secondary_y=True)
    fig.update_xaxes(type="category", title=None)
    fig.update_yaxes(title_text="Daily sales", secondary_y=False)
    fig.update_yaxes(title_text="Cumulative sales", secondary_y=True)
    fig.update_layout(
    template="plotly_dark",

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(10,18,35,0.55)",

    height=500,

    title="Sales over time",

    legend=dict(
        orientation="h",
        y=-0.15,
    ),

    xaxis=dict(
        gridcolor="rgba(255,255,255,0.05)",
        zeroline=False,
    ),

    yaxis=dict(
        gridcolor="rgba(255,255,255,0.07)",
        zeroline=False,
    ),

    font=dict(
        color="#DDE5F5",
    )
  )

    return fig
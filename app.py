from contextlib import contextmanager

import pandas as pd
import plotly.express as px
import streamlit as st

from analysis.analysis import (
    df,
    q1_product_group,
    q2_salesperson,
    q7_top_customers,
    q8_ups_customers,
    q9_wf_customers,
    q10_em_customers,
    q12_top10_share,
    q16_daily_summary,
    get_day_data,
)

from visualization.chart import (
    fig_q1,
    fig_q15,
)


# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="Sales Performance",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ---------------- MAIN BACKGROUND ---------------- */

    .stApp {
        background-color: #0B0F19;
        color: #F5F7FA;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
        padding-bottom: 4rem;
        max-width: 1500px;
    }


    /* ---------------- SIDEBAR ---------------- */

    section[data-testid="stSidebar"] {
        background-color: #080D17;
        border-right: 1px solid #1D2636;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }

    .sidebar-logo {
        padding: 0.5rem 0.5rem 1.5rem 0.5rem;
    }

    .sidebar-logo-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 0.15rem;
    }

    .sidebar-logo-subtitle {
        font-size: 0.75rem;
        color: #7F8AA3;
    }


    /* ---------------- HEADINGS ---------------- */

    h1 {
        color: #FFFFFF !important;
        font-weight: 750 !important;
        letter-spacing: -0.5px;
    }

    h2, h3 {
        color: #FFFFFF !important;
    }

    .page-subtitle {
        color: #7F8AA3;
        font-size: 0.9rem;
        margin-top: -0.7rem;
        margin-bottom: 1.8rem;
    }


    /* ---------------- KPI CARDS ---------------- */

    .kpi-card {
        background: linear-gradient(145deg, #141C2C, #101725);
        border: 1px solid #24304A;
        border-radius: 14px;
        padding: 1.25rem 1.35rem;
        min-height: 135px;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.18);
        transition:
            transform 0.2s ease,
            border-color 0.2s ease,
            box-shadow 0.2s ease;
    }

    .kpi-card:hover {
        transform: translateY(-4px);
        border-color: #4169E1;
        box-shadow: 0 8px 25px rgba(65, 105, 225, 0.16);
    }

    .kpi-label {
        color: #8C96AA;
        font-size: 0.78rem;
        font-weight: 600;
        margin-bottom: 0.55rem;
    }

    .kpi-value {
        color: #FFFFFF;
        font-size: 1.75rem;
        font-weight: 750;
        line-height: 1.1;
    }

    .kpi-description {
        color: #6F7A91;
        font-size: 0.72rem;
        margin-top: 0.6rem;
    }

    /* KPI accent colors */
    .primary { border-top: 3px solid #4F7CFF; }
    .violet  { border-top: 3px solid #8B5CF6; }
    .cyan    { border-top: 3px solid #22D3EE; }
    .gold    { border-top: 3px solid #34D399; }

    /* Total Sales card gets a subtle blue glow */
    .kpi-card.primary {
        background: linear-gradient(145deg, #17264F, #101725);
        box-shadow: 0 4px 22px rgba(79, 124, 255, 0.18);
    }


    /* ---------------- CARDS (real containers) ---------------- */

    div[class*="st-key-card_"],
    div[class*="st-key-nav_"] {
        background: linear-gradient(145deg, #111827, #0E1626);
        border: 1px solid #243452;
        border-radius: 14px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 0 18px rgba(79, 124, 255, 0.08);
        transition:
            transform 0.25s ease,
            box-shadow 0.25s ease,
            border-color 0.25s ease;
    }

    div[class*="st-key-card_"]:hover,
    div[class*="st-key-nav_"]:hover {
        border-color: #3157A6;
        box-shadow: 0 0 25px rgba(79, 124, 255, 0.16);
    }

    div[class*="st-key-nav_"]:hover {
        transform: translateY(-2px);
    }

    /* Link-style buttons inside navigation cards */
    div[class*="st-key-nav_"] button {
        background: transparent;
        border: none;
        padding: 0;
        color: #4F7CFF;
        font-weight: 600;
        font-size: 0.85rem;
    }

    div[class*="st-key-nav_"] button:hover {
        color: #7A9CFF;
        background: transparent;
    }

    .section-title {
        color: #FFFFFF;
        font-size: 1rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }

    .section-description {
        color: #727D92;
        font-size: 0.75rem;
        margin-bottom: 1rem;
    }


    /* ---------------- INSIGHT CARDS ---------------- */

    .insight-card {
        background: linear-gradient(145deg, #141C2C, #101725);
        border: 1px solid #25324A;
        border-radius: 14px;
        padding: 1.25rem;
        min-height: 175px;
    }

    .insight-icon {
        font-size: 1.4rem;
        margin-bottom: 0.5rem;
    }

    .insight-title {
        color: #FFFFFF;
        font-size: 0.9rem;
        font-weight: 700;
        margin-bottom: 0.55rem;
    }

    .insight-text {
        color: #929CAF;
        font-size: 0.78rem;
        line-height: 1.55;
    }


    /* ---------------- SELECTBOX ---------------- */

    div[data-baseweb="select"] > div {
        background-color: #111827;
        border-color: #293650;
        border-radius: 8px;
    }


    /* ---------------- DOWNLOAD BUTTON ---------------- */

    .stDownloadButton button {
        background-color: #4169E1;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
    }

    .stDownloadButton button:hover {
        background-color: #5278EF;
        color: white;
    }


    /* ---------------- DATAFRAME ---------------- */

    div[data-testid="stDataFrame"] {
        border: 1px solid #202B40;
        border-radius: 10px;
    }


    /* ---------------- SIDEBAR RADIO ---------------- */

    div[role="radiogroup"] label {
        background-color: transparent;
        border-radius: 8px;
        padding: 0.35rem 0.5rem;
        margin-bottom: 0.15rem;
    }

    div[role="radiogroup"] label:hover {
        background-color: #151E30;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CONSTANTS
# ============================================================

# Friendly name -> category code used in the data
CATEGORY_MAP = {
    "All Products": None,
    "UPS": "UPS",
    "Water Filter": "WF",
    "Electromechanical": "EM",
}

# Category code -> friendly name
CATEGORY_NAMES = {
    "UPS": "UPS",
    "WF": "Water Filter",
    "EM": "Electromechanical",
}

# Customer tables prepared in analysis.py, by category code
CUSTOMER_TABLES = {
    None: q7_top_customers,
    "UPS": q8_ups_customers,
    "WF": q9_wf_customers,
    "EM": q10_em_customers,
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def money(value):
    """Format money values."""
    return f"{value:,.0f}"


def compact(value):
    """17,650,000 -> 17.65M, 120,100 -> 120.1K"""
    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    if abs(value) >= 1_000:
        return f"{value / 1_000:.1f}K"
    return f"{value:,.0f}"


def pretty_table(table):
    """Format tables for the dashboard."""

    display_table = table.copy()

    for col in display_table.columns:

        if pd.api.types.is_datetime64_any_dtype(display_table[col]):
            display_table[col] = display_table[col].dt.strftime("%b %d, %Y")

        elif pd.api.types.is_numeric_dtype(display_table[col]):

            if "pct" in col.lower():
                display_table[col] = display_table[col].map(
                    lambda x: f"{x:,.2f}%"
                )

            else:
                is_whole = (display_table[col].dropna() % 1 == 0).all()
                decimals = 0 if is_whole else 2
                display_table[col] = display_table[col].map(
                    lambda x, d=decimals: f"{x:,.{d}f}"
                )

    return display_table


def kpi_card(label, value, description, color):
    """Create a dashboard KPI card (color: primary, violet, cyan, gold)."""

    st.markdown(
        f"""
        <div class="kpi-card {color}">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-description">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title, description=""):
    """Create a section heading."""

    st.markdown(
        f"""
        <div class="section-title">{title}</div>
        <div class="section-description">{description}</div>
        """,
        unsafe_allow_html=True,
    )


def show_table(table):
    """Display a formatted table."""

    st.dataframe(
        pretty_table(table),
        use_container_width=True,
        hide_index=True,
    )


_card_counter = 0


@contextmanager
def card():
    """A real container: everything inside `with card():` sits in the box."""

    global _card_counter
    _card_counter += 1

    with st.container(key=f"card_{_card_counter}"):
        yield


def style_fig(fig, height=400, margin=None):
    """Apply the dark theme to a Plotly figure."""

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#DDE3EF",
        height=height,
        margin=margin or dict(l=10, r=10, t=10, b=20),
    )
    return fig


PALETTE = ["#4F7CFF", "#8B5CF6", "#22D3EE", "#34D399"]


def recolor(fig):
    """Use the dashboard palette (blue, violet, cyan, green) on a figure."""

    line_i = 0

    for trace in fig.data:

        if trace.type == "pie":
            trace.marker.colors = PALETTE

        elif trace.type == "bar":
            trace.marker.color = PALETTE[0]

        elif trace.type == "scatter":
            color = PALETTE[(line_i + 2) % len(PALETTE)] if line_i == 0 else PALETTE[1]
            trace.line.color = color
            line_i += 1

    return fig


def hbar(data, x, y, key, color="#4F6EF7", height=400, x_title="Sales"):
    """Horizontal bar chart, sorted so the biggest bar is on top."""

    fig = px.bar(
        data.sort_values(x),
        x=x,
        y=y,
        orientation="h",
        text=x,
    )

    fig.update_traces(
        marker_color=color,
        texttemplate="%{text:,.0f}",
        textposition="outside",
        marker_line_width=0,
        opacity=0.9,
    )

    style_fig(fig, height=height, margin=dict(l=10, r=80, t=10, b=20))

    fig.update_layout(xaxis_title=x_title, yaxis_title=None)

    st.plotly_chart(fig, use_container_width=True, key=key)


def go_to(page_name):
    """Button callback: switch the sidebar page."""
    st.session_state["page"] = page_name


def nav_card(title, description, link_text, target):
    """Clickable card on the Overview page."""

    with st.container(key=f"nav_{target.lower().replace(' ', '_')}"):
        st.markdown(
            f"""
            <div class="section-title">{title}</div>
            <div class="section-description">{description}</div>
            """,
            unsafe_allow_html=True,
        )
        st.button(
            f"{link_text} →",
            key=f"btn_{target}",
            on_click=go_to,
            args=(target,),
        )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-logo">'
        '<div class="sidebar-logo-title">◈ Sales Performance</div>'
        '<div class="sidebar-logo-subtitle">Business Analytics Dashboard</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    page = st.radio(
        "Navigation",
        [
            "Overview",
            "Products",
            "Customers",
            "Sales Team",
            "Daily Sales",
            "Business Insights",
        ],
        key="page",
        label_visibility="collapsed",
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
        <div style="color:#68738A; font-size:0.72rem; line-height:1.5;">
            Oct 01 – Oct 16, 2026<br>
            All amounts include VAT
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# GLOBAL VALUES
# ============================================================

total_sales = df["total"].sum()
transactions = len(df)
average_sale = df["total"].mean()
top10_share = q12_top10_share["share_pct"].iloc[0]

top_product_group = q1_product_group.iloc[0]["category"]
top_product_group_sales = q1_product_group.iloc[0]["total"]

top_salesperson = q2_salesperson.iloc[0]["sales_person"]
top_salesperson_sales = q2_salesperson.iloc[0]["total"]


# ============================================================
# PAGE 1 — OVERVIEW
# ============================================================

if page == "Overview":

    st.title("Sales Performance")
    st.markdown(
        '<div class="page-subtitle">'
        'Business overview · Oct 01 – Oct 16, 2026'
        '</div>',
        unsafe_allow_html=True,
    )

    # ---------------- KPIs ----------------

    k1, k2, k3 = st.columns(3)

    with k1:
        kpi_card(
            "TOTAL SALES",
            compact(total_sales),
            "Total revenue including VAT",
            "primary",
        )

    with k2:
        kpi_card(
            "TRANSACTIONS",
            f"{transactions:,}",
            "Total sales transactions",
            "violet",
        )

    with k3:
        kpi_card(
            "AVERAGE SALE",
            compact(average_sale),
            "Average value per transaction",
            "cyan",
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------- CHARTS ----------------

    chart_left, chart_right = st.columns([1.6, 1])

    with chart_left:
        with card():
            section_header("Sales Trend", "Daily and cumulative sales")
            fig = recolor(style_fig(fig_q15(), height=320))
            st.plotly_chart(fig, use_container_width=True, key="overview_sales_trend")

    with chart_right:
        with card():
            section_header("Sales by Product Group", "Contribution to total sales")
            fig = recolor(style_fig(fig_q1(), height=320))
            st.plotly_chart(fig, use_container_width=True, key="overview_product_group")

    # ---------------- TOP CUSTOMERS + SUMMARY ----------------

    first = q1_product_group.iloc[0]
    first_name = CATEGORY_NAMES.get(first["category"], first["category"])
    first_share = first["total"] / total_sales * 100

    if len(q1_product_group) > 1:
        second = q1_product_group.iloc[1]
        second_name = CATEGORY_NAMES.get(second["category"], second["category"])
        ranking_text = (
            f"{first_name} contributed the largest share of sales "
            f"({first_share:.0f}%), followed by {second_name}."
        )
    else:
        ranking_text = (
            f"{first_name} contributed the largest share of sales "
            f"({first_share:.0f}%)."
        )

    bottom_left, bottom_right = st.columns([1.6, 1])

    with bottom_left:
        with card():
            section_header("Top 5 Customers", "Customers generating the highest sales")
            hbar(
                q7_top_customers.head(5),
                x="total",
                y="company_name",
                key="overview_top_customers",
                height=300,
            )

    with bottom_right:
        with card():
            section_header("Business Overview", "Summary of the reporting period")
            st.markdown(
                f"""
                <div class="insight-text" style="font-size:0.95rem;">
                    The business generated
                    <strong style="color:#FFFFFF;">{compact(total_sales)}</strong>
                    in sales across
                    <strong style="color:#FFFFFF;">{transactions:,}</strong>
                    transactions during the reporting period.
                    {ranking_text}
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ---------------- NAVIGATION ----------------

    st.markdown("<br>", unsafe_allow_html=True)

    section_header("Explore Performance", "Choose a page for the detailed analysis")

    c1, c2, c3 = st.columns(3)

    with c1:
        nav_card(
            "Products",
            "Product performance and category contribution.",
            "Explore products",
            "Products",
        )

    with c2:
        nav_card(
            "Customers",
            "Customer behavior and top customers.",
            "Explore customers",
            "Customers",
        )

    with c3:
        nav_card(
            "Sales Team",
            "Salesperson performance and contribution.",
            "Explore team",
            "Sales Team",
        )

    c4, c5, c6 = st.columns(3)

    with c4:
        nav_card(
            "Daily Sales",
            "Daily revenue and sales trends.",
            "Explore daily sales",
            "Daily Sales",
        )

    with c5:
        nav_card(
            "Business Insights",
            "Key findings, opportunities and business observations.",
            "View insights",
            "Business Insights",
        )

    with c6:
        with card():
            section_header("Data Period", "What this dashboard covers")
            st.markdown(
                """
                <div class="insight-text">
                    Oct 01 – Oct 16, 2026<br>
                    All amounts include VAT
                </div>
                """,
                unsafe_allow_html=True,
            )


# ============================================================
# PAGE 2 — PRODUCTS
# ============================================================

elif page == "Products":

    st.title("Product Performance")

    st.markdown(
        '<div class="page-subtitle">'
        'Explore product groups, products and sales contribution'
        '</div>',
        unsafe_allow_html=True,
    )

    product_group = st.selectbox(
        "Select product group",
        list(CATEGORY_MAP.keys()),
        key="products_group",
    )

    code = CATEGORY_MAP[product_group]

    if code is None:
        product_df = df.copy()
    else:
        product_df = df[df["category"] == code].copy()

    product_total = product_df["total"].sum()
    product_quantity = product_df["quantity"].sum()
    product_transactions = len(product_df)
    product_average = product_df["total"].mean() if product_transactions else 0

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        kpi_card("TOTAL SALES", money(product_total), "Selected product group", "primary")

    with k2:
        kpi_card("TOTAL QUANTITY", f"{product_quantity:,.0f}", "Units sold", "violet")

    with k3:
        kpi_card("TRANSACTIONS", f"{product_transactions:,}", "Sales transactions", "cyan")

    with k4:
        kpi_card("AVERAGE SALE", money(product_average), "Average transaction value", "gold")

    st.markdown("<br>", unsafe_allow_html=True)

    product_sales = (
        product_df.groupby("item")["total"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    left, right = st.columns([1.2, 1])

    with left:
        with card():
            section_header("Product Performance", "Top 10 products by sales")
            hbar(
                product_sales,
                x="total",
                y="item",
                key="product_performance",
                height=500,
                x_title="Total Sales",
            )

    with right:
        with card():
            section_header("Product Sales Table", "Highest-selling products")
            show_table(product_sales)


# ============================================================
# PAGE 3 — CUSTOMERS
# ============================================================

elif page == "Customers":

    st.title("Customer Performance")

    st.markdown(
        '<div class="page-subtitle">'
        'Explore customer contribution and individual performance'
        '</div>',
        unsafe_allow_html=True,
    )

    customer_group = st.selectbox(
        "Customer category",
        list(CATEGORY_MAP.keys()),
        format_func=lambda name: "All Customers" if name == "All Products" else name,
        key="customer_category_page",
    )

    code = CATEGORY_MAP[customer_group]

    if code is None:
        customer_df = df.copy()
        label = "All Customers"
    else:
        customer_df = df[df["category"] == code].copy()
        label = customer_group

    customer_total = customer_df["total"].sum()
    customer_transactions = len(customer_df)
    customer_average = customer_df["total"].mean() if customer_transactions else 0
    customer_share = customer_total / total_sales * 100 if total_sales else 0

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        kpi_card("CUSTOMER SALES", money(customer_total), "Total sales", "primary")

    with k2:
        kpi_card("TRANSACTIONS", f"{customer_transactions:,}", "Number of transactions", "violet")

    with k3:
        kpi_card("AVERAGE SALE", money(customer_average), "Average transaction", "cyan")

    with k4:
        kpi_card("SALES SHARE", f"{customer_share:.2f}%", "Share of total sales", "gold")

    st.markdown("<br>", unsafe_allow_html=True)

    top_customers = CUSTOMER_TABLES[code].copy()

    left, right = st.columns(2)

    with left:
        with card():
            if code is None:
                section_header("Top 10 Customers", "Customers ranked by total sales")
            else:
                section_header(
                    f"Top 10 {label} Customers",
                    f"Customers ranked by {label} sales",
                )

            hbar(
                top_customers,
                x="total",
                y="company_name",
                key="customer_top10",
                height=500,
            )

    with right:
        with card():
            if code is None:
                section_header("Customer Table", "Top customers by total sales")
            else:
                section_header(
                    f"{label} Customer Table",
                    f"Top customers by {label} sales",
                )

            show_table(top_customers)


# ============================================================
# PAGE 4 — SALES TEAM
# ============================================================

elif page == "Sales Team":

    st.title("Sales Team Performance")

    st.markdown(
        '<div class="page-subtitle">'
        'Explore salesperson performance and product group contribution'
        '</div>',
        unsafe_allow_html=True,
    )

    product_group = st.selectbox(
        "Select product group",
        list(CATEGORY_MAP.keys()),
        key="sales_team_product_group",
    )

    code = CATEGORY_MAP[product_group]

    if code is None:
        salesperson_df = df.copy()
    else:
        salesperson_df = df[df["category"] == code].copy()

    selected_salesperson = st.selectbox(
        "Select salesperson",
        [
            "All Salespeople",
            *sorted(salesperson_df["sales_person"].dropna().unique()),
        ],
        key="sales_team_salesperson",
    )

    if selected_salesperson != "All Salespeople":
        salesperson_df = salesperson_df[
            salesperson_df["sales_person"] == selected_salesperson
        ].copy()

    if salesperson_df.empty:

        st.info("No data for this selection.")

    else:

        salesperson_summary = (
            salesperson_df
            .groupby("sales_person")["total"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
        )

        salesperson_summary["share_pct"] = (
            salesperson_summary["total"]
            / salesperson_summary["total"].sum()
            * 100
        ).round(2)

        salesperson_total = salesperson_df["total"].sum()
        salesperson_transactions = len(salesperson_df)
        salesperson_average = salesperson_df["total"].mean()
        salesperson_share = (
            salesperson_total / total_sales * 100 if total_sales else 0
        )

        k1, k2, k3, k4 = st.columns(4)

        with k1:
            kpi_card("TOTAL SALES", money(salesperson_total), "Sales generated", "primary")

        with k2:
            kpi_card("TRANSACTIONS", f"{salesperson_transactions:,}", "Transactions handled", "violet")

        with k3:
            kpi_card("AVERAGE SALE", money(salesperson_average), "Average transaction", "cyan")

        with k4:
            kpi_card("SALES SHARE", f"{salesperson_share:.2f}%", "Share of total sales", "gold")

        st.markdown("<br>", unsafe_allow_html=True)

        if selected_salesperson == "All Salespeople":

            left, right = st.columns(2)

            with left:
                with card():
                    section_header(
                        "Salesperson Performance",
                        "Total sales generated by each salesperson",
                    )
                    hbar(
                        salesperson_summary,
                        x="total",
                        y="sales_person",
                        key="salesperson_performance",
                        height=500,
                    )

            with right:
                with card():
                    section_header("Salesperson Table", "Sales performance ranking")
                    show_table(salesperson_summary)

        else:

            salesperson_groups = (
                salesperson_df.groupby("category")["total"]
                .sum()
                .sort_values(ascending=False)
                .reset_index()
            )

            left, right = st.columns([1.2, 1])

            with left:
                with card():
                    section_header(
                        f"{selected_salesperson} - Product Groups",
                        "Sales contribution by product group",
                    )
                    hbar(
                        salesperson_groups,
                        x="total",
                        y="category",
                        key="selected_salesperson_groups",
                        height=400,
                    )

            with right:
                with card():
                    section_header(
                        f"{selected_salesperson} - Product Groups",
                        "Sales breakdown",
                    )
                    show_table(salesperson_groups)


# ============================================================
# PAGE 5 — DAILY SALES
# ============================================================

elif page == "Daily Sales":

    st.title("Daily Sales")

    st.markdown(
        '<div class="page-subtitle">'
        'Select a date to see exactly what was sold that day'
        '</div>',
        unsafe_allow_html=True,
    )

    first_day = q16_daily_summary["date"].min().date()
    last_day = q16_daily_summary["date"].max().date()

    selected_day = st.date_input(
        "Select date",
        value=last_day,
        min_value=first_day,
        max_value=last_day,
        key="daily_sales_date",
    )

    day_df = get_day_data(selected_day)

    day_total = day_df["total"].sum()
    day_transactions = len(day_df)
    day_average = day_df["total"].mean() if day_transactions else 0
    avg_daily_sales = q16_daily_summary["total"].mean()

    if avg_daily_sales:
        vs_average = (day_total - avg_daily_sales) / avg_daily_sales * 100
    else:
        vs_average = 0

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        kpi_card(
            "SALES ON THIS DAY",
            money(day_total),
            selected_day.strftime("%A, %b %d, %Y"),
            "primary",
        )

    with k2:
        kpi_card("TRANSACTIONS", f"{day_transactions:,}", "Sales recorded this day", "violet")

    with k3:
        kpi_card("AVERAGE SALE", money(day_average), "Average value per transaction", "cyan")

    with k4:
        kpi_card(
            "VS DAILY AVERAGE",
            f"{vs_average:+.1f}%",
            f"Average day: {money(avg_daily_sales)}",
            "gold",
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------- DAILY TREND ----------------

    with card():

        section_header("Daily Sales Trend", "The selected day is highlighted")

        bar_colors = [
            "#34D399" if d.date() == selected_day else "#4F6EF7"
            for d in q16_daily_summary["date"]
        ]

        fig = px.bar(q16_daily_summary, x="date", y="total")
        fig.update_traces(marker_color=bar_colors)
        style_fig(fig, height=350)
        fig.update_layout(xaxis_title=None, yaxis_title="Sales")

        st.plotly_chart(fig, use_container_width=True, key="daily_trend")

    # ---------------- DETAILS FOR THE SELECTED DAY ----------------

    if day_df.empty:

        st.info("No sales were recorded on this day.")

    else:

        def day_bar(data, y_col, key, color="#4F6EF7"):

            chart_data = (
                data.groupby(y_col)["total"]
                .sum()
                .sort_values(ascending=False)
                .head(10)
                .reset_index()
            )

            hbar(chart_data, x="total", y=y_col, key=key, color=color, height=380)

        left, right = st.columns(2)

        with left:
            with card():
                section_header("Top Products", "Best-selling products on this day")
                day_bar(day_df, "item", "day_products")

        with right:
            with card():
                section_header("Top Customers", "Customers who bought most on this day")
                day_bar(day_df, "company_name", "day_customers", "#8B5CF6")

        left, right = st.columns(2)

        with left:
            with card():
                section_header("By Product Group", "UPS, WF and EM on this day")
                day_bar(day_df, "category", "day_category", "#22D3EE")

        with right:
            with card():
                section_header("By Salesperson", "Who sold on this day")
                day_bar(day_df, "sales_person", "day_salespeople", "#34D399")

        with card():

            section_header(
                "All Transactions",
                f"Every sale recorded on {selected_day.strftime('%b %d, %Y')}",
            )

            st.dataframe(
                day_df,
                use_container_width=True,
                height=400,
                hide_index=True,
            )

            st.download_button(
                "Download this day's sales (CSV)",
                day_df.to_csv(index=False),
                file_name=f"sales_{selected_day}.csv",
                mime="text/csv",
            )

    # ---------------- DAY-BY-DAY TABLE ----------------

    with card():

        section_header("Day-by-Day Summary", "Sales for every day in the period")

        show_table(
            q16_daily_summary[
                ["date", "total", "transactions", "quantity", "average_sale"]
            ]
        )


# ============================================================
# PAGE 6 — BUSINESS INSIGHTS
# ============================================================

elif page == "Business Insights":

    st.title("Business Insights")

    st.markdown(
        '<div class="page-subtitle">'
        'Key findings and opportunities from the sales data'
        '</div>',
        unsafe_allow_html=True,
    )

    # Product opportunity: the item with the most units, compared
    # with how much of the sales value it brings in.
    by_item = df.groupby("item")[["quantity", "total"]].sum()
    top_qty_item = by_item["quantity"].idxmax()
    qty_share = by_item.loc[top_qty_item, "quantity"] / by_item["quantity"].sum() * 100
    value_share = by_item.loc[top_qty_item, "total"] / by_item["total"].sum() * 100

    top_group_name = CATEGORY_NAMES.get(top_product_group, top_product_group)

    a, b, c, d = st.columns(4)

    with a:
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-icon">🏆</div>
                <div class="insight-title">Best Product Group</div>
                <div class="insight-text">
                    <strong style="color:#FFFFFF;">{top_group_name}</strong>
                    <br><br>
                    Sales: {money(top_product_group_sales)}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with b:
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-icon">👥</div>
                <div class="insight-title">Customer Concentration</div>
                <div class="insight-text">
                    Top 10 customers represent
                    <strong style="color:#FFFFFF;">{top10_share:.1f}%</strong>
                    of total sales.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c:
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-icon">📦</div>
                <div class="insight-title">Volume Leader</div>
                <div class="insight-text">
                    <strong style="color:#FFFFFF;">{top_qty_item}</strong>
                    sold the most units ({qty_share:.1f}% of all units)
                    and brought in {value_share:.1f}% of sales value.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with d:
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-icon">👤</div>
                <div class="insight-title">Top Salesperson</div>
                <div class="insight-text">
                    <strong style="color:#FFFFFF;">{top_salesperson}</strong>
                    <br><br>
                    Sales: {money(top_salesperson_sales)}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns([1, 1.4])

    with left:
        with card():

            section_header("Sales Performance Summary", "Core business metrics")

            summary = pd.DataFrame(
                {
                    "Metric": [
                        "Total Sales",
                        "Transactions",
                        "Average Sale",
                        "Top 10 Customer Share",
                        "Top Product Group",
                        "Top Salesperson",
                    ],
                    "Value": [
                        money(total_sales),
                        f"{transactions:,}",
                        money(average_sale),
                        f"{top10_share:.1f}%",
                        top_group_name,
                        top_salesperson,
                    ],
                }
            )

            st.dataframe(summary, use_container_width=True, hide_index=True)

    with right:
        with card():

            section_header(
                "Category Performance",
                "How sales are distributed between product groups",
            )

            fig = style_fig(fig_q1(), height=400)

            st.plotly_chart(
                fig,
                use_container_width=True,
                key="insights_category",
            )

    with card():

        section_header("Sales Trend", "Daily and cumulative sales performance")

        fig = style_fig(fig_q15(), height=450)

        st.plotly_chart(
            fig,
            use_container_width=True,
            key="insights_sales_trend",
        )

    with card():

        section_header(
            "Explore Full Dataset",
            "The complete sales data behind the analysis",
        )

        show_full_data = st.checkbox(
            "Show full dataset",
            key="insights_full_data",
        )

        if show_full_data:
            st.dataframe(
                df,
                use_container_width=True,
                height=550,
                hide_index=True,
            )

        st.download_button(
            "Download Full Dataset CSV",
            df.to_csv(index=False),
            file_name="sales_data_oct_01_16_2026.csv",
            mime="text/csv",
        )
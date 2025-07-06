## Lets import all the necessary libraries for our Streamlit app
# Core
import pandas as pd
import numpy as np
import datetime

# Visualization
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns  

# Dashboard: Streamlit
import streamlit as st

# Utility
from io import BytesIO  # for downloads
import base64  # for embedding CSS/icons
import locale  # for formatting currency

# Styling / HTML
import streamlit.components.v1 as components
from generate_report import generate_pdf_report, save_chart_image
from generate_report import generate_alerts
import os
import smtplib
from email.message import EmailMessage
import re
## Lets Set Page Layout + Load Data
# Setting wide layout for dashboard
st.set_page_config(page_title="Superstore BI Dashboard", layout="wide")

# App Title & Subtitle
st.markdown("<h1 style='text-align: center; color: #2c3e50;'>Superstore Sales Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7f8c8d;'>Interactive Business Intelligence Dashboard built with Streamlit</p>", unsafe_allow_html=True)
st.markdown("---")

st.caption("Last updated: July 6, 2025")
@st.cache_data
def load_data():
    df = pd.read_csv("Batch2/Task5/cleaned_global_superstore.csv", sep=",")
    df.columns = df.columns.str.strip()
    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=False, errors="coerce")
    return df

df = load_data()
## Lets add Sidebar Filters

# Sidebar title
st.sidebar.title("Filter Data")

# Region (independent)
regions = df["Region"].unique()
selected_region = st.sidebar.multiselect("Select Region", regions)

# Category (parent)
categories = df["Category"].unique()
selected_category = st.sidebar.multiselect("Select Category", categories)

# Sub-Category (depends on selected Category)
if selected_category:
    available_subcats = df[df["Category"].isin(selected_category)]["Sub-Category"].unique()
else:
    available_subcats = df["Sub-Category"].unique()

selected_subcat = st.sidebar.multiselect("Select Sub-Category", available_subcats)

# Date Range
# Get min and max date from full data
min_date = df["Order Date"].min()
max_date = df["Order Date"].max()
# Date range selector
date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    # fallback to full range if only one date or invalid input
    start_date, end_date = min_date, max_date

st.sidebar.markdown("### Trend Chart Options")

trend_mode = st.sidebar.radio("Chart Type", ["Single Axis", "Dual Axis"])
show_margin = st.sidebar.checkbox("Show Profit Margin %", value=True)
## Lets Apply Filters to DataFrame
# Filter data based on sidebar inputs
filtered_df = df.copy()

if selected_region:
    filtered_df = filtered_df[filtered_df["Region"].isin(selected_region)]

if selected_category:
    filtered_df = filtered_df[filtered_df["Category"].isin(selected_category)]

if selected_subcat:
    filtered_df = filtered_df[filtered_df["Sub-Category"].isin(selected_subcat)]

filtered_df = filtered_df[
    (filtered_df["Order Date"] >= pd.to_datetime(start_date)) &
    (filtered_df["Order Date"] <= pd.to_datetime(end_date))
]
## Lets add KPI Cards (with Light CSS)
# --- KPI Section ---
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df.shape[0]
unique_customers = filtered_df["Customer ID"].nunique()

# Custom CSS (lightweight)
st.markdown("""
<style>
.kpi-card {
    padding: 20px;
    background-color: #F7F7F7;
    border-radius: 12px;
    margin-bottom: 10px;
    box-shadow: 1px 1px 5px rgba(0,0,0,0.05);
    text-align: center;
}
.kpi-title {
    font-size: 16px;
    color: #666;
}
.kpi-value {
    font-size: 26px;
    font-weight: bold;
    color: #2B547E;
}
</style>
""", unsafe_allow_html=True)

st.markdown("### Key Performance Indicators")

# Show KPIs in 4 columns
col1, col2, col3, col4 = st.columns(4)

col1.markdown(f"<div class='kpi-card'><div class='kpi-title'>Total Sales</div><div class='kpi-value'>${total_sales:,.0f}</div></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='kpi-card'><div class='kpi-title'>Total Profit</div><div class='kpi-value'>${total_profit:,.0f}</div></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='kpi-card'><div class='kpi-title'>Total Orders</div><div class='kpi-value'>{total_orders:,}</div></div>", unsafe_allow_html=True)
col4.markdown(f"<div class='kpi-card'><div class='kpi-title'>Unique Customers</div><div class='kpi-value'>{unique_customers:,}</div></div>", unsafe_allow_html=True)



## Lets add Auto-Generated Insights Panel
# -------------------------------
# Auto-Generated Insights Panel
# -------------------------------

st.markdown("### Business Insights")

# Only show if data is not empty
if not filtered_df.empty:
    # Best sales month
    monthly_sales = (
        filtered_df.groupby(filtered_df["Order Date"].dt.to_period("M"))["Sales"]
        .sum()
        .reset_index()
    )
    best_month = str(monthly_sales.loc[monthly_sales["Sales"].idxmax(), "Order Date"])

    # Worst profit month
    monthly_profit = (
        filtered_df.groupby(filtered_df["Order Date"].dt.to_period("M"))["Profit"]
        .sum()
        .reset_index()
    )
    worst_profit_month = str(monthly_profit.loc[monthly_profit["Profit"].idxmin(), "Order Date"])

    # Top Sub-Category by Sales
    top_subcat = (
        filtered_df.groupby("Sub-Category")["Sales"]
        .sum()
        .idxmax()
    )

    # Average revenue per order
    avg_rev_per_order = filtered_df["Sales"].sum() / len(filtered_df)

    # Sub-Categories with Net Loss
    loss_subcats = (
        filtered_df.groupby("Sub-Category")["Profit"]
        .sum()
        .reset_index()
    )
    loss_subcats = loss_subcats[loss_subcats["Profit"] < 0]["Sub-Category"].tolist()

    # Display insights
    st.markdown(f"""
    - **Highest Sales Month:** {best_month}
    - **Lowest Profit Month:** {worst_profit_month}
    - **Top Performing Sub-Category:** {top_subcat}
    - **Avg. Revenue per Order:** ${avg_rev_per_order:,.2f}
    - **Sub-Categories in Loss:** {", ".join(loss_subcats) if loss_subcats else "None"}
    """)
else:
    st.warning("No data available with current filters to generate insights.")

## Lets add Business Insight Alerts
# -------------------------------
# Business Alerts & Anomaly Detection (BI-style)
# -------------------------------

st.markdown("### Business Alerts")

# Ensure Month-Year column exists
filtered_df["Month_Year"] = filtered_df["Order Date"].dt.to_period("M").astype(str)

# Monthly Aggregation
monthly_data = (
    filtered_df.groupby("Month_Year")[["Sales", "Profit"]]
    .sum()
    .reset_index()
    .sort_values("Month_Year")
)

# 1. Detect Loss Months (Profit < 0)
loss_months = monthly_data[monthly_data["Profit"] < 0]

if not loss_months.empty:
    for _, row in loss_months.iterrows():
        st.error(f"Loss recorded in **{row['Month_Year']}** -> Profit: ${row['Profit']:,.0f}")

# 2. Detect Sharp Profit Declines
monthly_data["Profit_Change"] = monthly_data["Profit"].diff()

sharp_drops = monthly_data[monthly_data["Profit_Change"] < -5000]  # Adjust threshold as needed

for _, row in sharp_drops.iterrows():
    st.warning(f"Sharp profit decline in **{row['Month_Year']}** -> Drop: ${abs(row['Profit_Change']):,.0f}")

# 3. Detect Sales Outlier (using IQR method)
q1 = monthly_data["Sales"].quantile(0.25)
q3 = monthly_data["Sales"].quantile(0.75)
iqr = q3 - q1
upper_bound = q3 + 1.5 * iqr
lower_bound = q1 - 1.5 * iqr

outliers = monthly_data[(monthly_data["Sales"] > upper_bound) | (monthly_data["Sales"] < lower_bound)]

for _, row in outliers.iterrows():
    st.info(f"Unusual sales in **{row['Month_Year']}** -> Sales: ${row['Sales']:,.0f}")

# 4. Positive Streak Detection
if (monthly_data["Profit"] > 0).all():
    st.success("No negative profit months detected in selected period.")

# -------------------------------
# Best Performing Segment Insight
# -------------------------------

segment_perf = (
    filtered_df.groupby("Segment")[["Sales", "Profit"]]
    .sum()
    .reset_index()
    .sort_values("Sales", ascending=False)
)
best_segment = segment_perf.sort_values("Sales", ascending=False).iloc[0]

st.markdown(f"""
### Best Performing Segment
- **Segment:** {best_segment['Segment']}
- **Sales:** ${best_segment['Sales']:,.0f}
- **Profit:** ${best_segment['Profit']:,.0f}
""")

# -------------------------------
# Customer/Product Lookup Tool
# -------------------------------

st.sidebar.markdown("### Lookup")

# Unique names
all_customers = sorted(filtered_df["Customer Name"].dropna().unique())
all_products = sorted(filtered_df["Sub-Category"].dropna().unique()) 

# Add dropdowns (empty by default)
selected_customer = st.sidebar.selectbox("Select Customer", [""] + all_customers)
selected_product = st.sidebar.selectbox("Select Product", [""] + all_products)

# Initialize filter flag
filtered_result = False

# Filter based on input
lookup_df = filtered_df.copy()

if selected_customer:
    lookup_df = lookup_df[lookup_df["Customer Name"] == selected_customer]
    filtered_result = True

if selected_product:
    lookup_df = lookup_df[lookup_df["Sub-Category"] == selected_product]
    filtered_result = True

# Display results only if something selected
if filtered_result and not lookup_df.empty:
    st.markdown("#### Lookup Results")

    # Sales summary
    total_sales = lookup_df["Sales"].sum()
    total_profit = lookup_df["Profit"].sum()
    order_count = len(lookup_df)
    top_region = lookup_df["Region"].mode().values[0] if "Region" in lookup_df.columns else "N/A"

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Sales", f"${total_sales:,.0f}")
    col2.metric("Total Profit", f"${total_profit:,.0f}")
    col3.metric("Orders Found", f"{order_count}")
    col4.metric("Top Region", top_region)

    # Show detailed table
    st.markdown("#### Matching Transactions")
    st.dataframe(lookup_df[["Order Date", "Customer Name", "Sub-Category", "Sales", "Profit", "Region", "City"]].sort_values("Order Date"))

elif filtered_result and lookup_df.empty:
    st.warning("No matching transactions found for selected customer/product.")

# -------------------------------
# CSV Download for Lookup Result
# -------------------------------

@st.cache_data
def convert_lookup_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8-sig')

csv_lookup = convert_lookup_df_to_csv(
    lookup_df[["Order Date", "Customer Name", "Sub-Category", "Sales", "Profit", "Region", "City"]]
)
st.sidebar.download_button(
    label="⬇️ Download Transactions CSV",
    data=csv_lookup,
    file_name="lookup_transactions.csv",
    mime='text/csv',
    use_container_width=False
)
## lets plot Top 5 Customers by Sales — Plotly Bar Chart
# -----------------------
# Top 5 Customers by Sales
# -----------------------

st.markdown("### Top 5 Customers by Sales")

# Group and sort data
top_customers = (
    filtered_df.groupby("Customer Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

# Plotly Bar Chart
fig_top_customers = px.bar(
    top_customers,
    x="Customer Name",
    y="Sales",
    text="Sales",
    color="Sales",
    color_continuous_scale="Blues",
    title="Top 5 Customers by Total Sales",
)

fig_top_customers.update_traces(texttemplate='%{text:.2s}', textposition='auto')
fig_top_customers.update_layout(
    xaxis_title="Customer",
    yaxis_title="Total Sales",
    coloraxis_showscale=False,
    template="plotly_white",
    height=400
)

# Show chart
st.plotly_chart(fig_top_customers, use_container_width=True)

# -------------------------------
# Segment-Level KPIs
# -------------------------------

st.markdown("### Segment-Level KPIs")

col1, col2, col3 = st.columns(3)

for i, seg in enumerate(segment_perf["Segment"]):
    seg_sales = segment_perf.loc[segment_perf["Segment"] == seg, "Sales"].values[0]
    seg_profit = segment_perf.loc[segment_perf["Segment"] == seg, "Profit"].values[0]

    col = [col1, col2, col3][i]
    col.metric(label=f"{seg} - Sales", value=f"${seg_sales:,.0f}")
    col.metric(label=f"{seg} - Profit", value=f"${seg_profit:,.0f}")

# -------------------------------
# Monthly Sales Trend Chart (Toggle: Single vs Dual Axis)
# -------------------------------

st.markdown("### Monthly Sales Trend Analysis")

# Ensure Month-Year column
filtered_df["Month_Year"] = filtered_df["Order Date"].dt.to_period("M").astype(str)

# Group by Month-Year
trend_data = (
    filtered_df.groupby("Month_Year")[["Sales", "Profit"]]
    .sum()
    .reset_index()
    .sort_values("Month_Year")
)

# Profit Margin %
trend_data["Margin %"] = (trend_data["Profit"] / trend_data["Sales"]) * 100

# --------- SINGLE AXIS ---------
if trend_mode == "Single Axis":
    fig_trend = go.Figure()

    # Sales
    fig_trend.add_trace(go.Scatter(
        x=trend_data["Month_Year"],
        y=trend_data["Sales"],
        name="Sales",
        mode="lines+markers",
        line=dict(color="#1f77b4", width=3)
    ))

    # Profit
    fig_trend.add_trace(go.Scatter(
        x=trend_data["Month_Year"],
        y=trend_data["Profit"],
        name="Profit",
        mode="lines+markers",
        line=dict(color="#2ca02c", width=3, dash="dot")
    ))

    # Margin %
    if show_margin:
        fig_trend.add_trace(go.Scatter(
            x=trend_data["Month_Year"],
            y=trend_data["Margin %"],
            name="Margin %",
            mode="lines+markers",
            line=dict(color="#ff7f0e", width=2, dash="dash"),
            yaxis="y2"
        ))

        # Add second y-axis for margin %
        fig_trend.update_layout(
            yaxis2=dict(
                title="Profit Margin (%)",
                overlaying="y",
                side="right",
                showgrid=False
            )
        )

    fig_trend.update_layout(
        xaxis_title="Month-Year",
        yaxis_title="Amount ($)",
        hovermode="x unified",
        legend_title="Metric",
        template="plotly_white",
        height=450
    )

    st.plotly_chart(fig_trend, use_container_width=True)

    # For PDF
    trend_chart_for_pdf = fig_trend

# --------- DUAL AXIS ---------
else:
    fig_dual = go.Figure()

    # Sales (Left)
    fig_dual.add_trace(go.Scatter(
        x=trend_data["Month_Year"],
        y=trend_data["Sales"],
        name="Sales",
        mode="lines+markers",
        line=dict(color="#1f77b4", width=3),
        yaxis="y1"
    ))

    # Profit (Right)
    fig_dual.add_trace(go.Scatter(
        x=trend_data["Month_Year"],
        y=trend_data["Profit"],
        name="Profit",
        mode="lines+markers",
        line=dict(color="#2ca02c", width=3, dash="dot"),
        yaxis="y2"
    ))

    # Optional: Profit Margin (Right Axis as %)
    if show_margin:
        fig_dual.add_trace(go.Scatter(
            x=trend_data["Month_Year"],
            y=trend_data["Margin %"],
            name="Margin %",
            mode="lines+markers",
            line=dict(color="#ff7f0e", width=2, dash="dash"),
            yaxis="y2"
        ))

    fig_dual.update_layout(
        xaxis=dict(title="Month-Year"),
        yaxis=dict(
            title=dict(text="Sales ($)", font=dict(color="#1f77b4")),
            tickfont=dict(color="#1f77b4")
        ),
        yaxis2=dict(
            title=dict(text="Profit / Margin", font=dict(color="#2ca02c")),
            tickfont=dict(color="#2ca02c"),
            overlaying="y",
            side="right"
        ),
        legend_title="Metric",
        hovermode="x unified",
        template="plotly_white",
        height=450,
        margin=dict(t=40, b=40, l=40, r=40)
    )

    st.plotly_chart(fig_dual, use_container_width=True)

    # For PDF
    trend_chart_for_pdf = fig_dual

# -------------------------------
# Segment-wise Sales and Profit Comparison
# -------------------------------

st.markdown("### Segment-Wise Sales & Profit Breakdown")

# Aggregate by segment
segment_perf = (
    filtered_df.groupby("Segment")[["Sales", "Profit"]]
    .sum()
    .reset_index()
    .sort_values("Sales", ascending=False)
)

# Bar chart (grouped)
fig_segment_bar = px.bar(
    segment_perf.melt(id_vars="Segment", value_vars=["Sales", "Profit"]),
    x="Segment",
    y="value",
    color="variable",
    barmode="group",
    text_auto='.2s',
    color_discrete_map={"Sales": "#1f77b4", "Profit": "#2ca02c"},
    title="Sales & Profit by Segment"
)

fig_segment_bar.update_layout(
    xaxis_title="Segment",
    yaxis_title="Amount ($)",
    legend_title="Metric",
    template="plotly_white",
    height=400
)

st.plotly_chart(fig_segment_bar, use_container_width=True)


# -------------------------------
# Dynamic Pie Chart: Clean for Sub-Category
# -------------------------------

st.markdown("### Sales Share Breakdown")

# Dimension Toggle
pie_dim = st.radio("Group Sales By:", ["Category", "Sub-Category"], horizontal=True)

if pie_dim == "Category":
    # Simple pie by Category
    pie_data = (
        filtered_df.groupby("Category")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Sales", ascending=False)
    )

    fig_pie = px.pie(
        pie_data,
        names="Category",
        values="Sales",
        hole=0.4,
        title="Sales Distribution by Category",
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_pie.update_layout(template="plotly_white", height=400)
    st.plotly_chart(fig_pie, use_container_width=True)

else:
    st.markdown("#### Sub-Category Breakdown by Each Category")
    categories = filtered_df["Category"].unique()
    fig_subcat_list = []
    # Layout for 3 pie charts side-by-side
    col1, col2, col3 = st.columns(3)

    for cat, col in zip(categories, [col1, col2, col3]):
        cat_df = filtered_df[filtered_df["Category"] == cat]

        subcat_sales = (
            cat_df.groupby("Sub-Category")["Sales"]
            .sum()
            .reset_index()
            .sort_values("Sales", ascending=False)
        )

        fig_subcat = px.pie(
            subcat_sales,
            names="Sub-Category",
            values="Sales",
            hole=0.4,
            title=cat,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_subcat_list.append(fig_subcat) 
        fig_subcat.update_traces(textposition='inside', textinfo='percent+label')
        fig_subcat.update_layout(template="plotly_white", height=400, margin=dict(t=40, b=40, l=10, r=10))
        
        col.plotly_chart(fig_subcat, use_container_width=True)

## Lets add a Beautiful CSV Download Button
# -------------------------------
# Download Filtered Data as CSV
# -------------------------------

@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8-sig')

# ------------------------------------------
# Generate and Return PDF Report to App
# ------------------------------------------
@st.cache_data
def generate_and_return_pdf():
    # Prepare KPI dictionary
    kpis = {
        "Total Sales": f"${total_sales:,.0f}",
        "Total Profit": f"${total_profit:,.0f}",
        "Total Orders": f"{total_orders:,}",
        "Unique Customers": f"{unique_customers:,}"
    }

    # Prepare Insight List
    insights = [
        f"Highest Sales Month: {best_month}",
        f"Lowest Profit Month: {worst_profit_month}",
        f"Top Performing Sub-Category: {top_subcat}",
        f"Avg. Revenue per Order: ${avg_rev_per_order:,.2f}",
        f"Sub-Categories in Loss: {', '.join(loss_subcats) if loss_subcats else 'None'}"
    ]

    alerts = generate_alerts(filtered_df)
    # Output path
    output_file = "superstore_report.pdf"

    # Generate PDF
    generate_pdf_report(filtered_df, kpis, insights, output_file, alerts=alerts)

    # Read PDF as bytes for download
    with open(output_file, "rb") as f:
        pdf_bytes = f.read()

    return pdf_bytes

st.sidebar.markdown("### Download Options")

# CSV Download
csv = convert_df_to_csv(filtered_df)
st.sidebar.markdown("### Download Filtered Data")
st.sidebar.download_button(
    label="⬇️ Download CSV",
    data=csv,
    file_name="filtered_superstore_data.csv",
    mime='text/csv'
)

# PDF Report Button
if st.sidebar.button("Generate PDF Report"):
    with st.spinner("Generating report..."):
        pdf_data = generate_and_return_pdf()

    st.sidebar.download_button(
        label="📥 Download PDF",
        data=pdf_data,
        file_name="superstore_report.pdf",
        mime="application/pdf"
    )


st.sidebar.markdown("### Email Report")

user_email = st.sidebar.text_input("Recipient Email")
# From st.secrets
sender_email = st.secrets["email"]["sender"]
sender_pass = st.secrets["email"]["password"]
if st.sidebar.button("📤 Send PDF to Email"):
    if not user_email or not re.match(r"[^@]+@[^@]+\.[^@]+", user_email):
        st.sidebar.error("Please enter a valid email address.")
    else:
        try:
            # Load PDF
            with open("superstore_report.pdf", "rb") as f:
                file_data = f.read()

            # Compose email
            msg = EmailMessage()
            msg['Subject'] = 'Superstore Dashboard Report'
            msg['From'] = "sender_email"
            msg['To'] = user_email
            msg.set_content("Hello,\n\nPlease find attached the Superstore dashboard report.\n\nBest regards,\nBI Dashboard")

            msg.add_attachment(file_data, maintype='application', subtype='pdf', filename="superstore_report.pdf")

            # SMTP send
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login("sender_email", "sender_pass")
                smtp.send_message(msg)

            st.sidebar.success(f"Report sent to {user_email}")

        except Exception as e:
            st.sidebar.error(f"Failed to send email: {e}")

st.markdown("""
<style>
.footer-box {
    background-color: #f0f2f6;
    border-top: 1px solid #d3d3d3;
    padding: 15px 0 10px;
    margin-top: 40px;
    text-align: center;
    font-size: 14px;
    color: #333333;
}
.footer-box a {
    color: #1a73e8;
    text-decoration: none;
    margin: 0 8px;
    font-weight: 500;
}
.footer-box a:hover {
    text-decoration: underline;
}
</style>

<div class='footer-box'>
    Developed & maintained by <strong>Zeeshan Akram</strong> —
    <a href='https://github.com/zeeshan-akram-ds' target='_blank'>GitHub</a> |
    <a href='https://www.linkedin.com/in/zeeshan-akram-572bbb34a/' target='_blank'>LinkedIn</a>
</div>
""", unsafe_allow_html=True)

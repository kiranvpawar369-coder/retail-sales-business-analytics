
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from io import BytesIO

st.set_page_config(
    page_title="Retail Analytics Pro",
    page_icon="📊",
    layout="wide"
)

DATA_PATH = Path(__file__).parent / "Dataset" / "superstore_cleaned.csv"

st.title("📊 Retail Analytics Pro")
st.caption("Retail Sales & Business Performance Analytics")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    return df

if "run_analysis" not in st.session_state:
    st.session_state.run_analysis = False

if st.sidebar.button("🚀 Run Analysis"):
    st.session_state.run_analysis = True

if st.sidebar.button("🔄 Reset Analysis"):
    st.session_state.run_analysis = False

if not st.session_state.run_analysis:
    st.info("Click 'Run Analysis' in the sidebar to load your retail data.")
    st.stop()

try:
    df = load_data()
except Exception as e:
    st.error(f"Unable to load dataset: {e}")
    st.stop()

st.sidebar.header("Dashboard Filters")

categories = st.sidebar.multiselect(
    "Select Category",
    sorted(df["Category"].dropna().unique()),
    default=sorted(df["Category"].dropna().unique())
)

regions = st.sidebar.multiselect(
    "Select Region",
    sorted(df["Region"].dropna().unique()),
    default=sorted(df["Region"].dropna().unique())
)

min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()

date_range = st.sidebar.date_input(
    "Select Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

filtered = df[
    df["Category"].isin(categories) &
    df["Region"].isin(regions)
].copy()

if len(date_range) == 2:
    start_date, end_date = date_range
    filtered = filtered[
        filtered["Order Date"].dt.date.between(start_date, end_date)
    ]

if filtered.empty:
    st.warning("No records found for the selected filters.")
    st.stop()

total_sales = filtered["Sales"].sum()
total_profit = filtered["Profit"].sum()
total_orders = filtered["Order ID"].nunique()
total_quantity = filtered["Quantity"].sum()
profit_margin = (total_profit / total_sales * 100) if total_sales else 0

st.subheader("Business Performance")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Total Sales", f"${total_sales:,.2f}")
c2.metric("Total Profit", f"${total_profit:,.2f}")
c3.metric("Total Orders", f"{total_orders:,}")
c4.metric("Total Quantity", f"{total_quantity:,}")
c5.metric("Profit Margin", f"{profit_margin:.2f}%")

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Sales by Category")
    category_data = filtered.groupby("Category", as_index=False)["Sales"].sum()
    fig = px.bar(
        category_data,
        x="Category",
        y="Sales",
        color="Category",
        title="Category-wise Sales"
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Sales by Region")
    region_data = filtered.groupby("Region", as_index=False)["Sales"].sum()
    fig = px.bar(
        region_data,
        x="Region",
        y="Sales",
        color="Region",
        title="Regional Sales Performance"
    )
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)

with left:
    st.subheader("Monthly Sales Trend")
    monthly = (
        filtered.set_index("Order Date")
        .resample("MS")["Sales"]
        .sum()
        .reset_index()
    )
    fig = px.line(
        monthly,
        x="Order Date",
        y="Sales",
        markers=True,
        title="Monthly Sales"
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Profit by Sub-Category")
    subcategory = (
        filtered.groupby("Sub-Category", as_index=False)["Profit"]
        .sum()
        .sort_values("Profit", ascending=False)
    )
    fig = px.bar(
        subcategory,
        x="Profit",
        y="Sub-Category",
        orientation="h",
        title="Sub-Category Profitability"
    )
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Detailed Sales Data")
st.dataframe(filtered, use_container_width=True)

csv_data = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇️ Download Filtered Data (CSV)",
    data=csv_data,
    file_name="retail_sales_analysis.csv",
    mime="text/csv"
)

excel_buffer = BytesIO()
with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
    filtered.to_excel(writer, index=False, sheet_name="Sales Data")

st.download_button(
    "⬇️ Download Excel Report",
    data=excel_buffer.getvalue(),
    file_name="retail_sales_analysis.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.success("Retail sales analysis completed successfully!")

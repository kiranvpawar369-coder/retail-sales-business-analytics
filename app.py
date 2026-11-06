
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from io import BytesIO

# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Retail Analytics Pro",
    page_icon="📊",
    layout="wide"
)

DATA_PATH = (
    Path(__file__).parent
    / "Dataset"
    / "superstore_cleaned.csv"
)

# =====================================================
# 2. APPLICATION HEADER
# =====================================================

st.title("📊 Retail Analytics Pro")
st.caption("Retail Sales & Business Performance Analytics")

st.markdown(
    "Analyze retail sales, understand business performance, "
    "and generate actionable business insights."
)

# =====================================================
# 3. DATA LOADING
# =====================================================

@st.cache_data
def load_data(file_bytes=None, file_extension="csv"):
    if file_bytes is not None:
        if file_extension == "xlsx":
            df = pd.read_excel(BytesIO(file_bytes))
        else:
            df = pd.read_csv(BytesIO(file_bytes))
    else:
        if not DATA_PATH.exists():
            raise FileNotFoundError(
                f"Default dataset not found: {DATA_PATH}"
            )
        df = pd.read_csv(DATA_PATH)

    required_columns = [
        "Order ID", "Order Date", "Category",
        "Sub-Category", "Region", "Sales",
        "Profit", "Quantity"
    ]

    missing = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            "Missing required columns: " + ", ".join(missing)
        )

    df["Order Date"] = pd.to_datetime(
        df["Order Date"], errors="coerce"
    )

    for col in ["Sales", "Profit", "Quantity"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(
        subset=[
            "Order Date", "Sales", "Profit",
            "Quantity", "Category", "Region"
        ]
    )

    return df


# =====================================================
# 4. CLIENT DATA UPLOAD
# =====================================================

st.sidebar.title("Retail Analytics Pro")

st.sidebar.header("📁 Client Data Upload")

uploaded_file = st.sidebar.file_uploader(
    "Upload your sales dataset",
    type=["csv", "xlsx"],
    help="Upload a CSV or Excel retail sales dataset."
)

if uploaded_file is not None:
    file_bytes = uploaded_file.getvalue()
    extension = uploaded_file.name.split(".")[-1].lower()
    st.sidebar.success(
        f"Uploaded: {uploaded_file.name}"
    )
else:
    file_bytes = None
    extension = "csv"
    st.sidebar.info(
        "Using the default Superstore dataset unless a file is uploaded."
    )

st.sidebar.divider()

# =====================================================
# 5. RUN AND RESET BUTTONS
# =====================================================

if "run_analysis" not in st.session_state:
    st.session_state.run_analysis = False

if st.sidebar.button(
    "🚀 Run Analysis",
    use_container_width=True
):
    st.session_state.run_analysis = True

if st.sidebar.button(
    "🔄 Reset Analysis",
    use_container_width=True
):
    st.session_state.run_analysis = False
    st.rerun()

if not st.session_state.run_analysis:
    st.info(
        "Upload your sales dataset or use the default dataset, "
        "then click 'Run Analysis'."
    )
    st.stop()

# =====================================================
# 6. LOAD SELECTED DATASET
# =====================================================

try:
    df = load_data(file_bytes, extension)
except Exception as e:
    st.error(f"Unable to load dataset: {e}")
    st.stop()

if df.empty:
    st.error("The uploaded dataset contains no valid records.")
    st.stop()

st.sidebar.success(
    f"Dataset loaded: {len(df):,} records"
)

# =====================================================
# 7. DASHBOARD FILTERS
# =====================================================

st.sidebar.header("🔎 Dashboard Filters")

categories = st.sidebar.multiselect(
    "Select Category",
    options=sorted(df["Category"].dropna().unique()),
    default=sorted(df["Category"].dropna().unique())
)

regions = st.sidebar.multiselect(
    "Select Region",
    options=sorted(df["Region"].dropna().unique()),
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

# =====================================================
# 8. FILTER DATA
# =====================================================

filtered = df[
    df["Category"].isin(categories)
    & df["Region"].isin(regions)
].copy()

if len(date_range) == 2:
    start_date, end_date = date_range

    filtered = filtered[
        filtered["Order Date"].dt.date.between(
            start_date, end_date
        )
    ]

if filtered.empty:
    st.warning(
        "No records found for the selected filters. "
        "Please change your filters."
    )
    st.stop()

# =====================================================
# 9. BUSINESS PERFORMANCE KPIs
# =====================================================

total_sales = filtered["Sales"].sum()
total_profit = filtered["Profit"].sum()
total_orders = filtered["Order ID"].nunique()
total_quantity = filtered["Quantity"].sum()

profit_margin = (
    total_profit / total_sales * 100
    if total_sales != 0 else 0
)

st.divider()
st.header("📈 Business Performance")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Total Sales", f"${total_sales:,.2f}")
c2.metric("Total Profit", f"${total_profit:,.2f}")
c3.metric("Total Orders", f"{total_orders:,}")
c4.metric("Total Quantity", f"{total_quantity:,.0f}")
c5.metric("Profit Margin", f"{profit_margin:.2f}%")

st.divider()

# =====================================================
# 10. SALES BY CATEGORY AND REGION
# =====================================================

left, right = st.columns(2)

with left:
    st.subheader("Sales by Category")

    category_data = (
        filtered.groupby("Category", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )

    fig = px.bar(
        category_data,
        x="Category",
        y="Sales",
        color="Category",
        title="Category-wise Sales",
        text_auto=".2s"
    )

    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Sales by Region")

    region_data = (
        filtered.groupby("Region", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )

    fig = px.bar(
        region_data,
        x="Region",
        y="Sales",
        color="Region",
        title="Regional Sales Performance",
        text_auto=".2s"
    )

    st.plotly_chart(fig, use_container_width=True)

# =====================================================
# 11. MONTHLY SALES TREND AND PROFIT
# =====================================================

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
        title="Monthly Sales Performance"
    )

    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Profit by Sub-Category")

    subcategory = (
        filtered.groupby(
            "Sub-Category", as_index=False
        )["Profit"]
        .sum()
        .sort_values("Profit", ascending=True)
    )

    fig = px.bar(
        subcategory,
        x="Profit",
        y="Sub-Category",
        orientation="h",
        color="Profit",
        title="Sub-Category Profitability"
    )

    st.plotly_chart(fig, use_container_width=True)

# =====================================================
# 12. PROFIT BY CATEGORY
# =====================================================

st.subheader("Profit by Category")

profit_category = (
    filtered.groupby("Category", as_index=False)["Profit"]
    .sum()
)

fig = px.pie(
    profit_category,
    names="Category",
    values="Profit",
    hole=0.45,
    title="Category-wise Profit Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# =====================================================
# 13. DETAILED SALES DATA
# =====================================================

st.divider()
st.header("📋 Detailed Sales Data")

st.caption(
    f"Showing {len(filtered):,} records based on your selected filters."
)

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True
)

# =====================================================
# 14. DOWNLOAD CSV AND EXCEL REPORTS
# =====================================================

st.subheader("📥 Download Reports")

download1, download2 = st.columns(2)

csv_data = filtered.to_csv(index=False).encode("utf-8")

with download1:
    st.download_button(
        "⬇️ Download CSV Report",
        data=csv_data,
        file_name="retail_sales_analysis.csv",
        mime="text/csv",
        use_container_width=True
    )

excel_buffer = BytesIO()

with pd.ExcelWriter(
    excel_buffer,
    engine="openpyxl"
) as writer:
    filtered.to_excel(
        writer,
        index=False,
        sheet_name="Sales Data"
    )

with download2:
    st.download_button(
        "⬇️ Download Excel Report",
        data=excel_buffer.getvalue(),
        file_name="retail_sales_analysis.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

# =====================================================
# 15. AUTOMATIC BUSINESS INSIGHTS
# =====================================================

st.divider()
st.header("🤖 Automatic Business Insights")

st.caption(
    "Business findings and recommendations generated "
    "automatically from the selected dataset."
)

# Category sales
category_insights = (
    filtered.groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

# Region profit
region_insights = (
    filtered.groupby("Region")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

# Sub-category profit
subcategory_insights = (
    filtered.groupby("Sub-Category")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

# Monthly sales
monthly_insights = (
    filtered.assign(
        Month=filtered["Order Date"].dt.to_period("M")
    )
    .groupby("Month")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

# Display insights
st.subheader("📊 Key Business Findings")

i1, i2 = st.columns(2)

with i1:
    if not category_insights.empty:
        st.success(
            f"🏆 Highest Sales Category: "
            f"{category_insights.idxmax()} "
            f"(${category_insights.max():,.2f})"
        )

    if not subcategory_insights.empty:
        st.info(
            f"💰 Most Profitable Sub-Category: "
            f"{subcategory_insights.idxmax()} "
            f"(${subcategory_insights.max():,.2f})"
        )

with i2:
    if not region_insights.empty:
        st.success(
            f"🌍 Most Profitable Region: "
            f"{region_insights.idxmax()} "
            f"(${region_insights.max():,.2f})"
        )

    if not monthly_insights.empty:
        best_month = monthly_insights.idxmax()

        st.info(
            f"📅 Highest Sales Month: "
            f"{best_month} "
            f"(${monthly_insights.max():,.2f})"
        )

# =====================================================
# 16. LOSS-MAKING PRODUCTS
# =====================================================

st.subheader("⚠️ Areas Requiring Attention")

loss_making = subcategory_insights[
    subcategory_insights < 0
]

if not loss_making.empty:
    st.warning(
        "These sub-categories generated negative profit:"
    )

    loss_df = loss_making.rename(
        "Total Loss"
    ).reset_index()

    st.dataframe(
        loss_df,
        use_container_width=True,
        hide_index=True
    )
else:
    st.success(
        "No loss-making sub-categories found in the selected data."
    )

# =====================================================
# 17. BUSINESS RECOMMENDATIONS
# =====================================================

st.subheader("💡 Business Recommendations")

recommendations = []

if not category_insights.empty:
    recommendations.append(
        f"Focus on the {category_insights.idxmax()} category "
        "because it generates the highest sales."
    )

if not region_insights.empty:
    recommendations.append(
        f"Study successful sales strategies in the "
        f"{region_insights.idxmax()} region."
    )

if not loss_making.empty:
    recommendations.append(
        "Review pricing, discounts, and operating costs "
        "for loss-making sub-categories."
    )

if profit_margin < 10:
    recommendations.append(
        "Profit margin is below 10%. Review discount policies "
        "and product costs to improve profitability."
    )
else:
    recommendations.append(
        "Monitor operating costs and discount policies "
        "to maintain healthy profitability."
    )

for number, recommendation in enumerate(
    recommendations, start=1
):
    st.markdown(
        f"**{number}.** {recommendation}"
    )

# =====================================================
# 18. DOWNLOAD BUSINESS INSIGHTS
# =====================================================

insights_text = "RETAIL BUSINESS INSIGHTS\n\n"

if not category_insights.empty:
    insights_text += (
        f"Highest Sales Category: "
        f"{category_insights.idxmax()}\n"
    )

if not region_insights.empty:
    insights_text += (
        f"Most Profitable Region: "
        f"{region_insights.idxmax()}\n"
    )

if not subcategory_insights.empty:
    insights_text += (
        f"Most Profitable Sub-Category: "
        f"{subcategory_insights.idxmax()}\n"
    )

if not monthly_insights.empty:
    insights_text += (
        f"Highest Sales Month: "
        f"{monthly_insights.idxmax()}\n"
    )

insights_text += "\nBUSINESS RECOMMENDATIONS\n"

for number, recommendation in enumerate(
    recommendations, start=1
):
    insights_text += (
        f"{number}. {recommendation}\n"
    )

st.download_button(
    "📥 Download Business Insights",
    data=insights_text,
    file_name="retail_business_insights.txt",
    mime="text/plain"
)

# =====================================================
# 19. COMPLETION MESSAGE
# =====================================================

st.divider()

st.success(
    "✅ Retail Analytics Pro: Analysis completed successfully!"
)

st.caption(
    "Retail Analytics Pro | Python • Pandas • Streamlit • Plotly"
)

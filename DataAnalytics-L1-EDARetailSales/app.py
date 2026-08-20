import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(
    page_title="Retail Sales Analysis",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Retail Sales Analysis – EDA")
st.write(
    "Interactive dashboard for exploring retail sales performance, "
    "customer behavior, product performance, and profitability."
)

# Load dataset
@st.cache_data
def load_data():
    file_path = "data/cleaned_retail_sales.csv"
    return pd.read_csv(file_path)

df = load_data()

# Sidebar
st.sidebar.header("Dashboard Filters")

# Show dataset
st.subheader("📁 Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Records", f"{len(df):,}")

with col2:
    st.metric("Total Columns", len(df.columns))

# Detect useful columns
revenue_col = None
profit_col = None
quantity_col = None

for col in df.columns:
    col_lower = col.lower()

    if "revenue" in col_lower or "sales" in col_lower:
        revenue_col = col

    if "profit" in col_lower:
        profit_col = col

    if "quantity" in col_lower:
        quantity_col = col

with col3:
    if revenue_col:
        st.metric(
            "Total Revenue",
            f"{df[revenue_col].sum():,.2f}"
        )
    else:
        st.metric("Total Revenue", "N/A")

with col4:
    if profit_col:
        st.metric(
            "Total Profit",
            f"{df[profit_col].sum():,.2f}"
        )
    else:
        st.metric("Total Profit", "N/A")

# Dataset preview
st.subheader("🔍 Dataset Preview")
st.dataframe(df.head(20), use_container_width=True)

# Basic statistics
st.subheader("📈 Statistical Summary")
st.dataframe(df.describe(include="all"), use_container_width=True)

# Revenue analysis
if revenue_col:

    st.subheader("💰 Revenue Analysis")

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.hist(df[revenue_col].dropna(), bins=30)

    ax.set_title("Revenue Distribution")
    ax.set_xlabel("Revenue")
    ax.set_ylabel("Frequency")

    st.pyplot(fig)

# Profit analysis
if profit_col:

    st.subheader("💵 Profit Analysis")

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.hist(df[profit_col].dropna(), bins=30)

    ax.set_title("Profit Distribution")
    ax.set_xlabel("Profit")
    ax.set_ylabel("Frequency")

    st.pyplot(fig)

# Quantity analysis
if quantity_col:

    st.subheader("📦 Order Quantity Analysis")

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.hist(df[quantity_col].dropna(), bins=20)

    ax.set_title("Order Quantity Distribution")
    ax.set_xlabel("Quantity")
    ax.set_ylabel("Frequency")

    st.pyplot(fig)

# Categorical analysis
categorical_columns = df.select_dtypes(
    include=["object", "category"]
).columns.tolist()

if categorical_columns:

    st.subheader("📊 Category Analysis")

    selected_column = st.selectbox(
        "Select a category",
        categorical_columns
    )

    value_counts = df[selected_column].value_counts().head(10)

    fig, ax = plt.subplots(figsize=(10, 5))

    sns.barplot(
        x=value_counts.values,
        y=value_counts.index,
        ax=ax
    )

    ax.set_title(f"Top 10 {selected_column}")
    ax.set_xlabel("Count")
    ax.set_ylabel(selected_column)

    st.pyplot(fig)

# Correlation
numeric_columns = df.select_dtypes(
    include=["number"]
).columns

if len(numeric_columns) > 1:

    st.subheader("🔗 Correlation Analysis")

    correlation = df[numeric_columns].corr()

    fig, ax = plt.subplots(figsize=(10, 7))

    sns.heatmap(
        correlation,
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        ax=ax
    )

    st.pyplot(fig)

# Footer
st.markdown("---")

st.write(
    "👤 **Author: Bejjanki Sanjay Kumar**"
)

st.write(
    "Python | Pandas | NumPy | Matplotlib | Seaborn | Streamlit"
)
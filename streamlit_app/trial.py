# ==============================
# E-COMMERCE BUSINESS DASHBOARD
# ==============================

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.set_page_config(
    page_title="E-Commerce Business Analytics",
    layout="wide"
)

st.title("📦 E-Commerce Business Analytics Dashboard")
st.write("End-to-End Data Analytics Project using Python & Streamlit")

# ==============================
# LOAD DATA
# ==============================

@st.cache_data
def load_data():
    return pd.read_csv("olist_master_cleaned.csv")

df = load_data()

# Date formatting
df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
df["order_delivered_customer_date"] = pd.to_datetime(df["order_delivered_customer_date"])
df["order_estimated_delivery_date"] = pd.to_datetime(df["order_estimated_delivery_date"])

# Delivery delay
df["delivery_delay"] = (
    df["order_delivered_customer_date"] -
    df["order_estimated_delivery_date"]
).dt.days

# ==============================
# SIDEBAR NAVIGATION
# ==============================

st.sidebar.title("📊 Dashboard Sections")

section = st.sidebar.radio(
    "Select Category",
    [
        "Overview",
        "Revenue Analysis",
        "Customer Analysis",
        "Delivery Performance",
        "Reviews & Satisfaction"
    ]
)

# ==============================
# OVERVIEW
# ==============================

if section == "Overview":

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("📊 Key Business Metrics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Orders", df["order_id"].nunique())
    col2.metric("Total Revenue", round(df["payment_value"].sum(), 2))
    col3.metric("Avg Review Score", round(df["review_score"].mean(), 2))
    col4.metric("Unique Customers", df["customer_unique_id"].nunique())


# ==============================
# REVENUE ANALYSIS
# ==============================

elif section == "Revenue Analysis":

    st.header("💰 Revenue Analysis")

    # Q1 Monthly Revenue
    st.subheader("📈 Monthly Revenue Trend")

    monthly_revenue = (
        df.groupby(df["order_purchase_timestamp"].dt.to_period("M"))["payment_value"]
        .sum()
        .reset_index()
    )

    monthly_revenue["order_purchase_timestamp"] = monthly_revenue["order_purchase_timestamp"].astype(str)

    fig, ax = plt.subplots(figsize=(12,5))
    ax.plot(monthly_revenue["order_purchase_timestamp"], monthly_revenue["payment_value"])
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.info(
        "🧠 **Insights:**\n\n"
        "- Revenue shows consistent growth trend\n"
        "- Seasonal spikes visible in specific months\n"
        "- Business revenue is scalable over time"
    )

    # Q2 Top Categories
    st.subheader("🏆 Top 10 Categories by Revenue")

    category_revenue = (
        df.groupby("product_category_name_english")["payment_value"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig, ax = plt.subplots()
    category_revenue.plot(kind="barh", ax=ax)
    ax.invert_yaxis()
    st.pyplot(fig)

    st.success(
        "🧠 **Insights:**\n\n"
        "- A small % of categories drive majority revenue\n"
        "- Business follows Pareto Principle (80/20 rule)\n"
        "- High performing categories should get more marketing focus"
    )


# ==============================
# CUSTOMER ANALYSIS
# ==============================

elif section == "Customer Analysis":

    st.header("👥 Customer Analysis")

    customer_orders = (
        df.groupby("customer_unique_id")["order_id"]
        .nunique()
        .reset_index(name="order_count")
    )

    new_customers = customer_orders[customer_orders["order_count"] == 1].shape[0]
    repeat_customers = customer_orders[customer_orders["order_count"] > 1].shape[0]

    col1, col2 = st.columns(2)
    col1.metric("New Customers", new_customers)
    col2.metric("Repeat Customers", repeat_customers)

    st.info(
        "🧠 **Insights:**\n\n"
        "- High repeat customers indicate strong retention\n"
        "- Low repeat rate signals retention opportunity\n"
        "- Loyalty programs can increase repeat purchases"
    )


# ==============================
# DELIVERY PERFORMANCE
# ==============================

elif section == "Delivery Performance":

    st.header("🚚 Delivery Performance")

    delivery_status = df.copy()
    delivery_status["delivery_status"] = delivery_status["delivery_delay"].apply(
        lambda x: "On-time" if x <= 0 else "Delayed"
    )

    delivery_percentage = (
        delivery_status["delivery_status"]
        .value_counts(normalize=True) * 100
    )

    fig, ax = plt.subplots()
    delivery_percentage.plot(kind="bar", ax=ax)
    st.pyplot(fig)

    st.info(
        "🧠 **Insights:**\n\n"
        "- A significant share of orders are delayed\n"
        "- Improving last-mile delivery can boost satisfaction\n"
        "- On-time delivery is a critical KPI"
    )


# ==============================
# REVIEWS & SATISFACTION
# ==============================

elif section == "Reviews & Satisfaction":

    st.header("⭐ Reviews & Customer Satisfaction")

    avg_review_score = df["review_score"].mean()
    st.metric("Overall Average Rating", round(avg_review_score,2))

    review_distribution = df["review_score"].value_counts().sort_index()

    fig, ax = plt.subplots()
    review_distribution.plot(kind="bar", ax=ax)
    st.pyplot(fig)

    st.success(
        "🧠 **Insights:**\n\n"
        "- Majority customers give high ratings\n"
        "- Low ratings correlate with delayed delivery\n"
        "- Customer satisfaction directly impacts retention"
    )
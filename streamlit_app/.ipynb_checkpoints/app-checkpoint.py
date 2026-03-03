# using streamlit we are making one web page (website) -->
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

st.set_page_config(
    page_title = "E-Commerce Business Analytics",
    layout = "wide"
)

st.title("📦 E-commerce Business Analytics Dashboard")
st.write("End-to-End Data Analytics Project using Python & Streamlit")

# load data
@st.cache_data # dataset ko fast load karne ke liye
def load_data():
    return pd.read_csv("olist_master_cleaned.csv")

df = load_data()

# create delivery delay column (if not exists)
df["order_delivered_customer_date"] = pd.to_datetime(df["order_delivered_customer_date"])
df["order_estimated_delivery_date"] = pd.to_datetime(df["order_estimated_delivery_date"])

df["delivery_delay"] = (
    df["order_delivered_customer_date"] - df["order_estimated_delivery_date"]
).dt.days


st.subheader("Dataset Preview")
st.dataframe(df.head())

# Data load karega
# Browser me dataset preview dikhaega
# Fast rahega (cache use kiya hai)


st.subheader("📊 Key Business Metrics")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Orders", df['order_id'].nunique())
col2.metric("Average Review Score", round(df['review_score'].mean(), 2))
col3.metric("Avg Delivery Delay (days)", round(df['delivery_delay'].mean(), 2))
col4.metric("👥 Unique Customers", df['customer_unique_id'].nunique())

# Q1. MONTHLY REVENUE TREND OVER TIME?
st.subheader("📈 Monthly Revenue Trend Over Time")

# --- Data Preparation ---
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

monthly_revenue = (
    df.groupby(df['order_purchase_timestamp'].dt.to_period("M"))['payment_value']
    .sum()
    .reset_index()
)

monthly_revenue['order_purchase_timestamp'] = monthly_revenue['order_purchase_timestamp'].astype(str)

# --- Visualization ---
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(
    monthly_revenue['order_purchase_timestamp'],
    monthly_revenue['payment_value']
)

ax.set_title("Monthly Revenue Trend")
ax.set_xlabel("Month")
ax.set_ylabel("Total Revenue")
plt.xticks(rotation=45)

st.pyplot(fig)

# INSIGHTS -->
st.markdown("### 🧠 Key Insights")

st.info("""
• Revenue shows a clear upward trend over time, indicating sustained business growth.  
• Certain months exhibit noticeable spikes, suggesting seasonal demand patterns or promotional campaigns.  
• Occasional revenue dips may indicate operational bottlenecks or market slowdowns.  
• Overall performance reflects scalable and expanding revenue capability.
""")


# Q2. TOP 10 PRODUCT CATEGORIES BY REVENUE?
st.subheader("🏆 Top 10 Product Categories by Revenue")

# --- Data Preparation ---
category_revenue = (
    df.groupby("product_category_name_english")['payment_value']
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

# --- Visualization ---
fig, ax = plt.subplots(figsize=(10, 5))
ax.barh(
    category_revenue['product_category_name_english'],
    category_revenue['payment_value']
)

ax.set_xlabel("Total Revenue")
ax.set_ylabel("Product Category")
ax.set_title("Top 10 Product Categories by Revenue")
ax.invert_yaxis()

st.pyplot(fig)


# INSIGHTS -->
st.markdown("### 🧠 Key Insights")

st.info("""
• A small number of categories contribute a disproportionately large share of total revenue, reflecting a clear Pareto (80/20) effect.  
• High-value categories such as electronics, furniture, and home appliances drive the majority of sales.  
• Lower-ranked categories contribute marginal revenue and may require strategic repositioning or targeted campaigns.  
• Revenue concentration suggests strong opportunities for inventory prioritization and promotional optimization.
""")



# Q3. TOP 10 PRODUCTS BY REVENUE?
st.subheader("🏆 Top 10 Products by Revenue")

# revenue per product
product_revenue = (
    df.groupby("product_id")["payment_value"]
      .sum()
      .reset_index()
      .sort_values(by="payment_value", ascending=False)
      .head(10)
)

# plot
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    data=product_revenue,
    x="payment_value",
    y="product_id",
    ax=ax
)

ax.set_title("Top 10 Products by Revenue")
ax.set_xlabel("Total Revenue")
ax.set_ylabel("Product ID")

st.pyplot(fig)


# INSIGHTS -->
st.markdown("### 🧠 Key Insights")

st.info("""
• The Top 10 products contribute a disproportionately large share of total revenue.  
• Revenue distribution is highly skewed, indicating strong product concentration.  
• A small set of high-performing products significantly influence overall sales performance.  
• These products are strategically critical for inventory planning, seller negotiations, and promotional campaigns.
""")



# Q4. AVERAGE ORDER VALUE?
# average order value = total revenue / total orders
st.subheader("💰 Average Order Value (AOV)")

# calculate AOV
total_revenue = df["payment_value"].sum()
total_orders = df["order_id"].nunique()
aov = total_revenue / total_orders

# display metric
st.metric("Average Order Value", f"₹ {aov:,.2f}")

# optional distribution plot
fig, ax = plt.subplots(figsize=(8, 4))

order_value = (
    df.groupby("order_id")["payment_value"]
      .sum()
      .reset_index()
)

sns.histplot(order_value["payment_value"], bins=40, kde=True, ax=ax)

ax.set_title("Distribution of Order Values")
ax.set_xlabel("Order Value")
ax.set_ylabel("Number of Orders")

st.pyplot(fig)


# INSIGHTS -->
st.markdown("### 🧠 Key Insights")

st.info("""
• Average Order Value (AOV) measures the average revenue generated per transaction.  
• The order value distribution is right-skewed, where most transactions fall in the low-to-mid price range.  
• A small number of high-value orders significantly lift total revenue performance.  
• Increasing AOV presents a strong opportunity for revenue growth without increasing customer acquisition cost.
""")


# Q5. REVENUE CONTRIBUTION BY PAYMENT TYPE?
st.subheader("💳 Revenue Contribution by Payment Type")

# aggregate revenue by payment type
payment_revenue = (
    df.groupby("payment_type")["payment_value"]
      .sum()
      .reset_index()
      .sort_values(by="payment_value", ascending=False)
)

# percentage calculation
payment_revenue["revenue_percent"] = (
    payment_revenue["payment_value"] / payment_revenue["payment_value"].sum() * 100
).round(2)

# show table
st.dataframe(payment_revenue)

# visualization
fig, ax = plt.subplots(figsize=(8, 5))

sns.barplot(
    data=payment_revenue,
    x="payment_type",
    y="payment_value",
    ax=ax
)

ax.set_title("Revenue Contribution by Payment Type")
ax.set_xlabel("Payment Type")
ax.set_ylabel("Total Revenue")

plt.xticks(rotation=30)

st.pyplot(fig)


# INSIGHTS -->
st.markdown("### 🧠 Key Insights")

st.info("""
• Credit card remains the dominant payment method, contributing the highest share of total revenue.  
• Digital payment channels demonstrate strong and growing customer adoption.  
• A small number of payment methods account for the majority of transaction value.  
• Low-contribution payment types may be creating unnecessary checkout complexity without proportional revenue impact.
""")



# Q7. NEW VS REPEAT CUSTOMER RATIO?
st.subheader("🔁 New vs Repeat Customers")

# orders per customer
customer_orders = (
    df.groupby("customer_unique_id")["order_id"]
      .nunique()
      .reset_index(name="order_count")
)

new_customers = customer_orders[customer_orders["order_count"] == 1].shape[0]
repeat_customers = customer_orders[customer_orders["order_count"] > 1].shape[0]

total_customers = new_customers + repeat_customers

# KPIs:
col1, col2, col3 = st.columns(3)

col1.metric("Total Customers", total_customers)
col2.metric("New Customers", new_customers)
col3.metric("Repeat Customers", repeat_customers)

# visualisation:
import matplotlib.pyplot as plt
import seaborn as sns

ratio_df = pd.DataFrame({
    "Customer Type": ["New Customers", "Repeat Customers"],
    "Count": [new_customers, repeat_customers]
})

fig, ax = plt.subplots()
sns.barplot(data=ratio_df, x="Customer Type", y="Count", ax=ax)
ax.set_title("New vs Repeat Customer Distribution")
ax.set_ylabel("Number of Customers")
ax.set_xlabel("")

st.pyplot(fig)

# percentage insights -->
new_pct = (new_customers / total_customers) * 100
repeat_pct = (repeat_customers / total_customers) * 100

st.markdown("### 🧠 Key Insights")

st.info("""
• 97% of customers are one-time buyers, indicating very low repeat purchase behavior.  
• Only 3% of customers return for subsequent transactions.  
• The current repeat customer ratio suggests a significant customer retention gap.  
• Improving retention could substantially increase lifetime value (LTV) without increasing acquisition costs.
""")



# Q8. AVERAGE ORDERS PER CUSTOMERS?
st.subheader("📦 Average Orders per Customer")

orders_per_customer = (
    df.groupby("customer_unique_id")["order_id"]
      .nunique()
      .reset_index(name="order_count")
)

avg_orders = orders_per_customer["order_count"].mean()

# KPI Metric:
st.metric(
    "Average Orders per Customer",
    round(avg_orders, 2)
)

# visualisation:
import matplotlib.pyplot as plt
import seaborn as sns

fig, ax = plt.subplots()
sns.histplot(orders_per_customer["order_count"], bins=20, kde=False, ax=ax)
ax.set_title("Distribution of Orders per Customer")
ax.set_xlabel("Number of Orders")
ax.set_ylabel("Number of Customers")

st.pyplot(fig)

# INSIGHTS -->
import matplotlib.pyplot as plt
import seaborn as sns

fig, ax = plt.subplots()
sns.histplot(orders_per_customer["order_count"], bins=20, kde=False, ax=ax)
ax.set_title("Distribution of Orders per Customer")
ax.set_xlabel("Number of Orders")
ax.set_ylabel("Number of Customers")

st.pyplot(fig)

# < 1.5 → low retention
# 2+ → healthy repeat behavior
# Helps design:
   # subscription models
   # re-marketing campaigns
   # personalized offers


# Q9. HIGH VALUE CUSTOMERS (TOP 10% BY SPEND)?
# total spend per customers -->
st.subheader("💎 High Value Customers (Top 10% by Spend)")

customer_spend = (
    df.groupby("customer_unique_id")["payment_value"]
      .sum()
      .reset_index(name="total_spend")
)

# top 10% threshold -->
threshold = customer_spend["total_spend"].quantile(0.90)

high_value_customers = customer_spend[
    customer_spend["total_spend"] >= threshold
]

# KPI Metrics:
col1, col2, col3 = st.columns(3)

col1.metric(
    "High Value Customers",
    high_value_customers.shape[0]
)

col2.metric(
    "Revenue from High Value Customers",
    f"₹ {round(high_value_customers['total_spend'].sum(), 2)}"
)

col3.metric(
    "Revenue Share (%)",
    round(
        high_value_customers["total_spend"].sum()
        / customer_spend["total_spend"].sum() * 100,
        2
    )
)
 # visualisation (spend distribution) -->
import matplotlib.pyplot as plt
import seaborn as sns

fig, ax = plt.subplots()
sns.histplot(customer_spend["total_spend"], bins=50, ax=ax)
ax.axvline(threshold, color="red", linestyle="--", label="Top 10% Threshold")
ax.set_title("Customer Spend Distribution")
ax.set_xlabel("Total Spend per Customer")
ax.legend()

st.pyplot(fig)

# sample high value customers -->
st.write("🔝 Sample High Value Customers")
st.dataframe(
    high_value_customers
    .sort_values("total_spend", ascending=False)
    .head(10)
)

# INSIGHTS -->
st.markdown("### 🧠 Key Insights")

st.info(
    f"""
• Top 10% of customers spend ₹ {round(threshold, 2)} or more.  
• This segment contributes {round(high_value_customers['total_spend'].sum() / customer_spend['total_spend'].sum() * 100, 2)}% of total revenue.  
• Revenue concentration among a small customer base indicates a strong Pareto effect.  
• Retaining and nurturing this segment offers the highest return on investment (ROI).
"""
)
# We segmented customers based on total spend and identified the top 10% as high-value customers. Despite being a small group, they contribute a disproportionately large share of revenue, highlighting the importance of retention-focused strategies.


# Q10. CUSTOMERS CONTRIBUTION TO TOTAL REVENUE?
# total revenue per customer -->
st.subheader("👥 Customer Contribution to Total Revenue")

customer_revenue = (
    df.groupby("customer_unique_id")["payment_value"]
      .sum()
      .reset_index(name="revenue")
      .sort_values("revenue", ascending=False)
)

# cumulative revenue percentage -->
customer_revenue["cumulative_revenue"] = customer_revenue["revenue"].cumsum()
customer_revenue["cumulative_percentage"] = (
    customer_revenue["cumulative_revenue"]
    / customer_revenue["revenue"].sum()
) * 100

# contribution KPIs:
top_10 = customer_revenue.iloc[:int(0.10 * len(customer_revenue))]
top_20 = customer_revenue.iloc[:int(0.20 * len(customer_revenue))]
top_50 = customer_revenue.iloc[:int(0.50 * len(customer_revenue))]

col1, col2, col3 = st.columns(3)

col1.metric(
    "Top 10% Customers Revenue %",
    round(top_10["revenue"].sum() / customer_revenue["revenue"].sum() * 100, 2)
)

col2.metric(
    "Top 20% Customers Revenue %",
    round(top_20["revenue"].sum() / customer_revenue["revenue"].sum() * 100, 2)
)

col3.metric(
    "Top 50% Customers Revenue %",
    round(top_50["revenue"].sum() / customer_revenue["revenue"].sum() * 100, 2)
)

# pareto curve (visualisation):
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

ax.plot(
    range(1, len(customer_revenue) + 1),
    customer_revenue["cumulative_percentage"],
    marker="."
)

ax.axhline(80, color="red", linestyle="--", label="80% Revenue")
ax.set_xlabel("Customers (Sorted by Spend)")
ax.set_ylabel("Cumulative Revenue (%)")
ax.set_title("Customer Revenue Contribution (Pareto Analysis)")
ax.legend()

st.pyplot(fig)

# INSIGHTS -->
st.markdown("### 🧠 Key Insights")

st.info("""
• A small percentage of customers contribute a disproportionately large share of total revenue.  
• The business clearly reflects the Pareto Principle (80/20 dynamic).  
• Revenue concentration increases dependency risk on top contributors.  
• Retention strategies should prioritize high-value customer segments.
""")
# We analyzed customer contribution using cumulative revenue analysis and found that a small percentage of customers generate a majority of total revenue, indicating a strong Pareto effect. This insight helps prioritize retention and personalized engagement strategies.

# Q11. ON-TIME VS DELAYED DELIVERY PERCENTAGE?
# delivery status column -->
st.subheader("🚚 On-time vs Delayed Delivery Performance")

delivery_status = df.copy()
delivery_status["delivery_status"] = delivery_status["delivery_delay"].apply(
    lambda x: "On-time" if x <= 0 else "Delayed"
)

# calculate percentages -->
delivery_counts = delivery_status["delivery_status"].value_counts()
delivery_percentage = (delivery_counts / delivery_counts.sum()) * 100

# KPIs:
col1, col2 = st.columns(2)

col1.metric("On-time Deliveries (%)", round(delivery_percentage["On-time"], 2))
col2.metric("Delayed Deliveries (%)", round(delivery_percentage["Delayed"], 2))

# visualisation (bar chart) -->
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

delivery_percentage.plot(
    kind="bar",
    ax=ax
)

ax.set_title("On-time vs Delayed Delivery Percentage")
ax.set_ylabel("Percentage (%)")
ax.set_xlabel("Delivery Status")

st.pyplot(fig)

# INSIGHTS -->
st.markdown("### 🧠 Key Insights")

st.info(
    """
• A considerable proportion of orders experience delivery delays, negatively affecting customer satisfaction.  
• Delivery performance has a direct correlation with review ratings and brand perception.  
• On-time delivery should be treated as a core operational KPI for logistics and seller evaluation.  
• Reducing delay rates can significantly improve customer retention and repeat purchase behavior.
"""
)
# We categorized deliveries into on-time and delayed based on delivery delay days. The analysis highlights logistics efficiency and its direct impact on customer experience.



# Q12. AVERAGE DELIVERY TIME?
st.subheader("🚚 Average Delivery Time")

# calculate delivery time in days
df['delivery_time_days'] = (
    pd.to_datetime(df['order_delivered_customer_date']) -
    pd.to_datetime(df['order_purchase_timestamp'])
).dt.days

avg_delivery_time = df['delivery_time_days'].mean()

# KPI
st.metric(
    label="📦 Average Delivery Time (Days)",
    value=round(avg_delivery_time, 2)
)

# distribution plot
fig, ax = plt.subplots()
ax.hist(df['delivery_time_days'].dropna(), bins=30)
ax.set_xlabel("Delivery Time (Days)")
ax.set_ylabel("Number of Orders")
ax.set_title("Distribution of Delivery Time")

st.pyplot(fig)

# INSIGHTS -->
st.markdown("### 🧠 Key Insights")

st.info(
    f"""
    • Average delivery time is **~{round(avg_delivery_time,2)} days**, indicating overall logistics performance  
    • Majority of orders are delivered within a standard time range  
    • Presence of long-tail delays suggests operational inefficiencies  
    • Delivery time directly impacts **customer satisfaction & reviews**
    """
)
st.markdown("### 🎯 Business Recommendations")

st.success(
    """
    ✔ Optimize last-mile delivery in high-delay regions  
    ✔ Track sellers with frequent delivery delays  
    ✔ Introduce stricter delivery SLAs for logistics partners  
    ✔ Use delivery-time KPIs to improve customer experience
    """
)


# Q13. REVENUE LOSS DUE TO DELAYED DELIVERIES?
st.subheader("💸 Revenue Loss Due to Delayed Deliveries")
# identity delayed orders -->
# delayed orders
delayed_df = df[df["delivery_delay"] > 0]

# revenue calculations
total_revenue = df["payment_value"].sum()
delayed_revenue = delayed_df["payment_value"].sum()

revenue_loss_percentage = (delayed_revenue / total_revenue) * 100

# KPI Metrics -->
col1, col2 = st.columns(2)

col1.metric(
    "Revenue from Delayed Orders",
    f"₹{delayed_revenue:,.0f}"
)

col2.metric(
    "Revenue at Risk (%)",
    f"{revenue_loss_percentage:.2f}%"
)

# revenue comparison charts -->
on_time_revenue = total_revenue - delayed_revenue

comparison_df = pd.DataFrame({
    "Delivery Status": ["On-Time", "Delayed"],
    "Revenue": [on_time_revenue, delayed_revenue]
})

fig, ax = plt.subplots()
ax.bar(comparison_df["Delivery Status"], comparison_df["Revenue"])
ax.set_title("Revenue Impact of Delivery Delays")
ax.set_ylabel("Revenue")
st.pyplot(fig)

# INSIGHTS -->
st.markdown("### 🧠 Key Insights")

st.info(
    f"""
    • Delayed deliveries generated ₹{delayed_revenue:,.0f} in revenue  
    • {revenue_loss_percentage:.2f}% of total revenue is exposed to delay risk  
    • High dependency on delayed orders increases churn probability  
    • Delivery delays directly affect repeat purchase behavior
    """
)

# BUSINESS RECOMMENDATIONS -->
st.markdown("### 🎯 Business Recommendations")

st.success(
    """
    ✔ Reduce delayed orders to protect revenue  
    ✔ Monitor sellers contributing most to delayed revenue  
    ✔ Optimize high-delay regions in logistics network  
    ✔ Track revenue-at-risk as a core KPI
    """
)



# Q14. REGION WISE DELIVERY PERFORMANCE?
st.subheader("🌍 Region-wise Delivery Performance")
# creating delivery status column -->
df["delivery_status"] = df["delivery_delay"].apply(
    lambda x: "On-Time" if x <= 0 else "Delayed"
)
# group-by state/ region -->
region_performance = (
    df.groupby("customer_state")["delivery_status"]
    .value_counts(normalize=True)
    .unstack()
    .fillna(0) * 100
)

region_performance = region_performance.sort_values(
    by="Delayed", ascending=False
)
# showing top 10 worst performing states -->
top_delay_states = region_performance.head(10)

fig, ax = plt.subplots()
top_delay_states["Delayed"].plot(kind="bar", ax=ax)
ax.set_title("Top 10 States with Highest Delay %")
ax.set_ylabel("Delayed Delivery (%)")
ax.set_xlabel("State")
st.pyplot(fig)

# KPI summary -->
worst_state = region_performance.index[0]
worst_delay = region_performance.iloc[0]["Delayed"]

st.metric(
    "🚨 Worst Performing State (Delay %)",
    f"{worst_state} - {worst_delay:.2f}%"
)

# INSIGHTS -->
st.markdown("### 🧠 Key Insights")

st.info(
    f"""
    • {worst_state} has the highest delayed delivery rate at {worst_delay:.2f}%  
    • Significant regional variation exists in delivery performance  
    • Certain states consistently underperform in logistics efficiency  
    • Delivery delays are geographically concentrated
    """
)

# RECOMMENDATIONS -->
st.markdown("### 🎯 Business Recommendations")

st.success(
    """
    ✔ Strengthen logistics network in high-delay states  
    ✔ Partner with better last-mile providers in weak regions  
    ✔ Create region-specific SLA targets  
    ✔ Monitor state-level delay KPI monthly
    """
)



# Q15. STATES WITH HIGHEST DELIVERY DELAYS?
st.subheader("🚨 States with Highest Delivery Delays")
# filtering only delayed orders -->
delayed_df = df[df["delivery_delay"] > 0]

# aggregate delay metrics by state -->
state_delay_stats = (
    delayed_df.groupby("customer_state")
    .agg(
        total_delayed_orders=("order_id", "count"),
        avg_delay_days=("delivery_delay", "mean")
    )
    .sort_values(by="total_delayed_orders", ascending=False)
)
# showing top 10 states by delay volumes -->
top_states_delay = state_delay_stats.head(10)

fig, ax = plt.subplots()
top_states_delay["total_delayed_orders"].plot(kind="bar", ax=ax)
ax.set_title("Top 10 States by Number of Delayed Orders")
ax.set_ylabel("Number of Delayed Orders")
ax.set_xlabel("State")
st.pyplot(fig)

# KPI highlights -->
worst_state_volume = state_delay_stats.index[0]
worst_state_orders = state_delay_stats.iloc[0]["total_delayed_orders"]
worst_state_avg_delay = state_delay_stats.iloc[0]["avg_delay_days"]

st.metric(
    "⚠ Highest Delay Volume State",
    f"{worst_state_volume} ({int(worst_state_orders)} orders)"
)

st.metric(
    "⏳ Avg Delay in That State",
    f"{worst_state_avg_delay:.2f} days"
)

# INSIGHTS -->
st.markdown("### 🧠 Key Insights")

st.info(
    f"""
    • {worst_state_volume} has the highest number of delayed orders  
    • On average, delays in this state are {worst_state_avg_delay:.2f} days  
    • Delay concentration suggests regional logistics bottlenecks  
    • High delay volume directly impacts customer satisfaction in that region
    """
)

# recommendations -->
st.markdown("### 🎯 Business Recommendations")

st.success(
    """
    ✔ Investigate warehouse-to-customer distance in high-delay states  
    ✔ Optimize shipping routes and local courier partners  
    ✔ Increase inventory allocation closer to demand-heavy regions  
    ✔ Introduce region-specific performance monitoring
    """
)



# Q16. AVERAGE REVIEW SCORE OVERALL?
st.subheader("⭐ Average Review Score Overall")
# calculating average rating -->
avg_review_score = df["review_score"].mean()
# KPI analysis -->
st.metric(
    "🌟 Overall Average Rating",
    f"{avg_review_score:.2f} / 5"
)

# distribution chart -->
review_distribution = df["review_score"].value_counts().sort_index()

fig, ax = plt.subplots()
review_distribution.plot(kind="bar", ax=ax)
ax.set_title("Review Score Distribution")
ax.set_xlabel("Review Score")
ax.set_ylabel("Number of Reviews")
st.pyplot(fig)

# INSIGHTS -->
st.markdown("### 🧠 Key Insights")

st.info(
    f"""
    • The overall average customer rating is {avg_review_score:.2f} out of 5  
    • Review distribution shows concentration in higher ratings (if 4-5 dominant)  
    • Lower ratings (1-2) highlight dissatisfaction segments  
    • Review score reflects product quality + delivery experience combined
    """
)

# recommendations -->
st.markdown("### 🎯 Business Recommendations")

st.success(
    """
    ✔ Monitor review score as a core customer satisfaction KPI  
    ✔ Investigate root causes of 1-2 star ratings  
    ✔ Align seller performance with review benchmarks  
    ✔ Improve post-delivery support experience
    """
)



# Q17. REVIEW SCORE VS DELIVERY DELAY?
st.subheader("⭐ Review Score vs Delivery Delay")
# creating delay category -->
df["delay_category"] = df["delivery_delay"].apply(
    lambda x: "On-Time" if x <= 0 
    else "1-3 Days Delay" if x <= 3
    else "4-7 Days Delay" if x <= 7
    else "7+ Days Delay"
)

# calculating average review per delay category -->
delay_review_analysis = (
    df.groupby("delay_category")["review_score"]
    .mean()
    .reindex(["On-Time", "1-3 Days Delay", "4-7 Days Delay", "7+ Days Delay"])
)

# visualisation -->
fig, ax = plt.subplots()
delay_review_analysis.plot(kind="bar", ax=ax)
ax.set_title("Average Review Score by Delivery Delay Category")
ax.set_xlabel("Delivery Delay Category")
ax.set_ylabel("Average Review Score")
st.pyplot(fig)

# KPI highlight -->
on_time_rating = delay_review_analysis["On-Time"]
max_delay_rating = delay_review_analysis["7+ Days Delay"]

st.metric(
    "⭐ On-Time Avg Rating",
    f"{on_time_rating:.2f}"
)

st.metric(
    "⚠ 7+ Days Delay Avg Rating",
    f"{max_delay_rating:.2f}"
)

# INSIGHTS -->
st.markdown("### 🧠 Key Insights")

st.info(
    f"""
    • On-time deliveries receive an average rating of {on_time_rating:.2f}  
    • Orders delayed by 7+ days drop to an average rating of {max_delay_rating:.2f}  
    • Customer satisfaction decreases as delivery delay increases  
    • Strong negative correlation between delay duration and review score
    """
)
# RECOMMENDATIONS -->
st.markdown("### 🎯 Business Recommendations")

st.success(
    """
    ✔ Reduce long delivery delays (7+ days) urgently  
    ✔ Set delay threshold alerts in logistics system  
    ✔ Offer compensation for heavily delayed orders  
    ✔ Track delay vs rating KPI monthly for service quality monitoring
    """
)



# Q18. CATEGORIES WITH LOWEST AVERAGE RATINGS?
st.subheader("📦 Categories with Lowest Average Ratings")
# calculating average rating by category -->
category_rating = (
    df.groupby("product_category_name")["review_score"]
    .mean()
    .sort_values()
)

# visualisation -->
lowest_rated_categories = category_rating.head(10)

fig, ax = plt.subplots()
lowest_rated_categories.plot(kind="bar", ax=ax)
ax.set_title("Bottom 10 Categories by Average Review Score")
ax.set_xlabel("Product Category")
ax.set_ylabel("Average Review Score")
plt.xticks(rotation=45)
st.pyplot(fig)

# KPI highlight -->
worst_category = lowest_rated_categories.index[0]
worst_category_rating = lowest_rated_categories.iloc[0]

st.metric(
    "⚠ Lowest Rated Category",
    f"{worst_category} ({worst_category_rating:.2f})"
)

# INSIGHTS -->
st.markdown("### 🧠 Key Insights")

st.info(
    f"""
    • {worst_category} has the lowest average rating at {worst_category_rating:.2f}  
    • Certain product categories consistently underperform in customer satisfaction  
    • Low ratings may indicate product quality, packaging, or expectation mismatch  
    • Category-level dissatisfaction impacts brand perception
    """
)
# recommendations -->
st.markdown("### 🎯 Business Recommendations")

st.success(
    """
    ✔ Conduct quality audit for lowest-rated categories  
    ✔ Identify sellers contributing to poor ratings  
    ✔ Improve product descriptions & images  
    ✔ Consider removing consistently underperforming products
    """
)



# Q19. SELLERS WITH HIGHEST DELAYED DELIVERIES?
st.subheader("🏪 Sellers with Highest Delayed Deliveries")
# delayed orders -->
delayed_df = df[df["delivery_delay"] > 0]
# count delayed orders per sellers -->
seller_delay_stats = (
    delayed_df.groupby("seller_id")
    .agg(
        total_delayed_orders=("order_id", "count"),
        avg_delay_days=("delivery_delay", "mean")
    )
    .sort_values(by="total_delayed_orders", ascending=False)
)
# visualisation -->
top_sellers_delay = seller_delay_stats.head(10)

fig, ax = plt.subplots()
top_sellers_delay["total_delayed_orders"].plot(kind="bar", ax=ax)
ax.set_title("Top 10 Sellers by Number of Delayed Orders")
ax.set_xlabel("Seller ID")
ax.set_ylabel("Number of Delayed Orders")
plt.xticks(rotation=45)
st.pyplot(fig)

# KPI highlight -->
worst_seller = seller_delay_stats.index[0]
worst_seller_orders = seller_delay_stats.iloc[0]["total_delayed_orders"]
worst_seller_avg_delay = seller_delay_stats.iloc[0]["avg_delay_days"]

st.metric(
    "⚠ Seller with Most Delays",
    f"{worst_seller} ({int(worst_seller_orders)} delays)"
)

st.metric(
    "⏳ Avg Delay for This Seller",
    f"{worst_seller_avg_delay:.2f} days"
)
# INSIGHTS -->
st.markdown("### 🧠 Key Insights")

st.info(
    f"""
    • Seller {worst_seller} has the highest number of delayed orders  
    • Their average delay is {worst_seller_avg_delay:.2f} days  
    • Delay-heavy sellers directly impact platform reputation  
    • Seller-level accountability is critical for service quality
    """
)
# recommendations -->
st.markdown("### 🎯 Business Recommendations")

st.success(
    """
    ✔ Introduce seller performance scorecards  
    ✔ Penalize sellers with repeated delays  
    ✔ Provide logistics support to underperforming sellers  
    ✔ Remove sellers who consistently breach SLA agreements
    """
)







st.sidebar.title("📊 Dashboard Sections")
section = st.sidebar.radio(
    "Go to",
    ["Overview", "Revenue Analysis", "Delivery Performance", "Customer Satisfaction"]
)
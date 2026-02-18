import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Coffee Sales Dashboard", layout="wide")

st.title(" Coffee Sales Analytics Dashboard")

df = pd.read_csv("cleaned_coffee_sales.csv")

df["transaction_time"] = pd.to_datetime(df["transaction_time"])
df["revenue"] = df["transaction_qty"] * df["unit_price"]
df["hour"] = df["transaction_time"].dt.hour
df["day"] = df["transaction_time"].dt.day_name()
df["date"] = df["transaction_time"].dt.date

# KPIs
col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", f"${df['revenue'].sum():,.2f}")
col2.metric("Total Transactions", df["transaction_id"].nunique())
col3.metric("Average Order Value", f"${df['revenue'].mean():.2f}")

st.markdown("---")

# Revenue by Hour
st.subheader("Revenue by Hour")
hourly = df.groupby("hour")["revenue"].sum()
st.line_chart(hourly)

# Revenue by Day
st.subheader("Revenue by Day of Week")
daily = df.groupby("day")["revenue"].sum()
st.bar_chart(daily)

# Store Comparison
st.subheader("Revenue by Store Location")
store = df.groupby("store_location")["revenue"].sum()
st.bar_chart(store)

# Heatmap
st.subheader("Heatmap: Day vs Hour")

pivot = df.pivot_table(values="revenue",
                       index="day",
                       columns="hour",
                       aggfunc="sum")

fig, ax = plt.subplots(figsize=(12,5))
sns.heatmap(pivot, cmap="YlGnBu", ax=ax)
st.pyplot(fig)

import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import pandas as pd
import matplotlib.pyplot as plt

# -------------------- LOAD CREDENTIALS --------------------
with open('credentials.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    'sales_dashboard',
    'abcdef',
    cookie_expiry_days=1
)

# -------------------- LOGIN FORM --------------------
authenticator.login(location='sidebar')

# -------------------- IF LOGIN SUCCESS --------------------
if st.session_state["authentication_status"]:
    name = st.session_state["name"]
    username = st.session_state["username"]

    authenticator.logout('Logout', 'sidebar')
    st.sidebar.success(f"Welcome, {name} 👋")
    st.title("📊 Electronic Sales Dashboard")

    # Load your CSV
    df = pd.read_csv("electronic_daily_sales.csv", parse_dates=["Date"])
    df["TotalPrice"] = df["Quantity"] * df["Price"]

    # Daily Summary
    daily_summary = df.groupby("Date").agg({
        "Quantity": "sum",
        "TotalPrice": "sum"
    }).reset_index()
    daily_summary["Revenue_MA_3"] = daily_summary["TotalPrice"].rolling(window=3).mean()

    # Product Summary
    product_summary = df.groupby("Product").agg({
        "Quantity": "sum",
        "TotalPrice": "sum"
    }).reset_index()

    # Chart 1: Daily Revenue
    st.subheader("📈 Daily Revenue")
    fig1, ax1 = plt.subplots()
    ax1.plot(daily_summary["Date"], daily_summary["TotalPrice"], marker='o', label="Revenue")
    ax1.plot(daily_summary["Date"], daily_summary["Revenue_MA_3"], linestyle='--', label="3-Day Avg")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Revenue")
    ax1.legend()
    st.pyplot(fig1)

    # Chart 2: Daily Quantity
    st.subheader("📦 Daily Quantity Sold")
    fig2, ax2 = plt.subplots()
    ax2.bar(daily_summary["Date"], daily_summary["Quantity"], color='orange')
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Quantity")
    st.pyplot(fig2)

    # Chart 3: Revenue by Product
    st.subheader("💰 Revenue by Product")
    fig3, ax3 = plt.subplots()
    ax3.bar(product_summary["Product"], product_summary["TotalPrice"], color='green')
    ax3.set_ylabel("Revenue")
    ax3.set_xticklabels(product_summary["Product"], rotation=45)
    st.pyplot(fig3)

    # Chart 4: Quantity by Product
    st.subheader("📦 Quantity by Product")
    fig4, ax4 = plt.subplots()
    ax4.bar(product_summary["Product"], product_summary["Quantity"], color='skyblue')
    ax4.set_ylabel("Quantity")
    ax4.set_xticklabels(product_summary["Product"], rotation=45)
    st.pyplot(fig4)

    # Chart 5: Product Share Pie Chart
    st.subheader("🥧 Product Sales Share")
    fig5, ax5 = plt.subplots()
    ax5.pie(product_summary["Quantity"], labels=product_summary["Product"], autopct='%1.1f%%', startangle=140)
    st.pyplot(fig5)

    # Top-selling Product Info
    top_product = product_summary.loc[product_summary["Quantity"].idxmax()]
    st.success(f"🏆 Top Product: **{top_product['Product']}** with **{top_product['Quantity']} units** sold.")

# -------------------- IF LOGIN FAIL --------------------
elif st.session_state["authentication_status"] is False:
    st.error("❌ Incorrect username or password")

elif st.session_state["authentication_status"] is None:
    st.warning("🔐 Please enter your credentials")

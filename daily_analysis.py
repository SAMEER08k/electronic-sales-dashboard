import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("electronic_daily_sales.csv", parse_dates=["Date"])

# Calculate Total Price per row
df["TotalPrice"] = df["Quantity"] * df["Price"]

# Group by date for daily summary
daily_summary = df.groupby("Date").agg({
    "Quantity": "sum",
    "TotalPrice": "sum"
}).reset_index()

# Add a moving average for better trend visualization
daily_summary["Revenue_MA_3"] = daily_summary["TotalPrice"].rolling(window=3).mean()

# ----------- PLOTS --------------

# Plot 1: Daily Revenue
plt.figure(figsize=(12, 6))
plt.plot(daily_summary["Date"], daily_summary["TotalPrice"], label="Daily Revenue", marker='o')
plt.plot(daily_summary["Date"], daily_summary["Revenue_MA_3"], label="3-Day Moving Avg", linestyle="--")
plt.title("Daily Revenue of Electronic Sales")
plt.xlabel("Date")
plt.ylabel("Revenue")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("daily_revenue.png")
plt.show()

# Plot 2: Daily Quantity Sold
plt.figure(figsize=(12, 6))
plt.bar(daily_summary["Date"], daily_summary["Quantity"], color='orange')
plt.title("Daily Quantity Sold")
plt.xlabel("Date")
plt.ylabel("Quantity")
plt.grid(axis='y')
plt.tight_layout()
plt.savefig("daily_quantity.png")
plt.show()

# ----------- Product-wise Summary -----------

product_summary = df.groupby("Product").agg({
    "Quantity": "sum",
    "TotalPrice": "sum"
}).reset_index()

# Plot 3: Total Revenue by Product
plt.figure(figsize=(10, 6))
plt.bar(product_summary["Product"], product_summary["TotalPrice"], color='green')
plt.title("Total Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("revenue_by_product.png")
plt.show()

# Plot 4: Total Quantity by Product
plt.figure(figsize=(10, 6))
plt.bar(product_summary["Product"], product_summary["Quantity"], color='skyblue')
plt.title("Total Quantity Sold by Product")
plt.xlabel("Product")
plt.ylabel("Quantity")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("quantity_by_product.png")
plt.show()

# Plot 5: Pie Chart of Product Sales Share (by Quantity)
plt.figure(figsize=(8, 8))
plt.pie(product_summary["Quantity"], labels=product_summary["Product"], autopct='%1.1f%%', startangle=140)
plt.title("Product Sales Share (by Quantity)")
plt.tight_layout()
plt.savefig("product_sales_pie_chart.png")
plt.show()

# ----------- Print Top-Selling Product -----------

top_product = product_summary.loc[product_summary["Quantity"].idxmax()]
print(f"📌 Top-selling product: {top_product['Product']} with {top_product['Quantity']} units sold.")

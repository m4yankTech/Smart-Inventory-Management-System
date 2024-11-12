import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from scipy.optimize import minimize

# Step 1: Load Data
data = pd.read_csv("C:\\Users\\shend\\Downloads\\solar\\inventory_data.csv")
data['Date'] = pd.to_datetime(data['Date'])

# Streamlit App Setup
st.title("Smart Inventory Management System")

# Show raw data
st.write("## Raw Inventory Data")
st.write(data.head())

# Step 2: Data Preprocessing for Time Series Forecasting
# Aggregate sales data to daily levels for each product
sales_data = data.groupby(['Date', 'Product_ID'])['Sales'].sum().unstack(fill_value=0)

# Display data for selected product
product_id = st.selectbox("Select Product ID", sales_data.columns)
st.write(f"Sales Data for Product ID: {product_id}")
st.line_chart(sales_data[product_id])

# Step 3: Demand Forecasting Model
st.write("## Demand Forecasting using Exponential Smoothing")
# Remove seasonal component if there's insufficient data for it
model = ExponentialSmoothing(sales_data[product_id], trend="add", seasonal=None)
fitted_model = model.fit()
forecast = fitted_model.forecast(14)  # Forecast next 14 days

# Plot Forecast
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(sales_data[product_id], label="Historical Sales")
ax.plot(forecast, label="Forecast", linestyle='--')
ax.set_title("Sales Forecast")
ax.legend()
st.pyplot(fig)


# Step 4: Inventory Optimization - Calculate Safety Stock and Reorder Point
# Safety stock = z * σ * √LT, where z is the service level factor, σ is the demand std dev, LT is lead time
# Reorder Point (ROP) = (Average Daily Demand * Lead Time) + Safety Stock

# Parameters
lead_time = data[data['Product_ID'] == product_id]['Lead_Time'].iloc[0]  # Get lead time for product
avg_daily_demand = sales_data[product_id].mean()
demand_std_dev = sales_data[product_id].std()
service_level = 1.65  # Service level for 95% (z = 1.65)

# Safety Stock Calculation
safety_stock = service_level * demand_std_dev * np.sqrt(lead_time)

# Reorder Point Calculation
reorder_point = (avg_daily_demand * lead_time) + safety_stock

# Display Results
st.write(f"**Product ID {product_id}**")
st.write(f"Average Daily Demand: {avg_daily_demand:.2f}")
st.write(f"Demand Standard Deviation: {demand_std_dev:.2f}")
st.write(f"Safety Stock: {safety_stock:.2f}")
st.write(f"Reorder Point: {reorder_point:.2f}")

# Optimization: Inventory Cost Minimization
holding_cost_per_unit = st.number_input("Enter Holding Cost per Unit", min_value=0.0, value=0.5)
stockout_cost_per_unit = st.number_input("Enter Stockout Cost per Unit", min_value=0.0, value=1.5)

# Define the cost function for optimization
def inventory_cost(order_qty):
    holding_cost = holding_cost_per_unit * order_qty
    stockout_risk = np.maximum(0, avg_daily_demand * lead_time + safety_stock - order_qty) * stockout_cost_per_unit
    return holding_cost + stockout_risk

# Optimize for the optimal order quantity
result = minimize(inventory_cost, x0=[avg_daily_demand * lead_time], bounds=[(0, None)])
optimal_order_qty = result.x[0]

st.write(f"Optimal Order Quantity: {optimal_order_qty:.2f} units")

# Step 5: Real-Time Dashboard for Inventory Monitoring
st.write("## Inventory Monitoring Dashboard")
st.write(f"Reorder Point: {reorder_point:.2f} units")
st.write(f"Safety Stock Level: {safety_stock:.2f} units")
st.write(f"Optimal Order Quantity: {optimal_order_qty:.2f} units")

st.write("### Current Stock Level")
current_stock = data[data['Product_ID'] == product_id]['Stock_Level'].iloc[-1]
st.write(f"Current Stock Level: {current_stock} units")

# Check if reorder is needed
if current_stock < reorder_point:
    st.warning("Reorder recommended! Current stock level is below the reorder point.")
else:
    st.success("Stock level is sufficient.")

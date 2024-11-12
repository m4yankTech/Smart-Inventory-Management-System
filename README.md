# Smart-Inventory-Management-System
The Smart Inventory Management System optimizes stock levels and forecasts demand using data science. It includes demand forecasting, inventory optimization to minimize costs, and a real-time dashboard for tracking stock, forecasts, and reorder points—enhancing supply chain efficiency.

Steps to Run the Code
Clone the Repository:

bash
Copy code
git clone <repository_url>
cd <repository_name>
Install Dependencies: Ensure you have the required packages. Install them using:

bash
Copy code
pip install -r requirements.txt
Prepare the Dataset: Place the inventory data CSV file in the specified path:

plaintext
Copy code
C:\Users\shend\Downloads\solar\inventory_data.csv
Make sure it includes columns such as Date, Product_ID, Sales, Lead_Time, and Stock_Level.

Run the Application: Start the Streamlit application with:

bash
Copy code
streamlit run inventory_management.py
Interact with the Dashboard:

View sales data trends and demand forecasts.
Access inventory optimization insights, including reorder points and safety stock.
Modify parameters like holding and stockout costs to see updated recommendations.

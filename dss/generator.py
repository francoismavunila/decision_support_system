import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Constants
products = {
    "bread": {"product_id": 1, "base_price": 1.0, "base_sales": 50},
    "softdrinks": {"product_id": 2, "base_price": 1.5, "base_sales": 70},
    "snacks": {"product_id": 3, "base_price": 2.0, "base_sales": 30},
}

holidays = [
    "2023-01-01", "2023-01-02", "2023-02-21", "2023-04-07", "2023-04-08", 
    "2023-04-09", "2023-04-10", "2023-04-18", "2023-05-01", "2023-05-25", 
    "2023-08-14", "2023-08-15", "2023-08-23", "2023-12-22", "2023-12-25", 
    "2023-12-26"
]

school_holidays = [
    ("2023-03-31", "2023-05-05"), ("2023-08-04", "2023-09-01"), ("2023-12-01", "2024-01-05")
]

# Initialize the DataFrame
date_range = pd.date_range(start="2023-01-01", end="2023-12-31")
data = []

# Function to adjust sales based on holidays and other factors
def adjust_sales(base_sales, date_str, product_name):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    sales = base_sales
    
    # Holiday adjustments
    if date_str in holidays:
        sales *= 1.5  # 50% increase on holidays
    
    # School holiday adjustments
    for start, end in school_holidays:
        if start <= date_str <= end:
            sales *= 1.2  # 20% increase during school holidays
    
    # Weather adjustments for soft drinks
    if product_name == "softdrinks" and date.month in [5, 6, 7]:
        sales *= 0.7  # 30% decrease in winter

    return int(sales)

# Generate data for each day and each product
for single_date in date_range:
    date_str = single_date.strftime("%Y-%m-%d")
    
    for product_name, details in products.items():
        product_id = details["product_id"]
        base_price = details["base_price"]
        base_sales = details["base_sales"]
        
        units_sold = adjust_sales(base_sales, date_str, product_name)
        price = round(base_price * (0.95 + 0.1 * random.random()), 2)  # Randomize price slightly
        
        data.append([product_id, date_str, units_sold, price])

# Create DataFrame and save to CSV
df = pd.DataFrame(data, columns=["product_id", "date", "units_sold", "price"])
csv_file_path = "./sales_data_2023.csv"
df.to_csv(csv_file_path, index=False)
csv_file_path

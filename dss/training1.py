import pandas as pd
from sklearn.model_selection import train_test_split

# Load the dataset
df = pd.read_csv('/mnt/data/sales_data_2023.csv')

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

# Extract day of the week
df['day_of_week'] = df['date'].dt.dayofweek

# Add holiday indicator
holidays = [
    "2023-01-01", "2023-01-02", "2023-02-21", "2023-04-07", "2023-04-08", 
    "2023-04-09", "2023-04-10", "2023-04-18", "2023-05-01", "2023-05-25", 
    "2023-08-14", "2023-08-15", "2023-08-23", "2023-12-22", "2023-12-25", 
    "2023-12-26"
]
df['is_holiday'] = df['date'].isin(pd.to_datetime(holidays)).astype(int)

# Add season indicator (1: Winter, 0: Other)
df['is_winter'] = df['date'].dt.month.isin([5, 6, 7]).astype(int)

# Add season indicator (1: Summer, 0: Other)
df['is_summer'] = df['date'].dt.month.isin([12, 1, 2]).astype(int)

# Drop the original date column
df.drop(columns=['date'], inplace=True)

# One-hot encode the product_id
df = pd.get_dummies(df, columns=['product_id'])

# Define the features and target variable
X = df.drop(columns=['units_sold', 'price'])
y = df['units_sold']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Display the first few rows of the prepared data
X_train.head()

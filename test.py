import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Sample data
data = {
    'size': [10985, 23936, 6523, 15824, 3489, 2598, 12230],
    'rental_rate': [44, 44, 44, 45, 45, 46, 46],
    'year_built': [2021] * 7,
    'total_building_size': [589945] * 7
}

# Create a DataFrame
df = pd.DataFrame(data)

# Define features (X) and target (y)
X = df[['size', 'year_built', 'total_building_size']]
y = df['rental_rate']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create the model
model = LinearRegression()

# Train the model
model.fit(X_train, y_train)

# Predict rental rates
y_pred = model.predict(X_test)

# Display coefficients and intercept
print("Coefficients:", model.coef_)
print("Intercept:", model.intercept_)

# Display predictions
print("Predicted rental rates:", y_pred)

# prompt: k lets get this setup for multiple linear regression. i want only the miles distance ones. i want city made into a categorical variable with logan being the default. i want space_category split into categorical variable with warehouse being default. i want the variables renamed to more friendly versions. i want _price_per_month_for_min_SF to be the first one seems that will be the predictor. i want all the ones that don't start with an underscore removed.

import pandas as pd

# Assuming 'spaces_df' is your DataFrame
# Create a copy to avoid modifying the original DataFrame
df = spaces_df.copy()

# Select only the specified columns and rename for clarity
# All columns that don't start with "_" were removed as requested
df = df[[
    '_price_per_month_for_min_SF',
    '_distance_in_miles_to_city_hotspot',
    '_distance_in_miles_to_nearest_heavily_trafficked_road',
    '_distance_in_miles_to_city_center_line',
    '_city',
    '_space_category',
    '_months_since_listed',
    '_min_size_SF',
    '_years_since_built'
]].rename(columns={
    '_price_per_month_for_min_SF': 'price_per_sqft',
    '_distance_in_miles_to_city_hotspot': 'distance_to_hotspot',
    '_distance_in_miles_to_nearest_heavily_trafficked_road': 'distance_to_road',
    '_distance_in_miles_to_city_center_line': 'distance_to_center',
    '_city': 'city',
    '_space_category': 'space_category',
    '_months_since_listed': 'months_since_listed',
    '_min_size_SF': 'min_size_sqft',
    '_years_since_built': 'years_since_built'
})

# Convert 'city' to categorical with 'Logan' as the default
df['city'] = pd.Categorical(df['city'], categories=df['city'].unique(), ordered=True)
df['city'] = df['city'].fillna('Logan')

# Convert 'space_category' to categorical with 'Warehouse' as the default
df['space_category'] = pd.Categorical(df['space_category'], categories=df['space_category'].unique(), ordered=True)
df['space_category'] = df['space_category'].fillna('warehouse/industrial')

# Display first few rows of the modified DataFrame
print(df.head())
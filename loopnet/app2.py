import streamlit as st
import pandas as pd
import statsmodels.api as sm
import numpy as np
from geopy.distance import geodesic
import folium
from streamlit_folium import st_folium

# Load the dataset
@st.cache
def load_data():
    return pd.read_csv('/Users/light/code/fall2024/data6500/loopnet/final7.csv')  # Update path if necessary

spaces_df = load_data()

# Verify required columns are present
required_columns = ['price_per_month', 'min_size_sqft', 'years_since_built', 'space_type', 'county']
missing_cols = [col for col in required_columns if col not in spaces_df.columns]
if missing_cols:
    st.error(f"Missing columns in the dataset: {', '.join(missing_cols)}")
    st.stop()

# Define the model
def build_model(data):
    # Ensure categorical variables are treated as such
    data = pd.get_dummies(data, columns=['space_type', 'county'], drop_first=True)
    y = data['price_per_month']
    X = data.drop(columns=['price_per_month'])
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()
    return model, X.columns

model, model_features = build_model(spaces_df)

# Sidebar inputs for predictions
st.sidebar.header("Prediction Input Parameters")
sqft = st.sidebar.number_input("Min Size (sqft)", min_value=100, max_value=10000, value=2000)
years_since_built = st.sidebar.number_input("Years Since Built", min_value=0, max_value=100, value=10)
space_type = st.sidebar.selectbox("Space Type", spaces_df['space_type'].unique())
county = st.sidebar.selectbox("County", spaces_df['county'].unique())

# Prepare input data for prediction
def prepare_input(sqft, years_since_built, space_type, county):
    input_data = {
        'min_size_sqft': [sqft],
        'years_since_built': [years_since_built],
        **{f"space_type_{space_type}": [1]},
        **{f"county_{county}": [1]}
    }
    input_df = pd.DataFrame(input_data)
    for feature in model_features:
        if feature not in input_df.columns:
            input_df[feature] = 0
    input_df = sm.add_constant(input_df, has_constant='add')
    return input_df

input_df = prepare_input(sqft, years_since_built, space_type, county)

# Display prediction result
st.title("Commercial Rental Price Prediction")
st.write("This application predicts rental prices for commercial spaces based on features like size, location, and type.")

try:
    prediction = model.get_prediction(input_df.iloc[0])
    prediction_summary = prediction.summary_frame(alpha=0.05)
    st.write("Predicted Monthly Rental Price (with 95% CI):")
    st.write(prediction_summary[['mean', 'mean_ci_lower', 'mean_ci_upper']])
except Exception as e:
    st.error(f"Error in prediction: {e}")

# Display model summary
with st.expander("View Full Model Summary"):
    st.write(model.summary())

# Display the data in a table
st.subheader("Dataset Overview")
st.dataframe(spaces_df.head())

# Add Folium map for visualization
st.subheader("Geographical Distribution of Listings")
mymap = folium.Map(location=[41.7369, -111.8338], zoom_start=8)
for idx, row in spaces_df.iterrows():
    coords = eval(row['coordinates']) if isinstance(row['coordinates'], str) else row['coordinates']
    folium.Marker(
        location=[coords[1], coords[0]],  # Latitude, Longitude
        popup=f"{row['space_type']}, ${row['price_per_month']}/month",
        tooltip=f"County: {row['county']}, Price: ${row['price_per_month']}"
    ).add_to(mymap)

st_folium(mymap, width=700, height=500)

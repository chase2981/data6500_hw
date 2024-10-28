import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
import seaborn as sns

# Load data and model (make sure to load your processed data)
@st.cache
def load_data():
    return pd.read_csv('/Users/light/code/fall2024/data6500/loopnet/final7.csv')  # Update path if needed

spaces_df = load_data()

# Fit the model traditionally
model = sm.OLS.from_formula(
    "price_per_month ~ min_size_sqft + years_since_built + C(space_type) + C(county)",
    data=spaces_df
).fit()

# Sidebar for input parameters
st.sidebar.header("Prediction Input Parameters")
sqft = st.sidebar.number_input("Min Size (sqft)", min_value=100, max_value=10000, value=2000)
years_since_built = st.sidebar.number_input("Years Since Built", min_value=0, max_value=100, value=10)
space_type = st.sidebar.selectbox("Space Type", spaces_df['space_type'].unique())
county = st.sidebar.selectbox("County", spaces_df['county'].unique())

# Prepare input data for prediction
def prepare_input(sqft, years_since_built, space_type, county):
    data = {
        'min_size_sqft': [sqft],
        'years_since_built': [years_since_built],
        'space_type': [space_type],
        'county': [county]
    }
    df = pd.DataFrame(data)
    df = pd.get_dummies(df, columns=['space_type', 'county'], drop_first=True)
    for col in model.model.exog_names:
        if col not in df.columns:
            df[col] = 0
    df = df[model.model.exog_names]
    return df

# Get prediction interval
def get_prediction_interval(input_df):
    prediction = model.get_prediction(input_df)
    return prediction.summary_frame(alpha=0.05)[['mean', 'obs_ci_lower', 'obs_ci_upper']]

# Prediction Output
st.title("Commercial Rental Price Prediction")
st.markdown("""
This application helps to predict rental prices for commercial spaces based on features like size, location, and type.
Use the input parameters in the sidebar to get a price prediction with confidence intervals.
""")

# Prepare input and display prediction result
input_df = prepare_input(sqft, years_since_built, space_type, county)
try:
    pred_result = get_prediction_interval(input_df)
    st.write("Predicted Monthly Rental Price (with 95% Prediction Interval):")
    st.write(pred_result)
except Exception as e:
    st.error(f"Error in prediction: {e}")

# Show summary of findings
st.header("Model Summary and Findings")
st.markdown("### Key Findings:")
st.write("1. **Space Size** is a significant predictor, with larger spaces commanding higher rents.")
st.write("2. **Space Type** influences rent - Office spaces generally have higher rents than other types.")
st.write("3. **Location (County)** also impacts rent, with some counties, like Salt Lake, generally having higher rates.")

# Show OLS regression summary
with st.expander("View Full Model Summary"):
    st.write(model.summary())

# Data Visualization Section
st.header("Data Visualizations")

# Plot for rental prices per county
st.subheader("Rental Prices by County")
fig, ax = plt.subplots()
sns.boxplot(data=spaces_df, x='county', y='price_per_month', ax=ax)
plt.xticks(rotation=90)
st.pyplot(fig)

# Show heatmap and hotspots using Folium
st.subheader("Geographical Analysis of Rental Prices")
st.markdown("The map below shows hotspots of high rental prices across different locations.")

# # Create Folium map
# latitude, longitude = 41.7369, -111.8338
# mymap = folium.Map(location=[latitude, longitude], zoom_start=8, tiles='CartoDB dark_matter')
# for idx, row in spaces_df.iterrows():
#     coords = eval(row['coordinates']) if isinstance(row['coordinates'], str) else row['coordinates']
#     folium.Marker(
#         location=[coords[1], coords[0]],  # Latitude, Longitude
#         popup=f"{row['space_type']}, ${row['price_per_month']}/month",
#         tooltip=f"County: {row['county']}, Price: ${row['price_per_month']}"
#     ).add_to(mymap)

# # Display the map in Streamlit
# st_folium(mymap, width=700, height=500)

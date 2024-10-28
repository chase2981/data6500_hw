import streamlit as st
import pandas as pd
import numpy as np
import statsmodels.api as sm
from PIL import Image

@st.cache
def load_data():
    return pd.read_csv('/Users/light/code/fall2024/data6500/loopnet/final7.csv')  # Update path if needed

spaces_df = load_data()

# Load model and data (ensure you have a model ready in the same directory)
# You may need to adjust the model loading path
model = sm.OLS.from_formula("price_per_month ~ min_size_sqft + years_since_built + C(space_type) + C(county)", data=spaces_df).fit()

# Define properties with images and details
properties = {
    "Property 1": {
        "image": "190347061_299253608411743_1849517218867124353_n.jpg",  # First uploaded image
        "space_type": "Flex",
        "min_size_sqft": 2710,
        "years_since_built": 17,
        "months_since_listed": 0,
        "county": "Cache County",
    },
    "Property 2": {
        "image": "248550568_420216343012514_1667664650711490342_n.jpg",  # Second uploaded image
        "space_type": "Retail",
        "min_size_sqft": 1600,
        "years_since_built": 17,
        "months_since_listed": 0,
        "county": "Cache County",
    },
    "Property 3": {
        "image": "190939485_313054793708581_8522967930423099646_n.jpg",  # Third uploaded image
        "space_type": "Office",
        "min_size_sqft": 2600,
        "years_since_built": 17,
        "months_since_listed": 0,
        "county": "Cache County",
    }
}

# Function to make predictions based on selected property details
def predict_price(min_size_sqft, years_since_built, space_type, county, months_since_listed=0):
    data = {
        "min_size_sqft": [min_size_sqft],
        "years_since_built": [years_since_built],
        "space_type": [space_type],
        "county": [county],
        "months_since_listed": [months_since_listed]
    }
    df = pd.DataFrame(data)
    df = pd.get_dummies(df, columns=["space_type", "county"], drop_first=True)
    for col in model.model.exog_names:
        if col not in df.columns:
            df[col] = 0
    prediction = model.get_prediction(df.iloc[0])
    return prediction.summary_frame(alpha=0.05)

# Application layout
st.title("Commercial Property Rental Prediction")
st.markdown("""
Select a property below to view its rental prediction. Each property has unique characteristics that factor into its estimated price.
""")

# Display images as clickable options for properties
selected_property = None
for prop_name, details in properties.items():
    col = st.columns(1)[0]
    with col:
        image = Image.open(details["image"])
        if st.button(prop_name, help="Click to select this property"):
            selected_property = prop_name

# Prediction and display details for the selected property
if selected_property:
    details = properties[selected_property]
    st.subheader(f"{selected_property} - {details['space_type']} Space")
    st.image(details["image"], use_column_width=True)
    
    st.write(f"**Space Type:** {details['space_type']}")
    st.write(f"**Size (sq ft):** {details['min_size_sqft']}")
    st.write(f"**Years Since Built:** {details['years_since_built']}")
    st.write(f"**County:** {details['county']}")
    
    # Get the prediction
    pred_result = predict_price(
        details["min_size_sqft"],
        details["years_since_built"],
        details["space_type"],
        details["county"],
        details["months_since_listed"]
    )
    
    st.write("### Predicted Monthly Rental Price")
    st.write(pred_result[['mean', 'mean_ci_lower', 'mean_ci_upper']])

import streamlit as st
import pandas as pd
import statsmodels.api as sm
from PIL import Image

# Load your dataset
unit_df = pd.read_csv('/Users/light/code/fall2024/data6500/loopnet/final7.csv')  # Update with the actual file path

# Prepare the data with Cache County and Industrial as reference categories
df = pd.get_dummies(unit_df, columns=['space_type', 'county'], dtype=float).drop(columns=['space_type_Industrial', 'county_Cache County'])

# Set up the target variable and features
y = df['price_per_month']
X_full = sm.add_constant(df[['min_size_sqft', 'years_since_built', 'months_since_listed', 
                             'space_type_Flex', 'space_type_Office', 'space_type_Office/Medical', 
                             'space_type_Office/Retail', 'space_type_Retail', 'county_Box Elder County', 
                             'county_Davis County', 'county_Iron County', 'county_Uintah County', 
                             'county_Wasatch County', 'county_Weber County', 'county_Salt Lake County']])

# Fit the model
mod_full = sm.OLS(y, X_full)
res_full = mod_full.fit()

# Define properties with images and details
properties = {
    "Property 1": {
        "image": "190347061_299253608411743_1849517218867124353_n.jpg",
        "space_type": "Flex",
        "min_size_sqft": 2710,
        "years_since_built": 17,
        "months_since_listed": 0,
        "county": "Cache County",
    },
    "Property 2": {
        "image": "248550568_420216343012514_1667664650711490342_n.jpg",
        "space_type": "Retail",
        "min_size_sqft": 1600,
        "years_since_built": 17,
        "months_since_listed": 0,
        "county": "Cache County",
    },
    "Property 3": {
        "image": "190939485_313054793708581_8522967930423099646_n.jpg",
        "image2": "before.jpg",
        "space_type": "Office",
        "min_size_sqft": 2000,
        "years_since_built": 17,
        "months_since_listed": 0,
        "county": "Cache County",
    }
}

# Prediction function with dynamic variable handling
def predict_price(min_size_sqft, years_since_built, months_since_listed, space_type, county):
    # Prepare the input row with 0's for dummy variables not selected
    data = {
        "const": 1,
        "min_size_sqft": min_size_sqft,
        "years_since_built": years_since_built,
        "months_since_listed": months_since_listed,
        "space_type_Flex": int(space_type == "Flex"),
        "space_type_Office": int(space_type == "Office"),
        "space_type_Office/Medical": int(space_type == "Office/Medical"),
        "space_type_Office/Retail": int(space_type == "Office/Retail"),
        "space_type_Retail": int(space_type == "Retail"),
        "county_Box Elder County": int(county == "Box Elder County"),
        "county_Davis County": int(county == "Davis County"),
        "county_Iron County": int(county == "Iron County"),
        "county_Uintah County": int(county == "Uintah County"),
        "county_Wasatch County": int(county == "Wasatch County"),
        "county_Weber County": int(county == "Weber County"),
        "county_Salt Lake County": int(county == "Salt Lake County")
    }
    input_df = pd.DataFrame([data])
    
    # Get prediction with confidence intervals
    pred = res_full.get_prediction(input_df.iloc[0])
    pred_summary = pred.summary_frame(alpha=0.05)
    mean_pred = pred_summary['mean'].values[0]
    lower_bound = pred_summary['mean_ci_lower'].values[0]
    upper_bound = pred_summary['mean_ci_upper'].values[0]
    
    return mean_pred, lower_bound, upper_bound

# Streamlit Layout
st.title("Commercial Property Rental Price Prediction")
st.markdown("""
Select a property below to view its rental prediction. Each property has unique characteristics that factor into its estimated price.
""")

# Image.open('main.jpg')
st.image('main.jpg', use_column_width=True)

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

    if details.get('image2', None) is not None:
        st.image(details["image2"], use_column_width=True)

    
    st.write(f"**Space Type:** {details['space_type']}")
    st.write(f"**Size (sq ft):** {details['min_size_sqft']}")
    st.write(f"**Years Since Built:** {details['years_since_built']}")
    st.write(f"**County:** {details['county']}")
    st.write(f"**Months Since Listed:** {details['months_since_listed']}")
    
    # Get the prediction
    mean_pred, lower_bound, upper_bound = predict_price(
        details["min_size_sqft"],
        details["years_since_built"],
        details["months_since_listed"],
        details["space_type"],
        details["county"]
    )
    
    # Display the formatted prediction result
    st.write("### Predicted Monthly Rental Price")
    st.write(f"The predicted rental price for this property is **${mean_pred:,.2f}** per month.")
    st.write(f"With a 95% confidence interval, this property's price could range from **${lower_bound:,.2f}** to **${upper_bound:,.2f}** per month.")

    # Extract coefficients and display model equation
    coef = res_full.params
    model_equation = "Price per Month = "

    # Constructing the equation by iterating through coefficients
    terms = [f"{coef['const']:.2f}"]  # Start with the intercept
    for var, val in coef.items():
        if var != 'const':
            terms.append(f"{val:+.2f} * {var}")

    model_equation += " ".join(terms)

    # Display model equation in Streamlit
    st.write("### Model Equation")
    st.write(model_equation)

    # Fitted values for the original dataset
    fitted_values = res_full.fittedvalues
    unit_df['Fitted Price per Month'] = fitted_values

    # Show fitted values as a table in Streamlit
    st.write("### Fitted Values")
    st.write(unit_df[['min_size_sqft', 'years_since_built', 'months_since_listed', 'price_per_month', 'Fitted Price per Month']].head())



# Collapsible panel for model summary
with st.expander("View Model Summary"):
    st.write(res_full.summary())




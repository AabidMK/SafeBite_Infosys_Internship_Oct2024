import streamlit as st
import pandas as pd
import requests

# Streamlit App Configuration
st.set_page_config(page_title="Food Allergen Prediction", layout="centered")

# Styling and Page Header
st.markdown(
    """
    <style>
        body { background-color: #F4F6F7; }
        .main-content { background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); }
        .title-header { text-align: center; font-size: 28px; font-weight: bold; color: #2E86C1; margin-bottom: 5px; }
        .sub-header { text-align: center; font-size: 18px; color: #566573; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="main-content">
        <div class="title-header">Food Allergen Prediction</div>
        <div class="sub-header">Predict allergens in food products based on their attributes</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# Input Form
st.subheader("Enter Details for Prediction")
with st.form("prediction_form"):
    col1, col2 = st.columns(2)

    with col1:
        food_product = st.text_input("Food Product")
        sweetener = st.text_input("Sweetener")
        seasoning = st.text_input("Seasoning")
        price = st.number_input("Price ($)", min_value=0.0, step=0.01)

    with col2:
        main_ingredient = st.text_input("Main Ingredient")
        fat_or_oil = st.text_input("Fat/Oil")
        allergens = st.text_input("Allergens")
        customer_rating = st.number_input("Customer rating (Out of 5)", min_value=0.0, max_value=5.0, step=0.1)

    submitted = st.form_submit_button("Predict")

# Prediction Logic
if submitted:
    # Create Input Data Dictionary
    input_data = {
        "Food Product": food_product,
        "Main Ingredient": main_ingredient,
        "Sweetener": sweetener,
        "Fat/Oil": fat_or_oil,
        "Seasoning": seasoning,
        "Allergens": allergens,
        "Price": price,
        "Customer rating": customer_rating
    }

    # Debug: Display Input Data
    st.write("Input Data Sent to Flask API:", input_data)

    try:
        # Send POST request to Flask API
        api_url = "http://127.0.0.1:5000/predict"  # Update with deployed API URL if hosted
        response = requests.post(api_url, json=input_data)

        # Check for successful response
        if response.status_code == 200:
            result = response.json()
            if result["prediction"] == 0:
                st.success("This product does not contain allergens.")
            else:
                st.error("This product contains allergens.")
        else:
            st.error(f"Error: Received response code {response.status_code}")

    except Exception as e:
        st.error(f"An error occurred while connecting to the API: {e}")

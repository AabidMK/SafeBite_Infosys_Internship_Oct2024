import streamlit as st
import requests

# Constants
API_URL = 'http://127.0.0.1:5000/predict'

# App Title and Description
st.markdown(
    """
    <h1 style="text-align: center; font-size: 35px;">🍽️ SafeBite - Allergen Detection App</h1>
    <p style="text-align: center; font-size: 18px;">
        Welcome to <b>SafeBite</b>! 🌱 <br> 
        📋 Enter the Product Details & ensure you're Safe 
    </p>
    """,
    unsafe_allow_html=True,
)

# Sidebar Information
st.sidebar.title("ℹ️ About SafeBite")
st.sidebar.markdown(
    """
    - **Project Name**: SafeBite  
    - **Purpose**: Predict allergen content in food products  
    - **Technology**: AI-powered with advanced encoding and modeling  
    """
)

# Custom CSS for Styling
st.markdown(
    """
    <style>
        .stButton>button {
            font-size: 16px !important;
            font-weight: bold !important;
            height: 50px !important;
            width: 250px !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Helper Function to Validate Inputs
def validate_input(field_name, value):
    if value.isnumeric():
        st.error(f"{field_name} should not contain numbers. Please correct it.")
        return False
    return True

# Main Form for User Input
with st.form(key="product_form"):
    error_flag = False

    # Two-column Layout
    col1, col2 = st.columns(2)

    # Input Fields in Column 1
    with col1:
        food_product = st.text_input("🥘 Food Product", placeholder="Enter food product name")
        main_ingredient = st.text_input("🌾 Main Ingredient", placeholder="Enter the main ingredient")
        sweetener = st.text_input("🍯 Sweetener", placeholder="Enter the sweetener used")
        fat_oil = st.text_input("🧈 Fat/Oil", placeholder="Enter the type of fat or oil used")

        # Validate Inputs in Column 1
        for field_name, value in [
            ("Food Product", food_product),
            ("Main Ingredient", main_ingredient),
            ("Sweetener", sweetener),
            ("Fat/Oil", fat_oil),
        ]:
            if not validate_input(field_name, value):
                error_flag = True

    # Input Fields in Column 2
    with col2:
        seasoning = st.text_input("🧂 Seasoning", placeholder="Enter the seasoning used")
        allergens = st.text_input("⚠️ Allergens", placeholder="List potential allergens (if any)")
        price = st.number_input("💲 Price ($)", min_value=0.0, step=0.1, format="%.2f")
        customer_rating = st.number_input(
            "⭐ Customer Rating (Out of 5)", min_value=0.0, max_value=5.0, step=0.1
        )

        # Validate Inputs in Column 2
        for field_name, value in [("Seasoning", seasoning), ("Allergens", allergens)]:
            if not validate_input(field_name, value):
                error_flag = True

    # Submit Button
    submit_button = st.form_submit_button(label="🔍 Predict Allergens 🚀")

# Handle Form Submission
if submit_button:
    if error_flag:
        st.warning("⚠️ Please resolve all errors before submission!")
    elif not all([food_product, main_ingredient, sweetener, fat_oil, seasoning, allergens]):
        st.warning("⚠️ Please fill in all fields! If a field doesn't apply, type 'None'.")
    else:
        # Prepare Data for API Request
        user_input = {
            "Food Product": food_product,
            "Main Ingredient": main_ingredient,
            "Sweetener": sweetener,
            "Fat/Oil": fat_oil,
            "Seasoning": seasoning,
            "Allergens": allergens,
            "Price ($)": price,
            "Customer rating (Out of 5)": customer_rating,
        }

        # Send Data to API and Handle Response
        try:
            response = requests.post(API_URL, json=user_input)
            response.raise_for_status()
            prediction = response.json().get("result", "Error: No prediction received")

            if "contains allergens" in prediction:
                st.success(f"✅ {prediction}. Please proceed with caution! 🚨")
            else:
                st.success(f"❌ {prediction}. It's safe to consume! 🎉")
        except requests.exceptions.RequestException as e:
            st.error(f"Error during prediction: {e}")

# Footer
st.markdown(
    """
    <hr>
    <p style="text-align:center;">
        Built with ❤️ using Streamlit. <br>
        SafeBite® - Protecting you from hidden allergens! <br>
        Made by: <b>Ikraj Khan</b> <br>
        &copy;2024. All rights reserved.
    </p>
    """,
    unsafe_allow_html=True,
)

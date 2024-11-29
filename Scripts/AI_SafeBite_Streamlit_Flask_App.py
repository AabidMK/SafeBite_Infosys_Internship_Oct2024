import streamlit as st
import requests

# Constants
API_URL = 'http://127.0.0.1:5000/predict'

# Custom CSS
st.markdown(
    """
    <style>
        body {
            background-color: #f8f9fa;
        }
        .stButton>button {
            font-size: 16px !important;
            font-weight: bold !important;
            height: 50px !important;
            width: 100% !important;
            background-color: #007bff !important;
            color: white !important;
            border-radius: 5px !important;
        }
        .stTextInput>div>input {
            font-size: 15px !important;
            border-radius: 5px !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# App Title
st.markdown(
    """
    <h1 style="text-align: center; font-size: 36px;">🍽️ SafeBite - Allergen Detection App</h1>
    <p style="text-align: center; font-size: 18px;">
        Welcome to <b>SafeBite</b>! 🌱 <br> 
        Enter the product details below and ensure you're safe!
    </p>
    """,
    unsafe_allow_html=True,
)

# Sidebar Information
with st.sidebar:
    st.title("ℹ️ About SafeBite")
    st.markdown(
        """
        - **Project Name**: SafeBite  
        - **Purpose**: Predict allergen content in food products  
        - **Technology**: AI-powered with advanced encoding and modeling  
        """
    )
    st.divider()
    st.caption("© 2024 SafeBite. All rights reserved.")

# Helper Function to Validate Inputs
def validate_input(field_name, value):
    if value.isnumeric():
        st.error(f"{field_name} should not contain numbers. Please correct it.")
        return False
    return True

# Main Form
with st.form(key="product_form"):
    st.subheader("📋 Enter Product Details")
    col1, col2 = st.columns(2)

    with col1:
        food_product = st.text_input("🥘 Food Product", placeholder="Enter food product name")
        main_ingredient = st.text_input("🌾 Main Ingredient", placeholder="Enter the main ingredient")
        sweetener = st.text_input("🍯 Sweetener", placeholder="Enter the sweetener used")
        fat_oil = st.text_input("🧈 Fat/Oil", placeholder="Enter the type of fat or oil used")

    with col2:
        seasoning = st.text_input("🧂 Seasoning", placeholder="Enter the seasoning used")
        allergens = st.text_input("⚠️ Allergens", placeholder="List potential allergens (if any)")
        price = st.number_input("💲 Price ($)", min_value=0.0, step=0.1, format="%.2f")
        customer_rating = st.number_input(
            "⭐ Customer Rating (Out of 5)", min_value=0.0, max_value=5.0, step=0.1
        )

    st.divider()
    submit_button = st.form_submit_button(label="🔍 Predict Allergens 🚀")

# Handle Form Submission
if submit_button:
    with st.spinner("Processing your request..."):
        error_flag = False

        # Validate Inputs
        for field_name, value in [
            ("Food Product", food_product),
            ("Main Ingredient", main_ingredient),
            ("Sweetener", sweetener),
            ("Fat/Oil", fat_oil),
            ("Seasoning", seasoning),
            ("Allergens", allergens),
        ]:
            if not validate_input(field_name, value):
                error_flag = True

        if error_flag:
            st.warning("⚠️ Please resolve all errors before submission!")
        elif not all([food_product, main_ingredient, sweetener, fat_oil, seasoning, allergens]):
            st.warning("⚠️ Please fill in all fields! If a field doesn't apply, type 'None'.")
        else:
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
    <p style="text-align:center; font-size:14px;">
        Built with ❤️ using Streamlit. <br>
        SafeBite® - Protecting you from hidden allergens! <br>
        Made by: <b>Ikraj Khan</b> <br>
        &copy;2024. All rights reserved.
    </p>
    """,
    unsafe_allow_html=True,
)

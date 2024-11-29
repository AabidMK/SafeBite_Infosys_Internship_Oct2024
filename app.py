import streamlit as st
import pandas as pd
import pickle
import joblib
import requests

# URL of the Flask API
API_URL = "http://127.0.0.1:5000/predict"

# Load the model
model = joblib.load("Model/Allergen_detection.pkl")

# Load the encoder
with open('Model/leave_one_out_encoder.pkl', 'rb') as file:
    loaded_encoder = pickle.load(file)

# Sidebar for customization or branding
st.sidebar.image("Assets/logo.jpg", use_container_width=True)
st.sidebar.markdown("<p style='text-align: center; font-family: cursive; font-style: italic; font-size: 20px; color: #00ffff;'>\"Every bite should be a safe bite!\"</p>", unsafe_allow_html=True)
st.sidebar.title("SafeBite AI")
st.sidebar.write("SafeBite AI ensures food safety by predicting the presence of allergens in food products, helping individuals make informed choices.")
st.sidebar.markdown("<h3>Mission</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<p>To promote safe eating habits and reduce allergic reactions through technology.</p>", unsafe_allow_html=True)

# Main page
st.markdown("<h1 style='text-align: center; color: #ff7f50;'>Food Product Allergen Prediction</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Predict if your product is allergen-free based on its ingredients and details.</p>", unsafe_allow_html=True)

# Input fields in columns
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Product Details")
    food_product = st.text_input("Food Product", placeholder="Enter the name of the food product")
    main_ingredient = st.text_input("Main Ingredient", placeholder="Enter the main ingredient")
    sweetener = st.text_input("Sweetener", placeholder="Enter sweetener details")
    fat_oil = st.text_input("Fat/Oil", placeholder="Enter fat/oil used")

with col2:
    st.markdown("### Additional Information")
    seasoning = st.text_input("Seasoning", placeholder="Enter seasoning details")
    allergens = st.text_input("Allergens", placeholder="Specify any known allergens")
    price = st.number_input("Price ($)", min_value=0.0, format="%.2f")
    rating = st.number_input("Customer Rating (Out of 5)", min_value=0.0, max_value=5.0, value=3.0, step=0.1)

# Creating a DataFrame
data = {
    "Price ($)": price,
    "Customer rating": rating,
    "Food Product": food_product,
    "Main Ingredient": main_ingredient,
    "Sweetener": sweetener,
    "Fat/Oil": fat_oil,
    "Seasoning": seasoning,
    "Allergens": allergens,
}

# Add some space
st.markdown("<br>", unsafe_allow_html=True)

# Add predict button with effects
if st.button("🔍 Predict", help="Click to predict allergen presence"):

    try:
        # Send POST request
        response = requests.post(API_URL, json=data)

        if response.status_code == 200:
            prediction = response.json().get("Prediction", "No prediction available")
            st.markdown("---")
            st.markdown("<h3 style='text-align: center; color: #4682b4;'>Prediction Results</h3>", unsafe_allow_html=True)
            st.success(f"Prediction: {prediction}")
        else:
            st.error("Failed to get prediction from API")
    except Exception as e:
        st.error(f"Error: {str(e)}")

    

    # # Display results in a styled container
    # if prediction == 0:
    #     st.markdown(
    #         "<div style='text-align: center; background-color: #3bb143; padding: 20px; border-radius: 5px;'>"
    #         "<h3>This product contains allergens.</h3>"
    #         "</div>",
    #         unsafe_allow_html=True
    #     )
    # else:
    #     st.markdown(
    #         "<div style='text-align: center; background-color: #ff0800; padding: 20px; border-radius: 5px;'>"
    #         "<h3>This product does not contain allergens.</h3>"
    #         "</div>",
    #         unsafe_allow_html=True
    #     )

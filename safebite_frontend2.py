import streamlit as st
import pandas as pd
import pickle
import joblib
import requests

# URL of the Flask API
API_URL = "http://127.0.0.1:5000/predict"

# Load the model
model = joblib.load("../Model/Allergen_detection.pkl")

# Load the encoder
with open('../Model/leave_one_out_encoder.pkl', 'rb') as file:
    loaded_encoder = pickle.load(file)

# Set Streamlit page config
st.set_page_config(
    page_title="SafeBite AI - Allergen Detection",
    page_icon="🍽️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS for night blue theme
st.markdown(
    """
    <style>
        body {
            background-color: #001f3f;
            border-radius:20px;
            border-color: #9F4576
            color: #ffffff;
        }
        .stButton > button {
            background-color: #0074d9;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 16px;
        }
        .stTextInput > div > input {
            background-color: #001f3f;
            color: white;
        }
        .stNumberInput > div {
            background-color: #001f3f;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Main title and description
st.markdown("<h1 style='text-align: center; color: #00c4ff;'>SafeBite AI</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; font-size: 18px;'>Predict if your food product is allergen-free and ensure safety with every bite.</p>",
    unsafe_allow_html=True,
)

# Step-by-step form
with st.form("Allergen_Prediction_Form"):
    st.markdown("<h3 style='color: #00c4ff;'>1. Product Details</h3>", unsafe_allow_html=True)
    food_product = st.text_input("Food Product", placeholder="Enter the name of the food product")
    main_ingredient = st.text_input("Main Ingredient", placeholder="Enter the main ingredient")

    st.markdown("<h3 style='color: #00c4ff;'>2. Additional Ingredients</h3>", unsafe_allow_html=True)
    sweetener = st.text_input("Sweetener", placeholder="Enter sweetener details")
    fat_oil = st.text_input("Fat/Oil", placeholder="Enter fat/oil used")
    seasoning = st.text_input("Seasoning", placeholder="Enter seasoning details")

    st.markdown("<h3 style='color: #00c4ff;'>3. Known Allergens</h3>", unsafe_allow_html=True)
    allergens = st.text_input("Allergens", placeholder="Specify any known allergens")

    st.markdown("<h3 style='color: #00c4ff;'>4. Pricing & Rating</h3>", unsafe_allow_html=True)
    price = st.number_input("Price ($)", min_value=0.0, format="%.2f")
    rating = st.number_input("Customer Rating (Out of 5)", min_value=0.0, max_value=5.0, value=3.0, step=0.1)

    st.markdown("<br>", unsafe_allow_html=True)

    # Submit button
    submit = st.form_submit_button("🔍 Predict")

# Collect and send data for prediction
if submit:
    # Prepare data payload
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

    try:
        # Send POST request to the Flask API
        response = requests.post(API_URL, json=data)

        if response.status_code == 200:
            prediction = response.json().get("Prediction", "No prediction available")
            st.markdown("<h3 style='color: #00ff00; text-align: center;'>Prediction Result</h3>", unsafe_allow_html=True)
            st.success(f"Prediction: {prediction}")
        else:
            st.error("Failed to get prediction from API")
    except Exception as e:
        st.error(f"Error: {str(e)}")

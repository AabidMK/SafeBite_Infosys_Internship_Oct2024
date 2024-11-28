import streamlit as st
import pandas as pd
import joblib
import os

# Load the model and encoder from the file
encoder_path = 'C:/Users/Admin/Desktop/food_allergen_detection/Models/encoder.pkl'
model_path = 'C:/Users/Admin/Desktop/food_allergen_detection/Models/rf_model.pkl'

encoder = joblib.load(encoder_path)
rf_model = joblib.load(model_path)

# Set a title for the page
st.set_page_config(page_title='SafeBite: AI-Powered Allergen Detection in Food')

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
    }
    .stTextInput > div > div > input, .stNumberInput > div > div > input {
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ddd;
        box-shadow: 1px 1px 3px rgba(0,0,0,0.1);
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        padding: 15px 32px;
        font-size: 16px;
        margin: 20px 0px;
        border-radius: 5px;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    footer {
        text-align: center;
        padding: 10px;
        font-size: 14px;
        color: #888;
        border-top: 1px solid #ddd;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title('About SafeBite')
st.sidebar.info("""
    SafeBite is an AI-powered platform designed to detect allergens in food products.
    Enter the details of the food product, and our model will predict the presence of allergens.
""")

# Title of the application
st.title('SafeBite: AI-Powered Allergen Detection in Food')

# Create two columns for input fields
col1, col2 = st.columns(2)

with col1:
    food_product = st.text_input('Food Product')
    sweetener = st.text_input('Sweetener')
    seasoning = st.text_input('Seasoning')
    price = st.number_input('Price($)', min_value=0.0, step=0.01)

with col2:
    main_ingredient = st.text_input('Main Ingredient')
    fat_oil = st.text_input('Fat/Oil')
    allergens = st.text_input('Allergens')
    customer_rating = st.number_input('Customer Rating', min_value=0.0, max_value=5.0, step=0.1)

# When the 'Predict' button is clicked
if st.button('Predict'):
    # Check if all fields are filled
    if not all([food_product, main_ingredient, sweetener, fat_oil, seasoning, allergens, price, customer_rating]):
        st.warning('Please fill all the fields')
    else:
        # Create a dictionary from the input values
        input_data = {
            'food_product': food_product,
            'main_ingredient': main_ingredient,
            'sweetener': sweetener,
            'fat_oil': fat_oil,
            'seasoning': seasoning,
            'allergens': allergens,
            'price': price,
            'customer_rating': customer_rating
        }
        try:

         response = requests.post('http://127.0.0.1:5000/predict', json=input_data)
         result = response.json()

         if result['prediction'] == 'contains allergens':
            st.error('The food product **Contains** allergens.. Please proceed with caution! 🚨')
         else:
            st.success('The food product **Does not contains** allergens.It is safe to consume.')

        except Exception as e:
            st.error(f"Error during prediction: {e}")

# Footer
st.markdown("""
    <footer>
        &copy; 2024 SafeBite. Developed by Leena Geepalem.
    </footer>
""", unsafe_allow_html=True)

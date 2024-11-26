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
        # Create a DataFrame from the input values
        input_data = pd.DataFrame({
            'Food Product': [food_product],
            'Main Ingredient': [main_ingredient],
            'Sweetener': [sweetener],
            'Fat/Oil': [fat_oil],
            'Seasoning': [seasoning],
            'Allergens': [allergens],
            'Price': [price],
            'Customer rating': [customer_rating]
        })

        # Encode the categorical features
        categorical_columns = input_data.select_dtypes(include=['object']).columns
        input_data_encoded = encoder.transform(input_data[categorical_columns])

        # Combine the encoded features with the numerical features
        input_data = pd.concat([input_data.drop(categorical_columns, axis=1), pd.DataFrame(input_data_encoded, columns=encoder.get_feature_names_out())], axis=1)

        # Make the prediction
        prediction = rf_model.predict(input_data)

        # Display the prediction result
        if prediction[0] == 0:
            st.success('The food product **Contains** allergens.')
        else:
            st.error('The food product **Does not contains** allergens.')

# Footer
st.markdown("""
    <footer>
        &copy; 2024 SafeBite. Developed by Leena Geepalem.
    </footer>
""", unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import pickle
import joblib
import requests
from flask import Flask, request, jsonify
from threading import Thread
import os

# Flask App
app = Flask(__name__)

current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, "Allergen_detection.pkl")
encoder_path = os.path.join(current_dir,"leave_one_out_encoder.pkl")
# Load the trained model and encoder
loaded_model = joblib.load(model_path)
loaded_encoder = joblib.load(encoder_path) 

# Flask route for prediction API
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    input_data = pd.DataFrame(data, index=[0])

    # Encode categorical columns
    categorical_columns = input_data.select_dtypes(['object']).columns
    input_data_encoded = loaded_encoder.transform(input_data[categorical_columns])
    input_data = pd.concat([input_data.drop(categorical_columns, axis=1), input_data_encoded], axis=1)

    # Make prediction
    prediction = loaded_model.predict(input_data)
    result = "This product contains allergens." if prediction == 0 else "This product does not contain allergens."

    return jsonify({"Prediction": result})

# Function to run Flask app in a thread
def run_flask():
    app.run(port=5000, debug=False)

# Streamlit App
def run_streamlit():
    # URL of the Flask API
    API_URL = "http://127.0.0.1:5000/predict"

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
            body { background-color: #001f3f; color: #ffffff; }
            .stButton > button {
                background-color: #0074d9;
                color: white;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 16px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Main title and description
    st.markdown("<h1 style='text-align: center; color: #00c4ff;'>SafeBite AI</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center;'>Predict if your food product is allergen-free and ensure safety with every bite.</p>",
        unsafe_allow_html=True,
    )

    # Form for input
    with st.form("Allergen_Prediction_Form"):
        food_product = st.text_input("Food Product")
        main_ingredient = st.text_input("Main Ingredient")
        sweetener = st.text_input("Sweetener")
        fat_oil = st.text_input("Fat/Oil")
        seasoning = st.text_input("Seasoning")
        allergens = st.text_input("Allergens")
        price = st.number_input("Price ($)", min_value=0.0, format="%.2f")
        rating = st.number_input("Customer Rating (Out of 5)", min_value=0.0, max_value=5.0, value=3.0, step=0.1)
        submit = st.form_submit_button("🔍 Predict")

    if submit:
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
            response = requests.post(API_URL, json=data)
            if response.status_code == 200:
                prediction = response.json().get("Prediction", "No prediction available")
                st.success(f"Prediction: {prediction}")
            else:
                st.error("Failed to get prediction from API")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Run Flask in a thread and Streamlit in the main process
if __name__ == "__main__":
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    run_streamlit()
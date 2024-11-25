import os
import sys
import streamlit as st
from predict import load_model_and_encoder, make_prediction
from preprocess import preprocess_inputs

# Add the root directory to the system path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load the model and encoder at app start
try:
    model, encoder = load_model_and_encoder()

except Exception as e:
    st.error(f"Error loading model or encoder: {e}")
    st.stop()

# Configure Streamlit page
st.set_page_config(
    page_title="SafeBite",
    page_icon="assets/favicon.jpg",  # Path to your favicon
    layout="centered"
)

# Title and description
# st.title("Food Allergen Prediction")
# Title and description with custom CSS for centering
st.markdown("""
    <style>
    .title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
    }
    </style>
    <div class="title">Food Allergen Prediction</div>
""", unsafe_allow_html=True)

st.markdown("This app predicts whether a food product contains allergens based on its ingredients, seasoning, and other details.")

# Input Form
with st.form("prediction_form"):
    col1, col2 = st.columns(2)

    # Left column inputs
    with col1:
        food_product = st.text_input("Food Product", "Gluten-Free Chocolate Cake")
        main_ingredient = st.text_input("Main Ingredient", "Almond Flour")
        sweetener = st.text_input("Sweetener", "Coconut sugar")
        fat_oil = st.text_input("Fat/Oil", "Coconut oil")

    # Right column inputs
    with col2:
        seasoning = st.text_input("Seasoning", "Vanilla extract, Cocoa")
        allergens = st.text_input("Allergens", "Almond")
        
        # Use slider for price
        price = st.slider("Price ($)", min_value=0.01, max_value=100.0, value=10.50, step=0.1)
        
        customer_rating = st.number_input("Customer Rating (Out of 5)", min_value=0.0, max_value=5.0, value=3.0, step=0.1)

    # Submit button
    submit = st.form_submit_button("Predict")

# Prediction logic
if submit:
    # Check for mandatory fields
    if not food_product or not main_ingredient:
        st.error("⚠️ Food product name and main ingredient are mandatory fields. Please fill them in.")
    else:
        try:
            # Preprocess inputs
            input_data = preprocess_inputs(
                food_product,
                main_ingredient,
                sweetener,
                fat_oil,
                seasoning,
                allergens,
                price,
                customer_rating,
            )

            # Make prediction
            result = make_prediction(model, encoder, input_data)

            # Display the result
            if result == 1:
                st.success(f"❌ {food_product} contains allergens. Please review the ingredient list carefully.")
            else:
                st.success(f"✅ {food_product} does not contain allergens. Safe to proceed!")
        except Exception as e:
            st.error(f"⚠️ An error occurred during prediction: {e}")

# Footer with "All Rights Reserved" message
st.markdown("""
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        text-align: center;
        background-color: black;
        padding: 10px;
        color: white;
    }
    </style>
    <div class="footer">
        <p>&copy; 2024 All Rights Reserved</p>
    </div>
""", unsafe_allow_html=True)

import os
import sys
import streamlit as st
from prediction import load_model_and_encoder, make_prediction
from preprocessor import preprocess_inputs

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

# Apply custom CSS
st.markdown("""
    <style>
    body {
        background-color: #f9f9f9;
    }
    .title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        color: #4CAF50;
    }
    .form-container {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        text-align: center;
        background-color: #333;
        color: white;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<div class="title">SafeBite - Food Allergen Prediction</div>', unsafe_allow_html=True)
st.write("Use this app to predict whether a food product contains allergens based on its ingredients and details.")

# Input Form
st.markdown('<div class="form-container">', unsafe_allow_html=True)
with st.form("prediction_form"):
    # Input fields split into two columns for better layout
    col1, col2 = st.columns(2)

    with col1:
        food_product = st.text_input("Food Product", "Gluten-Free Chocolate Cake", help="Name of the food product")
        main_ingredient = st.text_input("Main Ingredient", "Almond Flour", help="Primary ingredient in the product")
        sweetener = st.text_input("Sweetener", "Coconut sugar", help="Sweetener used (if any)")
        fat_oil = st.text_input("Fat/Oil", "Coconut oil", help="Fat or oil used in the product")

    with col2:
        seasoning = st.text_input("Seasoning", "Vanilla extract, Cocoa", help="Spices or flavorings used")
        allergens = st.text_input("Known Allergens", "Almond", help="Known allergens in the product")
        price = st.slider("Price ($)", min_value=0.01, max_value=100.0, value=10.50, step=0.1, help="Price of the product")
        customer_rating = st.number_input("Customer Rating (Out of 5)", min_value=0.0, max_value=5.0, value=3.0, step=0.1, help="Customer rating (0-5)")

    submit = st.form_submit_button("Predict")

st.markdown('</div>', unsafe_allow_html=True)

# Prediction logic
if submit:
    if not food_product.strip() or not main_ingredient.strip():
        st.error("⚠️ Food product name and main ingredient are required fields. Please fill them in.")
    else:
        try:
            # Preprocess inputs
            input_data = preprocess_inputs(
                food_product.strip(),
                main_ingredient.strip(),
                sweetener.strip(),
                fat_oil.strip(),
                seasoning.strip(),
                allergens.strip(),
                price,
                customer_rating
            )

            # Make prediction
            result = make_prediction(model, encoder, input_data)

            # Display results
            if result == 1:
                st.error(f"❌ **{food_product}** contains allergens. Review the ingredient list carefully.")
            else:
                st.success(f"✅ **{food_product}** does not contain allergens. It is safe to proceed!")
        except ValueError as ve:
            st.error(f"⚠️ Invalid input: {ve}")
        except Exception as e:
            st.error(f"⚠️ An error occurred during prediction: {e}")

# Footer
st.markdown("""
    <div class="footer">
        <p>&copy; 2024 Ikraj Khan - All Rights Reserved</p>
    </div>
""", unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import joblib

# Flask API URL
FLASK_API_URL = "http://127.0.0.1:5000/predict"

# Load the trained model and encoder
model = joblib.load(r"C:\Users\ariji\SafeBite\Models\best_knn_model2.pkl")
encoder = joblib.load(r'C:\Users\ariji\SafeBite\Models\encoder2.pkl')

# App title and description
st.markdown(
    """
    <h1 style='text-align: center; font-size: 30px;'>🍴 SafeBite: Allergen Detection in Food 🍴</h1>
    """, 
    unsafe_allow_html=True
)
st.markdown("""
**SafeBite** helps users detect allergens in food based on various parameters.  
Simply fill in the details below to check if the food contains allergens.  
""")

# Input form
col1, col2 = st.columns(2)

with col1:
    food_product = st.text_input("Food Product", "Pasta")
    sweetener = st.text_input("Sweetener", "Sugar")
    price = st.number_input("Price ($)", min_value=0.0, format="%.2f", value=10.0)
    customer_rating = st.slider("Customer Rating (Out of 5)", min_value=0.0, max_value=5.0, step=0.1, value=4.5)

with col2:
    main_ingredient = st.text_input("Main Ingredient", "Wheat")
    fat_oil = st.text_input("Fat/Oil", "Olive Oil")
    seasoning = st.text_input("Seasoning", "Salt, Oregano")
    allergens = st.text_input("Known Allergens", "Gluten")

st.markdown("---")

# Predict button
if st.button("🔍 Predict Allergen Risk"):
    # Create a DataFrame for the input
    input_data = pd.DataFrame({
        'Food Product': [food_product],
        'Main Ingredient': [main_ingredient],
        'Sweetener': [sweetener],
        'Fat/Oil': [fat_oil],
        'Seasoning': [seasoning],
        'Allergens': [allergens],
        'Price ($)': [price],
        'Customer rating (Out of 5)': [customer_rating]
    })

    # Handle missing or unknown values
    input_data['Sweetener'].fillna('Unknown', inplace=True)
    input_data['Fat/Oil'].fillna('Unknown', inplace=True)
    input_data['Seasoning'].fillna('Unknown', inplace=True)
    input_data['Allergens'].fillna('Unknown', inplace=True)

    # Encode categorical features
    cat_cols = ['Food Product', 'Main Ingredient', 'Sweetener', 'Fat/Oil', 'Seasoning', 'Allergens']
    encoded_data = encoder.transform(input_data[cat_cols])
    input_data = pd.concat([input_data.drop(cat_cols, axis=1), pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out())], axis=1)

    # Make a prediction
    prediction = model.predict(input_data)

    # Display the result
    if prediction[0] == 1:
        st.error(f"⚠️ The food is likely to contain allergens.")
    else:
        st.success(f"✅ The food is unlikely to contain allergens.")

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center;'>Created by <strong>Arijit</strong></div>", unsafe_allow_html=True)

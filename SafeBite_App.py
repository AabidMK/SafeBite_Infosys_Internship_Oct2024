import streamlit as st
import requests

st.title("🍴 SafeBite: Allergen Detection in Food 🍴")

# Input fields
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

if st.button("🔍 Predict Allergen Risk"):
    url = "http://127.0.0.1:5000/predict"
    payload = {
        "Food Product": food_product,
        "Main Ingredient": main_ingredient,
        "Sweetener": sweetener,
        "Fat/Oil": fat_oil,
        "Seasoning": seasoning,
        "Allergens": allergens,
        "Price ($)": price,
        "Customer rating (Out of 5)": customer_rating
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        result = response.json()
        if result["prediction"] == 1:
            st.error(f"⚠️ The food is likely to contain allergens. (Confidence: {result['confidence']:.2f})")
        else:
            st.success(f"✅ The food is unlikely to contain allergens. (Confidence: {result['confidence']:.2f})")
    else:
        st.error(f"Error: {response.text}")

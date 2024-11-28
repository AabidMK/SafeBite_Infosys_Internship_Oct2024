import streamlit as st
import requests

# App title and description:
st.markdown("""
    <h1 style="text-align: center; font-size: 35px;">SafeBite - Allergen Detection App</h1>
    <p style="text-align: center; font-size: 18px;">Welcome to SafeBite! <br> 
    Enter the Product Details and ensure you're Safe.</p> 
""", unsafe_allow_html=True)

# Form for user input:
with st.form(key="product_form"):
    error_flag = False  # Flag to track validation errors

    # Split the inputs into two columns:
    col1, col2 = st.columns(2)

    with col1:
        food_product = st.text_input(
            "Food Product",
            placeholder="Enter the food product name",
            key="food_product"
        )
        if food_product.isnumeric():
            st.error("Food Product should not contain numbers. Please correct it.")
            error_flag = True

        main_ingredient = st.text_input(
            "Main Ingredient",
            placeholder="Enter the main ingredient",
            key="main_ingredient"
        )
        if main_ingredient.isnumeric():
            st.error("Main Ingredient should not contain numbers. Please correct it.")
            error_flag = True

        sweetener = st.text_input(
            "Sweetener",
            placeholder="Enter the sweetener used",
            key="sweetener"
        )
        if sweetener.isnumeric():
            st.error("Sweetener should not contain numbers. Please correct it.")
            error_flag = True

        fat_oil = st.text_input(
            "Fat/Oil",
            placeholder="Enter the type of fat or oil used",
            key="fat_oil"
        )
        if fat_oil.isnumeric():
            st.error("Fat/Oil should not contain numbers. Please correct it.")
            error_flag = True

    with col2:
        seasoning = st.text_input(
            "Seasoning",
            placeholder="Enter the seasoning used",
            key="seasoning"
        )
        if seasoning.isnumeric():
            st.error("Seasoning should not contain numbers. Please correct it.")
            error_flag = True

        allergens = st.text_input(
            "Allergens",
            placeholder="List potential allergens (if any)",
            key="allergens"
        )
        if allergens.isnumeric():
            st.error("Allergens should not contain numbers. Please correct it.")
            error_flag = True

        # Numeric inputs for Price and Customer Rating:
        price = st.number_input(
            "Price ($)",
            min_value=0.0,
            step=0.1,
            format="%.2f"
        )

        customer_rating = st.number_input(
            "Customer Rating (Out of 5)",
            min_value=0.0,
            max_value=5.0,
            step=0.1
        )

    # Predict Allergens button:
    col1, col2, col3 = st.columns([1, 1.3, 1])

    with col2:
        submit_button = st.form_submit_button(label="Predict Allergens")

# On form submission:
if submit_button:
    if error_flag:
        st.warning("Please resolve all errors before submission!")
    elif not all([food_product, main_ingredient, sweetener, fat_oil, seasoning, allergens]):
        st.warning("Please fill in all fields! If a field doesn't apply, type 'None'.")
    else:
        # User input in a JSON format:
        user_input = {
            "Food Product": food_product,
            "Main Ingredient": main_ingredient,
            "Sweetener": sweetener,
            "Fat/Oil": fat_oil,
            "Seasoning": seasoning,
            "Allergens": allergens,
            "Price ($)": price,
            "Customer rating (Out of 5)": customer_rating
        }

        # Send the data to the Flask API for prediction:
        api_url = 'http://127.0.0.1:5000/predict'

        try:
            response = requests.post(api_url, json=user_input)
            prediction = response.json()["result"]

            # Display the result based on prediction:
            if "contains allergens" in prediction:
                st.success(f"{prediction}. Please proceed with caution!")
            else:
                st.success(f"{prediction}. It's safe to consume!")
        except Exception as e:
            st.error(f"Error during prediction: {e}")
import pandas as pd

def preprocess_inputs(
    food_product, main_ingredient, sweetener, fat_oil, seasoning, allergens, price, customer_rating
):
    """
    Preprocess the input data for model prediction.
    """
        
    # Handle empty or missing inputs
    sweetener = sweetener if sweetener.strip() else "None"
    fat_oil = fat_oil if fat_oil.strip() else "None"
    seasoning = seasoning if seasoning.strip() else "None"
    allergens = allergens if allergens.strip() else "None"

    data = pd.DataFrame([{
        "Food Product": food_product,
        "Main Ingredient": main_ingredient,
        "Sweetener": sweetener,
        "Fat/Oil": fat_oil,
        "Seasoning": seasoning,
        "Allergens": allergens,
        'Price ($)': price, 
        'Customer rating (Out of 5)': customer_rating 
    }])

    return data

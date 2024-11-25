from flask import Flask, request, jsonify
from app.preprocess import preprocess_inputs
from app.predict import load_model_and_encoder, make_prediction
import os

# Initialize the Flask app
app = Flask(__name__)

# Load model and encoder (for serving the predictions)
model, encoder = load_model_and_encoder()

@app.route('/')
def home():
    """
    Health check endpoint.
    """
    return jsonify({"message": "Welcome to the Food Allergen Prediction API!"}), 200

@app.route('/predict', methods=['POST'])
def predict_allergen():
    """
    Predict if a food product contains allergens based on input data.
    """
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Validate required fields
        required_fields = ['food_product', 'main_ingredient', 'price', 'customer_rating']
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

        # Replace empty optional fields with "None"
        optional_fields = ['sweetener', 'fat_oil', 'seasoning', 'allergens']
        for field in optional_fields:
            if field in data and not data[field].strip():
                data[field] = "None"

        # Extract fields from the JSON
        food_product = data['food_product']
        main_ingredient = data['main_ingredient']
        sweetener = data.get('sweetener', 'None')
        fat_oil = data.get('fat_oil', 'None')
        seasoning = data.get('seasoning', 'None')
        allergens = data.get('allergens', 'None')
        price = float(data['price'])
        customer_rating = float(data['customer_rating'])

        # Preprocess the input data
        input_data = preprocess_inputs(
            food_product,
            main_ingredient,
            sweetener,
            fat_oil,
            seasoning,
            allergens,
            price,
            customer_rating
        )

        # Make the prediction
        result = make_prediction(model, encoder, input_data)

        # Return the prediction in the response
        prediction_message = "allergen detected" if result == 1 else "no allergen detected"
        return jsonify({"prediction": prediction_message, "product": food_product}), 200

    except KeyError as e:
        return jsonify({"error": f"Missing or invalid key in input: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Error making prediction: {str(e)}"}), 500

if __name__ == '__main__':
    # Use environment variables for configuration
    debug_mode = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(debug=debug_mode)


'''
Invoke-WebRequest -Uri http://127.0.0.1:5000/predict `
    -Method POST `
    -Headers @{"Content-Type" = "application/json"} `
    -Body '{
        "food_product": "Gluten-Free Chocolate Cake",
        "main_ingredient": "Almond Flour",
        "sweetener": "Coconut sugar",
        "fat_oil": "Coconut oil",
        "seasoning": "Vanilla extract, Cocoa",
        "allergens": "Almond",
        "price": 10.50,
        "customer_rating": 4.5
    }'



    
    Invoke-WebRequest -Uri http://127.0.0.1:5000/predict `
    -Method POST `
    -Headers @{"Content-Type" = "application/json"} `
    -Body '{
         "food_product": "Lentil Soup",
         "main_ingredient": "Lentil",
         "sweetener": "None",
         "fat_oil": "Olive oil",
         "seasoning": "Herbs de Provence",
         "allergens": "None",
         "price": 4.50,
         "customer_rating": 4.0
    }'


'''



'''
curl.exe -X POST -H "Content-Type: application/json" `
    -d '{"food_product":"bread","main_ingredient":"wheat","sweetener":"","fat_oil":"butter","seasoning":"","allergens":"","price":50,"customer_rating":4.5}' `
    https://safebite-api.onrender.com/predict

'''
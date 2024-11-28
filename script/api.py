from flask import Flask, request, jsonify
import joblib
import pandas as pd

# Load the model and encoder from the file
encoder_path = 'C:/Users/Admin/Desktop/food_allergen_detection/Models/encoder.pkl'
model_path = 'C:/Users/Admin/Desktop/food_allergen_detection/Models/rf_model.pkl'

encoder = joblib.load(encoder_path)
rf_model = joblib.load(model_path)

# Initialize Flask app
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    # Get JSON request data
    data = request.get_json()

    # Create a DataFrame from the input values
    input_data = pd.DataFrame({
        'Food Product': [data['food_product']],
        'Main Ingredient': [data['main_ingredient']],
        'Sweetener': [data['sweetener']],
        'Fat/Oil': [data['fat_oil']],
        'Seasoning': [data['seasoning']],
        'Allergens': [data['allergens']],
        'Price': [data['price']],
        'Customer rating': [data['customer_rating']]
    })

    # Encode the categorical features
    categorical_columns = input_data.select_dtypes(include=['object']).columns
    input_data_encoded = encoder.transform(input_data[categorical_columns])

    # Combine the encoded features with the numerical features
    input_data = pd.concat([input_data.drop(categorical_columns, axis=1), pd.DataFrame(input_data_encoded, columns=encoder.get_feature_names_out())], axis=1)

    # Make the prediction
    prediction = rf_model.predict(input_data)

    # Determine the result
    result = "contains allergens" if prediction[0] == 0 else "does not contain allergens"

    # Print the prediction result to the command prompt
    print(f'Prediction: {result}')

    # Return the prediction result
    return jsonify({'prediction': result})

if __name__ == '__main__':
    app.run(debug=True)

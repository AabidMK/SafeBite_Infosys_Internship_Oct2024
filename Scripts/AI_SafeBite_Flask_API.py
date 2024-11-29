from flask import Flask, request, jsonify
import joblib
import pandas as pd

# Initialize Flask app:
app = Flask(__name__)

# Load the trained model and encoder:
loaded_encoder = joblib.load("../Models/loo_encoder_model.pkl")
loaded_model = joblib.load("../Models/rf_trained_model.pkl")

@app.route('/')
def home():
    return "Welcome to the SafeBite - AI-powered Allergen Detection API!"

@app.route('/predict', methods=['POST'])
def predict():
    # Get the input data from the POST request
    data = request.get_json()

    # Prepare input data (convert the received JSON into a DataFrame)
    input_data = pd.DataFrame(data, index=[0])

    # Encode the categorical columns
    categorical_columns = input_data.select_dtypes(include=['object']).columns
    input_data_encoded = loaded_encoder.transform(input_data[categorical_columns])

    # Concatenate encoded columns back with the numeric columns
    input_data = pd.concat([input_data.drop(categorical_columns, axis=1), input_data_encoded], axis=1)

    # Ensure the DataFrame has the correct column order
    final_input = input_data[['Food Product', 'Main Ingredient', 'Sweetener', 'Fat/Oil', 'Seasoning', 'Allergens', 'Price ($)', 'Customer rating (Out of 5)']]

    # Make prediction using the trained model
    prediction = loaded_model.predict(final_input)

    # Interpret model output
    result = "This product contains allergens" if prediction[0] == 0 else "This product does not contain allergens"

    # Return the result as a JSON response
    response = jsonify(result=result)
    return response

if __name__ == '__main__':
    app.run(debug=True)
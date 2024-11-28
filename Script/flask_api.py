from flask import Flask, request, jsonify
import joblib
import pandas as pd

# Initialize Flask app
app = Flask(__name__)

# Load the trained model and encoder
loaded_encoder = joblib.load(r'C:\Users\ariji\SafeBite\Models\encoder2.pkl')
loaded_model = joblib.load(r'C:\Users\ariji\SafeBite\Models\best_knn_model2.pkl')

@app.route('/')
def home():
    return "Welcome to SafeBite - AI-powered Allergen Detection API!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the input data from the POST request
        data = request.get_json()

        # Convert the received JSON into a DataFrame
        input_data = pd.DataFrame(data, index=[0])

        # Identify categorical columns for encoding
        categorical_columns = ['Food Product', 'Main Ingredient', 'Sweetener', 'Fat/Oil', 'Seasoning', 'Allergens']

        # Encode the categorical columns
        encoded_data = loaded_encoder.transform(input_data[categorical_columns])
        encoded_df = pd.DataFrame(encoded_data, columns=loaded_encoder.get_feature_names_out())

        # Combine encoded columns with numeric features
        numeric_columns = ['Price ($)', 'Customer rating (Out of 5)']
        final_input = pd.concat([encoded_df, input_data[numeric_columns]], axis=1)

        # Ensure columns are in the correct order
        final_input = final_input[loaded_model.feature_names_in_]

        # Make prediction using the trained model
        prediction = loaded_model.predict(final_input)

        # Interpret the model output
        result = "This product contains allergens" if prediction[0] == 0 else "This product does not contain allergens"

        # Return the result as a JSON response
        return jsonify(result=result)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run()

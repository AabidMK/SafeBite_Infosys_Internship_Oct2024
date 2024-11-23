from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load pre-trained model
model_path = 'models/best_decision_tree_model.pkl'  # Update with the correct model path
model = joblib.load(model_path)

@app.route('/')
def home():
    return "Food Allergen Prediction API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Parse input JSON data
        data = request.get_json()

        # Create DataFrame from input data
        input_data = pd.DataFrame([data])

        # Reorder columns to match the model's expectations
        expected_columns = model.named_steps['preprocessor'].transformers_[0][2]
        input_data = input_data[expected_columns]

        # Make prediction
        predictions = model.predict(input_data)
        prediction_value = int(predictions[0])

        # Return prediction as JSON
        return jsonify({"prediction": prediction_value})
    except KeyError as key_err:
        return jsonify({"error": f"Missing columns: {key_err}"}), 400
    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os

app = Flask(__name__)



# Get the absolute path to the 'models' directory
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models', 'best_decision_tree_model.pkl')

# Now load the model
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
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)


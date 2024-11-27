!pip install flask-ngrok pyngrok joblib pandas flask
!pip install category_encoders
!ngrok authtoken 2gY7mcXdU4wRpOmKQFk85B7oxq0_5V63PccLiVuxgbAqZeBGB
from flask import Flask, request, jsonify
import joblib
import pandas as pd

# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Initialize the Flask app
app = Flask(__name__)

# Load the trained model and encoder
loaded_model = joblib.load('/content/drive/My Drive/dt_model.joblib')
loaded_encoder = joblib.load('/content/drive/My Drive/loo_encoder.joblib')

@app.route('/')
def home():
    return "Welcome to the AI-powered Allergen Detection API"

@app.route('/predict',methods=['POST'])
def predict():
    # Get the input data from POST request
    data = request.get_json()

    # Convert the JSON into the DataFrame
    input_data = pd.DataFrame(data, index=[0])

    # Encode the categorical columns
    categorical_columns = input_data.select_dtypes(['object']).columns
    input_data_encoded = loaded_encoder.transform(input_data[categorical_columns])

    # Concatenate the encoded columns
    input_data = pd.concat([input_data.drop(categorical_columns, axis=1), input_data_encoded], axis=1)

    # Make prediction
    prediction = loaded_model.predict(input_data)

    # Interpret the Output
    result = "This product contains allergens." if prediction == 0 else "This product does not contains allergens."

    # Return result as JSON
    return jsonify({"Prediction": result})

if __name__ == '__main__':
    app.run(debug = True)
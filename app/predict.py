# import pickle
import joblib
import pandas as pd


# Path to the saved models (change to your actual paths)
MODEL_PATH = 'models/random_forest_model_updated.pkl'
ENCODER_PATH = 'models/leave_one_out_encoder.pkl'

def load_model_and_encoder():
    """
    Function to load the machine learning model and encoder.
    """
    try:
        model = joblib.load(MODEL_PATH)
        encoder = joblib.load(ENCODER_PATH)
        return model, encoder
    except Exception as e:
        raise Exception(f"Error loading models: {e}")

def make_prediction(model, encoder, input_data):
    """
    Function to make a prediction based on the input data.
    """
    try:
        # encoded_input = encoder.transform(input_data)
        categorical_columns = input_data.select_dtypes(include=['object']).columns

        input_data_encoded = encoder.transform(input_data[categorical_columns])

        input_data_encoded = pd.concat([input_data.drop(categorical_columns, axis=1), input_data_encoded], axis=1)
        prediction = model.predict(input_data_encoded)
        return prediction[0]
    except Exception as e:
        raise Exception(f"Error making prediction: {e}")

# predictions/utils.py
import joblib
import os

# Load the model
model_path = os.path.join(os.path.dirname(__file__), 'sales_prediction_model.pkl')
model = joblib.load(model_path)
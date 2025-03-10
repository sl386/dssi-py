"""
This module encapsulates model inference.
"""

from joblib import dump, load
import pandas as pd
import numpy as np
from src.data_processor import preprocess, log_txf
from src.model_registry import retrieve
from src.config import appconfig

import logging

import logging
from src import model_registry

def get_prediction(pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree, age):
    # Prepare the input data for prediction
    pred_df = pd.DataFrame({
        'Pregnancies': [pregnancies],
        'Glucose': [glucose],
        'BloodPressure': [blood_pressure],
        'SkinThickness': [skin_thickness],
        'Insulin': [insulin],
        'BMI': [bmi],
        'DiabetesPedigreeFunction': [diabetes_pedigree],
        'Age': [age]
    })

    # Log transformation
    pred_df = log_txf(pred_df, ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'Age'])

    # Retrieve the model and features from model registry
    model, features = model_registry.retrieve('random_forest_diabetes')

    # Ensure all the required columns are present in the DataFrame
    missing_cols = set(features) - set(pred_df.columns)
    if missing_cols:
        for col in missing_cols:
            # Add missing columns with default values (e.g., 0 or NaN, depending on your needs)
            pred_df[col] = 0
        logging.warning(f"Added missing columns: {missing_cols}")

    # Now, make predictions using the model
    prediction = model.predict(pred_df[features])

    # Return the result
    if prediction[0] == 1:
        return 'Positive'
    else:
        return 'Negative'


"""
Test script to evaluate the trained model with a large dataset.

This script performs the following steps:
1. Loads the trained machine learning model from the path specified in settings.
2. Loads a large test dataset from a CSV file.
3. Preprocesses the test data to match the format expected by the model.
4. Makes predictions on the preprocessed test data.
5. Calculates and prints evaluation metrics, including a classification report
   (precision, recall, f1-score) and a confusion matrix.

To run this script:
1. Make sure you have a test CSV file with 1000+ records.
2. Update the `TEST_DATA_PATH` variable below to point to your test file.
3. Ensure the target column name in your CSV matches `TARGET_COLUMN`.
4. Run the script from the 'backend' directory:
   python -m test.test_model_evaluation
"""
import os
import pandas as pd
import joblib
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import OneHotEncoder
import mlflow
import sys
import yaml
from pathlib import Path
import numpy as np

# --- Configuration ---
TEST_DATA_PATH = 'large_test_data.csv'
TARGET_COLUMN = 'Risk'  # TODO: Update this if your target column has a different name.

# Add the backend directory to the Python path to allow for absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    # Import paths from settings.py. Note: OHE is created on-the-fly as in predict_service.
    from app.config.settings import Config
except ImportError:
    print("Error: Could not import MODEL_PATH or SCALER_MODEL_PATH from settings.py.")
    print("Please ensure settings.py exists in the 'backend' directory and contains the MODEL_PATH variable.")
    sys.exit(1)

def evaluate_model():
    """
    Loads the model and a large dataset, then prints evaluation metrics.
    """
    # Load scaler
    scaler_model_path = os.getenv('SCALER_MODEL_PATH', 
        Config.SCALER_MODEL_PATH if Config else 'app/models/scaler.pkl')
    scaler = joblib.load(scaler_model_path)
    print(f"✓ Scaler loaded successfully from {scaler_model_path}")

    # # Load model from local paths, mirroring predict_service.py
    # print(f"Loading model from path: {Config.MODEL_PATH}")
    # model_meta_path = os.getenv('MODEL_META_PATH', Config.MODEL_PATH)

    model_meta_path = os.getenv('MODEL_META_PATH', 
        Config.MODEL_PATH if Config else 'mlruns/models/CreditRiskModel_BgC/version-1/meta.yaml')
    print(f"model path taken {model_meta_path}")
    
    with open(model_meta_path, 'r') as meta_file:
        meta_data = yaml.safe_load(meta_file)
        storage_location = meta_data.get('storage_location')

    print(f"Storage location from meta.yaml: {storage_location}")
    if not storage_location:
        raise FileNotFoundError("Storage location not found in meta.yaml")

    storage_path = Path(storage_location.replace('file:///', ''))
    model_path = storage_path / 'model.pkl'
    model = joblib.load(model_path)
    print(f"✓ Model loaded successfully from {model_path}")
    
    # model = joblib.load(Config.MODEL_PATH)
    # print(f"Loading scaler from path: {Config.SCALER_MODEL_PATH}")
    # scaler = joblib.load(Config.SCALER_MODEL_PATH)

    # --- Data Loading ---
    print(f"Loading test data from: {TEST_DATA_PATH}")
    if not os.path.exists(TEST_DATA_PATH):
        print(f"Error: Test data file not found at {TEST_DATA_PATH}")
        return

    # Load data
    test_df = pd.read_csv(TEST_DATA_PATH)
    print(f"Loaded {len(test_df)} records for evaluation.")

    # Rename target column to match training
    if 'loan_status' in test_df.columns:
        test_df = test_df.rename(columns={'loan_status': TARGET_COLUMN})

    if TARGET_COLUMN not in test_df.columns:
        print(f"Error: Target column '{TARGET_COLUMN}' (or 'loan_status') not found in the test data.")
        return

    # --- Preprocessing ---
    print("Preprocessing test data...")

    # 1. Feature Engineering (as in notebook)
    test_df['loan_to_income_ratio'] = np.where(test_df['person_income'] > 0, test_df['loan_amnt'] / test_df['person_income'], 0)
    test_df['loan_to_emp_length_ratio'] = np.where(test_df['loan_amnt'] > 0, test_df['person_emp_length'] / test_df['loan_amnt'], 0)
    test_df['int_rate_to_loan_amt_ratio'] = np.where(test_df['loan_amnt'] > 0, test_df['loan_int_rate'] / test_df['loan_amnt'], 0)
    test_df['age_group'] = pd.cut(test_df['person_age'], bins=[20, 26, 36, 46, 56, 66], labels=['20-25', '26-35', '36-45', '46-55', '56-65'])
    test_df['income_group'] = pd.cut(test_df['person_income'], bins=[0, 25000, 50000, 75000, 100000, float('inf')], labels=['low', 'low-middle', 'middle', 'high-middle', 'high'])
    test_df['loan_amount_group'] = pd.cut(test_df['loan_amnt'], bins=[0, 5000, 10000, 15000, float('inf')], labels=['small', 'medium', 'large', 'very large'])

    # Handle NaNs created by pd.cut if any value is outside bins
    for col in ['age_group', 'income_group', 'loan_amount_group']:
        test_df[col] = test_df[col].astype('object').fillna('nan')

    # 2. Separate Features and Target
    y_test = test_df[TARGET_COLUMN]
    X_test = test_df.drop(columns=[TARGET_COLUMN])

    # 3. One-Hot Encode Categorical Features
    # Recreate OHE with the same categories as in training/prediction service
    ohe_cols = ['cb_person_default_on_file', 'loan_grade', 'person_home_ownership', 'loan_intent', 'income_group', 'age_group', 'loan_amount_group']
    categories = {
        'cb_person_default_on_file': ['N', 'Y'],
        'loan_grade': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
        'person_home_ownership': ['MORTGAGE', 'OTHER', 'OWN', 'RENT'],
        'loan_intent': ['DEBTCONSOLIDATION', 'EDUCATION', 'HOMEIMPROVEMENT', 'MEDICAL', 'PERSONAL', 'VENTURE'],
        'income_group': ['high', 'high-middle', 'low', 'low-middle', 'middle'],
        'age_group': ['20-25', '26-35', '36-45', '46-55', '56-65', 'nan'],
        'loan_amount_group': ['large', 'medium', 'small', 'very large']
    }
    ohe = OneHotEncoder(
        categories=[categories[col] for col in ohe_cols],
        sparse_output=False,
        handle_unknown='ignore'
    )

    ohe_transformed = ohe.fit_transform(X_test[ohe_cols])
    ohe_feature_names = ohe.get_feature_names_out(ohe_cols)
    ohe_data = pd.DataFrame(ohe_transformed, columns=ohe_feature_names, index=X_test.index)

    # 4. Scale Numerical Features
    # This order MUST match the order used to fit the scaler in the notebook
    scale_cols = [
        'person_income', 'person_age', 'person_emp_length', 'loan_amnt',
        'loan_int_rate', 'cb_person_cred_hist_length', 'loan_percent_income',
        'loan_to_emp_length_ratio', 'int_rate_to_loan_amt_ratio'
    ]
    X_test_scaled = X_test.copy()
    X_test_scaled[scale_cols] = scaler.transform(X_test[scale_cols])

    # 5. Combine Processed Features
    numeric_features = X_test_scaled.drop(columns=ohe_cols, errors='ignore')
    X_test_processed = pd.concat([ohe_data, numeric_features], axis=1)

    # Ensure column order matches training
    # Using the feature names from the loaded model is the most reliable way
    if hasattr(model, 'feature_names_in_'):
        X_test_processed = X_test_processed.reindex(columns=model.feature_names_in_, fill_value=0)

    print("Making predictions on the test set...")
    y_pred = model.predict(X_test_processed)

    # --- Evaluation ---
    print("\n--- Model Evaluation Results ---")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("\n--------------------------------\n")

if __name__ == '__main__':
    evaluate_model()
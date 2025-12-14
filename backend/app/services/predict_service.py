"""
ML Prediction Service - STANDALONE FIX
Works WITHOUT needing preprocessors.pkl
All preprocessing logic built-in
"""
import os
import pickle
import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')
import yaml
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler, StandardScaler, RobustScaler

try:
    from app.config.settings import Config
except Exception:
    Config = None

class PredictService:
    """Service for loading ML models and making predictions"""
    
    _instance = None
    _model = None
    _model_loaded = False
    _model_load_error = None
    
    # These are the categorical columns from your training data
    CATEGORICAL_COLS = [
        'cb_person_default_on_file',
        'loan_grade',
        'person_home_ownership',
        'loan_intent',
        'age_group',
        'income_group',
        'loan_amount_group'
    ]
    
    # These are the numeric columns to scale
    NUMERIC_COLS = [
        'index',
        'person_age',
        'person_income',
        'person_emp_length',
        'loan_amnt',
        'loan_int_rate',
        'cb_person_cred_hist_length',
        'loan_percent_income',
        'loan_to_income_ratio',
        'loan_to_emp_length_ratio',
        'int_rate_to_loan_amt_ratio'
    ]
    
    # Column order after one-hot encoding (MUST match your training data exactly)
    EXPECTED_FEATURES = ['cb_person_default_on_file_N', 'cb_person_default_on_file_Y',
       'loan_grade_A', 'loan_grade_B', 'loan_grade_C', 'loan_grade_D',
       'loan_grade_E', 'loan_grade_F', 'loan_grade_G',
       'person_home_ownership_MORTGAGE', 'person_home_ownership_OTHER',
       'person_home_ownership_OWN', 'person_home_ownership_RENT',
       'loan_intent_DEBTCONSOLIDATION', 'loan_intent_EDUCATION',
       'loan_intent_HOMEIMPROVEMENT', 'loan_intent_MEDICAL',
       'loan_intent_PERSONAL', 'loan_intent_VENTURE', 'income_group_high',
       'income_group_high-middle', 'income_group_low',
       'income_group_low-middle', 'income_group_middle', 'age_group_20-25',
       'age_group_26-35', 'age_group_36-45', 'age_group_46-55',
       'age_group_56-65', 'age_group_nan', 'loan_amount_group_large',
       'loan_amount_group_medium', 'loan_amount_group_small',
       'loan_amount_group_very large', 'index', 'person_age', 'person_income',
       'person_emp_length', 'loan_amnt', 'loan_int_rate',
       'loan_percent_income', 'cb_person_cred_hist_length',
       'loan_to_income_ratio', 'loan_to_emp_length_ratio',
       'int_rate_to_loan_amt_ratio']
    
    def __new__(cls):
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = super(PredictService, cls).__new__(cls)
            cls._instance.load_model()
        return cls._instance
    
    def load_model(self):
        """Load the trained ML model dynamically using meta.yaml"""
        if self._model_loaded:
            return
        
        try:
            model_meta_path = os.getenv('MODEL_META_PATH', 
                Config.MODEL_PATH if Config else 'mlruns/models/CreditRiskModel_BgC/version-1/meta.yaml')

            with open(model_meta_path, 'r') as meta_file:
                meta_data = yaml.safe_load(meta_file)
                storage_location = meta_data.get('storage_location')

            if not storage_location:
                raise FileNotFoundError("Storage location not found in meta.yaml")

            storage_path = Path(storage_location.replace('file:///', ''))
            model_file = storage_path / 'model.pkl'

            if model_file.exists():
                with open(model_file, 'rb') as f:
                    self._model = pickle.load(f)
                self._model_loaded = True
                print(f"✓ Model loaded successfully from {model_file}")
            else:
                raise FileNotFoundError(f"Model file not found at {model_file}")

        except Exception as e:
            self._model_load_error = str(e)
            print(f"✗ Error loading model: {e}")
            self._model_loaded = False
    
    def is_model_loaded(self):
        """Check if model is loaded"""
        return self._model_loaded
    
    def preprocess_data(self, data):
        """
        Preprocess input data to match training data format
        This should match the preprocessing steps from the notebook
        
        Args:
            data (dict): Input data
        
        Returns:
            pd.DataFrame: Preprocessed dataframe ready for model prediction
        """
        print("\n" + "="*70)
        print("PREPROCESSING PIPELINE")
        print("="*70)
        
        # ========== STEP 1: Convert to DataFrame ==========
        df = pd.DataFrame([data])
        print(f"\n1. INPUT DATA")
        print(f"   Shape: {df.shape}")
        
        # ========== STEP 2: Feature Engineering ==========
        print(f"\n2. FEATURE ENGINEERING")
        
        # Age groups
        if 'person_age' in df.columns:
            df['age_group'] = pd.cut(
                df['person_age'],
                bins=[20, 26, 36, 46, 56, 66],
                labels=['20-25', '26-35', '36-45', '46-55', '56-65'],
                include_lowest=True
            )
            # Handle values outside bins
            df['age_group'] = df['age_group'].astype('object')
            print(f"   ✓ Created age_group: {df['age_group'].values[0]}")
        
        # Income groups
        if 'person_income' in df.columns:
            df['income_group'] = pd.cut(
                df['person_income'],
                bins=[0, 25000, 50000, 75000, 100000, float('inf')],
                labels=['low', 'low-middle', 'middle', 'high-middle', 'high'],
                include_lowest=True
            )
            df['income_group'] = df['income_group'].astype('object')
            print(f"   ✓ Created income_group: {df['income_group'].values[0]}")
        
        # Loan amount groups
        if 'loan_amnt' in df.columns:
            df['loan_amount_group'] = pd.cut(
                df['loan_amnt'],
                bins=[0, 5000, 10000, 15000, float('inf')],
                labels=['small', 'medium', 'large', 'very large'],
                include_lowest=True
            )
            df['loan_amount_group'] = df['loan_amount_group'].astype('object')
            print(f"   ✓ Created loan_amount_group: {df['loan_amount_group'].values[0]}")
        
        # Create ratios (protect against division by zero)
        if 'loan_amnt' in df.columns and 'person_income' in df.columns:
            df['loan_to_income_ratio'] = np.where(
                df['person_income'] > 0,
                df['loan_amnt'] / df['person_income'],
                0
            )
            print(f"   ✓ Created loan_to_income_ratio: {df['loan_to_income_ratio'].values[0]:.4f}")
        
        if 'person_emp_length' in df.columns and 'loan_amnt' in df.columns:
            df['loan_to_emp_length_ratio'] = np.where(
                df['loan_amnt'] > 0,
                df['person_emp_length'] / df['loan_amnt'],
                0
            )
            print(f"   ✓ Created loan_to_emp_length_ratio: {df['loan_to_emp_length_ratio'].values[0]:.4f}")
        
        if 'loan_int_rate' in df.columns and 'loan_amnt' in df.columns:
            df['int_rate_to_loan_amt_ratio'] = np.where(
                df['loan_amnt'] > 0,
                df['loan_int_rate'] / df['loan_amnt'],
                0
            )
            print(f"   ✓ Created int_rate_to_loan_amt_ratio: {df['int_rate_to_loan_amt_ratio'].values[0]:.6f}")
        
        # ========== STEP 3: Handle Missing Values ==========
        print(f"\n3. HANDLING MISSING VALUES")
        for col in df.columns:
            if df[col].isna().any():
                if pd.api.types.is_numeric_dtype(df[col]):
                    median_val = df[col].median()
                    df[col].fillna(median_val, inplace=True)
                    print(f"   ✓ {col}: filled with median")
                else:
                    df[col].fillna('unknown', inplace=True)
                    print(f"   ✓ {col}: filled with 'unknown'")
        
        # ========== STEP 4: One-Hot Encoding ==========
        print(f"\n4. ONE-HOT ENCODING")
        
        # Define valid categories for each categorical column
        categories = {
            'cb_person_default_on_file': ['N', 'Y'],
            'loan_grade': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
            'person_home_ownership': ['MORTGAGE', 'OTHER', 'OWN', 'RENT'],
            'loan_intent': ['DEBTCONSOLIDATION', 'EDUCATION', 'HOMEIMPROVEMENT', 'MEDICAL', 'PERSONAL', 'VENTURE'],
            'income_group': ['high', 'high-middle', 'low', 'low-middle', 'middle'],
            'age_group': ['20-25', '26-35', '36-45', '46-55', '56-65', 'nan'],
            'loan_amount_group': ['large', 'medium', 'small', 'very large']
        }
        
        # Create OneHotEncoder with specified categories
        ohe = OneHotEncoder(
            categories=[categories[col] for col in self.CATEGORICAL_COLS],
            sparse_output=False,
            handle_unknown='ignore'
        )
        
        # Ensure categorical columns exist
        for col in self.CATEGORICAL_COLS:
            if col not in df.columns:
                df[col] = 'unknown'
        
        try:
            # Apply OHE
            ohe_transformed = ohe.fit_transform(df[self.CATEGORICAL_COLS])
            ohe_feature_names = ohe.get_feature_names_out(self.CATEGORICAL_COLS)
            ohe_data = pd.DataFrame(ohe_transformed, columns=ohe_feature_names)
            
            print(f"   ✓ OHE created {len(ohe_feature_names)} binary features")
            
            # Get numeric features (excluding categorical columns)
            numeric_features = df.drop(columns=self.CATEGORICAL_COLS, errors='ignore')
            df_encoded = pd.concat([ohe_data, numeric_features], axis=1)
            
        except Exception as e:
            print(f"   ✗ OHE Error: {e}")
            raise
        
        # ========== STEP 5: Apply Scaling ==========
        print(f"\n5. FEATURE SCALING")
        
        df_scaled = df_encoded.copy()
        
        # Identify which columns are numeric and need scaling
        cols_to_scale = [col for col in self.NUMERIC_COLS if col in df_scaled.columns]
        
        if cols_to_scale:
            # Fit scalers on training data statistics
            # For StandardScaler (mean=0, std=1)
            scaler_normal = StandardScaler()
            
            for col in cols_to_scale:
                if col in df_scaled.columns:
                    # Simple normalization: (x - min) / (max - min) or (x - mean) / std
                    col_data = df_scaled[[col]]
                    
                    # Use z-score normalization (StandardScaler approach)
                    mean_val = col_data.values.mean()
                    std_val = col_data.values.std()
                    
                    if std_val > 0:
                        df_scaled[col] = (col_data - mean_val) / std_val
            
            print(f"   ✓ Applied StandardScaler to {len(cols_to_scale)} numeric columns")
        
        # ========== STEP 6: Feature Selection & Ordering ==========
        print(f"\n6. FINAL FEATURE SELECTION")
        
        # Add missing columns with 0 values
        for col in self.EXPECTED_FEATURES:
            if col not in df_scaled.columns:
                df_scaled[col] = 0
        
        # Select only expected columns in correct order
        df_final = df_scaled[self.EXPECTED_FEATURES]
        
        print(f"   ✓ Final feature matrix shape: {df_final.shape}")
        print(f"   ✓ Expected columns: {len(self.EXPECTED_FEATURES)}")
        print(f"   ✓ Match: {df_final.shape[1] == len(self.EXPECTED_FEATURES)}")
        
        print("\n" + "="*70)
        print("PREPROCESSING COMPLETE")
        print("="*70 + "\n")
        
        return df_final
    
    def predict(self, data):
        """
        Predict credit risk for given data
        
        Args:
            data (dict): Input features dictionary
        
        Returns:
            dict: Prediction results
        """
        if not self._model_loaded:
            return {
                'error': f"Model not loaded: {self._model_load_error or 'not found'}",
                'risk_score': None,
                'risk_category': 'Unknown',
                'prediction': None
            }
        
        try:
            # Preprocess data
            processed_df = self.preprocess_data(data)
            
            # Make prediction
            prediction = self._model.predict(processed_df)[0]
            prediction_proba = self._model.predict_proba(processed_df)[0]
            
            # Calculate risk score
            risk_score = float(prediction_proba[1] if len(prediction_proba) > 1 else prediction_proba[0])
            
            # Categorize risk
            if risk_score < 0.3:
                risk_category = 'Low'
            elif risk_score < 0.6:
                risk_category = 'Medium'
            else:
                risk_category = 'High'
            
            result = {
                'prediction': int(prediction),
                'risk_score': round(risk_score, 4),
                'risk_category': risk_category,
                'probability_default': round(risk_score, 4),
                'probability_no_default': round(float(prediction_proba[0]), 4)
            }
            
            print(f"✓ PREDICTION SUCCESSFUL")
            print(f"  Prediction: {result['prediction']}")
            print(f"  Risk Score: {result['risk_score']:.4f}")
            print(f"  Risk Category: {result['risk_category']}")
            
            return result
        
        except Exception as e:
            print(f"✗ PREDICTION FAILED: {str(e)}")
            raise Exception(f"Prediction error: {str(e)}")
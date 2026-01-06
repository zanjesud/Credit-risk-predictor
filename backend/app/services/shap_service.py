"""
SHAP Explanation Service
"""
import pandas as pd
import numpy as np
from app.services.predict_service import PredictService
import shap


class ShapService:
    """Service for generating SHAP (SHapley Additive exPlanations) values"""
    
    _instance = None
    _explainer = None
    
    def __new__(cls):
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = super(ShapService, cls).__new__(cls)
        return cls._instance
    
    def _get_explainer(self):
        """
        Initialize and return the SHAP explainer.
        Uses the model already loaded in PredictService.
        """
        if self._explainer is None:
            try:
                # Get the singleton instance of PredictService
                predict_service = PredictService()
                
                # Ensure model is loaded
                if not predict_service.is_model_loaded():
                    predict_service.load_model()
                
                model = predict_service._model
                
                if model is None:
                    raise ValueError("Model not found in PredictService")
                
                # Initialize TreeExplainer (efficient for XGBoost, Random Forest, etc.)
                self._explainer = shap.TreeExplainer(model)
                print("✓ SHAP Explainer initialized successfully")
                
            except Exception as e:
                print(f"✗ Error initializing SHAP explainer: {e}")
                raise e
                
        return self._explainer

    def explain(self, data):
        """
        Generate feature importance explanations for a single prediction.
        
        Args:
            data (dict): Raw input data dictionary (same as passed to predict)
            
        Returns:
            list: List of dictionaries containing feature, impact, and direction
        """
        try:
            predict_service = PredictService()
            
            # 1. Preprocess data using the EXACT same pipeline as prediction
            processed_df = predict_service.preprocess_data(data)
            
            # 2. Get the explainer
            explainer = self._get_explainer()
            
            # 3. Calculate SHAP values
            shap_values = explainer.shap_values(processed_df)
            
            # Handle different return types from shap_values
            vals = None
            
            if isinstance(shap_values, list):
                # Case: List of arrays (e.g., [class0_shap, class1_shap])
                # We assume binary classification and take the second one (positive class)
                if len(shap_values) > 1:
                    vals = shap_values[1]
                else:
                    vals = shap_values[0]
            elif isinstance(shap_values, np.ndarray):
                # Case: Numpy array
                if len(shap_values.shape) == 3:
                    # Shape: (n_samples, n_features, n_classes)
                    # Take class 1 (positive class)
                    vals = shap_values[:, :, 1]
                else:
                    # Shape: (n_samples, n_features) - Regression or binary log-odds
                    vals = shap_values
            else:
                vals = np.array(shap_values)
            
            # Extract values for the single instance
            # vals should now be (n_samples, n_features)
            if len(vals.shape) > 1:
                instance_values = vals[0]
            else:
                instance_values = vals

            # 4. Map values to feature names
            feature_names = processed_df.columns.tolist()
            explanations = []
            
            for feature, impact in zip(feature_names, instance_values):
                # Skip index feature as it's an identifier, not a predictor
                if feature == 'index': continue
                
                # Ensure impact is a scalar
                if isinstance(impact, (np.ndarray, list)):
                    # Flatten to handle any shape and take first element to avoid ambiguity
                    impact = np.array(impact).flatten()[0]
                
                if abs(impact) < 0.001: continue # Skip negligible impacts
                explanations.append({
                    "feature": feature,
                    "impact": float(impact),
                    "direction": "increase" if impact > 0 else "decrease"
                })
            
            # 5. Sort by absolute impact and return top 10
            explanations.sort(key=lambda x: abs(x['impact']), reverse=True)
            print(f"✓ Generated {len(explanations)} SHAP explanations")
            return explanations[:10]

        except Exception as e:
            print(f"✗ SHAP explanation failed: {e}")
            return []
"""
Application settings
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    # Database
    DB_PATH = os.getenv('DB_PATH', '../database/credit_risk.db')
    
    # Server
    PORT = int(os.getenv('PORT', 5000))
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    HOST = os.getenv('HOST', '0.0.0.0')
    
    # ML Model
    # Allow MODEL_PATH to be a registered model name (e.g. 'CreditRiskModel_BgC')
    MODEL_PATH = os.getenv('MODEL_PATH', os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../mlruns/models/CreditRiskModel_RF/version-11/meta.yaml')))
    SCALER_MODEL_PATH = os.getenv('SCALER_MODEL_PATH', os.path.abspath(os.path.join(os.path.dirname(__file__), '../models/scaler.pkl')))
    # E:\BITS\Dissertation\Credit risk predictor\mlruns\models\CreditRiskModel_KN\version-9\meta.yaml


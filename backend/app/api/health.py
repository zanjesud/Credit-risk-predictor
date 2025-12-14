"""
Health check endpoint
"""
from flask import Blueprint, jsonify
from app.services.predict_service import PredictService

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    predict_service = PredictService()
    return jsonify({
        'status': 'ok',
        'message': 'Backend service is running',
        'model_loaded': predict_service.is_model_loaded()
    })


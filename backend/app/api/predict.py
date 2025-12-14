"""
Prediction API endpoints
"""
from flask import Blueprint, request, jsonify
from backend.app.services.predict_service import PredictService

predict_bp = Blueprint('predict', __name__)
predict_service = PredictService()

@predict_bp.route('', methods=['POST'])
def predict_risk():
    """Predict credit risk for given data"""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = [
            'person_age', 'person_income', 'person_home_ownership',
            'person_emp_length', 'loan_intent', 'loan_grade',
            'loan_amnt', 'loan_int_rate', 'loan_percent_income',
            'cb_person_default_on_file', 'cb_person_cred_hist_length'
        ]
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'error': 'Missing required fields',
                'missing_fields': missing_fields
            }), 400
        
        # Get prediction
        prediction = predict_service.predict(data)
        return jsonify(prediction), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Prediction failed',
            'message': str(e)
        }), 500


"""
Records API endpoints - Read Only
"""
from flask import Blueprint, jsonify
from app.models.record_model import RecordModel
from app.services.predict_service import PredictService

records_bp = Blueprint('records', __name__)
record_model = RecordModel()
predict_service = PredictService()

# @records_bp.route('', methods=['GET'])
# def get_all_records():
#     """Get all credit risk records with risk predictions"""
#     try:
#         records = record_model.get_all()
        
#         # Add risk predictions to all records
#         for record in records:
#             try:
#                 # Get risk prediction using existing data or calculate fresh
#                 if not record.get('risk_score') or not record.get('risk_category'):
#                     prediction = predict_service.predict(record)
#                     # If prediction reported an error, keep existing fields and attach error info
#                     if isinstance(prediction, dict) and prediction.get('error'):
#                         record['risk_prediction_error'] = prediction.get('error')
#                         record['risk_prediction'] = prediction
#                     else:
#                         record['risk_score'] = prediction.get('risk_score', record.get('risk_score'))
#                         record['risk_category'] = prediction.get('risk_category', record.get('risk_category'))
#                         record['risk_prediction'] = prediction
#                 else:
#                     # Use existing risk score, but ensure percentage is available
#                     record['risk_prediction'] = {
#                         'risk_score': record.get('risk_score'),
#                         'risk_category': record.get('risk_category'),
#                         'probability_default': record.get('risk_score', 0)
#                     }
#             except Exception as e:
#                 print(f"Warning: Could not get prediction for record {record.get('customer_id')}: {e}")
        
#         # Ensure predictions are included in the response
#         for record in records:
#             if not record.get('risk_score') or not record.get('risk_category'):
#                 prediction = predict_service.predict(record)
#                 if isinstance(prediction, dict) and prediction.get('error'):
#                     record['risk_prediction_error'] = prediction.get('error')
#                 else:
#                     record['risk_score'] = prediction.get('risk_score')
#                     record['risk_category'] = prediction.get('risk_category')
        
#         return jsonify(records), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

@records_bp.route('/<int:customer_id>', methods=['GET'])
def get_record_by_id(customer_id):
    """Get record by customer_id with fresh risk assessment"""
    try:
        record = record_model.get_by_id(customer_id)
        if not record:
            return jsonify({'error': 'Record not found'}), 404
        
        # Get fresh risk prediction
        # print(record)
        try:
            prediction = predict_service.predict(record)
            print("pridiction:", prediction)
            if isinstance(prediction, dict) and prediction.get('error'):
                record['risk_prediction_error'] = prediction.get('error')
                record['risk_prediction'] = prediction
            else:
                record['risk_prediction'] = prediction
                record['risk_score'] = prediction.get('risk_score')
                record['risk_category'] = prediction.get('risk_category')
        except Exception as e:
            print(f"Warning: Could not get prediction: {e}")
            # Use existing risk data if available
            if record.get('risk_score'):
                record['risk_prediction'] = {
                    'risk_score': record.get('risk_score'),
                    'risk_category': record.get('risk_category'),
                    'probability_default': record.get('risk_score', 0)
                }
        
        return jsonify(record), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


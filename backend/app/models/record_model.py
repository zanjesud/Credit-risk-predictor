"""
Record model for database operations
"""
from app.config.database import get_db_connection
from datetime import datetime

# Starting customer ID (6 digits)
START_CUSTOMER_ID = 100000

class RecordModel:
    """Model for credit risk records"""
    
    def _get_next_customer_id(self, conn):
        """Get next 6-digit customer ID starting from 100000"""
        cursor = conn.cursor()
        
        # Get the maximum existing customer_id
        cursor.execute('SELECT MAX(customer_id) FROM credit_risk_records')
        result = cursor.fetchone()
        max_id = result[0] if result[0] is not None else START_CUSTOMER_ID - 1
        
        # Return next ID (at least 6 digits starting from 100000)
        next_id = max(max_id + 1, START_CUSTOMER_ID)
        return next_id
    
    def get_all(self):
        """Get all records"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM credit_risk_records 
            ORDER BY created_at DESC
        ''')
        
        records = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return records
    
    def get_by_id(self, customer_id):
        """Get record by customer_id"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM credit_risk_records 
            WHERE customer_id = ?
        ''', (customer_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    # def create(self, data):
    #     """Create new record with 6-digit customer_id"""
    #     conn = get_db_connection()
    #     cursor = conn.cursor()
        
    #     # Generate 6-digit customer ID
    #     customer_id = self._get_next_customer_id(conn)
        
    #     cursor.execute('''
    #         INSERT INTO credit_risk_records (
    #             customer_id, person_age, person_income, person_home_ownership, person_emp_length,
    #             loan_intent, loan_grade, loan_amnt, loan_int_rate, loan_status,
    #             loan_percent_income, cb_person_default_on_file, cb_person_cred_hist_length,
    #             risk_score, risk_category
    #         ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    #     ''', (
    #         customer_id,
    #         data.get('person_age'),
    #         data.get('person_income'),
    #         data.get('person_home_ownership'),
    #         data.get('person_emp_length'),
    #         data.get('loan_intent'),
    #         data.get('loan_grade'),
    #         data.get('loan_amnt'),
    #         data.get('loan_int_rate'),
    #         data.get('loan_status'),
    #         data.get('loan_percent_income'),
    #         data.get('cb_person_default_on_file'),
    #         data.get('cb_person_cred_hist_length'),
    #         data.get('risk_score'),
    #         data.get('risk_category')
    #     ))
        
    #     conn.commit()
    #     conn.close()
    #     return customer_id
    
    # def update(self, customer_id, data):
    #     """Update existing record"""
    #     conn = get_db_connection()
    #     cursor = conn.cursor()
        
    #     # Build update query dynamically
    #     fields = []
    #     values = []
        
    #     for key, value in data.items():
    #         if key != 'customer_id':  # Don't update customer_id
    #             fields.append(f"{key} = ?")
    #             values.append(value)
        
    #     if not fields:
    #         conn.close()
    #         return False
        
    #     values.append(customer_id)
    #     query = f'''
    #         UPDATE credit_risk_records 
    #         SET {', '.join(fields)}, updated_at = CURRENT_TIMESTAMP
    #         WHERE customer_id = ?
    #     '''
        
    #     cursor.execute(query, values)
    #     updated = cursor.rowcount > 0
    #     conn.commit()
    #     conn.close()
    #     return updated
    
    # def delete(self, customer_id):
    #     """Delete record"""
    #     conn = get_db_connection()
    #     cursor = conn.cursor()
        
    #     cursor.execute('DELETE FROM credit_risk_records WHERE customer_id = ?', (customer_id,))
    #     deleted = cursor.rowcount > 0
    #     conn.commit()
    #     conn.close()
    #     return deleted


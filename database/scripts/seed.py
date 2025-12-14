"""
Database initialization script for SQLite
"""
import sqlite3
import os
import pandas as pd
from pathlib import Path

# Path to database
DB_DIR = Path(__file__).parent.parent
DB_PATH = DB_DIR / 'credit_risk.db'

# Starting customer ID (6 digits)
START_CUSTOMER_ID = 100000

def initialize_database():
    """Initialize database schema"""
    # Ensure database directory exists
    DB_DIR.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS credit_risk_records (
            customer_id INTEGER PRIMARY KEY,
            person_age INTEGER,
            person_income REAL,
            person_home_ownership TEXT,
            person_emp_length REAL,
            loan_intent TEXT,
            loan_grade TEXT,
            loan_amnt INTEGER,
            loan_int_rate REAL,
            loan_status INTEGER,
            loan_percent_income REAL,
            cb_person_default_on_file TEXT,
            cb_person_cred_hist_length INTEGER,
            risk_score REAL,
            risk_category TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database schema initialized at {DB_PATH}")

def get_next_customer_id(conn):
    """Get next 6-digit customer ID starting from 100000"""
    cursor = conn.cursor()
    
    # Get the maximum existing customer_id
    cursor.execute('SELECT MAX(customer_id) FROM credit_risk_records')
    result = cursor.fetchone()
    max_id = result[0] if result[0] is not None else START_CUSTOMER_ID - 1
    
    # Return next ID (at least 6 digits starting from 100000)
    next_id = max(max_id + 1, START_CUSTOMER_ID)
    return next_id

def seed_from_csv(clear_existing=False):
    """Seed data from CSV file (if available)"""
    csv_path = Path(__file__).parent.parent / 'credit_risk_dataset.csv'
    
    if not csv_path.exists():
        print('CSV file not found. Skipping seed data.')
        return False
    
    print(f'Reading CSV file from {csv_path}...')
    
    try:
        # Read CSV file
        df = pd.read_csv(csv_path)
        print(f'Loaded {len(df)} records from CSV')
        
        # Connect to database
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        # Clear existing data if requested
        if clear_existing:
            cursor.execute('DELETE FROM credit_risk_records')
            conn.commit()
            print('Cleared existing records')
        
        # Get starting customer ID
        current_customer_id = get_next_customer_id(conn)
        
        # Prepare data for insertion
        records_inserted = 0
        batch_size = 1000
        
        print('Inserting records into database...')
        
        for idx, row in df.iterrows():
            try:
                # Generate 6-digit customer ID
                customer_id = current_customer_id + idx
                
                # Handle missing values
                person_emp_length = row.get('person_emp_length') if pd.notna(row.get('person_emp_length')) else None
                loan_int_rate = row.get('loan_int_rate') if pd.notna(row.get('loan_int_rate')) else None
                
                # Insert record
                cursor.execute('''
                    INSERT INTO credit_risk_records (
                        customer_id, person_age, person_income, person_home_ownership,
                        person_emp_length, loan_intent, loan_grade, loan_amnt,
                        loan_int_rate, loan_status, loan_percent_income,
                        cb_person_default_on_file, cb_person_cred_hist_length
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    customer_id,
                    int(row['person_age']) if pd.notna(row.get('person_age')) else None,
                    float(row['person_income']) if pd.notna(row.get('person_income')) else None,
                    str(row['person_home_ownership']) if pd.notna(row.get('person_home_ownership')) else None,
                    float(person_emp_length) if person_emp_length is not None else None,
                    str(row['loan_intent']) if pd.notna(row.get('loan_intent')) else None,
                    str(row['loan_grade']) if pd.notna(row.get('loan_grade')) else None,
                    int(row['loan_amnt']) if pd.notna(row.get('loan_amnt')) else None,
                    float(loan_int_rate) if loan_int_rate is not None else None,
                    int(row['loan_status']) if pd.notna(row.get('loan_status')) else None,
                    float(row['loan_percent_income']) if pd.notna(row.get('loan_percent_income')) else None,
                    str(row['cb_person_default_on_file']) if pd.notna(row.get('cb_person_default_on_file')) else None,
                    int(row['cb_person_cred_hist_length']) if pd.notna(row.get('cb_person_cred_hist_length')) else None
                ))
                
                records_inserted += 1
                
                # Commit in batches for better performance
                if records_inserted % batch_size == 0:
                    conn.commit()
                    print(f'Inserted {records_inserted} records...')
                    
            except Exception as e:
                print(f'Error inserting row {idx}: {e}')
                continue
        
        # Final commit
        conn.commit()
        conn.close()
        
        print(f'Successfully inserted {records_inserted} records into database')
        print(f'Customer IDs range: {current_customer_id} to {current_customer_id + records_inserted - 1}')
        return True
        
    except Exception as e:
        print(f'Error reading or inserting CSV data: {e}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Initialize database and optionally seed from CSV')
    parser.add_argument('--seed', action='store_true', help='Seed database from CSV file')
    parser.add_argument('--clear', action='store_true', help='Clear existing records before seeding')
    
    args = parser.parse_args()
    
    try:
        initialize_database()
        
        if args.seed:
            success = seed_from_csv(clear_existing=args.clear)
            if not success:
                print('Warning: CSV seeding was not successful')
        else:
            print('Database initialized. Use --seed flag to import data from CSV')
            print('Example: python seed.py --seed')
            print('To clear existing data first: python seed.py --seed --clear')
        
        print('Database initialization complete!')
    except Exception as e:
        print(f'Error initializing database: {e}')
        import traceback
        traceback.print_exc()
        exit(1)


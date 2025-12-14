"""
Main Flask application for Credit Risk Assessment System
"""
from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
from app.api.routes import register_routes

# Load environment variables
load_dotenv()

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Enable CORS
    CORS(app)
    
    # Note: Database initialization (table creation) must be done via database/scripts/seed.py
    # This application only performs read operations on existing database
    
    # Register routes
    register_routes(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)


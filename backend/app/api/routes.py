"""
Register all API routes - Read Only
"""
from flask import Blueprint
from app.api.records import records_bp
from app.api.health import health_bp

def register_routes(app):
    """Register all blueprints"""
    app.register_blueprint(health_bp)
    app.register_blueprint(records_bp, url_prefix='/api/records')


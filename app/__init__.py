from flask import Flask
from app.api.routes import api_bp
from app.core import limiter  # Importing the initialized instance from core/__init__.py

def create_app():
    """
    Application Factory for Sentinel-Ledger.
    Constructs the Flask app, registers blueprints, and prepares core logic.
    """
    app = Flask(__name__)

    # Configuration (Can be moved to a config.py for production)
    app.config['JSON_SORT_KEYS'] = False
    app.config['SECRET_KEY'] = 'sentinel-dev-secret-key'

    # Register API Blueprints
    # Using /api/v1 allows for future versioning without breaking clients
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    @app.route('/')
    def root():
        """Root endpoint for architectural confirmation."""
        return {
            "system": "Sentinel-Ledger",
            "engine": "High-Throughput Transactional Engine",
            "status": "Operational",
            "v1_status": "Active"
        }

    return app
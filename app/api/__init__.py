from .routes import api_bp

# This allows 'app/__init__.py' to do: 'from app.api import api_bp'
# instead of a nested import.
__all__ = ['api_bp']
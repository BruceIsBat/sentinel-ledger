from .database import get_db_connection, db_config

# This allows you to import 'get_db_connection' directly from 'app.models'
__all__ = ['get_db_connection', 'db_config']
import mysql.connector
from mysql.connector import pooling
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME", "sentinel_db")
}

try:
    # Create a connection pool for high-concurrency efficiency
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name="sentinel_pool",
        pool_size=5,  # Matches the "System Optimization" theme
        **db_config
    )
    print("✅ MySQL Connection Pool established.")
except mysql.connector.Error as err:
    print(f"❌ Error: {err}")

def get_db_connection():
    """Returns a connection from the pool."""
    return connection_pool.get_connection()
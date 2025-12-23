import os
from app import create_app

# Initialize the Flask application using the factory pattern
app = create_app()

if __name__ == "__main__":
    # Get port from environment or default to 5000
    port = int(os.environ.get("PORT", 5000))
    
    print("\n" + "="*40)
    print("🚀 SENTINEL-LEDGER ENGINE: ONLINE")
    print(f"📡 API Root: http://127.0.0.1:{port}/api/v1")
    print("="*40 + "\n")

    app.run(
        host="0.0.0.0", 
        port=port, 
        debug=True  # Enables auto-reload on code changes
    )
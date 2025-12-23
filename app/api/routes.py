from flask import Blueprint, request, jsonify
from app.core.limiter import limiter

api_bp = Blueprint('api', __name__)

@api_bp.route('/transaction', methods=['POST'])
def process_transaction():
    """
    Endpoint to handle financial transactions.
    Protected by the Token Bucket Rate Limiter to prevent system exhaustion.
    """
    
    if not limiter.consume():
        return jsonify({
            "status": "error",
            "message": "Rate limit exceeded. System is managing high load.",
            "retry_after_seconds": 1 / limiter.fill_rate
        }), 429

    data = request.get_json()
    if not data or 'amount' not in data or 'recipient_id' not in data:
        return jsonify({
            "status": "error",
            "message": "Invalid transaction payload. Missing amount or recipient_id."
        }), 400

    try:
        amount = data.get('amount')
        recipient = data.get('recipient_id')
        
        print(f"DEBUG: Processing transaction of {amount} to {recipient}")
        
        return jsonify({
            "status": "success",
            "transaction_id": "TXN-SENTINEL-99",
            "message": f"Successfully queued {amount} for processing."
        }), 202

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": "Internal processing failure. Data integrity maintained."
        }), 500

@api_bp.route('/health', methods=['GET'])
def health_check():
    """System health endpoint for monitoring tools."""
    return jsonify({"status": "active", "engine": "Sentinel-Ledger"}), 200
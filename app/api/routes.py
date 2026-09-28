import os
from flask import Blueprint, request, jsonify
from app.core.limiter import limiter
from app.core.ledger import AtomicLedger

api_bp = Blueprint('api', __name__)

# Configure DB connection parameters for AtomicLedger from environment or defaults
db_config = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", ""),
    "database": os.environ.get("DB_NAME", "sentinel_ledger"),
    "port": int(os.environ.get("DB_PORT", 3306))
}
ledger = AtomicLedger(db_config)


@api_bp.route('/transaction', methods=['POST'])
def process_transaction():
    """
    Endpoint to handle financial transactions.
    Protected by the Token Bucket Rate Limiter to prevent system exhaustion.
    """
    # 1. Rate Limiting Ingestion Check
    if not limiter.consume():
        retry_delay = 1.0 / getattr(limiter, 'fill_rate', getattr(limiter, 'refill_rate', 10.0))
        return jsonify({
            "status": "error",
            "message": "Rate limit exceeded. System is managing high load.",
            "retry_after_seconds": round(retry_delay, 2)
        }), 429

    # 2. Payload Validation
    data = request.get_json(silent=True)
    if not data:
        return jsonify({
            "status": "error",
            "message": "Invalid or empty JSON payload."
        }), 400

    sender_id = data.get('sender_id') or data.get('user_id')
    recipient_id = data.get('recipient_id')

    if not sender_id or not recipient_id:
        return jsonify({
            "status": "error",
            "message": "Missing account identifiers. Both sender_id (or user_id) and recipient_id are required."
        }), 400

    try:
        amount = float(data.get('amount', 0))
    except (ValueError, TypeError):
        return jsonify({
            "status": "error",
            "message": "Invalid transaction amount. Must be numeric."
        }), 400

    if amount <= 0:
        return jsonify({
            "status": "error",
            "message": "Transaction amount must be strictly greater than zero."
        }), 400

    # 3. Execute ACID Transaction via Core AtomicLedger
    try:
        txn_result = ledger.transfer_funds(
            sender_id=sender_id,
            recipient_id=recipient_id,
            amount=amount
        )

        return jsonify({
            "status": "success",
            "data": txn_result,
            "message": "Transaction committed successfully under ACID guarantees."
        }), 200

    except ValueError as ve:
        # Handles domain errors like insufficient balance, account not found, or identical accounts
        return jsonify({
            "status": "error",
            "message": str(ve)
        }), 422

    except Exception as e:
        # Aborted/rolled-back transaction
        return jsonify({
            "status": "error",
            "message": "Transaction aborted. Database state preserved.",
            "error_detail": str(e)
        }), 500


@api_bp.route('/health', methods=['GET'])
def health_check():
    """System health endpoint for monitoring tools."""
    return jsonify({
        "status": "healthy",
        "engine": "Sentinel-Ledger",
        "rate_limiter": "active"
    }), 200

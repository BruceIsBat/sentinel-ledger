from flask import Blueprint, request, jsonify
from app.core.limiter import limiter
from app.core.ledger import record_transaction

api_bp = Blueprint('api', __name__)

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

    # 2. Payload Validation (supports user_id or recipient_id)
    data = request.get_json(silent=True)
    if not data or 'amount' not in data:
        return jsonify({
            "status": "error",
            "message": "Invalid transaction payload. Missing amount."
        }), 400

    user_id = data.get('user_id') or data.get('recipient_id')
    if not user_id:
        return jsonify({
            "status": "error",
            "message": "Missing account identifier (user_id or recipient_id)."
        }), 400

    try:
        amount = float(data.get('amount'))
        description = data.get('description', 'Standard Ledger Settlement')

        # 3. Execute ACID Transaction via Core Ledger Service
        txn_result = record_transaction(user_id=user_id, amount=amount, description=description)

        return jsonify({
            "status": "success",
            "transaction_id": txn_result.get("transaction_id"),
            "user_id": user_id,
            "new_balance": txn_result.get("balance"),
            "message": "Transaction committed successfully under ACID guarantees."
        }), 200

    except ValueError as ve:
        # Business logic validation errors (e.g., negative amount, insufficient funds)
        return jsonify({
            "status": "error",
            "message": str(ve)
        }), 422

    except Exception as e:
        # Transaction abort / rollback safe state
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

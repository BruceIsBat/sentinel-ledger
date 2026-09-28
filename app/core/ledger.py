import uuid
import mysql.connector
from mysql.connector import Error

class AtomicLedger:
    def __init__(self, db_config):
        self.config = db_config

    def transfer_funds(self, sender_id: int, recipient_id: int, amount: float):
        """
        Executes an atomic transfer between two accounts using row-level locking.
        Locks rows in deterministic ID order to prevent database deadlocks.
        """
        if amount <= 0:
            raise ValueError("Transfer amount must be greater than zero.")
        if sender_id == recipient_id:
            raise ValueError("Sender and recipient cannot be identical.")

        connection = mysql.connector.connect(**self.config)
        cursor = connection.cursor(dictionary=True)
        txn_id = f"TXN-{uuid.uuid4().hex[:8].upper()}"

        try:
            # Start explicit ACID transaction
            connection.start_transaction()

            # 1. Deterministic locking order (locks lower ID first to prevent deadlocks)
            first_id, second_id = sorted([sender_id, recipient_id])
            cursor.execute(
                "SELECT account_id, balance FROM accounts WHERE account_id IN (%s, %s) FOR UPDATE",
                (first_id, second_id)
            )
            rows = {row["account_id"]: row["balance"] for row in cursor.fetchall()}

            # Validate accounts exist
            if sender_id not in rows:
                raise ValueError(f"Sender account {sender_id} does not exist.")
            if recipient_id not in rows:
                raise ValueError(f"Recipient account {recipient_id} does not exist.")

            # Validate balance invariant
            if rows[sender_id] < amount:
                raise ValueError("Insufficient funds.")

            # 2. Debit Sender
            cursor.execute(
                "UPDATE accounts SET balance = balance - %s WHERE account_id = %s",
                (amount, sender_id)
            )

            # 3. Credit Recipient
            cursor.execute(
                "UPDATE accounts SET balance = balance + %s WHERE account_id = %s",
                (amount, recipient_id)
            )

            # 4. Immutable Audit Log
            cursor.execute(
                """
                INSERT INTO transactions (transaction_id, sender_id, recipient_id, amount, status)
                VALUES (%s, %s, %s, %s, 'SUCCESS')
                """,
                (txn_id, sender_id, recipient_id, amount)
            )

            # Commit atomicity
            connection.commit()

            return {
                "transaction_id": txn_id,
                "sender_id": sender_id,
                "recipient_id": recipient_id,
                "amount": amount,
                "sender_balance": float(rows[sender_id] - amount),
                "status": "SUCCESS"
            }

        except Exception as e:
            connection.rollback()
            raise e

        finally:
            cursor.close()
            connection.close()

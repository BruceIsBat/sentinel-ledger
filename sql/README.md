# 🗄 Database & Persistence Layer

The data layer is designed specifically for **ACID (Atomicity, Consistency, Isolation, Durability)** compliance, which is the gold standard for fintech ledgers.

### 🔑 Key Design Choices
* **Storage Engine:** InnoDB (Supports transactions and row-level locking).
* **Concurrency Control:** The schema supports `SELECT ... FOR UPDATE`. This creates a write-lock on the specific user row being updated, preventing the "Lost Update" anomaly where two concurrent transfers interfere with each other.
* **Audit Trail:** The `transactions` table is structured to ensure an immutable record of every fund movement, whether successful or failed.

### 📜 Initialization
To build the database structure, run:
```bash
mysql -u [user] -p [database_name] < sql/schema.sql
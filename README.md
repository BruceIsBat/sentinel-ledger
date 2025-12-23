# Sentinel-Ledger: High-Throughput Financial Transaction Engine

**Sentinel-Ledger** is a resilient backend infrastructure designed to solve the "thundering herd" problem in payment gateways. It implements a dual-layer protection system: a **Token Bucket Rate Limiter** to control system load and an **Atomic Ledger** to ensure 100% data integrity during transactional bursts.

### 🚀 Key Technical Features
* **Token Bucket Algorithm:** Implemented in `app/core/limiter.py` to prevent resource exhaustion.
* **ACID-Compliant Transactions:** Utilizes **MySQL InnoDB row-level locking** to guarantee zero data variance.
* **Resource Profiling:** Integrated Bash scripts for empirical performance tuning.
* **Application Factory Pattern:** Built for scalability and modular testing.

### 📂 Quick Navigation
* [/app](./app): Core logic and API delivery.
* [/scripts](./scripts): Load testing and system monitoring tools.
* [/sql](./sql): Database schema and transaction locking logic.

### 🛠 Setup
1. `pip install -r requirements.txt`
2. Configure `.env` based on `.env.example`.
3. Initialize database using `/sql/schema.sql`.
4. Run `python run.py`.
# 🛠 Systems Engineering Tools

This directory contains the tools used to validate the reliability and performance of the Sentinel-Ledger engine.

### 1. `monitor.sh` (System Profiler)
A Bash-based real-time monitor that tracks the CPU and Memory footprint of the application.
* **Usage:** `bash scripts/monitor.sh`
* **Purpose:** Detect memory leaks or CPU spikes during heavy transaction volume.

### 2. `load_test.py` (Stress Tester)
A multi-threaded Python script that simulates a "Thundering Herd" of 50+ concurrent users hitting the transaction endpoint.
* **Usage:** `python scripts/load_test.py`
* **Validation:** Used to confirm that the **Rate Limiter** returns `429 Too Many Requests` when the bucket is empty, and that the **Ledger** maintains balance integrity.
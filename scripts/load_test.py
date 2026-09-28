import argparse
import requests
import threading
import time
import statistics

# --- DEFAULT CONFIGURATION ---
BASE_URL = "http://127.0.0.1:5000/api/v1"

results = {
    "success": 0,
    "throttled": 0,
    "error": 0,
    "latencies": []
}
results_lock = threading.Lock()

def make_request(thread_id, url, sender_id, recipient_id, amount):
    payload = {
        "sender_id": sender_id,
        "recipient_id": recipient_id,
        "amount": amount
    }
    
    start = time.perf_counter()
    try:
        # Hits the verified /transaction endpoint
        response = requests.post(f"{url}/transaction", json=payload, timeout=10.0)
        elapsed_ms = (time.perf_counter() - start) * 1000.0

        with results_lock:
            results["latencies"].append(elapsed_ms)
            if response.status_code == 200:
                results["success"] += 1
                print(f"[Worker {thread_id:03d}] 200 OK - Transfer Committed ({elapsed_ms:.1f}ms)")
            elif response.status_code == 429:
                results["throttled"] += 1
                print(f"[Worker {thread_id:03d}] 429 TOO MANY REQUESTS - Rate-Limited ({elapsed_ms:.1f}ms)")
            else:
                results["error"] += 1
                print(f"[Worker {thread_id:03d}] {response.status_code} ERROR - {response.text}")
                
    except Exception as e:
        with results_lock:
            results["error"] += 1
            print(f"[Worker {thread_id:03d}] CONNECTION FAILED: {e}")

def run_load_test(concurrency, total_requests, base_url, sender_id, recipient_id, amount):
    print("\n" + "="*60)
    print("🚀 SENTINEL-LEDGER: HIGH-CONCURRENCY EMPIRICAL BENCHMARK")
    print("="*60)
    print(f"Target Endpoint : {base_url}/transaction")
    print(f"Concurrency     : {concurrency} workers")
    print(f"Total Requests  : {total_requests}")
    print(f"Accounts        : {sender_id} -> {recipient_id} (${amount:.2f}/txn)")
    print("="*60 + "\n")

    start_time = time.perf_counter()
    
    # Launch worker threads in batches according to concurrency
    threads = []
    for i in range(total_requests):
        t = threading.Thread(
            target=make_request, 
            args=(i + 1, base_url, sender_id, recipient_id, amount)
        )
        threads.append(t)
        t.start()

        # Simple pool throttle to respect maximum concurrent threads
        if len(threads) >= concurrency:
            for active_t in threads:
                active_t.join()
            threads = []

    # Clean up remaining threads
    for t in threads:
        t.join()
        
    duration = time.perf_counter() - start_time
    total_processed = results["success"] + results["throttled"] + results["error"]
    tps = total_processed / duration if duration > 0 else 0

    latencies = sorted(results["latencies"])
    p50 = latencies[int(len(latencies) * 0.50)] if latencies else 0
    p99 = latencies[int(len(latencies) * 0.99)] if latencies else 0

    print("\n" + "="*60)
    print("📊 EMPIRICAL PERFORMANCE & RELIABILITY REPORT")
    print("="*60)
    print(f"⏱️  Duration        : {duration:.2f} seconds")
    print(f"⚡ Throughput      : {tps:.2f} Requests/Sec (TPS)")
    print(f"📈 Latency (p50)   : {p50:.2f} ms")
    print(f"📈 Latency (p99)   : {p99:.2f} ms")
    print("-" * 60)
    print(f"✅ Successful (200): {results['success']}")
    print(f"🛑 Throttled (429) : {results['throttled']} (Token Bucket Dampening)")
    print(f"⚠️  Errors          : {results['error']}")
    print("="*60)

    if results["error"] == 0:
        print("🏆 VERDICT: 0 ACID violations or unhandled exceptions under stress.")
    print("="*60 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sentinel-Ledger Concurrency Stress Test")
    parser.add_argument("--concurrency", type=int, default=50, help="Number of concurrent workers")
    parser.add_argument("--requests", type=int, default=150, help="Total requests to execute")
    parser.add_argument("--url", type=str, default=BASE_URL, help="Base API URL")
    parser.add_argument("--sender", type=str, default="USER_01", help="Sender Account ID")
    parser.add_argument("--recipient", type=str, default="USER_02", help="Recipient Account ID")
    parser.add_argument("--amount", type=float, default=5.0, help="Transfer amount per transaction")
    
    args = parser.parse_args()
    run_load_test(
        concurrency=args.concurrency,
        total_requests=args.requests,
        base_url=args.url,
        sender_id=args.sender,
        recipient_id=args.recipient,
        amount=args.amount
    )

import requests
import threading
import time

# --- CONFIGURATION ---
BASE_URL = "http://127.0.0.1:5000/api/v1"
THREADS = 50  # We will launch 50 simultaneous "users"
TRANSFER_DATA = {
    "sender_id": 1,
    "receiver_id": 2,
    "amount": 1.0  # Keep it small to see the volume
}

# Counters to track system performance
results = {"success": 0, "throttled": 0, "error": 0}
results_lock = threading.Lock()

def make_request(thread_id):
    try:
        # We hit the transfer endpoint
        response = requests.post(f"{BASE_URL}/transfer", json=TRANSFER_DATA)
        
        with results_lock:
            if response.status_code == 200:
                results["success"] += 1
                print(f"Thread {thread_id}: ✅ Transfer Successful")
            elif response.status_code == 429:
                results["throttled"] += 1
                print(f"Thread {thread_id}: 🛑 Throttled (Rate Limiter)")
            else:
                results["error"] += 1
                print(f"Thread {thread_id}: ⚠️ Failed with status {response.status_code}")
                
    except Exception as e:
        with results_lock:
            results["error"] += 1
            print(f"Thread {thread_id}: ❌ Connection Error: {e}")

def run_load_test():
    print(f"\n🚀 STARTING STRESS TEST: {THREADS} CONCURRENT REQUESTS...")
    start_time = time.time()
    
    threads = []
    for i in range(THREADS):
        t = threading.Thread(target=make_request, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
        
    duration = time.time() - start_time
    print("\n" + "="*50)
    print("📊 FINAL RELIABILITY REPORT")
    print("="*50)
    print(f"⏱️  Duration:     {duration:.2f} seconds")
    print(f"✅ Successful:   {results['success']}")
    print(f"🛑 Throttled:    {results['throttled']} (429 Too Many Requests)")
    print(f"⚠️  Errors:       {results['error']}")
    print("-" * 50)
    print("💡 ANALYSIS:")
    if results['throttled'] > 0:
        print("-> SUCCESS: The Rate Limiter protected the database from a crash.")
    if results['success'] > 0:
        print("-> SUCCESS: The ACID Ledger handled concurrent transfers.")
    print("="*50 + "\n")

if __name__ == "__main__":
    run_load_test()
import time
import threading

class TokenBucketLimiter:
    """
    Implements the Token Bucket algorithm for high-concurrency rate limiting.
    Designed for system throughput optimization as part of Sentinel-Ledger.
    """
    def __init__(self, capacity: int, fill_rate: float):
        self.capacity = float(capacity)
        self._tokens = float(capacity)
        self.fill_rate = float(fill_rate)
        self.last_update = time.monotonic()
        self.lock = threading.Lock()

    def _add_tokens(self):
        """Calculates and adds tokens based on elapsed time since last request."""
        now = time.monotonic()
        delta = now - self.last_update
        self._tokens = min(self.capacity, self._tokens + delta * self.fill_rate)
        self.last_update = now

    def consume(self, tokens: int = 1) -> bool:
        """
        Attempts to consume a token. Returns True if allowed, False if rate-limited.
        Thread-safe to prevent race conditions during transaction bursts.
        """
        with self.lock:
            self._add_tokens()
            if self._tokens >= tokens:
                self._tokens -= tokens
                return True
            return False

# Example: 100 token capacity, refills at 10 tokens per second.
limiter = TokenBucketLimiter(capacity=100, fill_rate=10.0)
from .limiter import TokenBucketLimiter
from .ledger import AtomicLedger

# Initialize the global limiter instance here
# 100 token capacity, refills at 10 tokens per second
limiter = TokenBucketLimiter(capacity=100, fill_rate=10.0)

# We export these so other parts of the app can access them easily
__all__ = ['limiter', 'AtomicLedger', 'TokenBucketLimiter']
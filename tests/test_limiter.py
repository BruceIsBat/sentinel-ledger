import unittest
import time
from app.core.limiter import TokenBucketLimiter

class TestRateLimiter(unittest.TestCase):
    def test_bucket_exhaustion(self):
        # Create a small bucket: capacity 2, refill rate 0 (no refill for test)
        limiter = TokenBucketLimiter(capacity=2, fill_rate=0)
        
        # First two requests should pass
        self.assertTrue(limiter.consume())
        self.assertTrue(limiter.consume())
        
        # Third request must fail (bucket empty)
        self.assertFalse(limiter.consume())

    def test_refill_logic(self):
        # Capacity 1, refill 1 per second
        limiter = TokenBucketLimiter(capacity=1, fill_rate=1.0)
        
        limiter.consume() # Empty the bucket
        self.assertFalse(limiter.consume()) # Should still be empty
        
        time.sleep(1.1) # Wait for refill
        self.assertTrue(limiter.consume()) # Should pass now
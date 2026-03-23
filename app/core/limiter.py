from fastapi import Request, HTTPException
from collections import defaultdict, deque
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window_seconds =  window_seconds
        self.requests = defaultdict(deque)
    
    def __call__(self, request: Request):
        ip = request.client.host
        now = datetime.now()
        cutoff = now - timedelta(seconds=self.window_seconds)

        while self.requests[ip] and self.requests[ip][0] < cutoff:
            self.requests[ip].popleft()
        
        if len(self.requests[ip]) >= self.max_requests:
            raise HTTPException(status_code=429, detail="Too many requests!")
        
        self.requests[ip].append(now)



register_limiter = RateLimiter(3, 60)
login_limiter = RateLimiter(5, 60)

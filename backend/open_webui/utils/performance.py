import asyncio
import time
from functools import wraps
from typing import Dict, Any
import logging

log = logging.getLogger(__name__)

class PerformanceCache:
    def __init__(self):
        self._cache = {}
        self._timestamps = {}
    
    def get(self, key: str, ttl: int = 300):
        if key in self._cache:
            if time.time() - self._timestamps[key] < ttl:
                return self._cache[key]
            else:
                del self._cache[key]
                del self._timestamps[key]
        return None
    
    def set(self, key: str, value: Any):
        self._cache[key] = value
        self._timestamps[key] = time.time()

cache = PerformanceCache()

def cached(ttl: int = 300):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            result = cache.get(cache_key, ttl)
            if result is not None:
                return result
            
            result = await func(*args, **kwargs)
            cache.set(cache_key, result)
            return result
        return wrapper
    return decorator

def debounce(wait: float):
    def decorator(func):
        last_called = {}
        
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{id(args[0]) if args else 'global'}"
            now = time.time()
            
            if key in last_called and now - last_called[key] < wait:
                return None
            
            last_called[key] = now
            return await func(*args, **kwargs)
        return wrapper
    return decorator
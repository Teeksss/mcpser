import redis
import os
import pickle

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
CACHE_TTL = 60 * 10  # 10 dakika

class RedisCache:
    def __init__(self, prefix="mcp:cache"):
        self.prefix = prefix
        self.client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=False)

    def _key(self, key):
        return f"{self.prefix}:{key}"

    def get(self, key):
        value = self.client.get(self._key(key))
        return pickle.loads(value) if value else None

    def set(self, key, value, ttl=CACHE_TTL):
        self.client.setex(self._key(key), ttl, pickle.dumps(value))

    def delete(self, key):
        self.client.delete(self._key(key))

cache = RedisCache()
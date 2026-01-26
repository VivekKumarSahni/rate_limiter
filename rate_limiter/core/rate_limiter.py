import time
from rate_limiter.clients.redis_client import RedisLuaClient

class RateLimiter:
    def __init__(
        self,
        redis_host: str,
        redis_port: int,
        prefix: str = "rl",
        ):
        self.redis = RedisLuaClient(redis_host=redis_host,redis_port=redis_port)
        self.prefix = prefix

    def build_key(self, ip: str, route: str):
        return f"{self.prefix}:{ip}:{route}"

    def allow(self, ip: str, route: str, capacity: int, per_seconds: int):
        key = self.build_key(ip, route)
        refill_rate = capacity / per_seconds
        now = int(time.time())

        allowed, remaining, retry_after = self.redis.token_bucket(
            key=key,
            capacity=capacity,
            refill_rate=refill_rate,
            now=now
        )
        return {
            "allowed": bool(allowed),
            "remaining": remaining,
            "retry_after": retry_after if retry_after != 0 else None
        }

        
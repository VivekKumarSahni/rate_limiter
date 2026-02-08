"""Factory for common Redis-backed rate limiter setup."""

from rate_limiter.core.rate_limiter import RateLimiter
from rate_limiter.core.defaults import ClusterSafeKeyBuilder, DefaultClock
from rate_limiter.clients.redis_client import RedisLuaClient


def rate_limiter(
    host: str = "localhost",
    port: int = 6379,
    prefix: str = "rl",
) -> RateLimiter:
    """Build a RateLimiter with Redis backend, prefix key builder, and system clock.

    One-line usage for library users:

        rate_limiter = rate_limiter(host="localhost", port=6379, prefix="rl")

    For custom backend/key_builder/clock, construct RateLimiter directly.
    """
    backend = RedisLuaClient(redis_host=host, redis_port=port)
    key_builder = ClusterSafeKeyBuilder(prefix=prefix)
    clock = DefaultClock()
    return RateLimiter(backend=backend, key_builder=key_builder, clock=clock)

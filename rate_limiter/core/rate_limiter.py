from rate_limiter.core.backend import RateLimitBackend, KeyBuilder, Clock


class RateLimiter:
    """Core rate limiter. Depends on Backend, KeyBuilder, Clock (small interfaces)."""

    def __init__(
        self,
        backend: RateLimitBackend,
        key_builder: KeyBuilder,
        clock: Clock,
    ):
        self._backend = backend
        self._key_builder = key_builder
        self._clock = clock

    def allow(self, ip: str, route: str, capacity: int, per_seconds: int) -> dict:
        key = self._key_builder.build_key(ip=ip, route=route)
        refill_rate = capacity / per_seconds
        now = self._clock.now()

        allowed, remaining, retry_after = self._backend.check(
            key=key,
            capacity=capacity,
            refill_rate=refill_rate,
            now=now,
        )
        return {
            "allowed": bool(allowed),
            "remaining": remaining,
            "retry_after": retry_after if retry_after != 0 else None,
        }

        
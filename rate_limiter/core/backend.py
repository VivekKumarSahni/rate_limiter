"""Small interfaces for rate limiter (Interface Segregation)."""

from typing import Protocol


class RateLimitBackend(Protocol):
    """Backend: script/allow. Only check()."""

    def check(
        self,
        key: str,
        capacity: int,
        refill_rate: float,
        now: int,
    ) -> tuple[int, int, int]:
        """Check rate limit. Returns (allowed 0/1, remaining, retry_after)."""
        ...


class KeyBuilder(Protocol):
    """Key builder: build_key(ip, route) -> key string."""

    def build_key(self, ip: str, route: str) -> str:
        """Build rate limit key from ip and route."""
        ...


class Clock(Protocol):
    """Clock: now() -> current time in seconds (e.g. Unix timestamp)."""

    def now(self) -> int:
        """Return current time in seconds."""
        ...

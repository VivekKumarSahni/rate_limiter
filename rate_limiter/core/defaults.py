"""Default implementations for KeyBuilder and Clock."""

import time
from rate_limiter.core.backend import KeyBuilder, Clock


class PrefixKeyBuilder:
    """Key builder: prefix:ip:route (flat key, no hash tag)."""

    def __init__(self, prefix: str = "rl"):
        self.prefix = prefix

    def build_key(self, ip: str, route: str) -> str:
        return f"{self.prefix}:{ip}:{route}"


class ClusterSafeKeyBuilder:
    """Key builder for Redis Cluster: prefix:{ip}:route so keys for same IP share slot."""

    def __init__(self, prefix: str = "rl"):
        self.prefix = prefix

    def build_key(self, ip: str, route: str) -> str:
        # Triple braces: {{{ip}}} -> literal { + ip value + literal }
        return f"{self.prefix}:{{{ip}}}:{route}"


class DefaultClock:
    """Clock using system time (Unix seconds)."""

    def now(self) -> int:
        return int(time.time())

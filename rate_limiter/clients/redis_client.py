import redis
from pathlib import Path
import importlib.resources as resources

class RedisLuaClient:
    def __init__(self, redis_host: str, redis_port: int):
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.client = redis.Redis(
            host=self.redis_host,
            port=self.redis_port,
            decode_responses=True,
        )
        self.script_sha = None

    def load_script(self):
        lua_path = Path(__file__).parent / "lua" / "token_bucket.lua"
        script = lua_path.read_text()
        # with resources.open_text(
        #     "rate_limiter.clients.lua",
        #     "token_bucket.lua"
        # ) as f:
        #     script = f.read()
        self.script_sha = self.client.script_load(script)

    def check(self, key: str, capacity: int, refill_rate: float, now: int) -> tuple[int, int, int]:
        """RateLimitBackend protocol: check rate limit. Returns (allowed 0/1, remaining, retry_after)."""
        return self.token_bucket(key=key, capacity=capacity, refill_rate=refill_rate, now=now)

    def token_bucket(self, key: str, capacity: int, refill_rate: float, now: int) -> tuple[int, int, int]:
        if not self.script_sha:
            self.load_script()

        try:
            return self.client.evalsha(
                self.script_sha,
                1,
                key,
                capacity,
                refill_rate,
                now,
            )
        except redis.exceptions.NoScriptError:
            # Redis restart or script cache lost
            self.load_script()
            return self.client.evalsha(
                self.script_sha,
                1,
                key,
                capacity,
                refill_rate,
                now,
            )
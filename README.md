# rate-limiter

A Redis-backed token bucket rate limiter for Python. Uses Lua scripts for atomic operations and currently ships with a **FastAPI** adapter.

## Requirements

- Python ≥ 3.12
- Redis (local or remote)
- FastAPI (only if using the FastAPI adapter)

## Installation

### As a dependency

**Install from GitHub (recommended for other projects)**

Add to your `pyproject.toml`:

```toml
dependencies = [
    # ... your other deps ...
    "rate-limiter @ git+https://github.com/VivekKumarSahni/rate_limiter.git@0.1.2",
]
```
# Use latest release tag instead of 0.1.2

Or with pip:

```bash
pip install "rate-limiter @ git+https://github.com/VivekKumarSahni/rate_limiter.git@0.1.2"
```

Or in `requirements.txt`:

```
rate-limiter @ git+https://github.com/VivekKumarSahni/rate_limiter.git@0.1.2
```


## Usage in other projects

### FastAPI (current adapter)

Ensure your endpoint receives a `Request` (so the decorator can read IP and path). Apply the decorator **below** `@app.get` (or equivalent) so FastAPI sees the route first.

```python
from fastapi import FastAPI, Request
from rate_limiter.core.rate_limiter import RateLimiter
from rate_limiter.adapters.fastapi import rate_limit

app = FastAPI()
rate_limiter = RateLimiter(redis_host="localhost", redis_port=6379, prefix="rl")

@app.get("/search")
@rate_limit(rate_limiter, capacity=5, per_seconds=60)
def search(request: Request):
    return {"message": "search results"}
```

- **Sync and async** — The decorator works with both; no need to change your endpoint.
- **429 responses** — When the limit is exceeded, the adapter raises `HTTPException(429)` and sets the `Retry-After` header from the limiter result.

### Using the core only (any framework)

You can use the core `RateLimiter` without FastAPI: pass in `ip` and `route` (or any identifiers) and interpret the result yourself.

```python
from rate_limiter.core.rate_limiter import RateLimiter

limiter = RateLimiter(redis_host="localhost", redis_port=6379, prefix="rl")
result = limiter.allow(ip="1.2.3.4", route="/api/expensive", capacity=10, per_seconds=60)

if not result["allowed"]:
    # Return 429, wait result["retry_after"] seconds, etc.
    pass
# result["remaining"] = tokens left
```

Use this in Flask, Django, Starlette, or any other Python app; you only need to map your framework’s request object to `ip` and `route` (or your own key scheme).

## Configuration

| Parameter       | Description                          |
|----------------|--------------------------------------|
| `redis_host`   | Redis host (e.g. `localhost`)        |
| `redis_port`   | Redis port (e.g. `6379`)             |
| `prefix`       | Key prefix in Redis (default `rl`)   |
| `capacity`     | Bucket size (max tokens)             |
| `per_seconds`  | Time window for refill (e.g. 60)     |

Limit is “`capacity` requests per `per_seconds`” with token bucket semantics.

## TODO / Roadmap

### Framework support

- **FastAPI** — Done (decorator in `rate_limiter.adapters.fastapi`).
- **Flask** — Adapter (e.g. `rate_limiter.adapters.flask`) to wrap views and return 429 with `Retry-After`.
- **Django** — Middleware or decorator (e.g. `rate_limiter.adapters.django`) using core `RateLimiter`.
- **Starlette** — Adapter for pure Starlette apps (reusable for FastAPI under the hood).
- **Generic** — Document “core only” usage so any framework can plug in with minimal code.

### Improvements

- **Weighted / cost-based limits** — Consume more than one token per request (e.g. by body size or “cost” parameter).
- **Configurable key builder** — Allow custom key strategy (e.g. user id, API key, or header-based) instead of only IP + route.
- **Graceful degradation** — Optional “allow by default” or “deny by default” when Redis is unavailable.

### Packaging / DX

- **Optional dependencies** — Make FastAPI (and future Flask/Django) extras so `pip install rate_limiter[fastapi]` doesn’t pull in unused frameworks.
- **Tests** — Unit tests for core + Redis mock; integration test with real Redis (e.g. in CI).

---

**Summary:** Use the **core** `RateLimiter` in any project; use the **FastAPI adapter** for FastAPI. For other frameworks, use the core and map request → `ip`/`route`, or add dedicated adapters (Flask, Django, Starlette) later.

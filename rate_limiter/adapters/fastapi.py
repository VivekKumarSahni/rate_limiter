import inspect
from fastapi import Request, HTTPException
from functools import wraps

def rate_limit(limiter, capacity: int, per_seconds: int):
    def decorator(endpoint):
        is_async = inspect.iscoroutinefunction(endpoint)
        
        @wraps(endpoint)
        async def wrapper(*args, **kwargs):
            # Extract Request from kwargs or args
            request: Request = kwargs.get("request") or next(
                (arg for arg in args if isinstance(arg, Request)), 
                None
            )
            
            if request is None:
                raise RuntimeError("FastAPI rate_limit decorator requires `request` argument")
            
            ip = request.client.host
            route = request.url.path

            result = limiter.allow(ip=ip, route=route, capacity=capacity, per_seconds=per_seconds)

            if not result["allowed"]:
                raise HTTPException(
                    status_code=429,
                    detail="Rate limit exceeded",
                    headers={"Retry-After": str(result["retry_after"])}
                )

            # Handle both sync and async endpoints
            if is_async:
                return await endpoint(*args, **kwargs)
            else:
                return endpoint(*args, **kwargs)
        return wrapper
    return decorator
 
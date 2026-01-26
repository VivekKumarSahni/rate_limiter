-- KEYS[1] = rate limit key
-- ARGV[1] = capacity
-- ARGV[2] = refill_rate (tokens per second)
-- ARGV[3] = current_timestamp (seconds)

local key = KEYS[1]
local capacity = tonumber(ARGV[1])
local refill_rate = tonumber(ARGV[2])
local now = tonumber(ARGV[3])

-- Fetch existing state
local data = redis.call("HMGET", key, "tokens", "last_refill")
local tokens = tonumber(data[1])
local last_refill = tonumber(data[2])

-- Initialize if missing
if tokens == nil then
  tokens = capacity
  last_refill = now
end

-- Refill tokens
local elapsed = math.max(0, now - last_refill)
local refill = elapsed * refill_rate
tokens = math.min(capacity, tokens + refill)

local allowed = 0
local retry_after = 0
if tokens >= 1 then
  allowed = 1
  tokens = tokens - 1
else
  retry_after = math.ceil((1 / refill_rate)*(1-tokens))
end

-- 

-- Persist updated state
redis.call("HMSET", key,
  "tokens", tokens,
  "last_refill", now
)

-- Set TTL to clean up inactive users
redis.call("EXPIRE", key, math.ceil(capacity / refill_rate * 2))

return { allowed, tokens, retry_after }
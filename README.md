

<!-- rate token 1 second 
1-tokens    (1/rate)*(1-tokens) -->

<!-- 1 type casting of lua scripts -->

handle request missing exception
handle abstracting redis and scripts
how weighted cost can be better approach from client usage perspective
handle slots when clusters are there


When this is not enough

If you’re:

running high throughput (Kafka / rate limiting / distributed locks)

using async FastAPI

or handling Lua reloads on Redis restart

then we should add:

connection pooling tuning

SCRIPT LOAD + fallback to EVAL

retry logic
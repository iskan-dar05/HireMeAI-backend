import redis

# Use your RedisLabs / Upstash credentials
redis_client = redis.Redis(
    host='redis-11253.c283.us-east-1-4.ec2.cloud.redislabs.com',
    port=11253,
    decode_responses=True,
    username="default",   # optional, depends on provider
    password="ClfnhpP6j2KoC3kMHTMbIQwKhEwESRTE",
)

# Test connection
success = redis_client.set('foo', 'bar')
print("SET success:", success)

result = redis_client.get('foo')
print("GET result:", result)

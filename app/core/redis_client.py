import redis
from .config import settings


redis_client = redis.Redis(
	host="redis",
	port=6379,
	db=0,
	decode_responses=True
)
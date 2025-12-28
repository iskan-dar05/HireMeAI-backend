import redis

r = redis.Redis(host='localhost', port=6379, db=0)


def set_blacklist_token(user_id: str, token: str):
	r.set(user_id, token)

def get_blacklist_token(user_id):
	return r.get(user_id)


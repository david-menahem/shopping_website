import redis

from config.config import Config

config = Config()

redis_client = redis.Redis(host=config.REDIS_HOST, port=int(config.REDIS_PORT))


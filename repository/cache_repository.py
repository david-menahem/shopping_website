from typing import Optional

from config.config import Config
from redis_client.redis_client import redis_client


config = Config()


def get_cache_entity(key: str) -> Optional[str]:
    if is_key_exists(key):
        return redis_client.get(key)
    else:
        return None


def create_entity(key: str, value: str):
    if not is_key_exists(key):
        redis_client.setex(key, config.REDIS_TTL, value)


def update_entity(key: str, value: str):
    if is_key_exists(key):
        print(key)
        redis_client.setex(key, config.REDIS_TTL, value)


def delete_entity(key: str):
    if is_key_exists(key):
        redis_client.delete(key)


def is_key_exists(key: str) -> bool:
    return redis_client.exists(key)

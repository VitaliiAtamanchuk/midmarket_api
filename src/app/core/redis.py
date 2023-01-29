import os
import json

from redis import asyncio as aioredis


redis = aioredis.from_url(os.getenv("REDIS_URL"), decode_responses=True)
DEFAULT_KEY_PREFIX = 'key'
TWO_MINUTES = 60 * 60


def prefixed_key(f):
    """
    A method decorator that prefixes return values.
    Prefixes any string that the decorated method `f` returns with the value of
    the `prefix` attribute on the owner object `self`.
    """

    def prefixed_method(*args, **kwargs):
        self = args[0]
        key = f(*args, **kwargs)
        return f'{self.prefix}:{key}'

    return prefixed_method


class Keys:
    """Methods to generate key names for Redis data structures."""

    def __init__(self, prefix: str = DEFAULT_KEY_PREFIX):
        self.prefix = prefix

    @prefixed_key
    def cache_key(self) -> str:
        return f'cache'


def make_keys():
    return Keys()


class Keys:
    """Methods to generate key names for Redis data structures."""

    def __init__(self, prefix: str = DEFAULT_KEY_PREFIX):
        self.prefix = prefix

    @prefixed_key
    def cache_key(self) -> str:
        return f'cache'


async def get_cache(keys: Keys):
    current_hour_cache_key = keys.cache_key()
    current_hour_stats = await redis.get(current_hour_cache_key)

    if current_hour_stats:
        return json.loads(current_hour_stats)


async def set_cache(data, keys: Keys):
    await redis.set(
        keys.cache_key(),
        json.dumps(data),
        ex=TWO_MINUTES,
    )

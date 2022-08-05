import logging

import redis
from src.settings import Settings


class TokensStorage:

    def __init__(self):
        logging.info('Connecting to Redis...')
        app_settings = Settings()
        self.redis_client = redis.Redis(host=app_settings.redis_host,
                                        port=app_settings.redis_port,
                                        charset='utf-8',
                                        decode_responses=True)

    def set(self, key, val, ttl=100):
        self.redis_client.set(key, val, ttl)

    def get(self, key):
        return self.redis_client.get(key)


redis_client = TokensStorage()

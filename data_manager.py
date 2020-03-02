from redis.client import StrictRedis
from settings import REDIS_PERSISTENT_DB


class DataManager:

    client = StrictRedis.from_url(REDIS_PERSISTENT_DB, decode_responses=True)
    words_counter = 'words'

    def increment_key(self, key, amount):
        self.client.hincrby(name=self.words_counter, key=key, amount=amount)

    def get_key(self, key):
        return self.client.hget(self.words_counter, key)

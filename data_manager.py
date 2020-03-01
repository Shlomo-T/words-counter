from redis.client import StrictRedis


class DataManager:

    client = StrictRedis(decode_responses=True)
    words_counter = 'words'
    jobs_hash = 'jobs'

    def increment_key(self, key, amount):
        self.client.hincrby(name=self.words_counter, key=key, amount=amount)

    def get_key(self, key):
        return self.client.hget(self.words_counter, key)

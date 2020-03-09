from redis.client import StrictRedis
from settings import REDIS_PERSISTENT_DB, DB_FILE_PATH
from logging import getLogger
from threading import Lock, current_thread
import json


logger = getLogger('app.data')


class DataManager:

    client = StrictRedis.from_url(REDIS_PERSISTENT_DB, decode_responses=True)
    words_counter = 'words'

    def increment_keys(self, values):
        if values:
            for key, amount in values.items():
                self.increment_key(key=key, amount=amount)

    def increment_key(self, key, amount):
        self.client.hincrby(name=self.words_counter, key=key, amount=amount)

    def get_key(self, key):
        return self.client.hget(self.words_counter, key)


class FileDBManager:

    lock = Lock()

    def __init__(self, file_name=DB_FILE_PATH):
        from pathlib import Path
        self.file_name = file_name
        Path(file_name).touch(exist_ok=True)

    def increment_keys(self, values):
        if values:
            with self.lock:
                with open(self.file_name, 'r+') as f:
                    print("{} start writing {} into {}".format(current_thread().name, values, self.file_name))
                    file_content = f.read()
                    content_dict = json.loads(file_content) if file_content else {}
                    for key, amount in values.items():
                        self.increment_key(content_dict, key=key, amount=amount)
                    f.seek(0)
                    json.dump(content_dict, f, indent=4)
                    print("{} finished writing {} into {}".format(current_thread().name, values, self.file_name))

    def increment_key(self, data_dict, key, amount):
        if key in data_dict:
            data_dict[key] += amount
            return
        data_dict[key] = amount

    def get_key(self, key):
        value = 0
        with open(self.file_name, 'r') as f:
            file_content = f.read()
            file_content = json.loads(file_content) if file_content else {}
            if key in file_content:
                value = file_content[key]
        return value

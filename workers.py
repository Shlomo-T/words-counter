import requests
from collections import Counter
from redis.client import StrictRedis
from data_manager import DataManager
from abc import ABC, abstractmethod


class BaseWorker(ABC):

    client = StrictRedis()
    data_manager = DataManager()

    def __init__(self, _input):
        self.input = _input

    @abstractmethod
    def invoke(self):
        pass

    def process_batch(self, text):
        return Counter(text.split())

    def save_results(self, results):
        for word, count in results.items():
            key = word.lower()
            self.data_manager.increment_key(key=key, amount=count)


class RawTextWorker(BaseWorker):

    def invoke(self):
        results = self.process_batch(self.input)
        self.save_results(results)


class WebUrlWorker(BaseWorker):

    def invoke(self):
        try:
            response = requests.get(self.input, stream=True)
            if response.status_code == 200:
                for line in response.iter_lines():
                    results = self.process_batch(line)
                    self.save_results(results)
        finally:
            response.close()


class FileSystemWorker(BaseWorker):

    def invoke(self):
        with open(self.input) as fp:
            for line in fp:
                results = self.process_batch(line)
                self.save_results(results)

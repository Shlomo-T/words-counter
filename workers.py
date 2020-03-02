import requests
from collections import Counter
from redis.client import StrictRedis
from data_manager import DataManager
from abc import ABC, abstractmethod
import string

# Punctuation to remove - not includes dash and comma
punctuation = (string.punctuation + string.digits).replace(",-'", '')
translation_map = str.maketrans('', '', punctuation)


class BaseWorker(ABC):

    client = StrictRedis()
    data_manager = DataManager()

    def __init__(self, _input):
        self.input = _input

    @abstractmethod
    def invoke(self):
        pass

    def process_batch(self, text):
        if text:
            text_without_punctuation = text.translate(translation_map)
            return Counter(text_without_punctuation.split())

    def save_results(self, results):
        if results:
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
                for line in response.iter_lines(decode_unicode=True):
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

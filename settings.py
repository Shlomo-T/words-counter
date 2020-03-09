import os

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/1')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/1')
REDIS_PERSISTENT_DB = os.environ.get('REDIS_PERSISTENT_DB', 'redis://localhost:6379/0')
USE_REDIS = bool(int(os.environ.get('USE_REDIS', 0)))
THREAD_POOL_SIZE = int(os.environ.get('THREAD_POOL_SIZE', 5))
DB_FILE_PATH = os.environ.get('DB_FILE_PATH', './words.json')

from flask import Flask, request
from workers import *
from data_manager import DataManager
from celery import Celery
from settings import CELERY_BROKER_URL, CELERY_RESULT_BACKEND


app = Flask(__name__)

app.config['CELERY_BROKER_URL'] = CELERY_BROKER_URL
app.config['CELERY_RESULT_BACKEND'] = CELERY_RESULT_BACKEND
app.config['CELERY_TRACK_STARTED'] = True
app.config['CELERY_SEND_EVENTS'] = True


celery = Celery(app.name, broker=CELERY_BROKER_URL)
celery.conf.update(app.config)


allowed_workers = {'text': RawTextWorker, 'url': WebUrlWorker, 'file': FileSystemWorker}


@celery.task
def naive_worker_execute(input_method, input_data):
    worker = allowed_workers[input_method](input_data)
    worker.invoke()


@app.route('/word-counter', methods=['POST'], strict_slashes=False)
def word_counter():
    payload = request.json
    if not payload or 'worker' not in payload or payload['worker'] not in allowed_workers or 'parameter' not in payload:
        return 'Bad Input', 400
    worker = payload['worker']
    input_data = payload['parameter']
    naive_worker_execute.delay(worker, input_data)
    return 'OK!', 200


@app.route('/word-statistics', methods=['GET'], strict_slashes=False)
def word_statistics():
    keyword = request.args.get('keyword')
    if not keyword:
        return 'Bad Input: Keyword parameter is missing', 400
    value = DataManager().get_key(key=keyword.lower())
    response_body = {'keyword': keyword, 'amount': value if value else 0}
    return response_body, 200


if __name__ == '__main__':
    app.run()

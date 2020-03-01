from flask import Flask, request
from workers import *
from data_manager import DataManager
from celery import Celery


app = Flask(__name__)

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/1'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/1'
app.config['CELERY_TRACK_STARTED'] = True
app.config['CELERY_SEND_EVENTS'] = True


celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


allowed_methods = {'text': RawTextWorker, 'url': WebUrlWorker, 'file': FileSystemWorker}


@celery.task
def naive_worker_execute(input_method, input_data):
    worker = allowed_methods[input_method](input_data)
    try:
        worker.invoke()
    except Exception as ex:
        return repr(ex), 400


@app.route('/word-counter', methods=['POST'], strict_slashes=False)
def word_counter():
    payload = request.json
    if not payload or 'method' not in payload or payload['method'] not in allowed_methods or 'parameter' not in payload:
        return 'Bad Input', 400
    input_method = payload['method']
    input_data = payload['parameter']
    naive_worker_execute.delay(input_method,input_data)
    return 'OK!', 200


@app.route('/word-statistics', methods=['POST'], strict_slashes=False)
def word_statistics():
    payload = request.json
    if not payload or 'keyword' not in payload:
        return 'Bad Input', 400
    key = payload['keyword'].lower()
    value = DataManager().get_key(key=key)
    response_body = {'keyword': key, 'amount': value if value else 0}
    return response_body, 200


if __name__ == '__main__':
    app.run()

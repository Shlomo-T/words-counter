# Words-Counter


### Prerequisites

* Python 3
* Redis should be installed as it used as a persistent DB for API results 
and queuing Celery tasks in background.

### Installation

All dependencies listed in the requirements.txt file. Install them using 
pip (preferably in virtual environment).

```
pip install -r requirements.txt
```

## Running the app

Celery workers should run in the background and handle tasks. 
Amount of workers should fit to machine resources.
```
celery worker -A app.celery --loglevel=info
```
App can be ran by flask development server or using real wsgi server.
```
Flask run 
----------
python app.py
```

## Assumptions for valid input

* All files and url should return textual data and special encoding is not needed.
* Resources availability - since celery running tasks in background and 
not necessarily immediately after the api call (i.e file isn't deleted / url still available on the web).
* Correct file paths and urls - this is not being validated and errors regarding to bad urls and file paths will be raised at execution time.

## Usage

#### Words count endpoint:
Request parameters should be sent on request body as json
* worker: worker type to handle the task - options are text, url or file
* parameter: input for the worker - options plain-text, file-path, url to a website

cUrl example:
```
curl -X POST \
  /word-counter \
  -H 'Content-Type: application/json' \
  -d '{
	"worker": "url",
	"parameter": "https://www.gutenberg.org/files/36/36-0.txt"
}'
```

#### Words statistics endpoint:
Keyword parameter should be passed on url params.

cUrl example:
```
curl -X GET \
  '/word-statistics?keyword=god' \
  -H 'Content-Type: application/json'
 ```

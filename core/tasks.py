from celery import Celery
import requests


app = Celery(broker="redis://redis:6379/0", backend="redis://redis:6379/1")


@app.task
def crawl_from_url(url: str):
    params = {"url": url}
    response = requests.post("http://crawler_app:8000/crawl", params=params)
    return response.json()

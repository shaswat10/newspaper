from celery import shared_task
import requests


@shared_task(bind=True)
def fetch_news(self, keyword):
    #perform operations
    response = ""
    return response
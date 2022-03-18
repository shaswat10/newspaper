from celery import shared_task
import requests
from newsProject.const import NEWS_API_CALL, API_KEY
import json
from . import serializers
from . import models

@shared_task(bind=True)
def save_news_todb(self, news):
    print("DSAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    # print(news['articles'][0])
    temp_dict = {}

    if news["status"] == 'ok':
        for article in news["articles"]:
            serialized_source = serializers.SourceSerializer(data=article['source'])

            if serialized_source.is_valid():
                serialized_source.save()

            article['source'] = article['source']['id']

            serialized_news = serializers.NewsSerializer(data=article)
            
            if serialized_news.is_valid():
                serialized_news.save()
            else:
                print(serialized_news.errors)
    # print(news)
    return "done"
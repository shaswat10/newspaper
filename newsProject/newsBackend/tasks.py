from celery import shared_task
import requests
from newsProject.const import NEWS_API_CALL, API_KEY
import json
from . import serializers
from . import models

@shared_task(bind=True)
def save_news_todb(self, news):

    if news["status"] == 'ok':
        for article in news["articles"]:

            if article['source']['id'] == None:
                article['source']['id'] = "Empty"

            # sometimes id data comes as null, so we check for soruce name to see if record exists
            source_obj = models.sourceModel.objects.filter(name=article['source']['name']).first()
    
            if not source_obj:
                source_dict = {'source_id':article['source']['id'], 'name':article['source']['name']}
                serialized_source = serializers.SourceSerializer(data=source_dict)

                if serialized_source.is_valid():
                    source_obj=serialized_source.save()                  
                else:
                    print(serialized_source.errors)
                    continue
                    
            article['source'] = source_obj.id   # setting up source i as foreignkey in article table

            serialized_news = serializers.NewsSerializer(data=article)
            
            if serialized_news.is_valid():
                serialized_news.save()
            else:
                print(serialized_news.errors)

    return "done"
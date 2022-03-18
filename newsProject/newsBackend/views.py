from django.shortcuts import render
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, getJWTTokenSerializer, UserSerializerWithToken, NewsSerializer
from rest_framework.decorators import api_view
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from . import models
from django.db.models import Q
from django.http import Http404
import requests
from . import tasks
# Create your views here.



# user login view
class userLoginView(TokenObtainPairView):
    serializer_class = getJWTTokenSerializer

@api_view(['POST'])
def registerView(request):
    data = request.data
    user_obj = User.objects.create(first_name=data['name'], username=data['username'], email=data['email'], password=data['password'])
    serialized_data = UserSerializerWithToken(user_obj, many=False)

    if serialized_data.is_valid:
        return Response(serialized_data.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)



class getNewsList(APIView):

    def fetch_news_from_api(self, keyword):
        print("FFFFFFFFFFFFFFFFFF")
        print(keyword)
        response = requests.get("https://newsapi.org/v2/everything?q=apple&apiKey=991b55fe3ff742f7a3d232202c6c4fdc")
        print(response.json())
        responseData = tasks.save_news_todb.delay(response.json())
        print("responseData")
        return response.json()

    def get_news_obj(self, keyword):
        try:
            return models.newsModel.objects.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword) | Q(content__icontains=keyword) | Q(author__icontains=keyword))
        except models.newsModel.DoesNotExist:
            return Http404

    def get(self, request, pk=None, format=None):
        news_obj = self.get_news_obj(pk)
        print("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")
        print(news_obj)
        if not news_obj:
            responseData = self.fetch_news_from_api(pk)
            return Response(responseData, status=status.HTTP_200_OK)
        else:
            serialized_news = NewsSerializer(news_obj, many=True)
            print(serialized_news.data)
            return Response(serialized_news.data, status=status.HTTP_200_OK)
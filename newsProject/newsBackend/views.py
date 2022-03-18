from django.shortcuts import render
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, getJWTTokenSerializer, UserSerializerWithToken, NewsSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from . import models
from django.db.models import Q
from django.http import Http404
import requests
from . import tasks
from django.contrib.auth.hashers import make_password
# Create your views here.



# user login view with jwt token
class userLoginView(TokenObtainPairView):
    serializer_class = getJWTTokenSerializer



# user registration view
@api_view(['POST'])
def registerView(request):
    data = request.data

    print(data)
    if data['password'] != data['checkpassword']:
        print("ehererere i amma")
        return Response(status=status.HTTP_400_BAD_REQUEST)

    user_obj = User.objects.create( username=data['username'], email=data['email'], password=make_password(data['password']))
    serialized_data = UserSerializerWithToken(user_obj, many=False)

    if serialized_data.is_valid:
        
        return Response(serialized_data.data, status=status.HTTP_201_CREATED)
    else:
   
        print(serialized_data.errors)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


# api to get news list
class getNewsList(APIView):
    permission_classes = [IsAuthenticated]
    # fetct news from remote api if not present in database and then send it to celery
    def fetch_news_from_api(self, keyword):
        response = requests.get("https://newsapi.org/v2/everything?q="+keyword+"&apiKey=991b55fe3ff742f7a3d232202c6c4fdc")

        # sending task to celery
        responseData = tasks.save_news_todb.delay(response.json())

        return response.json()

    def get_news_obj(self, keyword):
        try:
            return models.newsModel.objects.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword) | Q(content__icontains=keyword) | Q(author__icontains=keyword))
        except models.newsModel.DoesNotExist:
            return Http404

    def get(self, request, pk=None, format=None):
        news_obj = self.get_news_obj(pk)
        if not news_obj:
            responseData = self.fetch_news_from_api(pk)
            return Response(responseData["articles"], status=status.HTTP_200_OK)
        else:
            serialized_news = NewsSerializer(news_obj, many=True)
            return Response(serialized_news.data, status=status.HTTP_200_OK)
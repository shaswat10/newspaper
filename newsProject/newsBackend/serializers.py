from curses import meta
from dataclasses import fields
from pyexpat import model
from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from . import models
# external imports
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

############
class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'password']
        # write_only_fields = ['password']
    
    def get_name(self, obj):
        print("*********************")
        print(obj)
        name = obj.first_name
        if name == '':
            name = obj.email
        return name



class getJWTTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data["username"] = self.user.username
        data["email"] = self.user.email

        return data


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])   
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'token', 'password']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class SourceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.sourceModel
        fields = ['source_id', 'name']



class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.newsModel
        fields='__all__'



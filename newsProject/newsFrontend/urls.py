from django.urls import path
from . import views

urlpatterns = [
    path('news/', views.NewsPage, name='token_obtain_pair'),
]
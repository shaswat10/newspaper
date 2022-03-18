from django.urls import path
from . import views

urlpatterns = [
    path('news/', views.NewsPage, name='news_view'),
    path('login/', views.loginView, name='login_view'),
    path('register/', views.registerView, name='register_view'),
    path('logout/', views.logoutPage, name='logout_view'),
]
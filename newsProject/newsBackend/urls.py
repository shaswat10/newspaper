from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('users/login/', views.userLoginView.as_view(), name='token_obtain_pair'),
    path('user/register/', views.registerView, name='register'),
    path('news/<slug:pk>', views.getNewsList.as_view(), name='register'),
]
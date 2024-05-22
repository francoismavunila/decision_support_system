from django.urls import path

from .views import *

urlpatterns = [
    path("", CreateUser.as_view()),
    path("login/", Login.as_view()),
  
]

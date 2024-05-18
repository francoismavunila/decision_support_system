from django.urls import path

from .views import *

urlpatterns = [
    path("", User.as_view()),
  
]

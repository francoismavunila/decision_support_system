from django.urls import path

from .views import *

urlpatterns = [
    path("", CategoryList.as_view()),
]

# predictions/urls.py
from django.urls import path
from .views import PredictSales

urlpatterns = [
    path('', PredictSales.as_view(), name='predict-sales'),
]

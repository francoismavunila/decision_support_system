# predictions/urls.py
from django.urls import path
from .views import PredictSales, ProductInsights

urlpatterns = [
    path('', PredictSales.as_view(), name='predict-sales'),
    path('<int:product_id>/', ProductInsights.as_view(), name='product-detail'),
]

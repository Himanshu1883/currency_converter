from django.urls import path
from .views import CurrencyConvertAPIView

urlpatterns = [
    path('convert/', CurrencyConvertAPIView.as_view(), name='currency-convert'),
]

from django.urls import path
from .views import currency_converter_form_view, CurrencyConvertAPIView

urlpatterns = [
    path('convert/', currency_converter_form_view, name='currency_form'),
    path('convert-api/', CurrencyConvertAPIView.as_view(), name='currency_api'),
]

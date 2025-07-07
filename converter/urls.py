from django.urls import path
from .views import CurrencyConvertAPIView, currency_convert_form

urlpatterns = [
    path('', currency_convert_form, name='currency_form'),  # HTML form at "/"
    path('convert/', CurrencyConvertAPIView.as_view(), name='currency_convert_api'),  # API at "/api/convert/"
]

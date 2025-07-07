from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from converter.views import currency_converter_form_view  # 👈 Import the UI view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', currency_converter_form_view, name='home'),  # 👈 Root shows UI
    path('api/', include('converter.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

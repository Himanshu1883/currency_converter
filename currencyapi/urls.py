from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Remove this from here
# from django.http import JsonResponse
# def home(request):
#     return JsonResponse({"message": "Welcome to the Currency Converter API!"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('converter.urls')),  # converter handles both API + UI
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

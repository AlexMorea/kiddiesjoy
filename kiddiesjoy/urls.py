from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import token_obtain_pair, token_refresh


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),              
    path('api/', include('core.api.urls_api')), 
    path('api/token/', token_obtain_pair, name='token_obtain_pair'),
    path('api/token/refresh/', token_refresh, name='token_refresh'),
]

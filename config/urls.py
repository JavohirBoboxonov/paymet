from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Bank Payment API",
      default_version='v1',
      description="Documentation for Bank Payment Module endpoints",
      contact=openapi.Contact(email="support@yourdomain.com"),
      license=openapi.License(name="BSD License"),
   ),
)
urlpatterns = [
    path('admin/', admin.site.class_urls if hasattr(admin.site, 'class_urls') else admin.site.urls),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', include('bank.urls'))
]
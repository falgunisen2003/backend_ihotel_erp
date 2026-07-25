"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from hotels.views import SwitchHotelView  

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Simple home view for Render health check & cron-jobs
def home(request):
    return HttpResponse("Backend is Running Successfully!")

schema_view = get_schema_view(
   openapi.Info(
      title="Hotel Management API",
      default_version='v1',
      description="API documentation for Hotel Management Backend",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Root Health Check Path
    path("", home, name="home"),

    path("admin/", admin.site.urls),

    # Switch Hotel API 
    path("api/auth/switch-hotel/", SwitchHotelView.as_view(), name="switch-hotel"),

    # Authentication API
    path("api/auth/", include("authentication.urls")),

    path(
        "api/frontoffice/",
        include("frontoffice.urls")
    ),

    path('api/housekeeping/', include('housekeeping.urls')),
    path('api/finance/', include('finance.urls')),
    path('api/reports/', include('reports.urls')),

    # Swagger UI URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
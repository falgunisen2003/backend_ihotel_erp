"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from hotels.views import SwitchHotelView  

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

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
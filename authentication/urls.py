from django.urls import path
from .views import LoginAPIView, SwitchHotelAPIView, TempPasswordResetView

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path("switch-hotel/", SwitchHotelAPIView.as_view(), name="switch_hotel"),
    path("temp-reset/", TempPasswordResetView.as_view(), name="temp_reset"),
]
from django.urls import path
from .views import LoginAPIView, SwitchHotelAPIView

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path("switch-hotel/", SwitchHotelAPIView.as_view(), name="switch_hotel"),
]
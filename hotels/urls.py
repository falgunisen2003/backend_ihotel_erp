from django.urls import path
from .views import SwitchHotelView

urlpatterns = [
    path('switch-hotel/', SwitchHotelView.as_view(), name='switch-hotel'),
]
from django.urls import path
from .views import (
    GuestListCreateAPIView,
    RoomListCreateAPIView,
    ReservationListCreateAPIView,
    CheckInAPIView,
    CheckOutAPIView,
)

urlpatterns = [
    path('guests/', GuestListCreateAPIView.as_view(), name='guest_list_create'),
    path('rooms/', RoomListCreateAPIView.as_view(), name='room_list_create'),
    path('reservations/', ReservationListCreateAPIView.as_view(), name='reservation_list_create'),
    
    # Check-In & Check-Out Workflow Routes
    path('reservations/<int:reservation_id>/check-in/', CheckInAPIView.as_view(), name='check_in'),
    path('reservations/<int:reservation_id>/check-out/', CheckOutAPIView.as_view(), name='check_out'),
]
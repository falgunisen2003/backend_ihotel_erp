from rest_framework import serializers
from .models import Guest, Room, Reservation


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    guest_details = GuestSerializer(source='guest', read_only=True)
    room_details = RoomSerializer(source='room', read_only=True)

    class Meta:
        model = Reservation
        fields = '__all__'
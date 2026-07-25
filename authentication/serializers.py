from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class SwitchHotelSerializer(serializers.Serializer):
    hotel_id = serializers.IntegerField()
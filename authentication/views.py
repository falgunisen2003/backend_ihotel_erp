from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import UserHotel
from roles.models import RolePermission

from .serializers import (
    LoginSerializer,
    SwitchHotelSerializer,
)

User = get_user_model()


class LoginAPIView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = getattr(serializer, "validated_data", {}) or {}
        if not isinstance(validated_data, dict):
            validated_data = {}

        login_identifier = validated_data.get("username")
        password = validated_data.get("password")

        user = None

        if login_identifier:
            # Check if the input is an email address
            if "@" in login_identifier:
                try:
                    user_obj = User.objects.using("default").get(email=login_identifier)
                    user = authenticate(username=user_obj.username, password=password)
                except User.DoesNotExist:
                    user = None
            else:
                # Fallback to standard username authentication
                user = authenticate(username=login_identifier, password=password)

        if user is None:
            return Response(
                {
                    "success": False,
                    "message": "Invalid Username/Email or Password"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Read active hotels for the user from the Master DB
        hotels = UserHotel.objects.using("default").filter(
            user=user,
            is_active=True
        ).select_related(
            "hotel",
            "role"
        )

        if not hotels.exists():
            return Response(
                {
                    "success": False,
                    "message": "No active hotels assigned to this user."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        refresh = RefreshToken.for_user(user)

        hotel_list = []
        default_hotel = None

        for item in hotels:
            # Fetch permissions from the Master DB
            permissions = RolePermission.objects.using("default").filter(
                role=item.role
            ).select_related("permission")

            permission_list = [
                p.permission.code
                for p in permissions
            ]

            hotel_data = {
                "hotel_id": item.hotel.pk,
                "hotel_name": item.hotel.name,
                "role": item.role.name,
                "permissions": permission_list,
                "is_default": item.is_default,
            }

            hotel_list.append(hotel_data)

            # Explicit default or fallback to the first hotel
            if item.is_default or default_hotel is None:
                default_hotel = hotel_data

        return Response(
            {
                "success": True,
                "message": "Login Successful",

                "access": str(refresh.access_token),
                "refresh": str(refresh),

                "user": {
                    "id": user.pk,
                    "username": user.username,
                    "email": user.email,
                },

                "default_hotel": default_hotel,
                "hotels": hotel_list,
            },
            status=status.HTTP_200_OK
        )


class SwitchHotelAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = SwitchHotelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = getattr(serializer, "validated_data", {}) or {}
        hotel_id = data.get("hotel_id")

        if hotel_id is None:
            return Response(
                {
                    "success": False,
                    "message": "hotel_id is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Retrieve target UserHotel from Master DB
        user_hotel = UserHotel.objects.using("default").filter(
            user=request.user,
            hotel_id=hotel_id,
            is_active=True
        ).select_related(
            "hotel",
            "role"
        ).first()

        if user_hotel is None:
            return Response(
                {
                    "success": False,
                    "message": "You don't have access to this hotel."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # -----------------------------------------
        # Remove previous default hotel (Master DB)
        # -----------------------------------------
        UserHotel.objects.using("default").filter(
            user=request.user
        ).update(
            is_default=False
        )

        # -----------------------------------------
        # Set selected hotel as default
        # -----------------------------------------
        user_hotel.is_default = True
        user_hotel.save(using="default", update_fields=["is_default"])

        # Fetch Permissions
        permissions = RolePermission.objects.using("default").filter(
            role=user_hotel.role
        ).select_related("permission")

        permission_list = [
            p.permission.code
            for p in permissions
        ]

        # Generate new JWT Token with updated context if needed
        refresh = RefreshToken.for_user(request.user)

        return Response(
            {
                "success": True,
                "message": "Hotel switched successfully",

                "access": str(refresh.access_token),
                "refresh": str(refresh),

                "hotel": {
                    "id": user_hotel.hotel.pk,
                    "name": user_hotel.hotel.name,
                },

                "role": user_hotel.role.name,

                "permissions": permission_list,
            },
            status=status.HTTP_200_OK
        )
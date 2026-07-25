from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Hotel

class SwitchHotelView(APIView):
    """
    API view to switch between user hotels and generate new JWT tokens.
    """
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Allows viewing instructions directly in the browser DRF interface.
        """
        return Response(
            {
                "message": "Send a POST request with 'hotel_id' to switch hotel.",
                "example_payload": {"hotel_id": 1}
            },
            status=status.HTTP_200_OK
        )

    def post(self, request):
        """
        Handles switching hotel and returns new JWT access and refresh tokens.
        """
        hotel_id = request.data.get("hotel_id")

        if not hotel_id:
            return Response(
                {
                    "success": False,
                    "message": "hotel_id is required."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Check if the requested hotel exists and is active
            hotel = Hotel.objects.get(id=hotel_id, is_active=True)
            
        except Hotel.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": "Hotel not found or inactive."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Generate new JWT Refresh and Access tokens for the user
        refresh = RefreshToken.for_user(request.user)
        
        # Optionally attach hotel context into the token payload
        refresh["hotel_id"] = hotel.pk

        return Response(
            {
                "success": True,
                "message": "Hotel switched successfully",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "hotel": {
                    "id": hotel.pk,
                    "name": hotel.name
                },
                "role": "Owner",  # Customize role logically based on your app logic
                "permissions": [
                    "dashboard.view",
                    "reservation.view",
                    "reservation.create",
                    "checkin.create",
                    "checkout.create",
                    "housekeeping.view",
                    "laundry.view",
                    "finance.view",
                    "report.view"
                ]
            },
            status=status.HTTP_200_OK
        )
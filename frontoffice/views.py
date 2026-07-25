from django.db import connections
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Guest, Room, Reservation
from .serializers import GuestSerializer, RoomSerializer, ReservationSerializer
from permissions.custom_permissions import HasModulePermission

# Cross-app imports for automated workflows
from finance.models import Invoice
from housekeeping.models import HousekeepingTask


class GuestListCreateAPIView(APIView):
    """
    API View to list and create Guests in the active Tenant Database with Role Permissions.
    """
    permission_classes = [HasModulePermission]

    def get_required_permission(self, request):
        if request.method == "GET":
            return "reservation.view"
        elif request.method == "POST":
            return "reservation.create"
        return None

    def get(self, request):
        guests = Guest.objects.all()

        print("=" * 60)
        target_db = guests.db
        print("Query Model Target DB Alias :", target_db)
        print("Active Hotel Database Name  :", connections[target_db].settings_dict["NAME"])
        print("=" * 60)

        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = GuestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        instance = serializer.save()

        saved_instance = instance[0] if isinstance(instance, list) and instance else instance
        target_db = getattr(getattr(saved_instance, "_state", None), "db", "hotel") or "hotel"

        print("=" * 60)
        print("Data Saved in DB Alias      :", target_db)
        print("Data Saved in Database      :", connections[target_db].settings_dict["NAME"])
        print("=" * 60)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RoomListCreateAPIView(APIView):
    """
    API View to handle Rooms in active tenant database.
    """
    permission_classes = [HasModulePermission]

    def get_required_permission(self, request):
        return "reservation.view" if request.method == "GET" else "reservation.create"

    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReservationListCreateAPIView(APIView):
    """
    API View to handle Bookings & Reservations in active tenant database.
    """
    permission_classes = [HasModulePermission]

    def get_required_permission(self, request):
        return "reservation.view" if request.method == "GET" else "reservation.create"

    def get(self, request):
        reservations = Reservation.objects.select_related('guest', 'room').all()
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ReservationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CheckInAPIView(APIView):
    """
    Check-In API: Updates Reservation status to 'checked_in' and Room status to 'occupied'.
    """
    permission_classes = [HasModulePermission]

    def get_required_permission(self, request):
        return "reservation.create"

    def post(self, request, reservation_id):
        try:
            reservation = Reservation.objects.get(id=reservation_id)
            reservation.status = 'checked_in'
            reservation.save()

            # Automatically update associated Room Status
            room = reservation.room
            room.status = 'occupied'
            room.save()

            return Response({
                "message": f"Guest {reservation.guest.first_name} checked in successfully to Room {room.room_number}.",
                "reservation_id": reservation.pk,
                "room_status": room.status
            }, status=status.HTTP_200_OK)

        except Reservation.DoesNotExist:
            return Response({"error": "Reservation not found"}, status=status.HTTP_404_NOT_FOUND)


class CheckOutAPIView(APIView):
    """
    Check-Out API:
    1. Updates Reservation to 'checked_out'
    2. Updates Room status back to 'available'
    3. Auto-creates Invoice in Finance Module
    4. Auto-creates Cleaning Task in Housekeeping Module (Status: 'dirty')
    """
    permission_classes = [HasModulePermission]

    def get_required_permission(self, request):
        return "reservation.create"

    def post(self, request, reservation_id):
        try:
            reservation = Reservation.objects.get(id=reservation_id)
            room = reservation.room
            guest = reservation.guest

            # 1. Update Reservation status
            reservation.status = 'checked_out'
            reservation.save()

            # 2. Update Room status
            room.status = 'available'
            room.save()

            # 3. Calculate stayed nights and Auto-create Invoice in Finance DB
            nights = (reservation.check_out_date - reservation.check_in_date).days or 1
            total_amount = room.price_per_night * nights

            invoice = Invoice.objects.create(
                guest_name=f"{guest.first_name} {guest.last_name}",
                room_number=room.room_number,
                total_amount=total_amount,
                paid_amount=total_amount,
                payment_status='paid',
                payment_method=request.data.get('payment_method', 'cash')
            )

            # 4. Auto-create Cleaning Task in Housekeeping DB
            HousekeepingTask.objects.create(
                room_number=room.room_number,
                status='dirty',
                priority='high',
                remarks=f"Auto Generated Task: Guest checked out from Reservation #{reservation.pk}"
            )

            return Response({
                "message": f"Check-out complete for Room {room.room_number}.",
                "invoice_id": invoice.pk,
                "total_billed": total_amount,
                "housekeeping_task": "Created (Dirty)"
            }, status=status.HTTP_200_OK)

        except Reservation.DoesNotExist:
            return Response({"error": "Reservation not found"}, status=status.HTTP_404_NOT_FOUND)
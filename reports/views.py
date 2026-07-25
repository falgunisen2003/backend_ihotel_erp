from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from django.utils.timezone import now
from finance.models import Invoice
from frontoffice.models import Room


class DailyRevenueAPIView(APIView):
    """
    API to calculate total daily revenue from paid invoices.
    """
    def get(self, request):
        today = now().date()
        total_revenue = Invoice.objects.filter(
            created_at__date=today,
            payment_status='paid'
        ).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0.00

        return Response({
            "date": today,
            "daily_revenue": total_revenue
        }, status=status.HTTP_200_OK)


class OccupancyReportAPIView(APIView):
    """
    API to check overall room occupancy rates and current room statuses.
    """
    def get(self, request):
        total_rooms = Room.objects.count()
        occupied_rooms = Room.objects.filter(status='occupied').count()
        available_rooms = Room.objects.filter(status='available').count()
        maintenance_rooms = Room.objects.filter(status='maintenance').count()

        occupancy_rate = (occupied_rooms / total_rooms * 100) if total_rooms > 0 else 0.0

        return Response({
            "total_rooms": total_rooms,
            "occupied_rooms": occupied_rooms,
            "available_rooms": available_rooms,
            "maintenance_rooms": maintenance_rooms,
            "occupancy_rate_percentage": round(occupancy_rate, 2)
        }, status=status.HTTP_200_OK)
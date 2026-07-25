from django.urls import path
from .views import DailyRevenueAPIView, OccupancyReportAPIView

urlpatterns = [
    path('daily-revenue/', DailyRevenueAPIView.as_view(), name='daily_revenue'),
    path('occupancy/', OccupancyReportAPIView.as_view(), name='occupancy_report'),
]
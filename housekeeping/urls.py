from django.urls import path
from .views import HousekeepingTaskListCreateAPIView

urlpatterns = [
    path('tasks/', HousekeepingTaskListCreateAPIView.as_view(), name='housekeeping_tasks'),
]
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from permissions.custom_permissions import HasModulePermission
from .models import HousekeepingTask
from .serializers import HousekeepingTaskSerializer


class HousekeepingTaskListCreateAPIView(APIView):
    """
    API View to list and create Housekeeping Tasks in the active Tenant Database.
    """
    permission_classes = [HasModulePermission]

    def get_required_permission(self, request):
        """
        Dynamically returns required permission code for the Housekeeping module.
        """
        return "housekeeping.view"

    def get(self, request):
        tasks = HousekeepingTask.objects.all()
        serializer = HousekeepingTaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = HousekeepingTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
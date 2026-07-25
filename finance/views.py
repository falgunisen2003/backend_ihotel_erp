from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from permissions.custom_permissions import HasModulePermission
from .models import Invoice
from .serializers import InvoiceSerializer


class InvoiceListCreateAPIView(APIView):
    permission_classes = [HasModulePermission]

    def get_required_permission(self, request):
        return "finance.view"

    def get(self, request):
        invoices = Invoice.objects.all()
        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = InvoiceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
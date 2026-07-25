from django.urls import path
from .views import InvoiceListCreateAPIView

urlpatterns = [
    path('invoices/', InvoiceListCreateAPIView.as_view(), name='invoice_list_create'),
]
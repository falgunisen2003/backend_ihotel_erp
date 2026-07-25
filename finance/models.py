from decimal import Decimal
from django.db import models


class Invoice(models.Model):
    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('partially_paid', 'Partially Paid'),
    )

    PAYMENT_METHOD = (
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('upi', 'UPI / Online'),
    )

    guest_name = models.CharField(max_length=150)
    room_number = models.CharField(max_length=20)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD, default='cash')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "invoices"

    def __str__(self):
        return f"Invoice #{self.pk} - {self.guest_name}"
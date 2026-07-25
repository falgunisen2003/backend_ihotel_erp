from django.db import models


class Guest(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "guests"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Room(models.Model):
    ROOM_TYPES = (
        ('single', 'Single'),
        ('double', 'Double'),
        ('suite', 'Suite'),
        ('deluxe', 'Deluxe'),
    )

    ROOM_STATUS = (
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Under Maintenance'),
    )

    room_number = models.CharField(max_length=20, unique=True)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, default='single')
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ROOM_STATUS, default='available')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "rooms"

    def __str__(self):
        return f"Room {self.room_number} ({self.room_type})"


class Reservation(models.Model):
    STATUS_CHOICES = (
        ('booked', 'Booked'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
    )

    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name='reservations')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reservations')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='booked')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "reservations"

    def __str__(self):
        return f"Reservation {self.pk} - Room {self.room.room_number}"
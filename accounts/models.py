from django.contrib.auth.models import AbstractUser
from django.db import models
from hotels.models import Hotel
from roles.models import Role

class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    def __str__(self):
        return self.username


class UserHotel(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE
    )

    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE
    )

    is_default = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "user_hotels"
        unique_together = ("user", "hotel")

    def __str__(self):
        return f"{self.user.username} - {self.hotel.name} - {self.role.name}"
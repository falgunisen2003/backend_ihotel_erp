from django.db import models


class HotelGroup(models.Model):
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=50, unique=True)

    logo = models.ImageField(
        upload_to="hotel_groups/",
        blank=True,
        null=True
    )

    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    address = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "hotel_groups"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Hotel(models.Model):
    group = models.ForeignKey(
        HotelGroup,
        on_delete=models.CASCADE,
        related_name="hotels"
    )

    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)

    logo = models.ImageField(
        upload_to="hotels/",
        blank=True,
        null=True
    )

    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)

    timezone = models.CharField(
        max_length=100,
        default="Asia/Kolkata"
    )

    currency = models.CharField(
        max_length=10,
        default="INR"
    )

    language = models.CharField(
        max_length=50,
        default="en"
    )

    # -------------------------
    # Database Configuration
    # -------------------------
    database_name = models.CharField(max_length=100)
    database_host = models.CharField(
        max_length=100,
        default="localhost"
    )
    database_port = models.CharField(
        max_length=10,
        default="5432"
    )
    database_user = models.CharField(max_length=100)
    database_password = models.CharField(max_length=255)
    database_engine = models.CharField(
        max_length=100,
        default="django.db.backends.postgresql"
    )
    # -------------------------

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "hotels"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.code})"
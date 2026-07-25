from django.contrib import admin
from .models import Guest


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "first_name",
        "last_name",
        "phone",
        "email",
    )

    search_fields = (
        "first_name",
        "last_name",
        "phone",
    )
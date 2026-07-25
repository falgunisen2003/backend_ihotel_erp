from django.contrib import admin
from .models import HotelGroup, Hotel


@admin.register(HotelGroup)
class HotelGroupAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "code",
        "is_active",
    )

    search_fields = (
        "name",
        "code",
    )


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "group",
        "city",
        "database_name",
        "is_active",
    )

    list_filter = (
        "group",
        "is_active",
    )

    search_fields = (
        "name",
        "city",
        "database_name",
    )
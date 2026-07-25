from django.conf import settings
from django.db import connections


def connect_hotel_database(hotel):

    db = settings.DATABASES["hotel"]

    db["ENGINE"] = "django.db.backends.postgresql"
    db["NAME"] = hotel.database_name
    db["USER"] = hotel.database_user
    db["PASSWORD"] = hotel.database_password
    db["HOST"] = hotel.database_host
    db["PORT"] = hotel.database_port

    connections.databases["hotel"] = db

    try:
        connections["hotel"].close()
    except Exception:
        pass
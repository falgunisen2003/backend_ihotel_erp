from core.database_middleware import get_current_hotel

class DatabaseRouter:
    HOTEL_APPS = {
        "frontoffice",
        "housekeeping",
        "finance",
        "reports",
    }

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.HOTEL_APPS:
            if get_current_hotel():
                return "hotel"
        return "default"

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.HOTEL_APPS:
            if get_current_hotel():
                return "hotel"
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.HOTEL_APPS:
            return db == "hotel"
        return db == "default"
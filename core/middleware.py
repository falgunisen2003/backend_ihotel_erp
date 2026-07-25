from threading import local

_thread_locals = local()


def set_current_hotel(hotel):
    _thread_locals.hotel = hotel


def get_current_hotel():
    return getattr(_thread_locals, "hotel", None)
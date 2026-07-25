import threading
from django.db import connections
from hotels.models import Hotel

# Thread local variable
_thread_locals = threading.local()

def get_current_hotel():
    return getattr(_thread_locals, 'hotel', None)

class DatabaseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        hotel_id = request.headers.get('X-Hotel-ID')
        
        if hotel_id:
            try:
                # Master/Default DB থেকে Hotel details রিড করবে
                hotel = Hotel.objects.using('default').get(id=hotel_id)
                _thread_locals.hotel = hotel
                
                # Dynamic DB Switch Engine
                hotel_conn = connections['hotel']
                
                # যদি বর্তমানে থাকা DB Name আর নতুন Hotel-এর DB Name এক না হয়:
                if hotel_conn.settings_dict.get('NAME') != hotel.database_name:
                    hotel_conn.close()  # পুরানো connection close করো
                    hotel_conn.settings_dict['NAME'] = hotel.database_name  # নতুন DB Name বসাও
                    
            except (Hotel.DoesNotExist, ValueError):
                _thread_locals.hotel = None
        else:
            _thread_locals.hotel = None

        response = self.get_response(request)
        
        # Cleanup request context
        _thread_locals.hotel = None
        return response
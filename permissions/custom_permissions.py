from rest_framework.permissions import BasePermission
from accounts.models import UserHotel
from roles.models import RolePermission


class HasModulePermission(BasePermission):
    """
    Custom permission class to verify whether a user has specific permissions
    for a selected hotel based on the 'X-Hotel-ID' request header.
    """

    def has_permission(self, request, view):
        # 1. Verify User Authentication
        if not request.user or not request.user.is_authenticated:
            return False

        # 2. Extract Active Hotel ID from Request Headers
        hotel_id = request.headers.get("X-Hotel-ID")
        if not hotel_id:
            return False

        # 3. Retrieve User's Assigned Role for the Hotel from Master DB
        user_hotel = UserHotel.objects.using("default").filter(
            user=request.user,
            hotel_id=hotel_id,
            is_active=True
        ).select_related("role").first()

        if not user_hotel:
            return False

        # 4. Resolve Required Permission Code (Method-level or View-level)
        required_permission = getattr(view, "get_required_permission", None)
        if callable(required_permission):
            required_code = required_permission(request)
        else:
            required_code = getattr(view, "required_permission", None)

        # Allow access if no specific permission code is explicitly required
        if not required_code:
            return True

        # 5. Check if the Role has the required Permission Code in Master DB
        return RolePermission.objects.using("default").filter(
            role=user_hotel.role,
            permission__code=required_code
        ).exists()
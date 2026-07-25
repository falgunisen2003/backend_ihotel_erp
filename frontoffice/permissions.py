from rest_framework.permissions import BasePermission

class HasFrontOfficePermission(BasePermission):
    def has_permission(self, request, view):
       
        if request.user and request.user.is_superuser:
            return True
            
   
        user_permissions = getattr(request, 'user_permissions', [])
        return 'frontoffice.view' in user_permissions or 'frontoffice.manage' in user_permissions
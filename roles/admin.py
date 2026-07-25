from django.contrib import admin
from .models import Role
from .models import Role, RolePermission

admin.site.register(Role)
admin.site.register(RolePermission)
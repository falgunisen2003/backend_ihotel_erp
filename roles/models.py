from django.db import models
from permissions.models import Permission

class Role(models.Model):

    name = models.CharField(max_length=100, unique=True)

    description = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "roles"

    def __str__(self):
        return self.name

class RolePermission(models.Model):

    role = models.ForeignKey(
        "Role",
        on_delete=models.CASCADE
    )

    permission = models.ForeignKey(
        Permission,
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = "role_permissions"
        unique_together = ("role", "permission")    
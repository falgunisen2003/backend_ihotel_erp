from django.db import models


class Permission(models.Model):
    module = models.CharField(max_length=100)
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=150)

    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "permissions"
        ordering = ["module", "name"]

    def __str__(self):
        return f"{self.module} - {self.name}"









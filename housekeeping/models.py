from django.db import models


class HousekeepingTask(models.Model):
    TASK_STATUS = (
        ('dirty', 'Dirty'),
        ('in_cleaning', 'In Cleaning'),
        ('clean', 'Clean / Ready'),
        ('inspected', 'Inspected'),
    )

    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )

    
    room_number = models.CharField(max_length=20)
    assigned_staff_name = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=TASK_STATUS, default='dirty')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    remarks = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "housekeeping_tasks"

    def __str__(self):
        return f"Room {self.room_number} - {self.status}"
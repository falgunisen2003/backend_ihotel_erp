from rest_framework import serializers
from .models import HousekeepingTask


class HousekeepingTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = HousekeepingTask
        fields = '__all__'
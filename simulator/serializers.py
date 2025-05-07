from rest_framework import serializers
from .models import Sim, LoadTest
from notification.models import NotificationTemplate, NotificationHistory
from scenario.models import Scenario, ScenarioStep

class SimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sim
        fields = ['id', 'name', 'created_at']
        read_only_fields = ['id', 'created_at']


class LoadTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoadTest
        fields = [
            'id', 'user', 'scenario', 'endpoint', 'method',
            'headers', 'body', 'start_time', 'duration',
            'concurrent_users', 'requests_count', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']

from rest_framework import serializers
from .models import Scenario, ScenarioStep, ScenarioStepDependency


class ScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scenario
        fields = ['id', 'name', 'description', 'user', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class ScenarioStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScenarioStep
        fields = [
            'id', 'scenario', 'name', 'method', 'endpoint',
            'headers', 'body', 'description', 'user', 'order'
        ]
        read_only_fields = ['id', 'user']

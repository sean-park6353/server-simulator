from rest_framework import serializers
from .models import Scenario, ScenarioStep


class ScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scenario
        fields = ['id', 'name', 'description', 'user', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class ScenarioStepBulkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScenarioStep
        fields = '__all__'
        read_only_fields = ['user_id', 'scenario', 'created_at', 'updated_at']

    # class Meta:
    #     model = ScenarioStep
    #     fields = [
    #         'id', 'scenario', 'name', 'method', 'endpoint',
    #         'headers', 'body', 'description', 'user', 'order'
    #     ]
    #     read_only_fields = ['id', 'user']

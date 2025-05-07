from rest_framework import serializers
from .models import (
    Sim,
    Scenario,
    ScenarioStep,
    ScenarioStepOrder,
    LoadTest,
    NotificationTemplate,
    NotificationHistory,
)

class SimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sim
        fields = ['id', 'name', 'created_at']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Sim 이름은 비어있을 수 없습니다.")
        return value

class ScenarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scenario
        fields = ['id', 'name', 'description', 'user', 'created_at']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Scenario 이름은 비어있을 수 없습니다.")
        return value

class ScenarioStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScenarioStep
        fields = ['id', 'name', 'method', 'endpoint', 'headers', 'body', 'user', 'description']

    def validate_method(self, value):
        allowed_methods = ['GET', 'POST', 'PUT', 'DELETE']
        if value.upper() not in allowed_methods:
            raise serializers.ValidationError(f"허용되지 않은 HTTP 메서드입니다: {value}")
        return value

    def validate_endpoint(self, value):
        if not value.startswith("/"):
            raise serializers.ValidationError("Endpoint는 /로 시작해야 합니다.")
        return value

class LoadTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoadTest
        fields = ['id', 'user', 'endpoint', 'method', 'body', 'headers', 'start_time', 'duration', 'concurrent_users', 'requests_count', 'created_at']

    def validate_duration(self, value):
        if value <= 0:
            raise serializers.ValidationError("Duration은 0보다 커야 합니다.")
        return value

    def validate_concurrent_users(self, value):
        if value <= 0:
            raise serializers.ValidationError("Concurrent users는 0보다 커야 합니다.")
        return value

    def validate_requests_count(self, value):
        if value <= 0:
            raise serializers.ValidationError("Requests count는 0보다 커야 합니다.")
        return value

class NotificationTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationTemplate
        fields = ['id', 'title', 'body', 'notification_type', 'template_code', 'is_active', 'created_at']

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title은 비어있을 수 없습니다.")
        return value

    def validate_template_code(self, value):
        if not value.strip():
            raise serializers.ValidationError("Template Code는 비어있을 수 없습니다.")
        return value

class NotificationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationHistory
        fields = ['id', 'notification_template', 'sender', 'receiver', 'body', 'is_success', 'created_at']

    def validate_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Body는 비어있을 수 없습니다.")
        return value
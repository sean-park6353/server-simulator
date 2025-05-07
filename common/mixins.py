from rest_framework.request import Request
from rest_framework.serializers import Serializer

class AutoUserAssignmentMixin:
    request: Request  # for IDE type hint

    def perform_create(self, serializer: Serializer):
        serializer.save(user=self.request.user)

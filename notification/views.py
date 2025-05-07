from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import NotificationTemplate
from .serializers import NotificationTemplateSerializer


class NotificationTemplateCreateView(generics.CreateAPIView):
    queryset = NotificationTemplate.objects.all()
    serializer_class = NotificationTemplateSerializer
    permission_classes = [IsAuthenticated]


class NotificationTemplateUpdateDestroyView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = NotificationTemplate.objects.all()
    serializer_class = NotificationTemplateSerializer
    permission_classes = [IsAuthenticated]


class NotificationSendView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        template_id = request.data.get('template_id')
        receiver_ids = request.data.get('receiver_ids', [])
        # TODO: 발송 로직 연결
        return Response({'message': 'Notification sent', 'template_id': template_id}, status=status.HTTP_200_OK)

from django.urls import path
from . import views

urlpatterns = [
    path('notification-templates/', views.NotificationTemplateCreateView.as_view(), name='notificationtemplate_create'),
    path('notification-templates/<int:pk>/', views.NotificationTemplateUpdateDestroyView.as_view(), name='notificationtemplate_update_destroy'),

    path('notifications/send/', views.NotificationSendView.as_view(), name='notification_send'),
]

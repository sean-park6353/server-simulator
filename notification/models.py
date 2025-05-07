from django.db import models
from django.conf import settings


class NotificationType(models.IntegerChoices):
    SMS = 0, "SMS"
    ALIMTALK = 1, "알림톡"
    MAIL = 2, "메일"


class NotificationTemplate(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(help_text="메시지 본문 (템플릿)")
    notification_type = models.IntegerField(choices=NotificationType.choices)
    template_code = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        db_table = 'notification_template'
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.get_notification_type_display()}] {self.title}"


class NotificationHistory(models.Model):
    notification_template = models.ForeignKey(
        NotificationTemplate, on_delete=models.SET_NULL, null=True
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_notifications'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_notifications'
    )
    body = models.TextField(help_text="발송된 메시지 내용")
    is_success = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        db_table = 'notification_history'
        ordering = ['-created_at']

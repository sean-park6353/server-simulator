from django.db import models
from django.conf import settings

class Sim(models.Model):
    name = models.CharField(max_length=100, help_text="가상 유저 이름")
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        db_table = 'sim'

    def __str__(self):
        return self.name

class Scenario(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='scenarios'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        db_table = 'scenario'

    def __str__(self):
        return self.name

class ScenarioStep(models.Model):
    name = models.CharField(max_length=100)
    method = models.CharField(max_length=10)
    endpoint = models.CharField(max_length=255)
    headers = models.JSONField(blank=True, null=True)
    body = models.JSONField(blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='scenario_steps'
    )
    description = models.TextField(blank=True)

    objects = models.Manager()

    class Meta:
        db_table = 'scenario_step'

    def __str__(self):
        return self.name

class ScenarioStepOrder(models.Model):
    scenario = models.ForeignKey(
        Scenario,
        on_delete=models.CASCADE,
        related_name='step_orders'
    )
    step = models.ForeignKey(ScenarioStep, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    is_optional = models.BooleanField(default=False)
    weight = models.FloatField(default=1.0)
    group = models.CharField(max_length=50, blank=True, null=True)
    depends_on = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True
    )

    objects = models.Manager()



    class Meta:
        ordering = ['order']
        unique_together = ('scenario', 'order')
        db_table = 'scenario_step_order'

    def __str__(self):
        return f"{self.scenario.name} - {self.order}. {self.step.name}"

class LoadTest(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='load_tests',
        help_text="이 테스트를 생성한 유저"
    )
    endpoint = models.CharField(help_text="부하 테스트할 대상 URL")
    method = models.CharField(
        max_length=10,
        choices=[('GET','GET'),('POST','POST'),('PUT','PUT'),('DELETE','DELETE')],
        default='GET'
    )
    body = models.JSONField(null=True, blank=True, help_text="요청에 포함할 JSON 데이터")
    headers = models.JSONField(null=True, blank=True, help_text="요청 헤더")
    start_time = models.DateTimeField(help_text="테스트 시작 시각")
    duration = models.PositiveIntegerField(default=1, help_text="테스트 지속 시간 (초)")
    concurrent_users = models.PositiveIntegerField(default=1, help_text="동시 사용자 수")
    requests_count = models.PositiveIntegerField(default=1, help_text="한 유저당 요청 수")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'load_test'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.endpoint} - {self.concurrent_users} users"

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
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


class LoadTest(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='load_tests',
        help_text="이 테스트를 생성한 유저"
    )
    scenario = models.ForeignKey(
        'scenario.Scenario',
        on_delete=models.CASCADE,
        related_name='load_tests'
    )
    endpoint = models.CharField(help_text="부하 테스트할 대상 URL")
    method = models.CharField(
        max_length=10,
        choices=[('GET', 'GET'), ('POST', 'POST'), ('PUT', 'PUT'), ('DELETE', 'DELETE')],
        default='GET'
    )
    body = models.JSONField(null=True, blank=True, help_text="요청에 포함할 JSON 데이터")
    headers = models.JSONField(null=True, blank=True, help_text="요청 헤더")
    start_time = models.DateTimeField(help_text="테스트 시작 시각")
    duration = models.PositiveIntegerField(default=1, help_text="테스트 지속 시간 (초)")
    concurrent_users = models.PositiveIntegerField(default=1, help_text="동시 사용자 수")
    requests_count = models.PositiveIntegerField(default=1, help_text="한 유저당 요청 수")
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        db_table = 'load_test'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.endpoint} - {self.concurrent_users} users"

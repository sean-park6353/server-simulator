from django.db import models
from django.conf import settings

class Sim(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sims',
        help_text="이 가상 유저를 생성한 실제 유저",
        default=1
    )

    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        db_table = 'sim'

    def __str__(self):
        return self.name

class SimulationRun(models.Model):
    sim = models.ForeignKey(
        Sim,
        on_delete=models.CASCADE,
        related_name='runs',
        help_text="실행된 가상 유저"
    )
    scenario = models.ForeignKey(
        'scenario.Scenario',
        on_delete=models.CASCADE,
        related_name='simulation_runs',
        help_text="실행된 시나리오"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='simulation_runs',
        help_text="이 실행을 시작한 유저"
    )
    started_at = models.DateTimeField(auto_now_add=True, help_text="시뮬레이션 시작 시각")
    ended_at = models.DateTimeField(null=True, blank=True, help_text="시뮬레이션 종료 시각")
    status = models.CharField(max_length=20, default='running', help_text="시뮬레이션 상태")

    objects = models.Manager()

    class Meta:
        db_table = 'simulation_run'
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.sim.name} - {self.scenario.name} ({self.status})"

class LoadTest(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='load_tests',
        help_text="이 테스트를 생성한 유저"
    )
    endpoint = models.CharField(max_length=255,help_text="부하 테스트 할 대상 URL")
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

from django.db import models
from django.conf import settings


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
    scenario = models.ForeignKey(
        Scenario,
        on_delete=models.CASCADE,
        related_name='steps'
    )
    stepname = models.CharField(max_length=100)
    method = models.CharField(max_length=10)
    endpoint = models.CharField(max_length=255)
    headers = models.JSONField(blank=True, null=True)
    body = models.JSONField(blank=True, null=True)
    stepdescription = models.TextField(blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='scenario_steps'
    )

    objects = models.Manager()

    class Meta:
        db_table = 'scenario_step'

    def __str__(self):
        return self.name


class ScenarioStepDependency(models.Model):
    step = models.ForeignKey(
        ScenarioStep,
        on_delete=models.CASCADE,
        related_name='dependencies'
    )
    depends_on = models.ForeignKey(
        ScenarioStep,
        on_delete=models.CASCADE,
        related_name='dependents'
    )

    class Meta:
        db_table = 'scenario_step_dependency'
        unique_together = ('step', 'depends_on')

    def __str__(self):
        return f"{self.step} depends on {self.depends_on}"

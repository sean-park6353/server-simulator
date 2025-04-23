from django.db import models


class Sim(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        managed = True
        db_table = 'sim'


class LoadTest(models.Model):
    sim = models.ForeignKey('Sim', related_name='load_tests', on_delete=models.CASCADE)
    target_url = models.URLField()
    method = models.CharField(max_length=10, choices=[('GET', 'GET'), ('POST', 'POST')])
    headers = models.JSONField(blank=True, null=True)
    payload = models.JSONField(blank=True, null=True)
    rps = models.PositiveIntegerField(help_text='Requests per second')
    duration = models.PositiveIntegerField(help_text='Duration in seconds')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()


    class Meta:
        managed = True
        db_table = 'load_test'


class LoadTestResult(models.Model):
    test = models.ForeignKey(LoadTest, related_name='results', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    response_time_avg = models.FloatField(help_text='Average response time in milliseconds')
    success_rate = models.FloatField(help_text='Success rate as a percentage')
    error_rate = models.FloatField(help_text='Error rate as a percentage')
    status_distribution = models.JSONField(help_text='Distribution of HTTP status codes')
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        managed = True
        db_table = 'load_test_result'


